// Real Chromium UI QA via CDP, using an isolated owned profile. No npm dependencies.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const out=path.join(root,'artifacts','m4');
const stamp=new Date().toISOString().replaceAll(':','');
const profile=path.join(out,`browser-${stamp}`);
fs.mkdirSync(profile,{recursive:true});
const executable='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const args=['--headless=new','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--no-first-run','--no-default-browser-check','about:blank'];
const browser=spawn(executable,args,{windowsHide:true,stdio:['ignore',fs.openSync(path.join(profile,'stdout.log'),'a'),fs.openSync(path.join(profile,'stderr.log'),'a')]});
const report={started_at_utc:new Date().toISOString(),status:'RUNNING',browser_pid:browser.pid,executable,
  executable_sha256:crypto.createHash('sha256').update(fs.readFileSync(executable)).digest('hex'),arguments:args,checks:[],screenshots:[],exceptions:[]};
const pause=ms=>new Promise(r=>setTimeout(r,ms));
let socket,sequence=0;const pending=new Map();
function call(method,params={}) {return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));setTimeout(()=>{if(pending.delete(id))reject(new Error('CDP_TIMEOUT '+method));},30000).unref();});}
async function evaluate(expression) {const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
async function ready() {for(let i=0;i<100;i++){try{if(await evaluate('document.readyState==="complete" && !!document.querySelector("main")'))return;}catch{}await pause(100);}throw new Error('PAGE_NOT_READY');}
async function go(route) {await call('Page.navigate',{url:'http://127.0.0.1:8081'+route});await ready();await pause(200);}
async function shot(name,full=false) {
  let clip;
  if(full){const x=await call('Page.getLayoutMetrics');clip={x:0,y:0,width:x.cssContentSize.width,height:x.cssContentSize.height,scale:1};}
  const r=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:full,...(clip?{clip}:{})});
  const file=path.join(out,`${name}.png`);fs.writeFileSync(file,Buffer.from(r.data,'base64'));
  report.screenshots.push({file:path.relative(root,file),run_id:report.run_id,publication_version:report.publication_version,scope:'real DEVELOPMENT UI / descriptive all-period dashboard',caption:name});
}
function check(ok,label){if(!ok)throw new Error(label);report.checks.push(label);}
async function submit(query,version) {
  await go('/basket');
  await evaluate(`(()=>{const wanted=new Set(${JSON.stringify(query)});document.querySelectorAll('#catalog input').forEach(e=>e.checked=wanted.has(e.value));${version!==undefined?`document.querySelector('[name=version]').value=${JSON.stringify(String(version))};`:''}document.querySelector('#basket-form').requestSubmit();})()`);
  for(let i=0;i<100;i++){await pause(100);try{if(await evaluate('location.pathname==="/recommend" && document.readyState==="complete"'))break;}catch{}}
  await ready();await pause(200);
  return evaluate('[...document.querySelectorAll("#recommendations article")].map(e=>({code:e.dataset.code,antecedent:e.dataset.antecedent}))');
}
try {
  for(let i=0;i<100&&!fs.existsSync(path.join(profile,'DevToolsActivePort'));i++)await pause(100);
  const port=Number(fs.readFileSync(path.join(profile,'DevToolsActivePort'),'utf8').split('\n')[0]);
  const targets=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  socket=new WebSocket(targets.find(x=>x.type==='page').webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
  socket.addEventListener('message',event=>{const r=JSON.parse(event.data);if(r.id&&pending.has(r.id)){const p=pending.get(r.id);pending.delete(r.id);r.error?p.reject(new Error(JSON.stringify(r.error))):p.resolve(r.result);}else if(r.method==='Runtime.exceptionThrown')report.exceptions.push(r.params);});
  await call('Page.enable');await call('Runtime.enable');
  report.browser_version=await call('Browser.getVersion');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await go('/');
  const provenance=await evaluate('({...document.querySelector(".provenance").dataset})');
  report.run_id=provenance.run;report.publication_version=Number(provenance.version);
  check(await evaluate('document.querySelector("#basket-count").textContent==="39516"'),'dashboard real basket count');
  await shot('overview');await shot('overview-full',true);
  await go('/patterns');check(await evaluate('document.querySelector("#evaluation").textContent.includes("505 / 4293")'),'development denominator visible');await shot('patterns');
  await go('/patterns?kind=itemsets&sort=frequency');await shot('itemsets');
  await go('/basket');
  check(await evaluate('document.querySelectorAll("#catalog input").length===4556'),'all train items in browser');
  await evaluate('document.querySelector("#catalog-search").value="HEART";document.querySelector("#catalog-search").dispatchEvent(new Event("input"))');
  check(await evaluate('[...document.querySelectorAll("#catalog label")].filter(e=>!e.hidden).every(e=>e.textContent.toLowerCase().includes("heart"))'),'client literal name search');
  await shot('catalog-search');
  let result=await submit(['21080','21094','21467','21770','22704','22969']);
  check(JSON.stringify(result)===JSON.stringify([{code:'21086',antecedent:'21080|21094'},{code:'21212',antecedent:'21080'}]),'real development query exact codes and best antecedents');
  report.real_case=result;await shot('recommendation-real');
  await evaluate('document.querySelector("#catalog-search").value="ZZZZ";document.querySelector("#catalog-search").dispatchEvent(new Event("input"))');
  check(await evaluate('document.querySelectorAll("#catalog input:checked").length===6'),'search preserves six selections');
  await evaluate('document.querySelector("#show-selected").click()');check(await evaluate('document.querySelectorAll("#catalog label:not([hidden])").length===6'),'selected-only control');
  result=await submit([]);check(result.length===0,'empty basket no prediction');await shot('empty-basket');
  result=await submit(['21080'],0);check(result.length===0,'stale form no prediction');check(await evaluate('document.querySelector("button[type=submit]").disabled'),'stale form requires reload');await shot('stale-form');
  await go('/basket');await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});await pause(200);
  check(await evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth'),'mobile basket no horizontal overflow');await shot('basket-mobile');
  check(report.exceptions.length===0,'no browser JavaScript exceptions');report.status='PASS';
} catch(e) {report.status='FAIL';report.error=String(e);throw e;}
finally {
  if(socket?.readyState===1){try{await call('Browser.close');}catch{}socket.close();}
  // Only this child is owned; a closed browser may already have exited.
  if(browser.exitCode===null){await Promise.race([new Promise(r=>browser.once('exit',r)),pause(5000)]);}
  report.browser_exit_code=browser.exitCode;
  report.finished_at_utc=new Date().toISOString();fs.writeFileSync(path.join(out,`browser-${stamp}.json`),JSON.stringify(report,null,2));
  console.log(JSON.stringify({status:report.status,checks:report.checks.length,screenshots:report.screenshots.length,receipt:`artifacts/m4/browser-${stamp}.json`}));
}
