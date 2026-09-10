"""Publish reviewed procurement data alongside the unchanged P02 design."""
import json,shutil,csv,hashlib,re,html,zipfile
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output/unit6-procurement';REPO=ROOT.parent/'github-publication';DOCS=REPO/'docs';DEST=DOCS/'采购与报价';DEST.mkdir(exist_ok=True)
D=json.loads((OUT/'采购预算整合.json').read_text());T=D['totals'];C=json.loads((OUT/'research/contractors.json').read_text())
# Blank actual-quote columns are intentionally not zero.
with (OUT/'施工方逐项回填报价.csv').open('w',encoding='utf-8-sig',newline='') as fh:
 w=csv.writer(fh);w.writerow(['编号','项目','当前数量','单位','业主预算单价','本期计入','现场实测量','施工方含税单价','人工','主材品牌型号','辅材品牌型号','损耗计法','安装运输','税管理费是否已含','报价有效期','工期及交期','排除范围','说明'])
 for r in D['construction']+D['furniture']+D['appliances']:w.writerow([r['id'],r['name'],r['quantity'],r['unit'],r['budgetUnitPrice'],1 if r['included'] else 0]+['']*12)
readme=f'''# 第6户采购补充 V1

2026-09-10。用户确认毛坯、长期自住，风格简约舒适。地区暂按原图杭州/富阳，尚未确认实际城市区县。

当前已计预算 **¥{T['mainWithContingency']:,.2f}**（含12%预备费），不含电梯部分 **¥{T['withoutElevator']:,.2f}**。电梯系统18万元仅采购目标，非厂家报价。撤梯、开井、补板和加固等未计，不是全包封顶价。

## 从哪里看

- `第6户_预算采购与施工询价.pdf`：完整预算、型号清单、施工队、电梯候选、复尺条件、施工采购顺序与来源。
- `第6户_施工与采购预算.xlsx`：6个工作表。数量/预算单价/正式报价/计入可改；正式报价空白时用预算值，0为有效零报价。
- 三类CSV：供查阅或导入；`施工方逐项回填报价.csv`保留施工方填写栏。
- `采购预算整合.json`是本版网站和报告汇总的数据依据。
- `来源研究/`保留原始及调整过程研究。**原始 furniture/appliances 的旧合计不是本版总预算**；以整合JSON和本目录Excel/PDF为准。家具采用valuePlan分期，家电采用valuePlan并加网络/叠放配件1700元。

## 预算边界

- 硬装工程量与单价是预算假设，家具/家电逐行区分官网显示、参考价和暂列。地区库存、运输、安装和含税报价待核。
- 家具一期70632.88元；儿童家具及后添桌椅9530.88元延后。非标定制要复尺与签认加工图。
- 本轮补入淋浴侧屏、地漏小五金、合法洗衣点、燃气专业服务及三层网络；没有虚构完整型号或保证未知安装条件。
- 先按3家装修企业同清单询价：铭品、南鸿、都都；未联系、未量房、未报价。另有尚层、圣都范围对照。
- 电梯先询康力KLJ、西奥SIND/SINDII，快意VILLUX作对照；没有厂家确认适配1410×1660mm净井。
- 现三维仍为P02示意，未改原边界，也未置换为这些品牌实物。玻璃封闭阳光房未列入本版。

## 离线打开

完整解压ZIP后打开根目录`index.html`，点“预算与采购”。该页已内嵌发布数据，双击亦可搜索和试算。修改仅保存在此浏览器；恢复发布值用“恢复初始”。Excel与PDF独立可打开。

## 下一步

确认城市/区县与现场条件，安排毛坯验收、复尺，先解决电梯/撤梯合法性与专业条件；然后让候选提交同范围实际报价。未发出任何询价消息，也未采购或签约。
'''
(OUT/'预算阅读说明.md').write_text(readme)
rfp='# 第6户施工与采购询价任务书（待业主安排发送）\n\n本案毛坯、三层自住、简约舒适。地区杭州/富阳暂定；无现场报价。原图与P02边界为基础；不能承诺未核合法性的撤梯/开井工程。\n\n'
rfp+='\n'.join(f'{i}. {v}' for i,v in enumerate(C['inquiryChecklist'],1))+'\n\n请填写《施工方逐项回填报价.csv》，对暂估工程量逐项复测。报价须列同品牌型号、范围与不包含项，明确分包、合同主体、验收、变更、保修及含税费用。\n'
(OUT/'施工询价任务书.md').write_text(rfp)
mainfiles=['第6户_预算采购与施工询价.pdf','第6户_施工与采购预算.xlsx','硬装与花园.csv','家具与定制.csv','家电与卫浴.csv','施工方逐项回填报价.csv','采购预算整合.json','工程量预算依据.json','预算基础数据.json','项目预算与采购总结.md','预算阅读说明.md','施工询价任务书.md']
for f in mainfiles:shutil.copy2(OUT/f,DEST/f)
research=DEST/'来源研究';research.mkdir(exist_ok=True)
for f in (OUT/'research').iterdir():
 if f.suffix in ['.md','.json']:shutil.copy2(f,research/f.name)
# Keep a self-contained data snapshot for file:// viewing, while online fetch uses the same JSON.
p=DOCS/'procurement.html';s=p.read_text();s=re.sub(r'<script id="embedded-procurement" type="application/json">.*?</script>\s*','',s,flags=re.S)
blob=json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c');s=s.replace('</body>',f'<script id="embedded-procurement" type="application/json">{blob}</script>\n</body>');p.write_text(s)
release='https://github.com/HowardWHSrun/-/releases/download/procurement-v1/unit6-house-procurement-v1.zip'
p=DOCS/'index.html';s=p.read_text();s=s.replace('grid-template-columns:repeat(3,minmax(0,1fr))','grid-template-columns:repeat(2,minmax(0,1fr))');s=s.replace('  <div class="choices">','  <div class="choices">\n    <a class="choice" href="procurement.html"><span>新增 / 毛坯长期自住</span><strong>预算与采购</strong><span>118项预算 · 家具型号 · 施工队与电梯候选 · 可改价试算。</span></a>' if 'href="procurement.html"' not in s else '  <div class="choices">')
s=s.replace('https://github.com/HowardWHSrun/-/releases/download/p02-v1/unit6-house-garden-p02.zip',release).replace('下载完整离线包 · 87 MB','下载含预算的完整离线包');s=s.replace('<footer>P02 ·','<footer>P02设计 + 采购补充V1 ·');p.write_text(s)
# The original P02 hash manifest stays unchanged; this additional manifest describes the new supplement.
newpaths=sorted(p for p in DEST.rglob('*') if p.is_file() and p.name!='采购补充文件校验.sha256')
(DEST/'采购补充文件校验.sha256').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(DEST).as_posix() for p in newpaths)+'\n')
# Fresh complete catalog, excluding itself and the generated HTML catalog to avoid circular hashes.
paths=sorted(p for p in DOCS.rglob('*') if p.is_file() and not p.name.startswith('.') and p.name not in ['文件目录.json','files.html'])
records=[{'path':p.relative_to(DOCS).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
(DOCS/'文件目录.json').write_text(json.dumps({'version':'P02 + Procurement V1','fileCount':len(records),'note':'目录不含自身与files.html；原P02校验清单仍对应P02原始文件。','files':records},ensure_ascii=False,indent=2))
old=(DOCS/'files.html').read_text();css=old[old.index('<style>')+7:old.index('</style>')];groups=[('采购预算与施工询价',lambda x:x.startswith('采购与报价/')),('在线入口',lambda x:x in ['index.html','procurement.html']),('原设计资料',lambda x:True)];seen=set();sections=[]
for name,predicate in groups:
 rs=[r for r in records if r['path'] not in seen and predicate(r['path'])];seen.update(r['path'] for r in rs)
 li=''.join(f'<li data-file="{html.escape(r["path"].lower())}"><a href="{quote(r["path"])}">{html.escape(r["path"])}</a><span>{r["bytes"]/1e6:.1f} MB</span></li>' if r['bytes']>=1000000 else f'<li data-file="{html.escape(r["path"].lower())}"><a href="{quote(r["path"])}">{html.escape(r["path"])}</a><span>{max(1,round(r["bytes"]/1000))} KB</span></li>' for r in rs)
 sections.append(f'<section><h2>{name}<small>{len(rs)}</small></h2><ul>{li}</ul></section>')
js="const input=document.querySelector('#search');input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;document.querySelectorAll('li[data-file]').forEach(li=>{li.hidden=!li.dataset.file.includes(q);if(!li.hidden)n++});document.querySelectorAll('section').forEach(s=>s.hidden=![...s.querySelectorAll('li')].some(li=>!li.hidden));document.querySelector('#count').textContent=`显示 ${n} 份文件`;});"
(DOCS/'files.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第6户 · 全部文件</title><style>{css}</style><main><nav><a href="index.html">← 在线看家</a><a href="procurement.html">预算与采购</a><a href="{release}">完整离线 ZIP</a></nav><h1>资料放在一起，交接更清楚。</h1><p class="intro">P02原设计与采购补充V1。新增118项预算、家具型号与施工询价资料。来源研究旧合计保留为过程记录，当前预算以采购整合数据和新版Excel/PDF为准。目录列{len(records)}份文件；<a href="文件目录.json">机器可读目录</a>另附。</p><label for="search">查找文件</label><input id="search" type="search" placeholder="例如：预算、家具、验收、PDF、原图"><p id="count" role="status">共{len(records)}份文件</p>{"".join(sections)}<footer>供现场复测、深化与分项报价。未签章施工图；没有施工队正式报价；未知结构工程不在预算内。</footer></main><script>{js}</script></html>')
# New reproducible source files, avoiding local caches and vendor full documents.
src=REPO/'source/home-design';src.mkdir(parents=True,exist_ok=True)
for name in ['build_procurement_data.py','merge_procurement_data.py','build_procurement_report.py','prepare_procurement_publication.py']:shutil.copy2(ROOT/name,src/name)
(src/'procurement').mkdir(exist_ok=True);wb=(ROOT/'tmp/procurement-builder/build_workbook.mjs').read_text().replace("new URL('../../output/unit6-procurement/'", "new URL('../output/unit6-procurement/'");(src/'procurement/build_workbook.mjs').write_text(wb)
sd=src/'output/unit6-procurement';sd.mkdir(parents=True,exist_ok=True)
for name in ['工程量预算依据.json','预算基础数据.json','采购预算整合.json']:shutil.copy2(OUT/name,sd/name)
(sd/'research').mkdir(exist_ok=True)
for f in (OUT/'research').iterdir():
 if f.suffix in ['.json','.md','.py']:shutil.copy2(f,sd/'research'/f.name)
(src/'procurement/README.md').write_text('预算补充构建顺序：build_procurement_data.py → merge_procurement_data.py → build_procurement_report.py / procurement/build_workbook.mjs。需要ReportLab、pypdf、Pillow、macOS宋体和@oai/artifact-tool；原始研究JSON已提供，不必重新访问商家。prepare_procurement_publication.py按本地原工作区路径组织发布，移植时须设置ROOT/REPO路径。金额来源见每行，工程单价为估算。\n')
rr=REPO/'README.md';text=rr.read_text();heading='## 采购补充 V1（毛坯长期自住）'
if heading in text:text=text.split(heading)[0].rstrip()+'\n'
text+=f'\n{heading}\n\n[在线预算、型号与施工队](https://howardwhsrun.github.io/-/procurement.html) · [最新完整ZIP]({release})\n\n当前已计约83.8万元（含12%预备费），不含电梯约63.6万元；18万元电梯为采购目标，撤梯开井等未知费用未计。118行明细、可修改Excel和48页采购PDF均在`docs/采购与报价`。完整以文件当前值为准。未联系或委托候选施工方，不是正式工程报价。原P02几何和原始图册保留。\n';rr.write_text(text)
print('Published files ready:',len(records),'catalog entries;',len(newpaths),'procurement files')
