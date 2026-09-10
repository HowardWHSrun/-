import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {chromium} from '/Users/howardwang/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {fileURLToPath} from 'node:url';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1050,height:920}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const networkRequests=[];page.on('request',r=>{if(/^https?:/.test(r.url()))networkRequests.push(r.url());});
await page.context().setOffline(true);
const terraceOnly=process.argv.includes('--terrace-only');
const includeGarden=process.argv.includes('--include-garden');
const result={steps:[],errors,networkRequests,offline:true,scope:terraceOnly?'3F lift, workrooms and terrace'+(includeGarden?', plus south garden':''):'full house and garden'};
try {
  await page.goto(new URL('../../output/unit6-professional/漫游/住宅漫游.html',import.meta.url).href);
  const frame=page;
  const enter=frame.locator('[data-enter]');await enter.waitFor();
  for(let n=0;n<100 && await enter.isDisabled();n++)await page.waitForTimeout(200);
  if(await enter.isDisabled())throw new Error('Renderer startup: '+await frame.locator('[data-loading]').textContent());
  const root=frame.locator('#family-house-walkthrough');
  const inspect=fn=>root.evaluate((el,source)=>new Function('v',`return (${source})(v)`)(el.walkthroughInspection),fn.toString());
  const screenshot=async name=>page.screenshot({path:fileURLToPath(new URL('./'+name+'.png',import.meta.url))});
  const getPlayer=()=>inspect(v=>({x:v.world.player.x,y:v.world.player.y,yaw:v.world.player.yaw,floor:v.world.player.floor,z:v.camera.position.z,room:v.world.roomName}));
  const sourceBytes=await fs.readFile(new URL('../unit6-professional-scene.json',import.meta.url));
  const sourceData=JSON.parse(sourceBytes);
  assert.deepEqual(await inspect(v=>v.world.data),sourceData);
  result.sourceSha256=createHash('sha256').update(sourceBytes).digest('hex');result.sourceObjects=sourceData.objects.length;result.embeddedDataMatches=true;
  result.sourceMeshCount=await inspect(v=>v.sourceMeshCount);
  assert(result.sourceMeshCount>1000);assert.equal(await inspect(v=>v.camera.position.z),1.65);
  await screenshot('unit-six-offline-entry');await enter.click();
  const canvas=frame.locator('[data-stage] > canvas:not([data-map])');
  async function faceYaw(yaw){
    for(let n=0;n<8;n++){
      const p=await getPlayer();let delta=Math.atan2(Math.sin(yaw-p.yaw),Math.cos(yaw-p.yaw));if(Math.abs(delta)<.012)return;
      const box=await canvas.boundingBox(),pixels=Math.max(-box.width*.36,Math.min(box.width*.36,delta/.003));
      await page.mouse.move(box.x+box.width/2,box.y+box.height*.55);await page.mouse.down();await page.mouse.move(box.x+box.width/2+pixels,box.y+box.height*.55,{steps:6});await page.mouse.up();
    }
    throw new Error('Unable to turn view to path direction');
  }
  async function plan(goal){
    return root.evaluate((el,goal)=>{
      const w=el.walkthroughInspection.world,p=w.player,step=.12,queue=[[p.x,p.y]],parents=[-1],seen=new Set(['0,0']),coords=[[0,0]];
      const rooms=[...(w.floors.get(p.floor).rooms || []),...(w.config.rooms || []).filter(r=>r.floor===p.floor)];
      const room=rooms.find(r=>r.name===goal.room);
      const pip=(x,y,poly)=>{let inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside;};
      const clearance=(x,y,poly)=>Math.min(...poly.map((a,i)=>{const b=poly[(i+1)%poly.length],dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy || 1)));return Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy);}));
      const matches=(x,y)=>goal.cabin?Math.hypot(x-(w.elevator.bounds[0]+w.elevator.bounds[2])/2,y-(w.elevator.bounds[1]+w.elevator.bounds[3])/2)<.10:goal.point?Math.hypot(x-goal.point[0],y-goal.point[1])<.12:room && pip(x,y,room.polygon) && clearance(x,y,room.polygon)>.16;
      let hit=-1;
      for(let at=0;at<queue.length && at<30000;at++){
        const [x,y]=queue[at];if(matches(x,y)){hit=at;break;}
        for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){
          const ix=coords[at][0]+dx,iy=coords[at][1]+dy,key=ix+','+iy;if(seen.has(key))continue;
          const nx=p.x+ix*step,ny=p.y+iy*step,mx=(x+nx)/2,my=(y+ny)/2;if(!w.canStep(x,y,mx,my)||!w.canStep(mx,my,nx,ny))continue;
          seen.add(key);
          queue.push([nx,ny]);coords.push([ix,iy]);parents.push(at);
        }
      }
      if(hit<0)throw new Error('No walkable route to '+JSON.stringify(goal)+' on '+w.location+'; searched '+queue.length+' cells');
      const path=[];for(let i=hit;i>=0;i=parents[i])path.push(queue[i]);path.reverse();
      const line=(a,b)=>{const n=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/.04);let p=a;for(let i=1;i<=n;i++){const q=[a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n];if(!w.canStep(...p,...q))return false;p=q;}return true;};
      const simple=[path[0]];let from=0;while(from<path.length-1){let to=path.length-1;while(to>from+1&&!line(path[from],path[to]))to--;simple.push(path[to]);from=to;}
      return simple;
    },goal);
  }
  async function walkTo(goal){
    const path=await plan(goal);result.steps.push({goal,path});
    for(const target of path.slice(1)){
      const start=await getPlayer(),length=Math.hypot(target[0]-start.x,target[1]-start.y);if(length<.07)continue;
      await faceYaw(Math.atan2(target[0]-start.x,target[1]-start.y));
      await page.keyboard.down('KeyW');
      let arrived=false;
      try{for(let n=0;n<Math.ceil((length/1.3+3)*20);n++){
        const p=await getPlayer(),distance=Math.hypot(target[0]-p.x,target[1]-p.y);
        const along=((p.x-start.x)*(target[0]-start.x)+(p.y-start.y)*(target[1]-start.y))/length;
        if(distance<.075 || along>=length-.045){arrived=true;break;}
        await page.waitForTimeout(50);
      }}finally{await page.keyboard.up('KeyW');}
      if(!arrived)throw new Error('Keyboard walk did not reach '+JSON.stringify(target)+'; current '+JSON.stringify(await getPlayer()));
    }
    result.steps.push({arrived:await getPlayer()});
    if(goal.room)assert.equal((await getPlayer()).room,goal.room);
  }
  async function rideTo(floor){
    assert(await inspect(v=>v.world.inCabin()));await frame.locator(`[data-floor="${floor}"]`).click();
    for(let n=0;n<240;n++){if(await root.evaluate((el,f)=>el.walkthroughInspection.world.player.floor===f&&el.walkthroughInspection.world.elevator.state==='idle',floor))break;await page.waitForTimeout(50);}
    assert.equal((await getPlayer()).floor,floor);result.steps.push({elevatorArrival:await getPlayer()});
  }
  if((!terraceOnly||includeGarden)&&!process.argv.includes('--skip-garden')){
  await walkTo({point:[6.6,2.6]});assert(Math.abs((await getPlayer()).z-1.6)<.001);await screenshot('unit-six-offline-porch');
  await walkTo({point:[6.6,0]});const rampMid=await getPlayer();assert(rampMid.z>1.25&&rampMid.z<1.6);result.rampMid=rampMid;
  await walkTo({point:[6.6,-2.5]});assert(Math.abs((await getPlayer()).z-1.25)<.001);await faceYaw(0);await screenshot('unit-six-offline-garden');
  await walkTo({point:[6.6,2.6]});assert(Math.abs((await getPlayer()).z-1.6)<.001);
  await walkTo({room:'客厅'});assert.equal((await getPlayer()).z,1.65);
  }
  await walkTo({cabin:true});assert(await inspect(v=>v.world.inCabin()));
  await screenshot('unit-six-offline-elevator-1f');
  await frame.locator('[data-floor="2"]').click();
  const heights=[];for(let n=0;n<240;n++){heights.push(await inspect(v=>v.camera.position.z));if(await inspect(v=>v.world.player.floor===2&&v.world.elevator.state==='idle'))break;await page.waitForTimeout(50);}
  assert(heights.some(z=>z>2&&z<8));assert.equal(await inspect(v=>v.world.player.floor),2);assert(Math.abs((await inspect(v=>v.camera.position.z))-8.55)<1e-8);
  await walkTo({room:'书法房'});await screenshot('unit-six-offline-calligraphy');
  await walkTo({room:'妈妈毛线工作室'});await screenshot('unit-six-offline-yarn');
  await walkTo({room:'妈妈露台花园'});assert(Math.abs((await inspect(v=>v.camera.position.z))-(6.87+1.65))<1e-8);await screenshot('unit-six-offline-terrace');
  if(terraceOnly){
    await walkTo({point:[6.38,6.10]});assert(Math.abs((await getPlayer()).z-8.52)<1e-8);await faceYaw(0);await screenshot('unit-six-offline-terrace-workbench');
    await walkTo({cabin:true});await rideTo(0);assert.equal((await getPlayer()).z,1.65);
  }else{
  await walkTo({cabin:true});await rideTo(1);assert(Math.abs((await inspect(v=>v.camera.position.z))-5.35)<1e-8);
  await walkTo({room:'夫妻主卧'});await screenshot('unit-six-offline-master-bedroom');
  await walkTo({room:'儿童预留房'});await screenshot('unit-six-offline-child-room');
  await walkTo({cabin:true});await rideTo(0);assert.equal(await inspect(v=>v.camera.position.z),1.65);
  await walkTo({room:'爸爸操盘房'});await screenshot('unit-six-offline-trading');
  await walkTo({room:'厨房'});await screenshot('unit-six-offline-kitchen');
  }
  await page.keyboard.press('Escape');assert.equal(await enter.textContent(),'进入漫游');
  assert.deepEqual(errors,[]);assert.deepEqual(networkRequests,[]);result.passed=true;console.log(JSON.stringify(result,null,2));
} catch(error){result.passed=false;result.error=error.message;console.error(error);try{await page.screenshot({path:fileURLToPath(new URL('./unit-six-offline-failed.png',import.meta.url))});}catch{};process.exitCode=1;}
finally{await fs.writeFile(new URL('./unit-six-offline-browser-results.json',import.meta.url),JSON.stringify(result,null,2));await browser.close();}
