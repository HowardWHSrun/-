import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=fileURLToPath(new URL('../output/unit6-procurement/',import.meta.url));
const data=JSON.parse(await fs.readFile(path.join(root,'采购预算整合.json'),'utf8'));
const output=path.join(root,'outputs/01a088b6-e945-71b3-a8c3-0c06d22cd53e');
await fs.mkdir(output,{recursive:true});
const wb=Workbook.create();
const names=['预算总览','硬装与花园','家具与定制','家电与卫浴','施工队候选','复尺与未计项'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const palette={ink:'#263D38',header:'#34495A',line:'#DDE2DF',input:'#FFF2CE',blue:'#245BC1',muted:'#6B766F'};
const money='#,##0.00;(#,##0.00);"—"';
function base(s,lastCol,lastRow,title){
 s.showGridLines=false;
 const rg=s.getRange(`A1:${lastCol}${lastRow}`);rg.format.font={name:'Arial',size:11,color:palette.ink};rg.format.verticalAlignment='center';rg.format.rowHeight=24;
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={size:16,bold:true};s.getRange(`A3:${lastCol}3`).format.borders={bottom:{style:'thin',color:palette.line}};
}
function widths(s,ws){for(const [c,w] of Object.entries(ws))s.getRange(`${c}1:${c}4`).format.columnWidth=w;}
function header(s,rg){s.getRange(rg).format={fill:palette.header,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',rowHeight:30};}
const ranges={};
function costSheet(name,rows){
 const s=sheets[name],end=rows.length+6; ranges[name]={start:7,end};
 base(s,'O',end+2,`第6户 ${name}`);
 s.getRange('A3').values=[['人民币元。浅黄为可调输入；正式报价留空时采用预算单价，填0表示有效的零报价。']];
 s.getRange('A4').values=[['本表已计金额']];s.getRange('K4').formulas=[[`=SUM(K7:K${end})`]];s.getRange('K4').setNumberFormat(money);s.getRange('K4').format.font={size:14,bold:true};
 s.getRange('A6:M6').values=[['编号','类别','项目','品牌 / 型号 / 货号','数量','单位','预算单价','正式报价','计入1/0','采用单价','已计金额','价格类型','房间与尺寸条件']];header(s,'A6:M6');
 s.getRange('O6').values=[['来源链接与核价日期']];s.getRange('O6').format.font={bold:true,color:palette.muted};
 s.getRange(`A7:M${end}`).values=rows.map(r=>[r.id,r.category,r.name,r.model,r.quantity,r.unit,r.budgetUnitPrice,null,r.included?1:0,null,null,r.priceStatus,`${r.room||''} ${r.fitStatus||''}\n${r.scope||''}`.trim()]);
 s.getRange(`O7:O${end}`).values=rows.map(r=>[r.sourceUrl?`${r.sourceUrl}\n核对：${r.priceDate||data.asOf}`:`预算假设：${r.priceDate||data.asOf}，待实际询价`]);
 s.getRange(`J7:J${end}`).formulas=rows.map((r,i)=>[`=IF(ISBLANK(H${i+7}),G${i+7},H${i+7})`]);
 s.getRange(`K7:K${end}`).formulas=rows.map((r,i)=>[`=E${i+7}*J${i+7}*I${i+7}`]);
 s.getRange(`A7:O${end}`).format.wrapText=true;
 s.getRange(`A7:O${end}`).format.verticalAlignment='top';
 widths(s,{A:11,B:18,C:28,D:38,E:9,F:9,G:14,H:14,I:10,J:14,K:16,L:26,M:60,N:3,O:58});
 s.getRange(`E7:K${end}`).format.horizontalAlignment='right';s.getRange(`G7:K${end}`).setNumberFormat(money);s.getRange(`I7:I${end}`).setNumberFormat('0');s.getRange(`E7:E${end}`).setNumberFormat('0.###');
 for(const c of ['E','G','H','I']){s.getRange(`${c}7:${c}${end}`).format.fill=palette.input;s.getRange(`${c}7:${c}${end}`).format.font.color=palette.blue;}
 s.getRange(`J7:K${end}`).format.font.color='#000000';
 s.getRange(`I7:I${end}`).dataValidation={rule:{type:'whole',operator:'between',formula1:0,formula2:1}};
 s.getRange(`K7:K${end}`).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FBE7E5',font:{color:'#AA2222'}}});
 for(let r=7;r<=end;r++){if(r%2===0)s.getRange(`A${r}:D${r}`).format.fill='#F4F6F3';}
 s.getRange(`A7:O${end}`).format.autofitRows();
 s.freezePanes.freezeRows(6);s.freezePanes.freezeColumns(3);
 s.tabColor='#84988E';
 return end;
}
costSheet('硬装与花园',data.construction);
costSheet('家具与定制',data.furniture);
costSheet('家电与卫浴',data.appliances);
const total=(name)=>`'${name}'!$K$7:$K$${ranges[name].end}`;
const catTotal=(name,category)=>`SUMIFS(${total(name)},'${name}'!$B$7:$B$${ranges[name].end},"${category}")`;
const s=sheets['预算总览'];base(s,'L',43,'第6户 简约舒适预算');s.tabColor=palette.ink;
widths(s,{A:4,B:32,C:4,D:4,E:4,F:22,G:4,H:30,I:20,J:20,K:20,L:12});
s.getRange('A2').clear({applyTo:'contents'});s.getRange('B2').values=[['第6户 简约舒适预算']];s.getRange('B2').format.font={size:16,bold:true};
s.getRange('B3').values=[[`${data.asOf}  人民币  杭州/富阳暂定  未取得现场报价`]];
s.getRange('B5').values=[['毛坯长期自住：四位常住优先，未来儿童家具分期。']];
s.getRange('B7:F7').values=[['分项',null,null,null,'预算金额（元）']];header(s,'B7:F7');
const labels=['前期与验收','室内硬装','花园工程','成品家具','定制家具','家具附加','家电与卫浴','电梯暂列'];
const formulas=[...labels.slice(0,3).map(c=>'='+catTotal('硬装与花园',c)),...labels.slice(3,6).map(c=>'='+catTotal('家具与定制',c)),`=SUM(${total('家电与卫浴')})`,'='+catTotal('硬装与花园','电梯暂列')];
s.getRange('B8:B15').values=labels.map(x=>[x]);s.getRange('F8:F15').formulas=formulas.map(x=>[x]);
s.getRange('B16').values=[['已计范围小计']];s.getRange('F16').formulas=[['=SUM(F8:F15)']];
s.getRange('B18').values=[['预备费率（可调）']];s.getRange('F18').values=[[data.contingencyRate]];s.getRange('F18').setNumberFormat('0.0%');s.getRange('F18').format={fill:palette.input,font:{color:palette.blue}};
s.getRange('B19').values=[['已计范围预备费']];s.getRange('F19').formulas=[['=F16*F18']];
s.getRange('B21:B23').values=[['已计主方案预算'],['其中电梯及对应预备费'],['不含电梯的已计方案']];s.getRange('F21:F23').formulas=[['=SUM(F16,F19)'],['=F15*(1+F18)'],['=F21-F22']];
s.getRange('B21:F21').format.fill='#E9EEE8';s.getRange('B21:F21').format.font.bold=true;
let optional=Object.entries(ranges).map(([n,r])=>`SUMPRODUCT('${n}'!E7:E${r.end},'${n}'!J7:J${r.end})-SUM('${n}'!K7:K${r.end})`).join('+');
s.getRange('B25').values=[['未勾选可选升级（另计）']];s.getRange('F25').formulas=[['='+optional]];
s.getRange('B27:B28').values=[['你的预算上限（可填）'],['上限减已计预算']];s.getRange('F27').values=[[data.targetBudget]];s.getRange('F27').format={fill:palette.input,font:{color:palette.blue}};s.getRange('F28').formulas=[['=IF(ISBLANK(F27),"未设预算上限",F27-F21)']];
s.getRange('F8:F28').setNumberFormat(money);s.getRange('F18').setNumberFormat('0.0%');s.getRange('F28').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FBE7E5',font:{color:'#AA2222'}}});
s.getRange('H8').values=[['价格口径']];s.getRange('H9').values=[['商品显示价、预算预留和工程估算分列。']];
s.getRange('H11').values=[['单独列电梯']];s.getRange('H12').values=[['18万元为采购目标，尚无厂家报价。']];s.getRange('H13').values=[['不是某型号报价，也没有确认适配。']];
s.getRange('H15').values=[['调预算的方法']];s.getRange('H16').values=[['修改明细数量、单价或填写正式报价。']];s.getRange('H17').values=[['计入=0的可选项目不会加入主方案。']];
s.getRange('H20').values=[['重要未计费用']];s.getRange('H21').values=[['撤梯、开井、补板、加固未计价。']];s.getRange('H22').values=[['先核合法性和可施工方案，再询价。']];s.getRange('H23').values=[['预备费不代表已覆盖这些未知工程。']];
s.getRange('H26').values=[['工程量基础']];s.getRange('H27').values=[[`模型预算室内参考约${data.quantityBasis.interiorApproxM2.toFixed(1)}㎡。`]];s.getRange('H28').values=[['不是产权面积或施工结算面积。']];
s.getRange('B31').values=[['现阶段未计价项目']];s.getRange('B31').format.font.bold=true;
data.excludedUnpriced.forEach((r,i)=>s.getRange(`B${32+i}`).values=[[`${r.id} ${r.name}`]]);
s.getRange('B39').values=[['详细原因与采购前提见“复尺与未计项”。当前3D仍为P02示意家具。']];
s.getRange('F8:F28').format.horizontalAlignment='right';
const c=sheets['施工队候选'];base(c,'L',data.contractors.length+9,'杭州施工团队候选');
c.getRange('A3').values=[['公开资料初筛。未联系、未量房、无本案正式报价；资质和拟派项目经理须核验。']];
c.getRange('A6:H6').values=[['编号','品牌 / 合同主体','公开电话','服务区域','适合本案的依据','报价状态','需要核对','官方链接']];header(c,'A6:H6');
c.getRange(`A7:H${6+data.contractors.length}`).values=data.contractors.map(x=>[x.id,`${x.brand}\n${x.companyName}`,x.phone,x.serviceArea,x.whyShortlisted,'未联系 / 未报价',x.uncertainties.join('\n'),x.website]);
widths(c,{A:10,B:32,C:19,D:39,E:56,F:23,G:62,H:42,I:3,J:10,K:10,L:10});c.getRange(`A7:H${6+data.contractors.length}`).format.wrapText=true;c.getRange(`A7:H${6+data.contractors.length}`).format.verticalAlignment='top';c.getRange(`A7:H${6+data.contractors.length}`).format.autofitRows();c.freezePanes.freezeRows(6);
const f=sheets['复尺与未计项'];const issues=[...data.fitIssues,...data.excludedUnpriced.map(x=>({id:x.id,item:x.name,condition:x.why,action:'不作0元或已含处理；取得范围明确的正式报价后补入预算。'}))];
base(f,'F',issues.length+11,'尺寸、安装与未计范围');f.getRange('A3').values=[['先解决实际尺寸和施工条件，再锁定型号和订单。']];f.getRange('A6:D6').values=[['编号','项目','当前判断','下一步']];header(f,'A6:D6');f.getRange(`A7:D${6+issues.length}`).values=issues.map(x=>[x.id,x.item,x.condition,x.action]);widths(f,{A:12,B:28,C:80,D:76,E:3,F:15});f.getRange(`A7:D${6+issues.length}`).format.wrapText=true;f.getRange(`A7:D${6+issues.length}`).format.verticalAlignment='top';f.getRange(`A7:D${6+issues.length}`).format.autofitRows();f.freezePanes.freezeRows(6);
wb.recalculate();
const expected=data.totals.mainWithContingency;
const actual=s.getRange('F21').values[0][0];if(Math.abs(actual-expected)>.02)throw new Error(`Budget mismatch ${actual} vs ${expected}`);
// Exercise a real supplier quote, a valid zero quote and the inclusion control, then restore.
const detail=sheets['家具与定制'];const initial=detail.getRange('H7').values[0][0];const price=detail.getRange('G7').values[0][0],qty=detail.getRange('E7').values[0][0];
detail.getRange('H7').values=[[price+100]];wb.recalculate();if(Math.abs(s.getRange('F21').values[0][0]-actual-100*qty*(1+data.contingencyRate))>.02)throw new Error('Supplier quote did not update total');
detail.getRange('H7').values=[[0]];wb.recalculate();if(detail.getRange('K7').values[0][0]!==0)throw new Error('Zero quote incorrectly fell back');
detail.getRange('H7').values=[[initial??null]];detail.getRange('I7').values=[[0]];wb.recalculate();if(detail.getRange('K7').values[0][0]!==0)throw new Error('Inclusion switch failed');
detail.getRange('I7').values=[[1]];wb.recalculate();if(Math.abs(s.getRange('F21').values[0][0]-expected)>.02)throw new Error('Restore mismatch');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'final formula scan',maxChars:1800});
await fs.writeFile(path.join(output,'formula-inspection.json'),JSON.stringify(errors));
console.log((await wb.inspect({kind:'table',range:'预算总览!B7:F28',include:'values,formulas',tableMaxRows:22,tableMaxCols:5,maxChars:2500})).ndjson);
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(path.join(output,'第6户_施工与采购预算.xlsx'));await fs.copyFile(path.join(output,'第6户_施工与采购预算.xlsx'),path.join(root,'第6户_施工与采购预算.xlsx'));
const previews=[['预算总览','A1:L40'],['硬装与花园','A1:M11'],['家具与定制','A1:M11'],['家电与卫浴','A1:M11'],['施工队候选','A1:H11'],['复尺与未计项','A1:D13']];
for(const [name,range] of previews){const blob=await wb.render({sheetName:name,range,scale:1.3,format:'png'});await fs.writeFile(path.join(output,`${name}.png`),new Uint8Array(await blob.arrayBuffer()));}
await fs.writeFile(path.join(output,'workbook-validation.json'),JSON.stringify({mainBudget:expected,formulaValue:actual,supplierQuoteRecalculates:true,zeroQuotePreserved:true,inclusionControlRecalculates:true,restored:true,sheets:names},null,2));
console.log('Workbook exported and verified:',path.join(root,'第6户_施工与采购预算.xlsx'));
