import fs from 'node:fs';
import crypto from 'node:crypto';
import {WalkthroughWorld,pointInPolygon} from '../../blender/walkthrough-core.mjs';
const url=new URL('../../blender/unit6-professional-scene.json',import.meta.url),raw=fs.readFileSync(url),data=JSON.parse(raw),world=new WalkthroughWorld(data),step=.1;
const report={sceneSha256:crypto.createHash('sha256').update(raw).digest('hex'),objects:data.objects.length,stepMeters:step,bodyRadiusMeters:world.radius,method:'10cm grid; canStand nodes, canStep adjacency; actual support profile priority; lift stopped with doors open on each floor',floors:[],directRampPath:[]};
for(const f of data.walkthrough.floors){
 world.player.floor=f.id;Object.assign(world.elevator,{floor:f.id,z:f.elevation,state:'idle',open:1});
 const xs=f.boundary.map(p=>p[0]),ys=f.boundary.map(p=>p[1]),xmin=Math.floor(Math.min(...xs)/step)*step,ymin=Math.floor(Math.min(...ys)/step)*step;
 const nx=Math.ceil((Math.max(...xs)-xmin)/step)+1,ny=Math.ceil((Math.max(...ys)-ymin)/step)+1,ncells=nx*ny;
 const valid=new Uint8Array(ncells),seen=new Uint8Array(ncells),parent=new Int32Array(ncells);parent.fill(-1);
 const xy=n=>[xmin+(n%nx)*step,ymin+Math.floor(n/nx)*step];
 for(let n=0;n<ncells;n++)valid[n]=world.canStand(...xy(n))?1:0;
 const start=Math.round((10.45-ymin)/step)*nx+Math.round((3.25-xmin)/step);
 if(!valid[start])throw new Error('F'+(f.id+1)+' lift cabin grid start invalid');
 const q=[start];seen[start]=1;let disallowedHeightEdges=0;
 for(let k=0;k<q.length;k++){
  const n=q[k],i=n%nx,j=Math.floor(n/nx),[x,y]=xy(n);
  for(const [a,b] of [[i+1,j],[i-1,j],[i,j+1],[i,j-1]]){
   if(a<0||a>=nx||b<0||b>=ny)continue;const nb=b*nx+a;if(!valid[nb]||seen[nb])continue;
   if(!world.canStep(x,y,...xy(nb))){disallowedHeightEdges++;continue;}
   seen[nb]=1;parent[nb]=n;q.push(nb);
  }
 }
 const pathTo=n=>{const p=[];for(let k=n;k!==-1;k=parent[k])p.push(xy(k).map(v=>+v.toFixed(3)));return p.reverse();};
 const rooms=f.rooms.map(room=>{
  let walkable=0,reached=0,target=null;
  for(let n=0;n<ncells;n++)if(valid[n]&&pointInPolygon(...xy(n),room.polygon)){walkable++;if(seen[n]){reached++;target??=n;}}
  return {name:room.name,walkableCells:walkable,reachedCells:reached,reachable:reached>0,target:target===null?null:xy(target),path:target===null?[]:pathTo(target)};
 });
 report.floors.push({floor:f.id+1,walkableCells:valid.reduce((a,b)=>a+b,0),connectedCells:q.length,disallowedHeightEdges,rooms});
 fs.writeFileSync(new URL(`P02网格_F${f.id+1}.json`,import.meta.url),JSON.stringify({xmin,ymin,step,nx,ny,valid:[...valid],seen:[...seen],rooms}));
 console.log('F'+(f.id+1),q.length,'connected;',rooms.map(r=>r.name+':'+r.reachable).join(' / '));
}
world.player.floor=0;Object.assign(world.elevator,{floor:0,z:0,state:'idle',open:1});
for(let i=0;i<=270;i++){
 const x=6.6,y=4.5-i*.025,ny=y-.025;
 const stand=world.canStand(x,y),next=world.canStep(x,y,x,ny),z=world.supportElevation(x,y),nz=world.supportElevation(x,ny);
 report.directRampPath.push({x,y:+y.toFixed(3),z:+z.toFixed(6),stand,next,dz:+(nz-z).toFixed(6)});
}
report.directRampBlocked=report.directRampPath.filter(p=>!p.stand||!p.next);
report.allRoomsReachable=report.floors.every(f=>f.rooms.every(r=>r.reachable));
report.probes=[{label:'客厅门口室内到廊5cm',a:[6.6,4.225],b:[6.6,4.2]},{label:'廊到坡顶',a:[6.6,2.17],b:[6.6,2.15]},{label:'坡脚到庭院',a:[6.6,-2.03],b:[6.6,-2.05]}].map(p=>({...p,elevations:[world.supportElevation(...p.a),world.supportElevation(...p.b)],canStep:world.canStep(...p.a,...p.b)}));
fs.writeFileSync(new URL('P02房间与花园通达检查.json',import.meta.url),JSON.stringify(report,null,2));
console.log('direct ramp blocked',report.directRampBlocked.length,'probes',JSON.stringify(report.probes));
if(!report.allRoomsReachable||report.probes.some(p=>!p.canStep))process.exitCode=1;
