"""Prepare the final P02 package as a static GitHub Pages document site."""
import hashlib, html, json, shutil
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent/'github-publication'
PACKAGE=ROOT/'output/第6户_住宅与花园_P02_完整交付包'
DOCS=REPO/'docs'
RELEASE='https://github.com/HowardWHSrun/-/releases/download/p02-v1/unit6-house-garden-p02.zip'
SITE='https://howardwhsrun.github.io/-/'
if not DOCS.exists():shutil.copytree(PACKAGE,DOCS)
else:
 for p in PACKAGE.rglob('*'):
  if p.is_file():
   t=DOCS/p.relative_to(PACKAGE);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
(DOCS/'.nojekyll').write_text('')
start=(PACKAGE/'开始查看.html').read_text()
start=start.replace('第6户住宅 · 开始查看','第6户住宅与花园 · 在线看家')
start=start.replace('完整解压后，双击此页即可查看。三维漫游可离线使用；PDF 适合逐页阅读，多角度图册适合放大比较空间。','三层住宅、南院与露台花园。直接进入三维空间，走进房间、乘电梯换层；也可以逐页阅读报告，或下载完整资料。')
start=start.replace('  <div class="choices">','  <img class="cover" src="图册/images/01_完整建筑与庭院鸟瞰.png" alt="第6户三层住宅和南院的整体模型鸟瞰" width="1600" height="1100">\n  <div class="choices">')
start=start.replace('.models{','.cover{display:block;width:100%;height:clamp(250px,42vw,460px);object-fit:contain;background:#d6d3cc;border-radius:14px;margin:0 0 26px}.downloads{display:flex;flex-wrap:wrap;gap:14px;margin:26px 0}.downloads a{padding:10px 17px;border:1px solid var(--line);border-radius:8px;text-decoration:none}.models{')
start=start.replace('  <div class="models">',f'  <nav class="downloads" aria-label="全部资料"><a href="files.html">全部文件与施工交接资料</a><a href="{RELEASE}">下载完整离线包 · 87 MB</a><a href="https://github.com/HowardWHSrun/-">GitHub 项目与源文件</a></nav>\n  <div class="models">')
start=start.replace('整体布局、室内外细节与多角度方案。','61页 A3 报告 · 约39 MB。')
start=start.replace('方案定位 DXF 保存在「图纸」文件夹，CSV 清单保存在「清单」文件夹。','三层 DXF、点位与材料 CSV、原始 DWG、验收表和来源核对记录，均可在「全部文件」中查看或下载。')
start=start.replace('保留整个文件夹结构。模型中的原图依据、改造内容与待核细部，以设计图册内的说明为准。','P02 · 2026.09.10。供方案确认、现场复测、交底与报价。不是签章施工图；撤梯、开井、补板等须先核合法性并完成专业深化。原图未核细部以报告说明为准。')
(DOCS/'index.html').write_text(start)

groups=[('阅读与交接','', '项目总结、PDF报告、打开说明与版本记录。'),('三维漫游','漫游','可直接在浏览器中走动，支持键盘和触屏。'),('模型与方案数据','模型','Blender可编辑源文件、GLB和场景数据。'),('三层定位图','图纸','毫米单位DXF方案定位底图。'),('材料、点位与验收','清单','材料询价、62个点位、门窗状态及6种交接记录空表。'),('原图依据','原图依据','原始DWG、提取数据与原图核对图。'),('项目核对记录','核对记录','几何、通达、来源以及施工交接结构化数据。'),('21个视角','图册','独立PNG与完整图册。')]
sections=[];inventory=[]
for title,prefix,description in groups:
 files=[p for p in PACKAGE.rglob('*') if p.is_file() and ((len(p.relative_to(PACKAGE).parts)==1) if prefix=='' else p.relative_to(PACKAGE).parts[0]==prefix)]
 rows=[]
 for p in sorted(files):
  rel=p.relative_to(PACKAGE).as_posix();size=p.stat().st_size;size_text=f'{size/1e6:.1f} MB' if size>=1e6 else f'{max(1,round(size/1000))} KB'
  rows.append(f'<li data-file="{html.escape(rel.lower(),quote=True)}"><a href="{quote(rel)}">{html.escape(rel if prefix else p.name)}</a><span>{html.escape(p.suffix[1:].upper() or "SHA256")} · {size_text}</span></li>')
  inventory.append({'path':rel,'bytes':size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 sections.append(f'<section><h2>{title}<small>{len(files)}</small></h2><p>{description}</p><ul>{"".join(rows)}</ul></section>')
catalog='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第6户 · 全部文件与施工交接资料</title><style>
*{box-sizing:border-box}body{margin:0;background:#f8f6f1;color:#243d38;font:16px/1.7 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1040px;margin:auto;padding:42px 24px}a{color:inherit;text-underline-offset:4px}nav{display:flex;gap:22px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,40px);font-weight:500;line-height:1.3;margin:35px 0 12px}.intro{max-width:780px;color:#64736c}input{width:100%;background:#fff;border:1px solid #c5cfc7;border-radius:9px;padding:15px;font:inherit;color:inherit;margin:18px 0}section{margin:28px 0 36px}h2{font-size:22px;font-weight:500;margin:0}h2 small{font-size:14px;font-weight:400;margin-left:10px;color:#64736c}section p{color:#64736c;margin:3px 0 13px}ul{list-style:none;padding:0;border-top:1px solid #d4d8cf}li{display:flex;gap:18px;align-items:baseline;justify-content:space-between;border-bottom:1px solid #d4d8cf;padding:12px 3px}li a{overflow-wrap:anywhere}li span{color:#64736c;font-size:13px;white-space:nowrap}footer{font-size:14px;border-top:1px solid #d4d8cf;padding-top:24px;margin-top:42px}a:focus-visible,input:focus-visible{outline:3px solid #b5814c;outline-offset:3px}[hidden]{display:none!important}@media(max-width:600px){main{padding:28px 18px}li{flex-direction:column;gap:2px;padding:10px 0}}
</style><main><nav><a href="index.html">← 返回在线看家</a><a href="RELEASE">完整离线 ZIP · 87 MB</a><a href="https://github.com/HowardWHSrun/-">GitHub 仓库</a></nav><h1>资料放在一起，交接更清楚。</h1><p class="intro">全部74份交付文件均已上传。可直接查看漫游、报告和图片；Blender、CAD及表格文件可下载后交给相应专业人员使用。报告与部分模型较大，加载时请稍候。</p><label for="search">查找文件</label><input id="search" type="search" placeholder="例如：门窗、验收、DWG、PDF、原图"><p id="count" role="status">共74份文件</p>SECTIONS<footer>P02设计交接版。用于现场复测、方案交底、分项报价和专业深化；未签章施工图。原图已核对范围、新增改造及待核内容在报告中分别标注。</footer></main><script>
const input=document.querySelector('#search');input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;document.querySelectorAll('li[data-file]').forEach(li=>{li.hidden=!li.dataset.file.includes(q);if(!li.hidden)n++});document.querySelectorAll('section').forEach(s=>s.hidden=![...s.querySelectorAll('li')].some(li=>!li.hidden));document.querySelector('#count').textContent=`显示 ${n} 份文件`;});
</script></html>'''
(DOCS/'files.html').write_text(catalog.replace('RELEASE',RELEASE).replace('SECTIONS',''.join(sections)))
(DOCS/'文件目录.json').write_text(json.dumps({'version':'P02','fileCount':len(inventory),'files':inventory},ensure_ascii=False,indent=2))
(REPO/'.gitignore').write_text('.DS_Store\n__pycache__/\n*.pyc\n*.blend1\n.venv/\nnode_modules/\n')
(REPO/'README.md').write_text(f'''# 第6户住宅与花园 · P02

**[在线漫游与图册]({SITE}) · [全部文件]({SITE}files.html) · [完整离线 ZIP]({RELEASE})**

基于原图最右端第6户（E4）的三层住宅与庭院方案。为父母、儿子未来小家庭和妹妹安排独立生活与兴趣空间，包含中央电梯、书法房、操盘工作区、毛线工作室、南院和开敞露台花园。

## 直接查看

- [三维步行漫游]({SITE}{quote('漫游/住宅漫游.html')})：拖动看四周，W/A/S/D 或方向键行走；走进电梯后选择楼层。触屏可使用界面上的行走按钮。
- [61页设计报告 PDF]({SITE}{quote('设计图册.pdf')})：约39 MB，含多角度效果图、方案定位、房间交底和施工专业接口。
- [21个模型视角]({SITE}{quote('图册/全部视角.html')})：整体、平面、室内与花园。
- [全部74份交付文件]({SITE}files.html)：Blender/GLB、3张DXF、62个方案点位、门窗表、材料表、验收记录、原图DWG及核对资料。
- [完整离线包]({RELEASE})：解压后双击 `开始查看.html`，无需服务器或联网。

## 仓库结构

- `docs/`：GitHub Pages发布目录，包含全部最终交付文件，浏览器入口 `index.html`。
- `source/`：模型、漫游和报告生成源码的存档；说明见该目录README。
- GitHub Release `p02-v1`：保留完整原交付ZIP，便于一次下载。

## 版本与使用边界

P02 / 2026-09-10。原始74文件与已交付ZIP对应，可用 `docs/文件校验清单.sha256` 或 `docs/文件目录.json` 核对。

本版用于家庭确认、现场复测、方案交底、分项报价与专业深化，**不是签章施工图或施工许可**。取消楼梯、开井、补板及新增坡道属于方案；实施前须先确认所在地合法性，完成结构、建筑疏散、电梯、机电和防水排水等专业核查。若法规不允许，须改方案。

38处门窗中6处北窗有对应立面依据，其余32处竖向仍待核；模型屋顶完整形态和部分完成面尚未核实。不得依据透视截图量尺寸或直接拆改、开孔、采购。

## GitHub Pages

使用 `main` 分支的 `/docs` 目录发布。入口和资料均为静态文件，漫游已打包Three.js，无外部CDN、数据库或后端。更新 `docs/` 并推送后GitHub Pages自动重新部署。

Third-party viewer license: [Three.js MIT](docs/{quote('漫游/第三方许可.txt')}). 原始建筑图纸保留来源；本仓库未对其重新授予许可。
''')
print(f'Prepared {len(inventory)} original deliverables plus online index and file library in {DOCS}')
