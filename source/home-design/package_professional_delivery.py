"""Assemble only user-facing deliverables; verify links and a clean ZIP extraction."""
import hashlib, json, re, shutil, zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'output/unit6-professional'
NAME='第6户_住宅与花园_P02_完整交付包'
DEST=ROOT/'output'/NAME
ZIP=DEST.with_suffix('.zip')
EXPECTED='e9501fa42af81245b9acfdc1a1fd88f5f7d8ad7b7d4ec4ca1fda0ca6af334a2b'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def copy_file(src,rel):
 target=DEST/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)

def plain_summary():
 md=(SRC/'项目总结与施工交接说明.md').read_text()
 # Expand Markdown tables into labeled records for plain text readers.
 lines=[];header=None
 for line in md.splitlines():
  if line.startswith('|'):
   cells=[s.strip() for s in line.strip().strip('|').split('|')]
   if all(re.fullmatch(r'[-: ]+',s) for s in cells):continue
   if header is None:header=cells;continue
   lines.append(' · '.join(f'{header[i] if i<len(header) else "补充"}：{cell}' for i,cell in enumerate(cells)))
   lines.append('')
  else:
   header=None
   line=re.sub(r'^#{1,6}\s+','',line).replace('**','').replace('`','')
   line=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1（\2）',line)
   lines.append(line)
 return '\n'.join(lines)+'\n'

def assemble():
 assert sha(ROOT/'blender/unit6-professional-scene.json')==EXPECTED
 build=json.loads((SRC/'漫游/离线构建记录.json').read_text())
 views=json.loads((SRC/'图册/视角清单.json').read_text())
 assert build['scene_sha256']==EXPECTED
 assert views['scene_sha256']==EXPECTED
 assert len(views['views'])==21
 if DEST.exists():shutil.rmtree(DEST)
 DEST.mkdir()
 for name in ['开始查看.html','打开说明.txt','设计图册.pdf','项目总结与施工交接说明.md']:
  copy_file(SRC/name,name)
 (DEST/'项目总结与施工交接说明.txt').write_text(plain_summary())
 for folder in ['漫游','模型','图册','图纸','清单']:
  for p in sorted((SRC/folder).rglob('*')):
   if p.is_file() and p.suffix in {'.html','.txt','.json','.blend','.glb','.png','.dxf','.csv'}:copy_file(p,p.relative_to(SRC))
 for v in views['views']:v['file']=v['image']
 (DEST/'图册/视角清单.json').write_text(json.dumps(views,ensure_ascii=False,indent=2))
 build['scene']='../模型/方案数据.json'
 (DEST/'漫游/离线构建记录.json').write_text(json.dumps(build,ensure_ascii=False,indent=2))
 copy_file(ROOT/'blender/unit6-professional-scene.json','模型/方案数据.json')
 source_dwg=ROOT.parent/'02-10-20B#楼平立面图(1).dwg'
 assert sha(source_dwg)=='f8b152616a5b38dbc866076aca374d165bd5aefeea2e49652542c0df8c4b477b'
 copy_file(source_dwg,Path('原图依据')/source_dwg.name)
 for name in ['unit6-floors12.json','unit6-floor3.json','unit6-vertical-verified.json','unit6-landscape-source.json']:
  copy_file(ROOT/'blender'/name,Path('原图依据/提取数据')/name)
 for name in ['F1-unit6-grid.png','F2-unit6-grid.png','F3-unit6-grid.png','unit6-outdoor-source-check.png','室外范围核对.md','vertical/unit6-north-elevation-grid.png','vertical/竖向核对说明.md']:
  copy_file(ROOT/'audit/unit6'/name,Path('原图依据/核对图')/Path(name).name)
 for name in ['P02几何复核.md','P02几何数据.json','P02客厅家具检查.json','P02房间与花园通达检查.json','施工交接数据.json','方案点位与定制清单.json','sources.json','报告章节索引.json']:
  copy_file(SRC/name,Path('核对记录')/name)
 garden_check=SRC/'P02园林组检查.json'
 if garden_check.exists():copy_file(garden_check,'核对记录/P02园林组检查.json')
 for name in ['unit-six-offline-browser-results.json','professional-model-results.json','offline-package-pages-results.json']:
  copy_file(ROOT/'blender/qa'/name,Path('核对记录/离线与模型验证')/name)
 pages=len(PdfReader(DEST/'设计图册.pdf').pages)
 text=f'''第6户住宅与花园 · P02完整交付包
版本日期：2026-09-10

怎样打开
1. 将ZIP完整解压，保留全部子文件夹。
2. 双击“开始查看.html”，在浏览器中进入漫游、报告或多角度图册。
3. 漫游无需联网、无需服务器。拖动看四周；W/A/S/D或方向键步行；走进电梯后选择楼层。Esc暂停。
4. 如系统默认预览不能运行三维页面，请用Chrome、Edge或Safari打开HTML。手机需在允许本地HTML的浏览器中打开完整文件夹；优先用电脑查看。

交付内容
设计图册.pdf：{pages}页A3横版，含原图依据、三层定位平面、南院/露台、坡道剖面、21个模型视角、20处房间交底、点位门窗表、材料、专业接口、施工顺序、验收与暂停点。
项目总结与施工交接说明.txt/.md：完整可编辑文字总结。
漫游：可离线行走、进入中央电梯、换层的三维住宅；包括首层庭院与三层露台。
模型：可继续编辑的Blender文件、GLB通用模型和同版方案数据。
图册：21张独立PNG与浏览入口；按模型真实视角渲染。
图纸：3张毫米单位DXF方案定位底图，供现场复测和专业深化使用。
清单：62个方案点位、38处门窗状态、16组/类户外配置、材料询价表、12个暂停点及6种交接记录空表。
原图依据：原始DWG、三层及庭院/北立面的提取依据和核对图。
核对记录：几何、通达、模型与离线检查，公开要求来源和结构化交接资料。
文件校验清单.sha256：用于检查完整性。

本版设计
1F：父母日常、厨房餐厅与客厅、爸爸操盘区、南院四人休息与种植。
2F：儿子夫妻主卧、儿童预留与家庭阅读等。
3F：妹妹卧室、书法房、妈妈毛线工作室及开敞露台花园。
三层采用统一中央电梯；模型无楼梯。原图主要墙柱、平面洞口、采光井和各层退台采用第6户提取依据。新增内装、撤梯补板、电梯和庭院坡道单独列为方案。

使用边界与下一步
这套交付包用于家庭确认、现场复测、施工交底、分项报价及委托专业深化；不是签章施工图或审批许可。
原图图签指向杭州，具体地址与现状仍需确认。撤梯、开井、补板先核合法性；不得把结构报告当作住宅主体拆改的一般许可。若当地不允许，应改方案。
建筑结构、电梯土建、疏散救援、给排水电气、防水排水等需相关专业完成现场核查与可施工文件，按报告暂停点释放工序。
38处门窗中6处北窗有对应立面依据，其余32处竖向为展示或编号推定；禁止据此采购。屋顶完整形态尚未核实，不把模型屋面示意当作原图完整复原。
南院可讨论铺装范围47.504㎡，主南廊9.797㎡；保留下沉庭院上空。3F露台栏内原图参考18.684㎡，结构6.770已核，模型完成面6.870仅展示。种植、饱水荷载与室内外高差均需现场确认。
图纸与模型尺寸为方案定位数据；不得从透视截图量尺寸、直接采购、拆改或开孔。

版本核对
场景SHA256：{EXPECTED}
原始DWG SHA256：f8b152616a5b38dbc866076aca374d165bd5aefeea2e49652542c0df8c4b477b
模型、离线漫游及视角目录使用同一最终场景版本。交付包未包含历史试做版本。
'''
 (DEST/'交付目录与版本说明.txt').write_text(text)
 # The start page points to the full text summary, so create it in the working output too.
 (SRC/'项目总结与施工交接说明.txt').write_text(plain_summary())
 hashes={str(p.relative_to(DEST)):sha(p) for p in sorted(DEST.rglob('*')) if p.is_file()}
 (DEST/'文件校验清单.sha256').write_text(''.join(f'{v}  {k}\n' for k,v in hashes.items()))
 with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(DEST.rglob('*')):
   if p.is_file():z.write(p,Path(NAME)/p.relative_to(DEST))
 with zipfile.ZipFile(ZIP) as z:
  assert z.testzip() is None
  extract=ROOT/'tmp/package-check'
  if extract.exists():shutil.rmtree(extract)
  z.extractall(extract)
 check=extract/NAME
 for rel,digest in hashes.items():assert sha(check/rel)==digest,rel
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k in ['src','href'] and v and not v.startswith(('#','data:','blob:')):
     part=urlsplit(v)
     if not part.scheme and part.path:
      assert (self.origin/unquote(part.path)).is_file(),f'{self.origin} -> {v}'
 for p in check.rglob('*.html'):
  parser=Links();parser.origin=p.parent;parser.feed(p.read_text())
 result={'files':len(hashes)+1,'pdfPages':pages,'views':21,'zipBytes':ZIP.stat().st_size,'sceneSha256':EXPECTED,'zipCrcPassed':True,'extractedHashesPassed':True,'relativeHtmlLinksPassed':True,'zip':str(ZIP),'extracted':str(check)}
 (ROOT/'tmp/package-check-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':assemble()
