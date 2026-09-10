import fs from 'node:fs/promises';
import {WalkthroughWorld,pointInPolygon} from './walkthrough-core.mjs';
const scenePath=process.argv[2] || new URL('./unit6-professional-scene.json',import.meta.url);
const output=process.argv[3] || new URL('./unit6-professional-cameras.json',import.meta.url);
const data=JSON.parse(await fs.readFile(scenePath,'utf8'));
const world=new WalkthroughWorld(data),views=[];
const allRooms=[...(data.walkthrough.rooms || []),...data.walkthrough.floors.flatMap(f=>(f.rooms || []).map(r=>({...r,floor:f.id})))];
const bounds=points=>[Math.min(...points.map(p=>p[0])),Math.min(...points.map(p=>p[1])),Math.max(...points.map(p=>p[0])),Math.max(...points.map(p=>p[1]))];
function chooseRoomPosition(floor,name,preferred){
  const room=allRooms.find(r=>r.floor===floor && r.name===name);if(!room)throw new Error('Missing source room: '+name);
  const b=bounds(room.polygon),points=[];
  for(let x=b[0]+.24;x<=b[2]-.24;x+=.08)for(let y=b[1]+.24;y<=b[3]-.24;y+=.08)if(pointInPolygon(x,y,room.polygon)&&world.canStand(x,y,floor))points.push([x,y]);
  if(pointInPolygon(...preferred,room.polygon)&&world.canStand(...preferred,floor))return preferred;
  if(!points.length)throw new Error('No human-height camera space in '+name);
  points.sort((a,b)=>Math.hypot(a[0]-preferred[0],a[1]-preferred[1])-Math.hypot(b[0]-preferred[0],b[1]-preferred[1]));return points[0];
}
function interior(id,title,floor,room,preferred,target,lens=24){
  const p=chooseRoomPosition(floor,room,preferred),z=world.supportElevation(...p,floor)+1.65;
  views.push({id,title,group:`${floor+1}F室内`,mode:'full',cameraType:'PERSP',floor,position:[...p,z],target:[target[0],target[1],world.floors.get(floor).elevation+target[2]],lens,eyeHeight:1.65,room,coordinateSpace:'world'});
}
const buildingPoints=data.objects.filter(o=>o.kind==='mesh'&&o.name.includes('原图范围楼板')).flatMap(o=>o.vertices.map(v=>[v[0]+o.position[0],v[1]+o.position[1]]));
const body=bounds(buildingPoints),site=bounds(data.walkthrough.floors[0].boundary),cx=(site[0]+site[2])/2,cy=(site[1]+site[3])/2,span=Math.max(site[2]-site[0],site[3]-site[1]),roof=data.meta.roof_elevation;
views.push({id:'01',title:'完整建筑与庭院鸟瞰',group:'整体与庭院',mode:'full',cameraType:'ORTHO',position:[cx+span*.9,cy-span*.95,roof+span*.9],target:[cx,cy,roof*.38],orthoScale:span*1.3,coordinateSpace:'world'});
views.push({id:'02',title:'建筑另一侧鸟瞰',group:'整体与庭院',mode:'full',cameraType:'ORTHO',position:[cx-span,cy+span,roof+span*.8],target:[cx,cy,roof*.4],orthoScale:span*1.3,coordinateSpace:'world'});
for(const [i,floor] of data.walkthrough.floors.entries()){
  const polygons=data.objects.filter(o=>o.floor===floor.id&&o.kind==='mesh'&&o.name.includes('原图范围楼板')).flatMap(o=>o.vertices.map(v=>[v[0]+o.position[0],v[1]+o.position[1]]));
  const b=bounds(polygons),x=(b[0]+b[2])/2,y=(b[1]+b[3])/2;
  views.push({id:String(i+3).padStart(2,'0'),title:`${floor.label}完整俯视平面`,group:'楼层总览',mode:'cut',floor:floor.id,cameraType:'ORTHO',position:[x,y,floor.elevation+30],target:[x,y,floor.elevation],orthoScale:Math.max((b[2]-b[0])*1.08,(b[3]-b[1])*1.08*1600/1400),resolution:[1600,1400],coordinateSpace:'world'});
}
interior('06','客厅望向餐厅与中央电梯',0,'客厅',[8.6,5.3],[5.4,10,1.5],22);
interior('07','客厅休闲与采光面',0,'客厅',[7.3,8.0],[5.5,5.8,1.15],23);
interior('08','餐厅与中厨玻璃分隔',0,'餐厅',[4.48,8.99],[6.0,11.8,1.1],24);
interior('09','厨房工作区',0,'厨房',[7.24,13.02],[5.2,14.25,1.05],22);
interior('10','爸爸操盘工作区',0,'爸爸操盘房',[2.08,9.12],[1.15,11.55,1.1],22);
interior('11','父母卧室',0,'父母卧室',[3.05,1.83],[1.45,3.38,.9],22);
interior('12','二层夫妻主卧',1,'夫妻主卧',[7.21,4.69],[5.43,6.5,.9],23);
interior('13','儿童预留房',1,'儿童预留房',[3.04,1.77],[1.25,3.47,.9],23);
interior('14','二层家庭阅读区',1,'家庭阅读区',[2.10,9.16],[.85,11.55,1.1],23);
interior('15','三层书法房',2,'书法房',[6.04,9.23],[5.3,11.65,1.0],23);
interior('16','妈妈毛线工作室',2,'妈妈毛线工作室',[2.08,9.10],[1.25,11.68,1.0],22);
interior('17','妹妹卧室',2,'妹妹卧室',[3.04,1.9],[1.4,3.48,.9],23);
interior('18','三层露台花园',2,'妈妈露台花园',[7.1,4.0],[4.1,6.4,1.05],23);
interior('19','露台与室内工作区关系',2,'妈妈露台花园',[4.1,8.0],[7.1,4.2,1.0],24);
for(const room of allRooms.filter(r=>r.floor===0 && /南院|南花园|南侧庭院|室外花园/.test(r.name))){
  const b=bounds(room.polygon),p1=[b[2]-.6,b[1]+.6],p2=[b[0]+.7,b[1]+1.2];
  interior('20','南院人眼望向住宅',0,room.name,p1,[(body[0]+body[2])/2,body[1]+4,1.6],24);
  interior('21','南院休闲与种植细节',0,room.name,p2,[(b[0]+b[2])/2,(b[1]+b[3])/2,-.4+.75],24);
  views.at(-1).group=views.at(-2).group='整体与庭院';break;
}
for(const view of views.filter(v=>['20','21'].includes(v.id)))if(Math.abs(view.position[2]-1.25)>.001)throw new Error('Garden eye must be at 1.25 m: '+view.id);
const record={source:String(scenePath),coordinateSpace:'world',notes:['所有室内人眼位置从实际房间内的可站立位置求得，眼高1.65m。','顶视使用实际建筑楼板顶点包围范围；不会把庭院用地矩形当建筑轮廓。','庭院视角仅在输入包含匹配的经确认南院空间后产生。'],views};
await fs.writeFile(output,JSON.stringify(record,null,2));console.log(`Prepared ${views.length} camera views in ${output}`);
