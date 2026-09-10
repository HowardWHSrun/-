import assert from 'node:assert/strict';
import {chromium} from '/Users/howardwang/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {fileURLToPath} from 'node:url';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1000,height:850}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
try {
  await page.goto(new URL('./engine-synthetic-preview.html',import.meta.url).href);
  const frame=page.frameLocator('iframe');
  const enter=frame.locator('[data-enter]');
  await enter.waitFor();
  for(let n=0;n<100 && await enter.isDisabled();n++)await page.waitForTimeout(200);
  if(await enter.isDisabled())throw new Error('Renderer startup: '+await frame.locator('[data-loading]').textContent());
  const inspect=fn=>frame.locator('#family-house-walkthrough').evaluate((el,source)=>new Function('w',`return (${source})(w)`)(el.walkthroughInspection),fn.toString());
  assert.equal(await inspect(v=>v.camera.position.z),1.65);
  assert.equal(await inspect(v=>v.sourceMeshCount),45);
  assert.equal(await frame.locator('[data-floor="2"]').isDisabled(),true);
  await enter.click();
  await page.keyboard.down('KeyW');
  for(let n=0;n<120;n++) {if(await inspect(v=>v.world.player.y)>5.45)break;await page.waitForTimeout(50);}
  await page.keyboard.up('KeyW');
  assert.equal(await inspect(v=>v.world.inCabin()),true,'Keyboard walking reaches elevator through real door openings');
  assert.equal(await inspect(v=>v.world.player.floor),0);
  await frame.locator('[data-floor="2"]').click();
  const heights=[];
  for(let n=0;n<200;n++) {heights.push(await inspect(v=>v.camera.position.z));if(await inspect(v=>v.world.player.floor===2 && v.world.elevator.state==='idle'))break;await page.waitForTimeout(50);}
  assert(heights.some(z=>z>2 && z<8));
  assert.equal(await inspect(v=>v.world.player.floor),2);
  assert(Math.abs((await inspect(v=>v.camera.position.z))-8.55)<1e-9);
  const canvas=frame.locator('[data-stage] > canvas:not([data-map])'),rect=await canvas.boundingBox();
  const yawBefore=await inspect(v=>v.world.player.yaw);
  await page.mouse.move(rect.x+rect.width*.4,rect.y+rect.height*.5);await page.mouse.down();await page.mouse.move(rect.x+rect.width*.55,rect.y+rect.height*.48,{steps:8});await page.mouse.up();
  assert((await inspect(v=>v.world.player.yaw))>yawBefore+.1,'Pointer drag rotates view without Pointer Lock');
  // Return the gaze by user input, then verify a held on-screen walk button.
  await page.mouse.move(rect.x+rect.width*.55,rect.y+rect.height*.48);await page.mouse.down();await page.mouse.move(rect.x+rect.width*.4,rect.y+rect.height*.5,{steps:8});await page.mouse.up();
  const back=await frame.locator('[data-move="backward"]').boundingBox();
  const beforeButton=await inspect(v=>v.world.player.y);
  await page.mouse.move(back.x+back.width/2,back.y+back.height/2);await page.mouse.down();await page.waitForTimeout(600);await page.mouse.up();
  assert((await inspect(v=>v.world.player.y))<beforeButton-.5,'Press-and-hold movement button works');
  await page.keyboard.press('Escape');
  assert.equal(await enter.textContent(),'进入漫游');
  assert.equal(await frame.locator('[data-move="forward"]').isDisabled(),true);
  await page.screenshot({path:fileURLToPath(new URL('./engine-synthetic-tested.png',import.meta.url))});
  await page.setViewportSize({width:360,height:900});await page.waitForTimeout(250);
  assert(await frame.locator('#family-house-walkthrough').evaluate(el=>el.scrollWidth<=el.clientWidth+1),'Controls fit narrow viewport');
  await page.screenshot({path:fileURLToPath(new URL('./engine-synthetic-mobile.png',import.meta.url))});
  assert.deepEqual(errors,[]);
  console.log('PASS Chromium: WebGL rendering, 45 full-wall source objects, keyboard walking through doors, cabin-only floor controls, continuous ride over elevations 0/3.7/6.9, drag look without Pointer Lock, Escape pause; no page errors. Synthetic geometry only.');
} finally {await browser.close();}
