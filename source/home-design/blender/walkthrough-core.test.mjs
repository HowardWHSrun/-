import assert from 'node:assert/strict';
import {WalkthroughWorld, circleHitsBox, circleInPolygon, EYE_HEIGHT} from './walkthrough-core.mjs';

// Independent, synthetic engine fixture. This is not the user's house or source drawing.
const floors=[0,1,2].map(id=>({id,label:`${id+1}F`,elevation:[0,3.7,6.9][id],boundary:[[0,0],[10,0],[10,12],[0,12]],holes:[[[1,8],[3,8],[3,10],[1,10]]]}));
const box=(name,floor,position,size,category='wall')=>({name,floor,kind:'box',position,size,category,material:'plaster'});
const data={meta:{title:'Synthetic engine test only'},materials:{plaster:{color:'#dddddd'}},objects:floors.flatMap(f=>[
  box('左侧墙体',f.id,[2.1,3,1.5],[4.2,.08,3]),
  box('右侧墙体',f.id,[7.9,3,1.5],[4.2,.08,3]),
  box('门洞上方',f.id,[5,3,2.6],[1.6,.08,.8]),
  box('固定工作台',f.id,[8,5,.7],[1.5,1.5,1.4],'furniture'),
  box('地面',f.id,[5,6,-.15],[10,12,.3],'slab')
]),walkthrough:{floors,spawn:{floor:0,position:[5,1],yaw:0},elevator:{bounds:[4,5,6,7],stops:[0,1,2],door:{side:'south',center:5,width:1},initialFloor:0}}};
const create=()=>new WalkthroughWorld(structuredClone(data));
const walk=(world,forward,strafe,seconds)=>{for(let t=0;t<seconds;t+=.02){world.move(forward,strafe,.02);world.update(.02);}};
let passed=0;
function test(name,fn){fn();passed++;console.log(`PASS ${name}`);}

test('Explicit navigation required; old conceptual scene cannot silently bind',()=>assert.throws(()=>new WalkthroughWorld({objects:[],meta:{width:9.6,depth:14.9}}),/待绑定/));
test('Human eye height remains 1.65m while walking',()=>{const w=create();walk(w,1,0,1);assert.equal(w.eyeZ,EYE_HEIGHT);assert.equal(w.player.floor,0);});
test('Walls prevent tunneling even with a very long frame',()=>{const w=create();w.player.x=2;w.player.y=1;for(let i=0;i<100;i++)w.move(1,0,5);assert(w.player.y<2.741);assert(w.player.y>2.68);});
test('Door lintel does not block an open doorway',()=>{const w=create();walk(w,1,0,1.7);assert(w.player.y>3.7);});
test('Fixed furniture blocks walking',()=>{const w=create();w.player.x=8;w.player.y=3.6;walk(w,1,0,3);assert(w.player.y<4.04);});
test('Building perimeter prevents leaving the floor',()=>{const w=create();w.player.x=5;w.player.y=1;walk(w,-1,0,3);assert(w.player.y>=.22);});
test('Open floor holes prevent falling or walking over the opening',()=>{const w=create();w.player.x=2;w.player.y=7;walk(w,1,0,3);assert(w.player.y<7.781);assert(w.player.y>7.72);});
test('Diagonal input is normalized to the same walking speed',()=>{const a=create(),b=create();a.player.x=b.player.x=7;a.player.y=b.player.y=10;walk(a,1,0,.5);walk(b,1,1,.5);assert(Math.abs(Math.hypot(a.player.x-7,a.player.y-10)-Math.hypot(b.player.x-7,b.player.y-10))<1e-9);});
test('Rotated wall collision uses the rotated footprint',()=>{assert(circleHitsBox(.7,.7,.22,{x:0,y:0,hx:2,hy:.05,angle:Math.PI/4}));assert(!circleHitsBox(.7,-.7,.22,{x:0,y:0,hx:2,hy:.05,angle:Math.PI/4}));});
test('Concave floor boundary respects the missing corner',()=>{const poly=[[0,0],[5,0],[5,2],[2,2],[2,5],[0,5]];assert(circleInPolygon(1,4,.22,poly));assert(!circleInPolygon(3,3,.22,poly));assert(!circleInPolygon(1.9,2.1,.22,poly));});
test('Floor buttons cannot teleport a player outside the cabin',()=>{const w=create();assert.equal(w.requestFloor(2),false);assert.equal(w.player.floor,0);assert.equal(w.eyeZ,1.65);});
test('Walk into open cabin and ride with continuous height; no walking in transit',()=>{
  const w=create();walk(w,1,0,3.05);assert(w.inCabin());assert(w.requestFloor(2));
  const x=w.player.x,y=w.player.y;w.move(1,1,.1);assert.equal(w.player.x,x);assert.equal(w.player.y,y);
  const heights=[];for(let t=0;t<10;t+=.02){w.update(.02);heights.push(w.eyeZ);}
  assert(heights.some(z=>z>1.66 && z<8.54));assert(heights.every((z,i)=>i===0 || z>=heights[i-1]-1e-10));assert.equal(w.player.floor,2);assert.equal(w.elevator.state,'idle');assert.equal(w.eyeZ,8.55);
  walk(w,-1,0,1.25);assert(w.player.y<4.5);assert(!w.inCabin());assert.equal(w.eyeZ,8.55);
});
test('Closed landing door blocks the empty shaft on another floor',()=>{const d=structuredClone(data);d.walkthrough.spawn={floor:1,position:[5,4],yaw:0};const w=new WalkthroughWorld(d);walk(w,1,0,4);assert(w.player.y<4.75);assert.equal(w.player.floor,1);});
test('Elevator call brings an empty car without moving the waiting player',()=>{const d=structuredClone(data);d.walkthrough.spawn={floor:2,position:[5,4],yaw:0};const w=new WalkthroughWorld(d);const z=w.eyeZ;assert(w.callElevator());for(let t=0;t<10;t+=.02){w.update(.02);assert.equal(w.eyeZ,z);}assert.equal(w.elevator.floor,2);assert.equal(w.player.y,4);assert.equal(w.elevator.open,1);});
test('An invalid spawn inside furniture fails instead of teleporting automatically',()=>{const d=structuredClone(data);d.walkthrough.spawn.position=[8,5];assert.throws(()=>new WalkthroughWorld(d),/入口位置/);});
test('Look controls turn horizontally and clamp head tilt without flying',()=>{const w=create();w.look(100,10000);assert.equal(w.player.yaw,.3);assert.equal(w.player.pitch,-1.25);assert.equal(w.eyeZ,1.65);});
test('Repeated elevator journeys preserve location and supported floors',()=>{const w=create();walk(w,1,0,3.05);for(const target of [2,1,0,2,0]){assert(w.requestFloor(target));for(let t=0;t<10;t+=.02)w.update(.02);assert.equal(w.player.floor,target);assert(w.canStand(w.player.x,w.player.y));assert.equal(w.eyeZ,floors[target].elevation+1.65);}});
test('Terrace eye level follows its 6.87m surface without changing the room datum',()=>{
  const d=structuredClone(data);d.walkthrough.floors[2].surfaces=[{polygon:[[6,8],[9.5,8],[9.5,11.5],[6,11.5]],elevation:6.87}];
  d.walkthrough.spawn={floor:2,position:[7,7.6],yaw:0};const w=new WalkthroughWorld(d);
  assert.equal(w.eyeZ,8.55);walk(w,1,0,.5);assert.equal(w.surfaceElevation,6.87);assert.equal(w.eyeZ,6.87+1.65);
  walk(w,-1,0,.5);assert.equal(w.eyeZ,8.55);assert.equal(w.floors.get(2).elevation,6.9);
});
test('Elevator support overrides surface regions while parked and during the complete trip',()=>{
  const d=structuredClone(data);d.walkthrough.floors[2].surfaces=[{polygon:[[0,0],[10,0],[10,12],[0,12]],elevation:6.87}];
  const w=new WalkthroughWorld(d);walk(w,1,0,3.05);assert(w.requestFloor(2));
  for(let t=0;t<10;t+=.02){w.update(.02);assert.equal(w.eyeZ,w.elevator.z+1.65);}
  assert.equal(w.eyeZ,8.55);assert(w.inCabin());walk(w,-1,0,1.25);assert(!w.inCabin());assert.equal(w.eyeZ,6.87+1.65);
  walk(w,1,0,1.25);assert(w.inCabin());assert.equal(w.eyeZ,8.55);assert(w.requestFloor(0));
  for(let t=0;t<10;t+=.02){w.update(.02);assert.equal(w.eyeZ,w.elevator.z+1.65);}assert.equal(w.eyeZ,1.65);
});
test('Malformed surface elevation fails explicitly',()=>{const d=structuredClone(data);d.walkthrough.floors[0].surfaces=[{polygon:[[0,0],[2,0],[2,2]],elevation:'6.87'}];assert.throws(()=>new WalkthroughWorld(d),/分区地坪/);});
test('A continuous ramp walks down to the garden and back with a 1.65m eye height',()=>{
  const d=structuredClone(data);d.walkthrough.spawn.position=[7,8];
  d.walkthrough.floors[0].surfaces=[{polygon:[[6,8],[9,8],[9,12],[6,12]],elevation:-.4},{polygon:[[6,8],[9,8],[9,11],[6,11]],profile:{axis:'y',start:8,end:11,startElevation:0,endElevation:-.4}}];
  const w=new WalkthroughWorld(d);assert.equal(w.supportElevation(7,9.5),-.2);
  const heights=[];for(let t=0;t<2.2;t+=.02){w.move(1,0,.02);heights.push(w.eyeZ);}assert(w.player.y>11.5);assert.equal(w.eyeZ,1.25);assert(heights.every((z,i)=>i===0 || z<=heights[i-1]+1e-9));
  walk(w,-1,0,2.2);assert(w.player.y<8.1);assert(w.eyeZ>1.63);
});
test('An abrupt 40cm drop remains impassable without the ramp',()=>{
  const d=structuredClone(data);d.walkthrough.spawn.position=[7,8];d.walkthrough.floors[0].surfaces=[{polygon:[[6,9],[9,9],[9,12],[6,12]],elevation:-.4}];
  const w=new WalkthroughWorld(d);walk(w,1,0,3);assert(w.player.y<9);assert.equal(w.eyeZ,1.65);assert.equal(w.canStep(7,8.99,7,9.01),false);
});
test('Garden-height obstacles collide relative to the lowered ground',()=>{
  const d=structuredClone(data);d.walkthrough.spawn.position=[7,10];d.walkthrough.floors[0].surfaces=[{polygon:[[6,8],[9,8],[9,12],[6,12]],elevation:-.4}];
  d.objects.push(box('花园低矮花槽',0,[7,10.9,-.15],[1,.3,.5],'furniture'));
  const w=new WalkthroughWorld(d);walk(w,1,0,3);assert(w.player.y<10.54);assert.equal(w.eyeZ,1.25);
});
test('Ramp axes may decrease and malformed ramp profiles are rejected',()=>{
  const d=structuredClone(data);d.walkthrough.floors[0].surfaces=[{polygon:[[6,8],[9,8],[9,12],[6,12]],profile:{axis:'x',start:9,end:6,startElevation:0,endElevation:-.4}}];
  const w=new WalkthroughWorld(d);assert.equal(w.supportElevation(7.5,10),-.2);
  d.walkthrough.floors[0].surfaces[0].profile.end=9;assert.throws(()=>new WalkthroughWorld(d),/分区地坪/);
});
console.log(`${passed} engine tests passed. Fixture is synthetic and makes no source-drawing claim.`);
