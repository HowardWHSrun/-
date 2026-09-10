"""Detailed interior and reversible landscape proposals on the audited unit-6 shell."""
import copy, json, math, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'tmp/geometry-libs'))
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
import generate_unit6_scene as base
g=base.g
OUT=ROOT.parent/'output/unit6-professional'
OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/'unit6-scene.json').read_text())
g.O=copy.deepcopy(D['objects'])
g.M=copy.deepcopy(D['materials'])
g.M.update({
 'soil':{'color':'#645242','roughness':1},
 'gravel':{'color':'#bcb5a3','roughness':.95},
 'paving':{'color':'#c9c9bc','roughness':.85},
 'charcoal':{'color':'#555e59','roughness':.8},
 'linen':{'color':'#e5e0d4','roughness':1},
 'petalwhite':{'color':'#ede2c8','roughness':.9},
 'petalrose':{'color':'#ba7b80','roughness':.9},
 'petalblue':{'color':'#8f8cab','roughness':.9},
 'lamp':{'color':'#fff2d3','roughness':.35},
 'mirror':{'color':'#b6c5c4','roughness':.08,'metallic':.95}
})
points=[];garden_items=[];custom=[];random.seed(62)

def detail(o,collision=False):
 o['geometryStatus']='新增内装与园林方案；定位尺寸待现场复核'
 o['collision']=collision
 return o
def b(n,x,y,z,w,d,h,m='oak',cat='detail',collision=False,rz=0):
 return detail(g.box(n,x,y,z,w,d,h,m,cat,rz),collision)
def cy(n,x,y,z,r,h,m='metal',cat='detail',collision=False):
 return detail(g.cyl(n,x,y,z,r,h,m,cat),collision)
def sp(n,x,y,z,w,d,h,m='leaf'):
 return detail(g.sphere(n,x,y,z,w,d,h,m))
def point(kind,room,x,y,z,label,orientation='horizontal',note=''): 
 prefix={'light':'L','power':'P','data':'N','water':'W','drain':'D','switch':'S'}[kind]
 pid=f'{prefix}{g.F+1}-{1+sum(p["floor"]==g.F and p["kind"]==kind for p in points):02}'
 points.append({'id':pid,'floor':g.F,'kind':kind,'room':room,'position':[x,y,z],
  'label':label,'orientation':orientation,'status':'design_proposal','note':note or '位置为意向；设备、回路与接入由专业深化确认'})
 return pid
def ceiling_light(room,x,y,z,r=.19):
 pid=point('light',room,x,y,z,'基础照明')
 cy(pid+'灯体',x,y,z,r,.055,'white','ceiling')
 cy(pid+'柔光罩',x,y,z-.031,r*.90,.012,'lamp','ceiling')
def socket(room,x,y,z,axis='y',data=False):
 kind='data' if data else 'power';pid=point(kind,room,x,y,z,'双网口' if data else '插座预留',axis)
 b(pid+'面板',x,y,z,.085 if axis=='y' else .018,.018 if axis=='y' else .085,.085,'white')
 for k in [-1,1]:
  b(pid+'插孔',x+k*.016 if axis=='y' else x+.013,y-.013 if axis=='y' else y+k*.016,z,.006 if axis=='y' else .008,.008 if axis=='y' else .006,.020,'dark')
def tablelamp(n,x,y,z):
 cy(n+'底座',x,y,z+.018,.09,.036,'brass');cy(n+'杆',x,y,z+.20,.013,.38,'brass')
 cy(n+'灯罩',x,y,z+.38,.14,.16,'linen')
def planter(pid,x,y,w,d,h=.42,z=-.03,palette='flower'):
 # Containers remain removable; no excavated or masonry planter foundations are implied.
 b(pid+'轻型花箱',x,y,z+h/2,w,d,h,'terracotta','furniture',True)
 b(pid+'种植介质',x,y,z+h+.006,w-.05,d-.05,.025,'soil')
 count=max(2,round(w/.27))
 for i in range(count):
  xx=x-w*.36+i*w*.72/max(1,count-1); yy=y+random.uniform(-d*.13,d*.13)
  top=z+h+.22+random.uniform(0,.14)
  cy(pid+'枝茎',xx,yy,(z+h+top)/2,.007,top-z-h,'leaf')
  for j in range(3):
   a=j*2.2+i;sp(pid+'叶片',xx+math.cos(a)*.065,yy+math.sin(a)*.06,z+h+.09+j*.045,.16,.065,.045,'leaflight' if j%2 else 'leaf')
  if palette=='flower':
   for j in range(5):
    a=j*math.tau/5;sp(pid+'花瓣',xx+.047*math.cos(a),yy+.047*math.sin(a),top,.065,.065,.035,['petalrose','petalwhite','petalblue'][i%3])
   sp(pid+'花心',xx,yy,top+.008,.03,.03,.018,'brass')
  else:sp(pid+'香草冠',xx,yy,top-.02,.21,.16,.14,'leaflight')
 garden_items.append({'id':pid,'floor':g.F,'name':'轻型花箱 / 季相花卉' if palette=='flower' else '轻型香草花箱',
  'center':[x,y],'size':[w,d,h],'quantity':1,'status':'design_proposal',
  'note':'植物种类按当地气候与实际日照选定；饱水重量及摆位须结构复核'})
def outdoor_light(pid,x,y,z=-.03):
 cy(pid+'灯柱',x,y,z+.23,.028,.46,'charcoal');cy(pid+'灯头',x,y,z+.47,.065,.04,'lamp')
 point('light','室外花园',x,y,z+.47,'遮眩低位花园灯',note='灯具防护、漏电保护及线缆由电气深化；避免照入邻户')

def living_access_fix():
 # Opening the original south access requires relocating furniture, never the source opening.
 def move(predicate,pivot,dest,angle):
  for o in g.O:
   if o.get('floor')!=0 or not predicate(o):continue
   u,v=o['position'][0]-pivot[0],o['position'][1]-pivot[1]
   o['position'][:2]=[round(dest[0]+u*math.cos(angle)-v*math.sin(angle),4),round(dest[1]+u*math.sin(angle)+v*math.cos(angle),4)]
   o['rotation'][2]+=angle
 move(lambda o:o['name'].startswith('电视柜'),(6.8,4.59),(9.18,6.25),-math.pi/2)
 move(lambda o:o['name'] in ('电视','电视画面'),(6.8,4.57),(9.36,6.25),math.pi/2)
 move(lambda o:o['name'].startswith('家庭沙发'),(6.7,6.9),(5.30,6.35),math.pi/2)
 move(lambda o:o['name'].startswith('茶几'),(6.7,5.6),(6.75,6.35),math.pi/2)
 move(lambda o:o['name'].startswith('餐边收纳'),(9.2,7.48),(5.30,8.15),math.pi/2)
 move(lambda o:o['name'].startswith('窗边阅读椅'),(8.72,7.43),(8.20,7.75),0)
 move(lambda o:o['name'].startswith('客厅绿植'),(9.05,5.15),(9.03,4.65),0)
 for o in g.O:
  if o.get('floor')==0 and o['name']=='客厅地毯':o['position'][:2]=[6.7,6.32]
 television_point=next(p for p in points if p['floor']==0 and p['room']=='电视墙')
 television_point['position']=[9.43,6.25,.40];television_point['orientation']='x'
 # Relocate that small panel as well, preserving its point identity.
 move(lambda o:o['name'].startswith(television_point['id']),(7.8,4.25),(9.43,6.25),-math.pi/2)

def interior_details():
 lights={0:[('客厅',5.0,6.4),('客厅',8.3,6.4),('餐厅',6,10.7),('厨房',5.3,13.6),('厨房',6.8,13.6),('玄关',3,13.8),('操盘房',1.3,10.5),('父母卧室',1.8,2.3),('父母卫浴',1.2,6.1),('公卫',.9,13.6),('过厅',3.0,8.5)],
 1:[('主卧',5.5,5.2),('主卧',6.4,7.6),('衣帽间',5.1,10.2),('儿童预留房',1.6,2.1),('公卫',1.2,6.1),('阅读区',1.3,11.4),('家政区',1.5,9.2),('主卫',6.0,12.1),('过厅',3,8.5)],
 2:[('妹妹卧室',1.8,2.1),('妹妹卫浴',1.2,6.1),('毛线工作室',1.2,11.4),('书法房',5.4,10.2),('过厅',3,8.5)]}
 for f,items in lights.items():
  g.F=f;z=[3.43,2.93,2.93][f]
  for room,x,y in items:ceiling_light(room,x,y,z)
  wet=[(.12,5.30,2.30,7.28)]
  if f==0:wet += [(.12,12.82,1.72,14.78),(4.43,12.82,7.68,14.78)]
  if f==1:wet += [(4.32,11.20,7.68,13.48)]
  for x0,y0,x1,y1 in wet:
   b('湿区防滑地面_方案',(x0+x1)/2,(y0+y1)/2,.017,x1-x0,y1-y0,.004,'tile','floor-finish')
   for k in range(math.ceil(x0/.6),math.floor(x1/.6)+1):
    b('湿区地砖分缝',k*.6,(y0+y1)/2,.020,.006,y1-y0,.002,'gravel','floor-finish')
  # Bathroom mirrors, towel rail and accessible accessory zones are detailed without moving source walls.
  b('卫浴镜面示意',.145,5.74,1.44,.035,.64,.80,'mirror')
  b('卫浴镜侧灯',.18,6.10,1.45,.038,.035,.70,'lamp')
  b('毛巾杆',1.76,5.335,1.18,.43,.045,.025,'metal')
  b('折叠毛巾',1.76,5.36,1.12,.29,.038,.13,'linen')
  b('淋浴置物台',.16,6.28,1.10,.075,.26,.035,'stone')
  cy('洗浴瓶',.17,6.25,1.20,.028,.18,'sage')
  point('water','卫浴',.15,5.74,.55,'台盆冷热水意向','x')
  point('drain','卫浴',.68,6.90,.02,'淋浴地漏意向',note='以排水复测与专业坡向图为准，不代表原排水点')
  # Small skirting pieces follow confirmed solid west wall spans.
  for ya,yb in [(1.25,5.05),(5.35,7.20),(8.78,12.60)]:
   b('实墙踢脚收口',.135,(ya+yb)/2,.05,.026,yb-ya,.10,'oaklight')
  socket('床头',.17,4.42,.65,'x')
  socket('卫浴镜柜',.17,5.30,1.18,'x')
  # Fabric stacks remain beside the existing openings, never across an open door.
  for x in [.31,3.29]:
   for k in range(3):b('卧室窗帘褶边',x+k*.025,1.27,1.51,.025,.07,2.60,'linen')
  b('窗帘盒',1.80,1.28,2.86,3.18,.13,.11,'plaster','ceiling')
  point('switch','卧室',3.42,4.93,1.10,'卧室入口及床头联控','x')
 g.F=0
 # Kitchen assembly details and services correspond to actual worktop positions.
 for x in [5.1,5.6,6.1,6.6,7.1]:b('厨房柜门缝',x,14.094,.48,.009,.012,.72,'walnut')
 for x in [5.12,5.62,6.12,6.62,7.12]:b('厨房拉手',x,14.073,.73,.16,.035,.019,'brass')
 b('厨房防溅饰面',6.06,14.766,1.05,2.85,.014,.30,'tile')
 b('沥水盘',6.65,14.38,.937,.44,.30,.035,'charcoal')
 for x in [6.50,6.57,6.64,6.71,6.78]:b('沥水格',x,14.38,.966,.012,.28,.012,'metal')
 cy('电热水壶',5.05,14.37,1.045,.085,.26,'metal')
 b('砧板',7.35,14.12,.938,.44,.35,.025,'oak')
 cy('厨房调味罐',7.47,14.3,1.055,.038,.21,'white')
 b('厨下垃圾分类抽屉',6.68,14.105,.41,.45,.045,.64,'sage')
 b('洗碗机面板',5.03,14.087,.47,.52,.025,.74,'metal')
 custom.append({'id':'C1-01','name':'厨房L形地柜','floor':0,'nominalSize':'北段2820×640；东段640×1130；台面约885高','note':'毫米；现场复尺、设备选型与墙面完成厚度确定后下单'})
 for x in [5.02,6.92]:socket('厨房台面',x,14.738,1.12)
 point('water','厨房',5.93,14.66,.55,'水槽冷热水及净水预留')
 point('drain','厨房',5.93,14.66,.30,'水槽/洗碗机排水接入意向')
 socket('爸爸操盘房',.16,10.83,.95,'x');socket('爸爸操盘房',.16,11.03,.95,'x',True)
 b('操盘桌理线槽',1.04,11.16,.67,1.34,.09,.06,'charcoal')
 b('操盘主机',.40,10.76,.31,.18,.32,.53,'dark','furniture',True)
 tablelamp('操盘辅助灯',1.71,10.78,.81)
 socket('电视墙',7.8,4.25,.40)
 # Loose accessories add scale without interfering with passage widths.
 for x in [5.45,6.05,6.65]:
  for y in [10.42,10.98]:cy('餐盘',x,y,.825,.135,.016,'white')
 cy('餐桌花瓶',6.03,10.71,.94,.067,.22,'sage')
 for x in [6.30,6.82]:b('茶几书册',x,5.6,.463,.28,.20,.035,'paper')
 tablelamp('父母床头灯',.38,4.14,.55)
 g.F=1
 tablelamp('主卧床头灯',4.21,7.07,.55)
 b('主卫镜柜',4.34,11.90,1.47,.055,.68,.77,'mirror')
 socket('主卧床头',7.65,7.16,.65,'x');socket('儿童学习桌',3.42,1.95,1.0,'x')
 socket('阅读家政区',.16,9.9,1.1,'x')
 b('洗衣折叠台',1.53,9.23,1.97,.55,.52,.045,'stone')
 b('儿童画框',.15,2.70,1.50,.035,.67,.52,'oaklight')
 b('儿童画面',.174,2.70,1.50,.012,.59,.44,'paper')
 custom.append({'id':'C2-01','name':'夫妻衣柜','floor':1,'nominalSize':'2400×550×2280','note':'毫米；门板开启与主卫交通需施工放样确认'})
 g.F=2
 socket('毛线工作室',.16,11.8,1.0,'x');socket('书法房',6.46,11.7,.40,'x')
 socket('妹妹书桌',3.42,1.65,1.0,'x',True)
 tablelamp('妹妹学习灯',2.40,1.8,.80)
 tablelamp('毛线工作灯',.57,11.66,.81)
 b('毛线工具托盘',1.77,11.76,.831,.30,.20,.04,'oaklight')
 for i in range(4):cy('编织针',1.66+i*.027,11.72,.865,.004,.27,'metal')
 b('书法笔架',5.50,11.15,.90,.20,.12,.05,'walnut')
 cy('书法水盂',5.28,11.12,.904,.055,.08,'white')
 b('书法墙面展示轨',6.453,10.57,2.04,.030,1.35,.03,'brass')
 b('书法作品装裱框',6.446,10.57,1.55,.032,.62,.84,'walnut')
 b('装裱宣纸',6.424,10.57,1.55,.008,.55,.77,'paper')
 for k in range(5):b('装裱墨迹',6.416,10.57,1.78-k*.11,.008,.035,.062,'dark')
 custom.append({'id':'C3-01','name':'书法长案','floor':2,'nominalSize':'900×1940×800','note':'毫米；桌侧活动空间以实测放样复核'})
 custom.append({'id':'C3-02','name':'毛线工作台','floor':2,'nominalSize':'1650×700×760','note':'毫米；透光与灯位配合，毛线采用封闭干燥收纳'})

def terrace_garden():
 g.F=2
 obsolete=['露台花木','换盆台','露台休闲椅','露台圆几']
 g.O[:]=[o for o in g.O if not (o['floor']==2 and any(o['name'].startswith(s) for s in obsolete))]
 usable=Polygon([[3.74,3.64],[7.90,3.64],[7.90,7.26],[6.46,7.26],[6.46,8.46],[3.74,8.46]])
 # Fine paver joints sit on the source 6.870 terrace plane; they do not change levels.
 for axis in [0,1]:
  for k in range(6,16):
   t=k*.6;q=box(t-.004,3.63,t+.004,8.47) if axis==0 else box(3.73,t-.004,7.91,t+.004)
   p=usable.intersection(q)
   if not p.is_empty:base.mesh_solid('露台600模数分缝_方案',p,-.016,-.013,'gravel','floor-finish')
 planter('G3-P01',4.42,4.31,.88,.44,.37)
 planter('G3-P02',5.61,4.31,.88,.44,.37)
 planter('G3-P03',6.96,4.31,.95,.44,.37,palette='herb')
 planter('G3-P04',7.38,6.61,.72,.40,.47)
 # Rest zone is at the east; a direct central route remains from the original terrace door.
 for k in range(5):b('G3-B01坐凳条板',7.12+k*.045,5.55,.45,.038,1.42,.045,'oak')
 for y in [5.00,6.10]:b('G3-B01坐凳脚',7.20,y,.22,.30,.07,.43,'charcoal','furniture',True)
 b('G3-B01坐垫',7.21,5.55,.495,.39,1.30,.07,'sage')
 b('G3-B01坐凳靠背',7.42,5.55,.76,.055,1.44,.42,'oak')
 garden_items.append({'id':'G3-B01','floor':2,'name':'移动花园坐凳','center':[7.2,5.55],'size':[.45,1.45,.47],'quantity':1,'status':'design_proposal','note':'与护栏安全关系及儿童攀爬风险需现场审查'})
 cy('G3-T01小圆几',6.48,5.48,.46,.29,.065,'stone','furniture',True)
 cy('G3-T01圆几脚',6.48,5.48,.23,.085,.43,'charcoal')
 garden_items.append({'id':'G3-T01','floor':2,'name':'露台小圆几','center':[6.48,5.48],'size':[.58,.58,.49],'quantity':1,'status':'design_proposal','note':'移动成品；在露台地坪上实际台面高度由成品确认'})
 b('G3-W01换盆工作台',6.38,6.78,.85,.80,.46,.06,'stone','furniture',True)
 for x in [6.04,6.72]:b('换盆台支架',x,6.78,.40,.055,.38,.80,'charcoal')
 b('换盆台下层',6.38,6.78,.27,.80,.46,.035,'oak')
 cy('换盆工具桶',6.29,6.79,.98,.068,.20,'charcoal')
 garden_items.append({'id':'G3-W01','floor':2,'name':'换盆台','center':[6.38,6.78],'size':[.80,.46,.85],'quantity':1,'status':'design_proposal','note':'移动成品；不锚入防水层'})
 for pid,x,y in [('G3-L01',4.16,4.90),('G3-L02',7.49,6.15)]:outdoor_light(pid,x,y)
 point('water','露台',6.30,8.36,.45,'花园带阀灌溉接点意向',note='仅接口意向，原供水点未确认；设检修与防冻策略并防回流')
 point('drain','露台',7.69,6.94,-.03,'排水复测控制点',note='不是新增地漏施工坐标；先确认原地漏与溢流，不得擅自穿板')
 # Drip tubes are schematic above-ground removable distribution, not buried construction routes.
 b('花箱可拆滴灌软管',5.75,4.55,.10,3.20,.013,.013,'charcoal')
 D['landscape']={'terraceUsablePolygon':list(usable.exterior.coords)[:-1],
  'designIntent':'花箱+休息+换盆，保持原露台开敞和中央通路；不封阳光房、不设重土池',
  'plantingClimate':'城市及日照待确认；模型表现种植层次，不指定落地植物品种'}

def ground_garden():
 g.F=0
 garden=[[.14,-3.78],[9.46,-3.78],[9.46,2.16],[7.60,2.16],[7.60,1.86],[5.60,1.86],[5.60,2.16],[3.74,2.16],[3.74,.36],[2.995,.36],[2.995,.035],[.605,.035],[.605,.36],[.14,.36]]
 porch=[[3.755,2.455],[4.365,2.455],[4.365,2.16],[8.835,2.16],[8.835,2.455],[9.445,2.455],[9.445,3.945],[3.755,3.945]]
 evidence=json.loads((ROOT/'unit6-landscape-source.json').read_text())
 zones={z['id']:z for z in evidence['zones']}
 assert garden==zones['south_courtyard']['polygon'] and porch==zones['south_main_porch']['polygon']
 # At the masonry door axis the original porch and interior polygons leave a trim-width gap;
 # include only the existing door/porch connection rather than filling outside bays.
 link=[[4.29,3.90],[8.91,3.90],[8.91,4.22],[4.29,4.22]]
 ramp=[[5.90,-2.04],[7.30,-2.04],[7.30,2.16],[5.90,2.16]]
 gardenpoly=Polygon(garden)
 base.mesh_solid('原图南院完成面_不表达地下构造',gardenpoly,-.46,-.40,'paving','slab')
 base.mesh_solid('原图南廊完成面_展示板厚',Polygon(porch).union(Polygon(link)),-.13,-.05,'stone','slab')
 for obj in g.O:
  if obj['name'].startswith('原图南院完成面'):
   obj['source']=['3C6656','3C66A1','3C66A2'];obj['geometryStatus']='原图庭院平面与完成标高；模型薄板不代表地下构造'
  elif obj['name'].startswith('原图南廊完成面'):
   obj['source']=['3C665D','3C6681','3C6682'];obj['geometryStatus']='原图南廊平面与完成/结构标高；门口连接收口为方案'
 # New reversible ramp is a visible wedge surface, with no invented concrete/anchorage design.
 v=[[5.90,-2.04,-.44],[7.30,-2.04,-.44],[7.30,2.16,-.09],[5.90,2.16,-.09],
    [5.90,-2.04,-.40],[7.30,-2.04,-.40],[7.30,2.16,-.05],[5.90,2.16,-.05]]
 o=g.add('新增南院模块坡道_结构及审批待深化','mesh',(0,0,0),(1.4,4.2,.39),'oaklight','slab',
  vertices=v,faces=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]],collision=False)
 o['geometryStatus']='新设计坡道意向；净宽/扶手/荷载/节点待建筑结构确认'
 for x in [5.94,7.26]:
  for i in range(7):
   y=-2.04+i*.70;z=-.40+(y+2.04)*(.35/4.2)
   cy('坡道扶手立柱',x,y,z+.50,.02,1.0,'charcoal',collision=True)
  r=b('坡道扶手',x,.06,.275, .043,4.22,.043,'charcoal',collision=True)
  r['position'][2]=round((-.4-.05)/2+1.0,4);r['rotation'][0]=math.atan(.35/4.2)
 # Low-key paving grid and planted removable modules leave generous central gathering space.
 for k in range(1,16):
  q=box(k*.6-.004,-3.77,k*.6+.004,2.15);p=gardenpoly.intersection(q).difference(Polygon(ramp))
  if not p.is_empty:base.mesh_solid('南院铺装分缝',p,-.398,-.396,'gravel','floor-finish')
 for pid,x,y,w,d,pal in [('G1-P01',1.05,-2.55,1.3,.62,'flower'),('G1-P02',2.90,-2.55,1.3,.62,'flower'),
  ('G1-P03',4.62,-2.55,1.2,.62,'herb'),('G1-P04',.81,-.97,.68,1.0,'herb'),
  ('G1-P05',8.64,-1.95,.65,1.25,'flower'),('G1-P06',8.65,.08,.65,1.2,'flower')]:
  planter(pid,x,y,w,d,.44,-.40,pal)
 # Gathering furniture is set off the continuous ramp and its bottom landing.
 idx=len(g.O);g.table('G1-T01户外家人茶桌',3.3,-.90,1.45,.78,.34,'oak')
 for o in g.O[idx:]:o['position'][2]-=.40;detail(o,True)
 for x,y,a in [(2.30,-.90,-math.pi/2),(4.30,-.90,math.pi/2),(3.30,-.04,math.pi),(3.30,-1.73,0)]:
  idx=len(g.O);g.chair('G1-C01户外休闲椅',x,y,a,'sage')
  for o in g.O[idx:]:o['position'][2]-=.40;detail(o,True)
 cy('南院茶桌果盘',3.3,-.90,-.002,.16,.032,'stone')
 garden_items.extend([
  {'id':'G1-T01','floor':0,'name':'户外茶桌','center':[3.3,-.90],'size':[1.45,.78,.34],'quantity':1,'status':'design_proposal','note':'可移动家具'},
  {'id':'G1-C01','floor':0,'name':'户外休闲椅','quantity':4,'status':'design_proposal','note':'可移动家具'},
  {'id':'G1-R01','floor':0,'name':'模块式通行坡道','center':[6.6,.06],'size':[1.40,4.20,.35],'quantity':1,'status':'approval_hold','note':'高差350mm；坡道面宽1400mm；扶手占宽及平台/排水另需深化，不是已审定无障碍工程'}])
 for pid,x,y in [('G1-L01',1.80,-2.90),('G1-L02',4.80,-2.90),('G1-L03',8.75,1.23)]:outdoor_light(pid,x,y,-.4)
 # Guard follows the source south edge. Its height and members are a proposed safety detail.
 for x in [i*.1+.19 for i in range(93)]:cy('南院临空防护竖杆',x,-3.83,.14,.012,1.1,'charcoal',collision=True)
 b('南院临空防护扶手',4.80,-3.83,.70,9.36,.05,.05,'charcoal',collision=True)
 for x in [.03,9.57]:
  b('南院两侧墙_原图位置高度待核',x,-1.68,.15,.22,4.22,1.1,'plaster','wall-low',True)
 point('water','首层南院',8.88,1.38,.12,'可检修灌溉接口意向',note='需核实既有给水与冬季排空；与建筑防水及邻界协调')
 point('drain','首层南院',8.95,-2.89,-.40,'院内雨水复测控制点',note='不代表已确认地漏或雨水接驳，坡向与排水能力需专项复测')
 f=D['walkthrough']['floors'][0]
 enlarged=unary_union([Polygon(f['boundary']),gardenpoly,Polygon(porch),Polygon(link),Polygon(ramp)])
 # Tiny survey-line gaps are covered by the explicitly proposed deck at the source stair opening.
 assert enlarged.geom_type=='Polygon',enlarged.geom_type
 f['boundary']=[list(p) for p in enlarged.exterior.coords[:-1]]
 f['surfaces']=[{'polygon':ramp,'profile':{'axis':'y','start':2.16,'end':-2.04,'startElevation':-.05,'endElevation':-.40}},
  {'polygon':porch,'elevation':-.05},{'polygon':link,'elevation':-.05},{'polygon':garden,'elevation':-.40},*f['surfaces']]
 f['rooms'] += [{'name':'首层南院花园','polygon':garden},{'name':'南廊','polygon':porch}]
 D['landscape'].update({'groundGardenPolygon':garden,'porchPolygon':porch,'rampPolygon':ramp,
  'groundGardenElevation':-.40,'porchElevation':-.05,'sourceProjectCity':'杭州（原图图签，实际项目待业主复核）',
  'groundGardenArea':round(gardenpoly.area,3),'rampSlope':'1:12 几何意向；合法性及完整节点待专业深化',
  'excluded':'南缘y=-3.78以南及东侧下沉庭院上空保持空洞；未推定产权线'})
 (OUT/'室外原图依据.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))

def finish():
 D['meta']['title']='第6户 · 住宅与花园深化方案'
 D['meta']['issue']='P02 / 2026-09-10 / 方案交底、复测与报价使用'
 D['meta']['notes'] += ['P02增加内装、照明接口和轻型花园细节；不改变已核对主体墙位。','本包包含待复核项，未达到经签章的施工图发布条件。']
 D['meta']['notes']=[n.replace('三层退台及主标高','三层退台及室内主标高') for n in D['meta']['notes']]
 D['meta']['notes'].append('新核对：露台结构标高6.770有原图依据；6.870完成面仍为展示假设。南院-0.400、南廊-0.050按源标注表达。')
 D['objects']=g.O;D['materials']=g.M;D['designPoints']=points
 (ROOT/'unit6-professional-scene.json').write_text(json.dumps(D,ensure_ascii=False,separators=(',',':')))
 (OUT/'方案点位与定制清单.json').write_text(json.dumps({'points':points,'gardenItems':garden_items,'customFurniture':custom},ensure_ascii=False,indent=2))
 print(f'Professional scene: {len(g.O)} objects, {len(points)} service intents, {len(garden_items)} garden assemblies')

if __name__=='__main__':
 interior_details();living_access_fix();terrace_garden();ground_garden();finish()
