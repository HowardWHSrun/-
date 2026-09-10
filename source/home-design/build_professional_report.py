"""A3 design coordination book with vector plans, source evidence, views and trade handover."""
import csv,json,math,re,sys
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,Flowable,KeepTogether
from reportlab.lib.units import mm
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/unit6-professional';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tmp/geometry-libs'))
sys.path.insert(0,str(ROOT/'tmp/cad-recovery/python-libs'))
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
import ezdxf
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/Supplemental/Songti.ttc',subfontIndex=6))
pdfmetrics.registerFont(TTFont('CNB','/System/Library/Fonts/Supplemental/Songti.ttc',subfontIndex=1))
INK=colors.HexColor('#243D38');MUT=colors.HexColor('#64736C');RULE=colors.HexColor('#D8DED8')
PALE=colors.HexColor('#EEF2EC');OAK=colors.HexColor('#B5814C');BLUE=colors.HexColor('#498994');ROSE=colors.HexColor('#A45D51')
W,H=420*mm,297*mm;CW=W-32*mm
ST={
 'h1':ParagraphStyle('h1',fontName='CNB',fontSize=25,leading=31,textColor=INK,spaceAfter=9),
 'h2':ParagraphStyle('h2',fontName='CNB',fontSize=15,leading=21,textColor=INK,spaceAfter=8),
 'body':ParagraphStyle('body',fontName='CN',fontSize=11.3,leading=18,textColor=INK,wordWrap='CJK',spaceAfter=6),
 'small':ParagraphStyle('small',fontName='CN',fontSize=9.2,leading=14,textColor=MUT,wordWrap='CJK',spaceAfter=4),
 'cell':ParagraphStyle('cell',fontName='CN',fontSize=10.1,leading=15,textColor=INK,wordWrap='CJK'),
 'white':ParagraphStyle('white',fontName='CNB',fontSize=10.4,leading=15,textColor=colors.white,wordWrap='CJK'),
 'label':ParagraphStyle('label',fontName='CNB',fontSize=10.3,leading=16,textColor=OAK,spaceAfter=5)
}
D=json.loads((ROOT/'blender/unit6-professional-scene.json').read_text())
C=json.loads((OUT/'施工交接数据.json').read_text())
P=json.loads((OUT/'方案点位与定制清单.json').read_text())
LAND=json.loads((ROOT/'blender/unit6-landscape-source.json').read_text())
FLOORS=D['walkthrough']['floors']
SOURCE_FLOORS=json.loads((ROOT/'blender/unit6-floors12.json').read_text())['floors']+[json.loads((ROOT/'blender/unit6-floor3.json').read_text())]
ZONE={z['id']:z for z in LAND['zones']}
STORY=[];REGISTER=[]
VERIFIED=json.loads((ROOT/'blender/unit6-vertical-verified.json').read_text())['verified']

def opening_schedule():
 rows=[]
 for fi,f in enumerate(SOURCE_FLOORS):
  for i,o in enumerate(f['openings']):
   evidence=next((v for v in VERIFIED if v['floor']==fi+1 and (v['id']==o.get('id') or (v.get('planA')==o['a'] and v.get('planB')==o['b']))),None)
   code=o.get('code') or '';m=re.search(r'(\d{2})(\d{2})',code)
   door=o['type'] in ['door','entrance','glazed_door','passage'] or code.startswith('MLC')
   h=evidence['height'] if evidence else o.get('height') or (int(m.group(2))/10 if m else (2.1 if door else 1.6))
   sill=evidence['sill'] if evidence else o.get('sill')
   if sill is None:sill=0 if door else max(.25,2.6-h)
   h=min(h,f['ceilingElevation']-f['elevation']-.26-sill)
   rows.append({'id':f'O{fi+1}{i+1:02}','floor':fi+1,'sourceName':o.get('id',o.get('name')),'code':code or '未见编号',
    'a':o['a'],'b':o['b'],'widthMm':round(math.dist(o['a'],o['b'])*1000),'sillMm':round(sill*1000),'heightMm':round(h*1000),
    'verticalStatus':'北立面已核（框口包络）' if evidence else '展示/编号推定，待核',
    'evidence':evidence['id'] if evidence else '',
    'note':'宽度为原图墙皮洞口定位，非成窗采购净尺寸；高度仅在已核6项具有对应立面依据'})
 return rows
OPENINGS=opening_schedule()

def txt(s,style='body'):
 return Paragraph(escape(str(s)).replace('\n','<br/>'),ST[style])
def html(s,style='body'):return Paragraph(s,ST[style])
def heading(code,title,sub=''):
 if STORY:STORY.append(PageBreak())
 hp=txt(title,'h1');hp.bookmarkName=f'section-{len(REGISTER)+1}';hp.bookmarkTitle=code+' / '+title
 STORY.extend([txt(code,'label'),hp])
 if sub:STORY.append(txt(sub,'small'))
 STORY.append(Spacer(1,8))
 REGISTER.append((code,title))
def table(headers,rows,widths,small=False):
 cells=[[txt(x,'white') for x in headers]]+[[txt(x,'small' if small else 'cell') for x in row] for row in rows]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),
  ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
  ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,0),(-1,0),.5,INK),('LINEBELOW',(0,1),(-1,-1),.3,RULE)]))
 return t
def im(path,w,h):
 iw,ih=PILImage.open(path).size;s=min(w/iw,h/ih)
 return Image(str(path),width=iw*s,height=ih*s,hAlign='CENTER')
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(RULE);canvas.line(16*mm,16*mm,W-16*mm,16*mm)
 canvas.setFillColor(MUT);canvas.setFont('CN',8.5)
 canvas.drawString(16*mm,11.4*mm,'E4 / 第6户住宅与花园   ·   P02 / 2026.09.10   ·   方案交底、复测、报价及专业深化用')
 canvas.drawRightString(W-16*mm,11.4*mm,f'{doc.page:02d}')
 canvas.setFont('CN',8);canvas.drawRightString(W-16*mm,H-10.7*mm,'原图依据与新增方案分开表达 / 未签章施工图')
 canvas.restoreState()

class Book(SimpleDocTemplate):
 def afterFlowable(self,flowable):
  if hasattr(flowable,'bookmarkName'):
   self.canv.bookmarkPage(flowable.bookmarkName)
   self.canv.addOutlineEntry(flowable.bookmarkTitle,flowable.bookmarkName,level=0,closed=False)

def object_poly(o):
 x,y,_=o['position'];w,d,_=o['size'];a=o.get('rotation',[0,0,0])[2]
 return [[x+u*math.cos(a)-v*math.sin(a),y+u*math.sin(a)+v*math.cos(a)] for u,v in [(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]]

class Plan(Flowable):
 def __init__(self,floor,width=580,height=594,mode='furniture',garden=False):
  Flowable.__init__(self);self.f=floor;self.width=width;self.height=height;self.mode=mode;self.garden=garden
 def draw(self):
  c=self.canv;f=FLOORS[self.f];poly=f['boundary']
  c.saveState();clip=c.beginPath();clip.rect(0,0,self.width,self.height);c.clipPath(clip,stroke=0,fill=0)
  if self.garden:
   bounds=(0,-4.4,10.0,4.5) if self.f==0 else (3.35,3.15,8.5,8.9)
  else:
   xs=[p[0] for p in poly];ys=[p[1] for p in poly];bounds=(min(xs)-.9,min(ys)-.9,max(xs)+1.0,max(ys)+.9)
  x0,y0,x1,y1=bounds
  # Standard plotted scale except enlarged garden details; explicit scale bar handles PDF zoom.
  scale=min((self.width-30)/(x1-x0),(self.height-24)/(y1-y0))
  ox=(self.width-(x1-x0)*scale)/2;oy=(self.height-(y1-y0)*scale)/2
  xy=lambda x,y:(ox+(x-x0)*scale,oy+(y-y0)*scale)
  def line(a,b,col=INK,w=.6,dash=None):
   c.saveState();c.setStrokeColor(col);c.setLineWidth(w)
   if dash:c.setDash(dash)
   c.line(*xy(*a),*xy(*b));c.restoreState()
  def pg(p,fill=None,stroke=INK,lw=.6):
   q=c.beginPath();q.moveTo(*xy(*p[0]))
   for z in p[1:]:q.lineTo(*xy(*z))
   q.close();c.setLineWidth(lw)
   if fill:c.setFillColor(fill)
   if stroke:c.setStrokeColor(stroke)
   c.drawPath(q,fill=bool(fill),stroke=bool(stroke))
  def label(s,x,y,size=8,col=INK):
   c.setFillColor(col);c.setFont('CN',size);c.drawCentredString(*xy(x,y),s)
  pg(poly,colors.HexColor('#FAFAF6'),RULE)
  for hole in f.get('holes',[]):
   pg(hole,colors.HexColor('#DEE9ED'),BLUE,.7)
   for a,b in [(hole[0],hole[2]),(hole[1],hole[3])]:line(a,b,BLUE,.6)
  if self.f==0:
   for key in ['south_courtyard','south_main_porch']:
    pg(ZONE[key]['polygon'],colors.HexColor('#E6EADB') if key=='south_courtyard' else PALE,RULE)
   r=D['landscape']['rampPolygon'];pg(r,colors.HexColor('#E8D7BF'),OAK,.6)
   line((6.6,-1.7),(6.6,1.9),OAK,1.1);label('坡道 1:12 意向',6.6,-2.38,7.5,OAK)
   line((6.6,1.9),(6.49,1.68),OAK,1);line((6.6,1.9),(6.71,1.68),OAK,1)
   label('-0.400',2.0,-3.45,8,MUT);label('-0.050',8.7,3.3,8,MUT)
   if self.garden:
    line((.14,-4.03),(9.46,-4.03),BLUE,.8,[3,2]);label('下沉庭院上空 / 保持留空',4.8,-4.31,8,BLUE)
  src=SOURCE_FLOORS[self.f]
  for wall in src['boxes']:
   x,y,xx,yy=wall['bounds'];pg([[x,y],[xx,y],[xx,yy],[x,yy]],INK,INK,.25)
  for o in src['openings']:
   a,b=o['a'],o['b'];th=o.get('thickness',.24)
   c.saveState();c.setStrokeColor(colors.white);c.setLineWidth(max(2,th*scale-.5));c.line(*xy(*a),*xy(*b));c.restoreState()
   line(a,b,BLUE,1.0)
  for o in D['objects']:
   if o.get('floor')!=self.f:continue
   n=o.get('name','');cat=o.get('category','')
   if cat=='wall-low' and ('新增' in o.get('geometryStatus','') or '电梯' in n):pg(object_poly(o),colors.HexColor('#E5C69E'),OAK,.6)
   if self.mode!='furniture':continue
   if cat!='furniture' or o['kind']=='text':continue
   w,d,h=o['size'];z=o['position'][2]
   if min(w,d)<.10 or z-h/2>1.2 or z+h/2<-.20:continue
   if o['kind'] in ['cylinder','sphere']:
    c.setStrokeColor(OAK);c.setFillColor(colors.HexColor('#EBE0D0'));x,y=xy(*o['position'][:2]);c.ellipse(x-w*scale/2,y-d*scale/2,x+w*scale/2,y+d*scale/2,fill=1,stroke=1)
   elif o['kind']=='box':pg(object_poly(o),colors.HexColor('#EBE0D0'),OAK,.3)
  if self.mode=='points':
   placed=[]
   for p in P['points']:
    if p['floor']!=self.f:continue
    x,y,z=p['position'];sx,sy=xy(x,y);col={'light':OAK,'power':ROSE,'data':MUT,'water':BLUE,'drain':BLUE,'switch':MUT}[p['kind']]
    c.setStrokeColor(col);c.setFillColor(colors.white);c.circle(sx,sy,2.6,fill=1,stroke=1)
    for dx,dy in [(7,4),(7,-9),(-35,4),(-35,-9),(8,15),(-35,15),(8,-20)]:
     rr=(sx+dx,sy+dy,38,10)
     if all(rr[0]+rr[2]<r[0] or r[0]+r[2]<rr[0] or rr[1]+rr[3]<r[1] or r[1]+r[3]<rr[1] for r in placed):break
    placed.append(rr);c.setFont('CN',7.8);c.setFillColor(col);c.drawString(rr[0],rr[1],p['id']);c.line(sx,sy,rr[0],rr[1]+3)
  elif not self.garden:
   for i,r in enumerate(f['rooms']):
    q=Polygon(r['polygon']);p=q.representative_point();label(f'{self.f+1}F-{i+1:02}',p.x,p.y,8,INK)
  else:
   for item in P['gardenItems']:
    if item.get('floor')!=self.f or not item.get('center'):continue
    x,y=item['center']
    if item['id']=='G3-B01':
     w,d,_=item['size'];pg([[x-w/2,y-d/2],[x+w/2,y-d/2],[x+w/2,y+d/2],[x-w/2,y+d/2]],colors.HexColor('#EBE0D0'),OAK,.5)
    label(item['id'],x,y+.34 if item['id']=='G3-P04' else y-.37,7.5,INK)
  # Dimensions refer to original wall coordinates / surveyed designable envelope, not title boundaries.
  def dimx(a,b,y):
   line((a,y),(b,y),MUT,.4)
   for x in [a,b]:line((x-.06,y-.07),(x+.06,y+.07),MUT,.5)
   label(str(round((b-a)*1000)),(a+b)/2,y+.10,7.8,MUT)
  if self.garden and self.f==0:dimx(.14,9.46,-4.0)
  elif not self.garden:
   xs=[p[0] for p in SOURCE_FLOORS[self.f]['boundary']];dimx(min(xs),max(xs),max(p[1] for p in poly)+.44)
  # North and a metric scale bar remain legible in printed and zoomed versions.
  nx,ny=self.width-35,self.height-45;c.setStrokeColor(INK);c.line(nx,ny-20,nx,ny+5);c.line(nx,ny+5,nx-3,ny-1);c.line(nx,ny+5,nx+3,ny-1)
  c.setFont('CNB',9);c.setFillColor(INK);c.drawCentredString(nx,ny+12,'N*')
  c.setFont('CN',7);c.drawString(10,6,'* 图面方向，现场正北待复核')
  bx,by=self.width-125,11;c.setLineWidth(2);c.line(bx,by,bx+scale*2,by)
  c.setFont('CN',8);c.drawString(bx,by+7,'0                 2 m')
  c.restoreState()

class RampSection(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=CW;self.height=247
 def draw(self):
  c=self.canv;ox=72;oy=90;s=135
  pts=[(0,0),(4.2,.35),(4.2,.39),(0,.04)]
  p=c.beginPath();p.moveTo(ox,oy)
  for x,z in pts[1:]:p.lineTo(ox+x*s,oy+z*s)
  p.close();c.setFillColor(colors.HexColor('#E8D7BF'));c.setStrokeColor(OAK);c.drawPath(p,fill=1,stroke=1)
  c.setLineWidth(1);c.setStrokeColor(INK);c.line(ox-55,oy,ox,oy);c.line(ox+4.2*s,oy+.35*s,ox+4.2*s+105,oy+.35*s)
  c.setFont('CN',10);c.setFillColor(INK)
  c.drawString(ox-46,oy-19,'南院 -0.400');c.drawString(ox+4.2*s+13,oy+.35*s+12,'南廊 -0.050')
  c.drawString(ox+190,oy+95,'新增坡道意向：水平投影4200 / 高差350 / 1:12')
  c.setStrokeColor(MUT);c.line(ox,oy-34,ox+4.2*s,oy-34)
  c.drawCentredString(ox+2.1*s,oy-50,'4200 mm（放样参考，现场完成面确认后调整）')
  c.setFont('CN',9);c.drawString(72,15,'板外宽1400 mm；扶手间模型净距约1277 mm。端部平台、临空防护、承托、防滑和排水防水收口待专业深化。')

def export_tables_and_cad():
 dest=OUT/'清单';dest.mkdir(exist_ok=True)
 def csvfile(name,header,rows):
  name=re.sub(r'[\\/:*?"<>|]','_',name)
  with (dest/name).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.writer(f);w.writerow(header);w.writerows(rows)
 csvfile('方案点位表.csv',['编号','层','类型','房间','X米','Y米','相对本层Z米','说明','状态','备注'],
  [[p['id'],p['floor']+1,p['kind'],p['room'],*p['position'],p['label'],p['status'],p['note']] for p in P['points']])
 csvfile('园林与户外家具清单.csv',['编号','层','名称','方案数量','尺寸米','位置米','说明'],
  [[p['id'],p['floor']+1,p['name'],p['quantity'],str(p.get('size','待选型')),str(p.get('center','见平面')),p['note']] for p in P['gardenItems']])
 csvfile('门窗定位与竖向状态.csv',['编号','楼层','源洞口','源编号','A点X米','A点Y米','B点X米','B点Y米','平面洞宽mm','模型下口mm','模型洞高mm','竖向状态','核对ID','说明'],
  [[o['id'],o['floor'],o['sourceName'],o['code'],*o['a'],*o['b'],o['widthMm'],o['sillMm'],o['heightMm'],o['verticalStatus'],o['evidence'],o['note']] for o in OPENINGS])
 csvfile('材料询价清单.csv',['编号','材料','使用范围','意向','报价边界','验收','供应商','单价','复测工程量'],
  [[p['id'],p['name'],p['use'],p['intent'],p['quotationBasis'],p['acceptance'],'','',''] for p in C['materials']])
 csvfile('待复核及暂停工序.csv',['编号','事项','原因','责任专业','解除条件','回复','日期'],
  [[p['id'],p['item'],p['whyHold'],p['owner'],p['releaseEvidence'],'',''] for p in C['holdPoints']])
 for form in C.get('handoverForms',[]):csvfile(form['id']+'_'+form['name']+'.csv',form['fields'],[['']*len(form['fields']) for _ in range(8)])
 cad=OUT/'图纸';cad.mkdir(exist_ok=True)
 for f in range(3):
  doc=ezdxf.new('R2010');doc.units=4;doc.header['$INSUNITS']=4
  for name,col in [('SOURCE_WALL',7),('SOURCE_OPENING',4),('NEW_INTERIOR',30),('FURNITURE',32),('LANDSCAPE',3),('SERVICE_INTENT',6),('NOTE',8)]:doc.layers.new(name,dxfattribs={'color':col})
  ms=doc.modelspace()
  def pl(p,layer,closed=True):ms.add_lwpolyline([(x*1000,y*1000) for x,y in p],close=closed,dxfattribs={'layer':layer})
  for w in SOURCE_FLOORS[f]['boxes']:
   a,b,c,d=w['bounds'];pl([[a,b],[c,b],[c,d],[a,d]],'SOURCE_WALL')
  for op in SOURCE_FLOORS[f]['openings']:pl([op['a'],op['b']],'SOURCE_OPENING',False)
  for o in D['objects']:
   if o.get('floor')!=f or o['kind']!='box':continue
   if o.get('category')=='wall-low' and ('新增' in o.get('geometryStatus','') or '电梯' in o['name']):pl(object_poly(o),'NEW_INTERIOR')
   elif o.get('category')=='furniture' and min(o['size'][:2])>.1 and o['position'][2]<1.3:pl(object_poly(o),'FURNITURE')
  for p in P['points']:
   if p['floor']!=f:continue
   x,y,z=p['position'];ms.add_circle((x*1000,y*1000),50,dxfattribs={'layer':'SERVICE_INTENT'})
   ms.add_text(p['id'],dxfattribs={'height':110,'insert':(x*1000+80,y*1000+40),'layer':'SERVICE_INTENT'})
  if f==0:
   for p in [D['landscape']['groundGardenPolygon'],D['landscape']['porchPolygon'],D['landscape']['rampPolygon']]:pl(p,'LANDSCAPE')
  if f==2:pl(ZONE['third_floor_terrace']['polygon'],'LANDSCAPE')
  ms.add_text(f'E4 P02 FLOOR {f+1} / mm / DESIGN COORDINATION - NOT FOR CONSTRUCTION',dxfattribs={'height':160,'insert':(-1000,17000),'layer':'NOTE'})
  ms.add_text('Original wall positions; opening centre lines do not remove source wall segments. Check source DWG before editing.',dxfattribs={'height':110,'insert':(-1000,16680),'layer':'NOTE'})
  doc.saveas(cad/f'P02_{f+1}F_方案定位.dxf')

def room_cards(items):
 cells=[]
 for r in items:
  col=[txt(r['id']+' / '+r['name'],'h2')]
  for label,key in [('原有条件','existingBasis'),('空间安排','layout'),('材料与细节','finishes'),('照明与点位','lightingPowerData'),('水与设备','waterHVAC'),('现场验收','acceptance'),('复核 / 暂停','hold')]:
   col.append(html('<b>'+label+'</b>　'+escape(r.get(key,'')),'cell'));col.append(Spacer(1,5))
  cells.append(col)
 while len(cells)<4:cells.append([Spacer(1,1)])
 t=Table([[cells[0],cells[1]],[cells[2],cells[3]]],colWidths=[CW/2,CW/2])
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),16),('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),14),('LINEBELOW',(0,0),(-1,0),.5,RULE)]))
 return t

def build():
 heading('P02 / DESIGN COORDINATION','一家人的住宅与花园','第6户 / E4端户 · 原图图签：杭州富春玫瑰园华墅地块二期二区 · 2026年9月10日')
 imgs=OUT/'图册/images'
 hero=next(iter(sorted(imgs.glob('*exterior*'))),None)
 if hero is None:hero=next(iter(sorted(imgs.glob('*.png'))),ROOT/'output/unit6/01_1F_剖开.png')
 STORY.append(im(hero,CW,465))
 STORY.append(Spacer(1,12))
 STORY.append(txt('三层生活空间 + 首层南院 + 露台花园 + 可离线步行与乘梯的模型','h2'))
 STORY.append(txt('本版供家人确认、现场复测、施工交底、分项报价与专业深化。尚未取得建筑/结构/机电签章及适用审批，不作为撤梯、开井、补板或改排水的开工依据。','body'))
 heading('00 / 阅读顺序','先看空间，再核条件，最后交接','解压后双击“开始查看.html”；离线漫游无需安装额外运行环境。PDF与模型分别保存在包内。')
 STORY.append(table(['阅读部分','解决的问题','对应资料'],[
  ['项目与依据','核对成员需求、原图范围、高差、修改与保留边界','本册前部 / 原图依据目录'],
  ['平面与花园','查看三层布置、院内活动、通路与室外留空区域','A101-A103、L101-L103'],
  ['多角度视图','通过真实模型查看家具尺度、采光开口与室内外联系','V系列视图 / 图册文件夹'],
  ['点位与材料','把灯具、插座、水电接口、定制柜和花箱拆分讨论','E系列 / 清单CSV'],
  ['施工交接','明确复测、责任专业、工序、验收与不能先做的事项','T系列 / 项目总结与施工交接说明'],
  ['原始文件','由接手设计及施工团队追溯来源，检查现状差异','原DWG、模型、方案DXF、来源记录']],[190,415,CW-605]))
 STORY.append(Spacer(1,22))
 STORY.append(txt('状态用语','h2'))
 STORY.append(table(['状态','含义'],[[s['label'],s['meaning']] for s in C['statusLegend']],[180,CW-180]))
 heading('01 / 家庭与设计','各自专注，也有一起生活的地方')
 STORY.append(table(['楼层','家庭安排','细化重点'],[
  ['1F / 0.000','父母卧室、卫浴、爸爸操盘房、客餐厅、厨房、公卫','缩短日常路径；操盘防眩与网络；中厨油烟分隔；连接南院休息区'],
  ['2F / 3.700','夫妻主卧、衣帽区与主卫、儿童预留房、家政阅读区','未来家庭独立；卧室隐私、洗烘、夜间照明与成长型收纳'],
  ['3F / 6.900','妹妹卧室卫浴、书法区、妈妈毛线花艺工作室、露台花园','书法平放收纳；毛线防尘干燥；室内花艺和露天花箱分工'],
  ['室外 / 原图范围','南院47.50㎡、客厅南廊9.80㎡、三层露台18.68㎡','参考可用投影面积，不是产权、建筑面积或结算工程量']],[140,410,CW-550]))
 STORY.append(Spacer(1,18))
 for ch in C['chapters'][:1]:
  for p in ch['paragraphs']:STORY.append(txt(p))
 heading('02 / 原图与差异','可以核实的范围，和仍需现场确认的内容')
 evidence=ROOT/'audit/unit6/unit6-outdoor-source-check.png'
 STORY.append(im(evidence,CW,475))
 STORY.append(txt('主墙、洞口、采光井和各层轮廓来自原图；原室内主要标高为0.000/3.700/6.900。38处平面洞口中六处北窗竖向已限定核对，其余32处含编号推定或展示值。屋面简化表达，不能从外观截图反推原屋面做法。','small'))
 STORY.append(txt('本轮更正：露台6.770为已核实结构标高；模型6.870完成面仍是假设。南院-0.400与南廊-0.050有源标注。南、东下沉庭院上空不铺板，外围地界未据此推定。','small'))
 heading('03 / 高差控制','完成面、结构面和展示值分开记录','数值单位米。结构与完成标注之间的差值，不能直接当作新构造厚度或填土量。')
 levelrows=[]
 for p in C.get('levelControls',[]):
  values=[]
  for key,label in [('drawingM','源标注'),('structuralM','结构'),('modelFinishM','展示完成')]:
   if p.get(key) is not None:values.append(f'{label} {p[key]:+.3f}')
  levelrows.append([p['place'],' / '.join(values) or '保持孔洞',p['kind'],p['constructionMeaning']])
 STORY.append(table(['位置','数值 / m','证据状态','施工交接含义'],levelrows,[175,270,200,CW-645]))
 STORY.append(Spacer(1,24));STORY.append(txt('原南廊与南院高差350mm已在坡道意向中表达；门口50mm高差仍保留。漫游能跨越小高差，不是无障碍验收证明。现状每个门口、排水口和临空边缘都应纳入复测图。'))
 for f in range(3):
  heading(f'A10{f+1} / 方案平面',f'{f+1}F · '+['父母生活与南院联系','未来小家庭的独立生活层','兴趣工作与露台花园'][f],'矢量平面按模型坐标绘制；数字尺寸为原图/方案参考，施工放样前须完成实测与尺寸链复核。')
  rooms=FLOORS[f]['rooms'];rows=[]
  for i,r in enumerate(rooms):
   area=Polygon(r['polygon']).area
   rows.append([f'{f+1}F-{i+1:02}',r['name'],f'{area:.2f}'])
  side=[txt('功能定位索引','h2'),table(['索引','功能','投影㎡'],rows,[65,200,65],True),Spacer(1,12),txt('上表是功能定位多边形参考，部分区域含通道；不等于净使用或结算面积。','small'),
   txt('黑色：原图主要墙柱\n蓝色：原图门窗位置、保留孔洞\n赭色：新增内装、电梯和家具\n绿色：原图允许讨论的花园范围','small'),
   txt('中央电梯外占位1650×1900；内示意1410×1660；东开门950。单位毫米。须取得选定厂家的土建条件图后复核，不能直接下单。','small')]
  STORY.append(Table([[Plan(f,650,577),side]],colWidths=[680,CW-680],style=[('VALIGN',(0,0),(-1,-1),'TOP')]))
 heading('L101 / 南庭院深化','一处可以围坐、养花，也能顺畅通行的南院','完成面-0.400；主南廊-0.050。原庭院结构面-1.600不能被直接解释成可挖土或1.20米填土做法。')
 side=[txt('布局与使用','h2'),txt('西侧安排四人围坐区；西南与东侧设置可移动花箱。客厅南门经原南廊，沿中央偏东的模块坡道下到庭院。底部平台及其通路保持清空。'),
  txt('材料意向','h2'),txt('浅灰防滑铺装、暖木色可逆坡道、细金属扶手、陶土色花箱。先确认既有结构、防水和基层，再确定能否覆盖或替换；不指定未经核实的挖填与承托做法。'),
  txt('种植与维护','h2'),txt('常绿骨架、观叶地被和轮换花卉分层。茶梅、麦冬/玉簪等是方案候选，按实际日照、根域和荷载筛选；花箱组数不是苗木采购数量。种植养护流程参考S10，不代表规范指定品种。'),
  txt('必须保留','h2'),txt('南缘临空防护、东侧采光、排水检修及南端下沉庭院上空。外围地界未核实，未向北或向邻户扩园。')]
 STORY.append(Table([[Plan(0,675,552,garden=True),side]],colWidths=[695,CW-695],style=[('VALIGN',(0,0),(-1,-1),'TOP')]))
 heading('L102 / 坡道与排水交接','高差需要可验证的节点，不靠模型把地坪抬平')
 STORY.append(RampSection())
 STORY.append(table(['节点','本版表达','深化与验收要求'],[
  ['客厅门口','室内0.000 → 南廊-0.050，模型保留50mm高差','真实门槛、防雨与排水沟位置尚未核实；无障碍过渡由建筑防水专业协调。'],
  ['南廊 → 庭院','新坡道投影4200×1400；下降350，几何坡度1:12','净宽、端部平台、扶手、边挡、临空防护与承托节点须完整深化；不得凭本剖面加工。'],
  ['花箱与防水','移动模块；不在防水层中直接植筋或固定','核算饱水重量与集中荷载，检查排水孔/托盘，安排检修和移位路径。'],
  ['雨水与灌溉','图中只标接口和复测控制点','原雨水口、溢流与接入系统未确认；先做复测与排水能力校核，禁止向下沉井或邻地随意排水。']],[145,400,CW-545]))
 heading('L103 / 露台花园','室内干工作，室外养花与换盆','栏墙内原图参考18.68㎡。模型地坪6.870为展示假设，已核实结构标高为6.770。')
 items=[p for p in P['gardenItems'] if p['floor']==2]
 side=[txt('花艺与毛线的分工','h2'),txt('三层室内保留毛线工作、干燥防尘柜及窗边花艺；原露台保持开敞。花箱、休息坐凳与换盆台位于通道两侧，原露台门前保持通路。'),
  table(['编号','配置'],[[p['id'],p['name']] for p in items],[100,245],True),Spacer(1,12),
  txt('不配置重土池、鱼池、大树或固定封闭阳光房。栏墙完成高度、儿童攀爬条件、风荷载、楼板承载及防水节点必须现场与专业复核。','small')]
 STORY.append(Table([[Plan(2,655,556,garden=True),side]],colWidths=[675,CW-675],style=[('VALIGN',(0,0),(-1,-1),'TOP')]))
 # Views are actual final-model renders; contact sheet/index generated by the offline exporter.
 manifest=OUT/'图册/视角清单.json'
 views=json.loads(manifest.read_text()) if manifest.exists() else []
 if isinstance(views,dict):views=views.get('views',views.get('cameras',[]))
 if not views:
  views=[{'title':p.stem,'file':'images/'+p.name} for p in sorted(imgs.glob('*.png'))]
 for i in range(0,len(views),2):
  heading(f'V{i//2+1:02} / 实体模型视图','从人的视线看空间' if i else '从整体看三层与花园','所有图片来自本版Blender模型。家具与园林为方案；示意屋面和待核竖向尺寸不构成外立面施工依据。')
  row=[]
  for v in views[i:i+2]:
   view_file=v.get('file') or v.get('image') or v.get('path')
   if not view_file:raise ValueError(f'No image path for camera {v}')
   path=OUT/'图册'/view_file
   if not path.is_file():path=imgs/Path(view_file).name
   row.append([txt(v.get('title',path.stem),'h2'),im(path,(CW-24)/2,475),Spacer(1,8),txt(v.get('description',v.get('note','以图中家具帮助判断尺度；定制下单以复测深化尺寸为准。')),'small')])
  if len(row)==1:row.append([Spacer(1,1)])
  STORY.append(Table([row],colWidths=[CW/2,CW/2],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('RIGHTPADDING',(0,0),(-1,-1),12)]))
 for i in range(0,len(C['rooms']),4):
  heading(f'R{i//4+1:02} / 房间交底','把每个房间交代清楚','材料、照明、设备与验收一并表达；这些是设计意图，成品尺寸在现场复尺后锁定。')
  STORY.append(room_cards(C['rooms'][i:i+4]))
 for f in range(3):
  heading(f'E10{f+1} / 点位意向',f'{f+1}F · 照明与水电接口定位','标点不等于布线/给排水施工图；回路、负荷、线径、保护、坡向、管径、穿孔和接入位置由对应专业深化。')
  local=[p for p in P['points'] if p['floor']==f]
  kindnames={'light':'基础及辅助照明','power':'插座','data':'网络','switch':'开关','water':'给水接口','drain':'排水复测控制点'}
  rows=[[k.upper(),name,str(sum(p['kind']==k for p in local))] for k,name in kindnames.items() if any(p['kind']==k for p in local)]
  side=[txt('点位表达与范围','h2'),table(['类别','用途','数量'],rows,[72,215,55],True),Spacer(1,14),
   txt('L 灯具 / P 插座 / N 网络 / S 开关 / W 给水 / D 排水。逐点坐标表在本册下一组页面及清单CSV，单位米。','small'),
   txt('每个点的Z是相对所在楼层主基准的方案安装位置；花园地坪低于首层，不能把所有点一律从院地面起算。','small'),
   txt('给排水标点表示协调或复测对象，不表示已确认的原地漏、管线路由、管径和穿板位置。设备选型后再锁定接口。','small'),
   txt('照明是分层使用意向；照度、色温、眩光、回路保护及控制方式由样板与专业设计共同确定。','small')]
  STORY.append(Table([[Plan(f,660,586,mode='points'),side]],colWidths=[682,CW-682],style=[('VALIGN',(0,0),(-1,-1),'TOP')]))
 for start in range(0,len(P['points']),22):
  heading(f'E20{start//22+1} / 点位坐标表','按编号交接，避免位置各说各话','单位米；X/Y使用各层原图局部坐标，Z相对本层主基准。均为新增方案意向，供复测和专业协调。')
  rows=[[p['id'],str(p['floor']+1)+'F',p['room'],f'{p["position"][0]:.3f}',f'{p["position"][1]:.3f}',f'{p["position"][2]:.3f}',p['label']] for p in P['points'][start:start+22]]
  t=table(['编号','层','区域','X','Y','Z','用途'],rows,[70,45,180,85,85,85,CW-550],True)
  t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));STORY.append(t)
  STORY.append(Spacer(1,10));STORY.append(txt('完整注意事项逐点保存在“方案点位表.csv”。排水点不能据此直接开孔；插座点也不是供电回路或电气安全审查结论。','small'))
 for start in range(0,len(OPENINGS),19):
  heading(f'W10{start//19+1} / 门窗定位','每一个洞口，都保留来源和待核状态','38处平面洞口；仅6处北窗竖向有对应立面证据。尺寸单位毫米，非成窗/门扇下单尺寸。')
  rows=[[o['id'],str(o['floor'])+'F',o['code'],o['widthMm'],o['sillMm'],o['heightMm'],o['verticalStatus']] for o in OPENINGS[start:start+19]]
  t=table(['索引','层','原编号','平面洞宽','模型下口','模型洞高','竖向状态'],rows,[75,45,200,110,110,110,CW-650],True)
  t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));STORY.append(t)
  STORY.append(Spacer(1,12));STORY.append(txt('旧展示参数表曾列26项，另6处直接采用编号名义高度的门/门窗组合也未经逐洞立面确认；本表统一列为32处待核。完整A/B坐标、源名称和核对ID见CSV。','small'))
 for start in range(0,len(C['materials']),8):
  heading(f'M{start//8+1:02} / 材料与报价','材料要能说明范围，也要能验收','先做样板再锁定颜色、触感、收口和环境性能；品牌、供货及单价由本地报价核实。')
  rows=[[m['id']+' '+m['name'],m['use'],m['intent'],m['quotationBasis'],m['acceptance']] for m in C['materials'][start:start+8]]
  STORY.append(table(['编号 / 材料','使用范围','设计意向','报价范围','验收关注'],rows,[140,116,240,255,CW-751]))
 heading('M03 / 定制与成品','定制柜、桌案与园林模块','尺寸是方案意向，单位米；不从透视图量尺寸。全部下单需复尺和厂家加工图。')
 rows=[]
 for c in C['customFurniture']:
  dims=c.get('proposalM') or {}
  keys={'width':'宽','depth':'深','height':'高','top':'台面高','length':'长'}
  rows.append([c['id'],c['name'],' / '.join(f'{keys.get(k,k)}: {v}' for k,v in dims.items()) or '待现场复尺与厂家深化',c['note']])
 STORY.append(table(['编号','对象','方案尺寸 / m','下单前要求'],rows,[62,150,255,CW-467]))
 STORY.append(Spacer(1,15));STORY.append(txt(f'户外另有{len(P["gardenItems"])}组/类花箱与家具配置（含4把休闲椅）。各组尺寸、数量和位置见“园林与户外家具清单.csv”；模型的可移动意向不代替结构荷载及抗风确认。','small'))
 for i,ch in enumerate(C['chapters'][1:]):
  heading(f'T0{i+1} / 技术交接',ch['title'],'以下工艺用于组织专业深化和施工交底；遇到暂停点先完成书面条件。')
  for p in ch['paragraphs']:STORY.append(txt(p))
  if ch.get('evidenceRefs'):STORY.append(txt('参考来源：'+', '.join(ch['evidenceRefs'])+'；来源与适用说明见册末。','small'))
 heading('T10 / 专业接口','让各工种先把交接条件说清楚')
 for start in range(0,len(C['interfaces']),5):
  if start:heading('T10 / 专业接口（续）','设备、建筑与园林要共用同一版定位图')
  rows=[[p['id']+' '+p['trade'],p['lead'],p['inputs'],p['requiredOutputs'],p['coordinationCheck']] for p in C['interfaces'][start:start+5]]
  STORY.append(table(['专业','牵头责任','输入资料','应交付成果','交叉复核'],rows,[133,150,220,245,CW-748]))
 heading('T11 / 施工顺序','按条件释放工序，避免返工与掩盖问题')
 STORY.append(table(['阶段','工作内容','交付记录','进入下一步的条件'],[[p['id']+' '+p['name'],p['work'],p['deliverable'],p['release']] for p in C['phases']],[170,355,270,CW-795]))
 for start in range(0,len(C['acceptance']),7):
  heading(f'T12-{start//7+1} / 验收记录','隐蔽前留证据，交付时可复查')
  STORY.append(table(['检查项','检查方式','记录内容','参与专业'],[[p['id']+' '+p['item'],p['method'],p['record'],p['responsible']] for p in C['acceptance'][start:start+7]],[170,380,370,CW-920]))
 for start in range(0,len(C['holdPoints']),6):
  heading(f'T13-{start//6+1} / 暂停点','先核合法性，再按范围释放工序','普通家用电梯不能自动成为原疏散楼梯的替代；遇法定禁止情形必须调整方案，并非取得一份图纸就可放行。')
  STORY.append(table(['事项','暂停原因','责任专业','解除暂停所需证据'],[[p['id']+' '+p['item'],p['whyHold'],p['owner'],p['releaseEvidence']] for p in C['holdPoints'][start:start+6]],[180,365,185,CW-730]))
 heading('Q01 / 计量与分项报价','用可复核的计算底稿讨论价格','本版不编造当地单价、总预算或工期。原图面积、模型投影和可用功能面积不能相互替代。')
 def quantity_value(q):
  if isinstance(q['value'],dict):return f'已核北窗 {q["value"].get("verifiedNorth",0)}；展示参数 {q["value"].get("displayParameters",0)} 项'
  return str(q['value'])+' '+q['unit']
 STORY.append(table(['参考量','数值','使用边界'],[[q['name'],quantity_value(q),q.get('exclusions','')] for q in C['quantities']],[250,175,CW-425]))
 STORY.append(Spacer(1,12));STORY.append(txt('新增室外范围：南院47.504㎡、南廊9.797㎡、三层露台18.684㎡。坡道覆盖庭院和原踏步部分，不重复汇总采购；按实际铺装范围计量，仅扣不铺装部位。可移动花箱下若连续铺面仍应计入，不能机械扣除。','small'))
 heading('Q02 / 工程量方法','先讲清扣除和损耗，再谈总价')
 STORY.append(table(['项目','计量算法','不确定性'],[[q['item'],q['formula'],q['uncertainty']] for q in C['quantityMethods']],[160,590,CW-750]))
 heading('D01 / 后续图纸目录','施工图深化应补齐哪些文件','包内DXF是方案定位底图：保留来源墙线、标示洞口中心及新增意向。不是结构、水电或防水施工详图。')
 STORY.append(table(['编号','所需图纸','责任专业','状态'],[[p['id'],p['name'],p['requiredBy'],p['status']] for p in C['drawingRegister']],[62,560,240,CW-862]))
 heading('F01 / 现场闭环','复测、变更、验收和移交都留一份记录')
 STORY.append(table(['记录表','建议字段'],[[p['id']+' '+p['name'],' / '.join(p['fields'])] for p in C['handoverForms']],[220,CW-220]))
 STORY.append(Spacer(1,20));STORY.append(txt('这些记录表已附可填写CSV。每次变更注明原图/模型版本、位置、原因、影响工种、审核人和日期；隐蔽前拍照留比例尺。交付时保留竣工定位、设备说明、保修联系、材料批次和养护计划。'))
 heading('F02 / 项目总结','这次已经做到什么，下一步如何交给团队')
 for p in ['已以原DWG最右第6户建立三层模型；落实全家卧室与兴趣空间，厨房卫浴、收纳、照明接口与可移动园林均同步表达。',
  '新增首层南院与南廊，保留原室外高差，用明确的新坡道意向连接。三层露台保留开敞，并以轻型花箱、坐凳和换盆台组织使用。',
  '交付离线漫游、Blender/GLB模型、多角度模型图片、矢量平面与方案DXF、可填写分项清单、详细施工交接说明和原图追溯资料。',
  '目前可组织现场复测、家人评审、施工队交底与分项报价；建筑、结构、机电、电梯和防水专业需在复测后共同完成可施工版本。撤梯、开井、补板、承重变更、临空防护及未明排水暂不释放。',
  '图签杭州作为本版地区依据；产权范围、实际项目地址、现状改动、设备型号和材料预算仍应由业主与接手团队核实。']:
  STORY.append(txt(p));STORY.append(Spacer(1,9))
 heading('S01 / 来源与适用','图纸证据和公开要求都可以追溯','网络资料核对日期：2026-09-10。适用条款及过渡要求由所在地专业人员确认；本册不替代法规解释或审批。')
 source=C['sources']
 for i,s in enumerate(source):
  if i and i%5==0:heading('S01 / 来源与适用（续）','按正式版本与项目条件复核')
  STORY.append(txt(s['id']+' / '+s['title'],'h2'))
  STORY.append(txt((s.get('standard') or '')+'　'+(s.get('publisher') or '')+'　'+(s.get('effectiveDate') or ''),'small'))
  STORY.append(txt(s['supports'],'body'))
  url=s.get('url','');STORY.append(html('<link href="'+escape(url,{'"':'&quot;'})+'" color="#498994">'+escape(url)+'</link>','small'));STORY.append(Spacer(1,9))
 heading('S02 / 原图追溯与版本','接手团队使用同一份依据')
 STORY.append(table(['文件/证据','说明'],[
  ['原始DWG','02-10-20B#楼平立面图(1).dwg；原文件保持未修改。'],
  ['SHA-256','f8b152616a5b38dbc866076aca374d165bd5aefeea2e49652542c0df8c4b477b'],
  ['平面与立面','第6户墙柱与洞口分别从各层原点提取；六处北窗保留核对ID；门窗未核值清单单列。'],
  ['室外依据','室外范围核对图及JSON记录南院、南廊、下沉庭院上空、露台与外围待核边界。'],
  ['P02变更','增加花园、坡道与内装细节，修正露台完成标高的依据状态；室内主墙保持原图位置。'],
  ['数据与模型','模型对象标注原图/新增方案；网格尺度按米，方案DXF单位毫米。尺寸取整不等于现场测量精度。'],
  ['打开顺序','解压 → 开始查看.html → 漫游 / PDF / 图册 / 模型；直接打开PDF也可阅读完整报告。']],[220,CW-220]))
 export_tables_and_cad()
 doc=Book(str(OUT/'设计图册.pdf'),pagesize=(W,H),rightMargin=16*mm,leftMargin=16*mm,topMargin=18*mm,bottomMargin=21*mm,
  title=C['title'],author='住宅与花园设计协作',subject='第6户P02设计深化、原图核对及施工交接')
 doc.build(STORY,onFirstPage=footer,onLaterPages=footer)
 (OUT/'报告章节索引.json').write_text(json.dumps(REGISTER,ensure_ascii=False,indent=2))
 print('Built',OUT/'设计图册.pdf')

if __name__=='__main__':build()
