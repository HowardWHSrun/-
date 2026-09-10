import fs from 'node:fs';
import {WalkthroughWorld,pointInPolygon} from './walkthrough-core.mjs';
const data=JSON.parse(fs.readFileSync(new URL('./unit6-scene.json',import.meta.url)));
const w=new WalkthroughWorld(data),step=.10,report=[];
for(const f of data.walkthrough.floors){
 w.player.floor=f.id;w.elevator.floor=f.id;w.elevator.z=f.elevation;w.elevator.state='idle';
 const xs=f.boundary.map(p=>p[0]),ys=f.boundary.map(p=>p[1]);
 const xmin=Math.floor(Math.min(...xs)/step)*step,ymin=Math.floor(Math.min(...ys)/step)*step;
 const nx=Math.ceil((Math.max(...xs)-xmin)/step)+1,ny=Math.ceil((Math.max(...ys)-ymin)/step)+1;
 const valid=new Uint8Array(nx*ny),seen=new Uint8Array(nx*ny);
 for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)valid[j*nx+i]=w.canStand(xmin+i*step,ymin+j*step)?1:0;
 const sx=Math.round((3.25-xmin)/step),sy=Math.round((10.45-ymin)/step),start=sy*nx+sx;
 if(!valid[start])throw Error(`F${f.id+1} cabin center invalid`);
 const queue=[start];seen[start]=1;
 for(let k=0;k<queue.length;k++){
  const p=queue[k],i=p%nx,j=Math.floor(p/nx);
  for(const [a,b]of [[i+1,j],[i-1,j],[i,j+1],[i,j-1]]){
   if(a<0||a>=nx||b<0||b>=ny)continue;const n=b*nx+a;
   if(valid[n]&&!seen[n]){seen[n]=1;queue.push(n);}
  }
 }
 const rooms=f.rooms.map(r=>{
  let available=0,reached=0,target=null;
  for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){
   const n=j*nx+i,x=xmin+i*step,y=ymin+j*step;
   if(valid[n]&&pointInPolygon(x,y,r.polygon)){available++;if(seen[n]){reached++;target??=[+x.toFixed(3),+y.toFixed(3)];}}
  }
  return {name:r.name,available,reached,reachable:reached>0,target};
 });
 const inaccessible=rooms.filter(r=>!r.reachable);
 report.push({floor:f.id+1,reachableCells:queue.length,walkableCells:valid.reduce((a,b)=>a+b,0),rooms,inaccessible});
 console.log(`F${f.id+1}`,`${queue.length} connected cells`,inaccessible.length?'UNREACHABLE '+inaccessible.map(r=>r.name).join(', '):'all rooms reachable');
 fs.writeFileSync(new URL(`./qa/unit6-nav-floor${f.id+1}.json`,import.meta.url),JSON.stringify({xmin,ymin,step,nx,ny,valid:[...valid],seen:[...seen],rooms}));
}
fs.writeFileSync(new URL('../output/unit6/房间通达检查.json',import.meta.url),JSON.stringify(report,null,2));
if(report.some(r=>r.inaccessible.length))process.exitCode=1;
