// Metre-based walking and lift simulation. No DOM, rendering or network dependencies.
// Object positions use local floor Z, matching the existing scene.json schema.
export const EYE_HEIGHT = 1.65;
export const BODY_HEIGHT = 1.78;
export const BODY_RADIUS = 0.22;
const EPS = 1e-7;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const finite = v => typeof v === 'number' && Number.isFinite(v);

export function distanceToSegment(x, y, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const t = clamp(((x - a[0]) * dx + (y - a[1]) * dy) / (dx * dx + dy * dy || 1), 0, 1);
  return Math.hypot(x - a[0] - dx * t, y - a[1] - dy * t);
}
export function pointInPolygon(x, y, polygon) {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const a = polygon[i], b = polygon[j];
    if ((a[1] > y) !== (b[1] > y) && x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]) inside = !inside;
  }
  return inside;
}
function polygonClearance(x, y, polygon) {
  return Math.min(...polygon.map((a, i) => distanceToSegment(x, y, a, polygon[(i + 1) % polygon.length])));
}
export function circleInPolygon(x, y, radius, polygon) {
  return pointInPolygon(x, y, polygon) && polygonClearance(x, y, polygon) >= radius - EPS;
}
export function circleHitsBox(x, y, radius, box) {
  const c = Math.cos(box.angle || 0), s = Math.sin(box.angle || 0);
  const dx = x - box.x, dy = y - box.y;
  const lx = dx * c + dy * s, ly = -dx * s + dy * c;
  const ox = Math.max(Math.abs(lx) - box.hx, 0), oy = Math.max(Math.abs(ly) - box.hy, 0);
  return ox * ox + oy * oy < (radius - EPS) ** 2;
}
function rectPolygon(b) { return [[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]]]; }
function insideBounds(x, y, r, b) { return x >= b[0] + r - EPS && x <= b[2] - r + EPS && y >= b[1] + r - EPS && y <= b[3] - r + EPS; }

export function objectCollider(object) {
  if (object.collision === false || object.kind === 'text' || object.walkthroughRole === 'elevator-generated') return null;
  if (object.collision !== true && ['slab', 'label', 'landscape', 'ceiling', 'rug'].includes(object.category)) return null;
  const [x, y, z] = object.position, [sx, sy, sz] = object.size;
  const [rx, ry, rz] = object.rotation || [0, 0, 0];
  // Existing meshes are upright. Tilted boxes get a conservative world-space AABB.
  if (Math.abs(rx) > EPS || Math.abs(ry) > EPS) {
    const a = Math.cos(rx), b = Math.sin(rx), c = Math.cos(ry), d = Math.sin(ry), e = Math.cos(rz), f = Math.sin(rz);
    const matrix = [[c * e, -c * f, d], [a * f + b * d * e, a * e - b * d * f, -b * c], [b * f - a * d * e, b * e + a * d * f, a * c]];
    const extent = matrix.map(row => (Math.abs(row[0]) * sx + Math.abs(row[1]) * sy + Math.abs(row[2]) * sz) / 2);
    return {x, y, hx: extent[0], hy: extent[1], bottom: z - extent[2], top: z + extent[2], angle: 0, name: object.name};
  }
  return {x, y, hx: sx / 2, hy: sy / 2, bottom: z - sz / 2, top: z + sz / 2, angle: rz, name: object.name};
}

export class WalkthroughWorld {
  constructor(data) {
    if (!data.walkthrough) throw new Error('待绑定经核对的原图模型。');
    this.data = data;
    this.config = data.walkthrough;
    this.radius = BODY_RADIUS;
    this.speed = 1.65;
    this.floors = new Map();
    for (const f of this.config.floors || []) {
      if (this.floors.has(f.id) || !finite(f.elevation) || !Array.isArray(f.boundary) || f.boundary.length < 3 || f.boundary.some(p => p.length !== 2 || p.some(v => !finite(v)))) throw new Error('楼层轮廓或标高数据不完整。');
      if ((f.surfaces || []).some(surface=>{
        const profile=surface.profile;
        const validHeight=profile?['x','y'].includes(profile.axis) && [profile.start,profile.end,profile.startElevation,profile.endElevation].every(finite) && profile.start!==profile.end:finite(surface.elevation);
        return !validHeight || !Array.isArray(surface.polygon) || surface.polygon.length<3 || surface.polygon.some(p=>p.length!==2 || p.some(v=>!finite(v)));
      })) throw new Error('分区地坪的轮廓或绝对标高不完整。');
      const elevations=[f.elevation,...(f.surfaces || []).flatMap(surface=>surface.profile?[surface.profile.startElevation,surface.profile.endElevation]:[surface.elevation])];
      this.floors.set(f.id, {...f, holes: f.holes || [],minElevation:Math.min(...elevations),maxElevation:Math.max(...elevations)});
    }
    const spawn = this.config.spawn;
    if (!spawn || !this.floors.has(spawn.floor) || spawn.position?.length !== 2 || spawn.position.some(v => !finite(v))) throw new Error('缺少经核对的首层入口位置。');
    this.player = {x: spawn.position[0], y: spawn.position[1], floor: spawn.floor, yaw: spawn.yaw || 0, pitch: 0};
    this.colliders = new Map([...this.floors.keys()].map(id => [id, []]));
    for (const o of data.objects || []) {
      if (!Array.isArray(o.position) || !Array.isArray(o.size)) continue;
      const collider = objectCollider(o);
      const floor=this.floors.get(o.floor);
      if (collider && floor && collider.top > floor.minElevation-floor.elevation+0.08 && collider.bottom < floor.maxElevation-floor.elevation+BODY_HEIGHT) this.colliders.get(o.floor).push(collider);
    }
    this.elevator = null;
    if (this.config.elevator) this.initializeElevator(this.config.elevator);
    if (!this.canStand(this.player.x, this.player.y)) throw new Error('入口位置与墙体、家具或可行走范围冲突，请核对模型。');
  }
  initializeElevator(e) {
    if (!Array.isArray(e.bounds) || e.bounds.length !== 4 || e.bounds.some(v => !finite(v)) || e.bounds[2] - e.bounds[0] < 0.8 || e.bounds[3] - e.bounds[1] < 0.8 || !Array.isArray(e.stops) || e.stops.length < 2 || e.stops.some(id => !this.floors.has(id))) throw new Error('电梯净空、停靠楼层或标高数据不完整。');
    const bounds = e.bounds, door = {...e.door};
    if (!['south', 'north', 'west', 'east'].includes(door.side)) throw new Error('需要明确电梯开门方向。');
    const horizontal = ['south', 'north'].includes(door.side), low = bounds[horizontal ? 0 : 1], high = bounds[horizontal ? 2 : 3];
    door.center ??= (low + high) / 2;
    door.width ??= 0.95;
    if (door.width < this.radius * 2 + 0.08 || door.center - door.width / 2 < low || door.center + door.width / 2 > high) throw new Error('电梯门洞尺寸与轿厢范围冲突。');
    const initialFloor = e.initialFloor ?? e.stops[0];
    if (!e.stops.includes(initialFloor)) throw new Error('电梯初始楼层不在停靠楼层中。');
    this.elevator = {...e, bounds, door, horizontal, floor: initialFloor, z: this.floors.get(initialFloor).elevation, open: 1, trip: null, state: 'idle', polygon: rectPolygon(bounds)};
    this.elevator.walls = this.elevatorWalls();
  }
  elevatorWalls() {
    const e = this.elevator, b = e.bounds, d = e.door, t = 0.06, walls = [];
    const add = (x1, y1, x2, y2) => walls.push({x: (x1+x2)/2, y: (y1+y2)/2, hx: Math.max(t/2, (x2-x1)/2), hy: Math.max(t/2, (y2-y1)/2), angle: 0, bottom: 0, top: 2.3, name:'电梯围护'});
    if (d.side !== 'south') add(b[0],b[1],b[2],b[1]);
    if (d.side !== 'north') add(b[0],b[3],b[2],b[3]);
    if (d.side !== 'west') add(b[0],b[1],b[0],b[3]);
    if (d.side !== 'east') add(b[2],b[1],b[2],b[3]);
    if (e.horizontal) {
      const y = b[d.side === 'south' ? 1 : 3];
      add(b[0],y,d.center-d.width/2,y); add(d.center+d.width/2,y,b[2],y);
    } else {
      const x = b[d.side === 'west' ? 0 : 2];
      add(x,b[1],x,d.center-d.width/2); add(x,d.center+d.width/2,x,b[3]);
    }
    return walls;
  }
  gate() {
    const e = this.elevator, d = e.door, b = e.bounds;
    return e.horizontal ? {x:d.center,y:b[d.side==='south'?1:3],hx:d.width/2,hy:.035,angle:0} : {x:b[d.side==='west'?0:2],y:d.center,hx:.035,hy:d.width/2,angle:0};
  }
  inCabin(x = this.player.x, y = this.player.y) {
    return !!this.elevator && insideBounds(x,y,this.radius+.035,this.elevator.bounds);
  }
  nearElevator() {
    if (!this.elevator || !this.elevator.stops.includes(this.player.floor)) return false;
    const g = this.gate();
    return Math.hypot(this.player.x-g.x,this.player.y-g.y) < 1.6;
  }
  cabinAtPlayerFloor() { return this.elevator && this.elevator.floor === this.player.floor && this.elevator.state === 'idle'; }
  canStand(x,y,floor = this.player.floor) {
    const f = this.floors.get(floor), r = this.radius;
    if (!f || !circleInPolygon(x,y,r,f.boundary)) return false;
    const e = this.elevator;
    const overShaft = e && e.stops.includes(floor) && pointInPolygon(x,y,e.polygon);
    if (overShaft && (e.floor !== floor || e.state !== 'idle')) return false;
    for (const hole of f.holes) {
      // Shaft holes are declared separately by elevator.bounds. Other holes stay impassable.
      if (pointInPolygon(x,y,hole) || polygonClearance(x,y,hole) < r-EPS) return false;
    }
    const localFoot=this.supportElevation(x,y,floor)-f.elevation;
    for (const box of this.colliders.get(floor)) if (box.top>localFoot+.08 && box.bottom<localFoot+BODY_HEIGHT && circleHitsBox(x,y,r,box)) return false;
    if (e && e.stops.includes(floor)) {
      for (const box of e.walls) if (circleHitsBox(x,y,r,box)) return false;
      if ((e.floor !== floor || e.open < .985) && circleHitsBox(x,y,r,this.gate())) return false;
    }
    return true;
  }
  supportElevation(x,y,floor=this.player.floor){
    const f=this.floors.get(floor),surfaces=f.surfaces || [];
    const surface=surfaces.find(s=>s.profile && pointInPolygon(x,y,s.polygon)) || surfaces.find(s=>!s.profile && pointInPolygon(x,y,s.polygon));
    if(!surface)return f.elevation;
    if(!surface.profile)return surface.elevation;
    const p=surface.profile,coordinate=p.axis==='x'?x:y;
    const ratio=clamp((coordinate-p.start)/(p.end-p.start),0,1);
    return p.startElevation+(p.endElevation-p.startElevation)*ratio;
  }
  canStep(x,y,nx,ny,floor=this.player.floor){
    return this.canStand(nx,ny,floor) && Math.abs(this.supportElevation(nx,ny,floor)-this.supportElevation(x,y,floor))<=.08+EPS;
  }
  move(forward,strafe,dt) {
    if (this.elevator?.trip?.passenger) return;
    const length = Math.hypot(forward,strafe);
    if (!length || !finite(dt)) return;
    // Yaw 0 faces +Y; +PI/2 faces +X. A/D always strafe at human eye height.
    const amount = this.speed * clamp(dt,0,.12) / Math.max(1,length);
    const dx = (Math.sin(this.player.yaw)*forward + Math.cos(this.player.yaw)*strafe)*amount;
    const dy = (Math.cos(this.player.yaw)*forward - Math.sin(this.player.yaw)*strafe)*amount;
    const count = Math.max(1,Math.ceil(Math.hypot(dx,dy)/.04));
    for (let n=0;n<count;n++) {
      const sx=dx/count, sy=dy/count, p=this.player;
      if (this.canStep(p.x,p.y,p.x+sx,p.y+sy)) {p.x+=sx;p.y+=sy;}
      else {
        if (this.canStep(p.x,p.y,p.x+sx,p.y)) p.x+=sx;
        if (this.canStep(p.x,p.y,p.x,p.y+sy)) p.y+=sy;
      }
    }
  }
  look(dx,dy) {
    this.player.yaw += dx*.003;
    this.player.pitch = clamp(this.player.pitch-dy*.003,-1.25,1.25);
  }
  requestFloor(target) {
    const e=this.elevator;
    if (!e || e.state!=='idle' || !e.stops.includes(target) || !this.inCabin() || e.floor!==this.player.floor) return false;
    if (target===e.floor) return true;
    return this.startTrip(target,true);
  }
  callElevator() {
    const e=this.elevator;
    if (!e || e.state!=='idle' || !this.nearElevator() || this.inCabin() || circleHitsBox(this.player.x,this.player.y,this.radius+.08,this.gate())) return false;
    if (e.floor===this.player.floor) return true;
    return this.startTrip(this.player.floor,false);
  }
  startTrip(target,passenger) {
    const e=this.elevator;
    e.trip={target,passenger,fromZ:e.z,toZ:this.floors.get(target).elevation,elapsed:0,duration:Math.max(2.4,Math.abs(this.floors.get(target).elevation-e.z)/1.1)};
    e.state='closing';
    return true;
  }
  update(dt) {
    const e=this.elevator;
    if (!e?.trip) return;
    // Small substeps preserve distinct close / travel / arrival stages after long frames.
    let remaining=clamp(dt,0,.25);
    while (remaining>EPS && e.trip) {
      const step=Math.min(remaining,.025); remaining-=step;
      const t=e.trip;t.elapsed+=step;
      if (e.state==='closing') {
        e.open=Math.max(0,1-t.elapsed/.7);
        if(t.elapsed>=.7){e.state='moving';t.elapsed=0;e.open=0;}
      } else if(e.state==='moving') {
        const q=clamp(t.elapsed/t.duration,0,1), smooth=q*q*(3-2*q);
        e.z=t.fromZ+(t.toZ-t.fromZ)*smooth;
        if(q>=1){e.floor=t.target;e.z=t.toZ;e.state='opening';t.elapsed=0;if(t.passenger)this.player.floor=t.target;}
      } else if(e.state==='opening') {
        e.open=Math.min(1,t.elapsed/.7);
        if(t.elapsed>=.7){e.state='idle';e.open=1;e.trip=null;}
      }
    }
  }
  get surfaceElevation(){
    return this.supportElevation(this.player.x,this.player.y,this.player.floor);
  }
  get eyeZ(){
    const e=this.elevator;
    const supportedByCabin=e && (e.trip?.passenger || (this.inCabin() && e.floor===this.player.floor));
    return (supportedByCabin?e.z:this.surfaceElevation)+EYE_HEIGHT;
  }
  get location(){return this.floors.get(this.player.floor).label || `${Number(this.player.floor)+1}F`;}
  get roomName(){
    if(this.inCabin())return '电梯';
    const p=this.player,f=this.floors.get(p.floor);
    const rooms=[...(f.rooms || []),...(this.config.rooms || []).filter(room=>room.floor===p.floor)];
    return rooms.find(room=>Array.isArray(room.polygon) && pointInPolygon(p.x,p.y,room.polygon))?.name || '';
  }
}
