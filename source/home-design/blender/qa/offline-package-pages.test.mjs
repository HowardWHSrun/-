import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {chromium} from '/Users/howardwang/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1200,height:950}});
await page.context().setOffline(true);
const network=[],errors=[];page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});page.on('pageerror',e=>errors.push(e.message));
const start=new URL('../../output/unit6-professional/开始查看.html',import.meta.url).href;
const screenshot=async name=>page.screenshot({path:fileURLToPath(new URL('./'+name+'.png',import.meta.url))});
const result={offline:true};
try{
 await page.goto(start);assert.equal(await page.locator('h1').textContent(),'从这里，走进你的家。');
 assert.equal(await page.locator('a[href="项目总结与施工交接说明.txt"]').count(),1);await screenshot('offline-package-start');
 await page.getByText('浏览全部角度',{exact:true}).click();
 assert.equal(await page.locator('figure').count(),21);
 await page.locator('img').evaluateAll(images=>images.forEach(im=>im.loading='eager'));
 await page.waitForFunction(()=>Array.from(document.images).every(im=>im.complete&&im.naturalWidth>0));await screenshot('offline-package-gallery');
 result.galleryImages=await page.locator('img').count();
 await page.setViewportSize({width:360,height:800});await page.goto(start);await screenshot('offline-package-start-mobile');
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.getByText('进入三维漫游',{exact:true}).click();
 await page.waitForFunction(()=>{const b=document.querySelector('[data-enter]');return b&&!b.disabled});
 await screenshot('offline-package-walk-mobile');
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 result.mobileWidth=360;result.errors=errors;result.networkRequests=network;assert.deepEqual(errors,[]);assert.deepEqual(network,[]);result.passed=true;
}catch(e){result.passed=false;result.error=e.message;process.exitCode=1;}
finally{await fs.writeFile(new URL('./offline-package-pages-results.json',import.meta.url),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));await browser.close();}
