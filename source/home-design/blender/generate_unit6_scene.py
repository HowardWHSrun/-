"""Drawing-grounded unit 6 shell plus separately identified interior proposals."""
import json, math, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'tmp'/'geometry-libs'))
from shapely.geometry import Polygon, box as sbox
from shapely import constrained_delaunay_triangles
from shapely.ops import unary_union
import generate_scene as g

OUT=ROOT.parent/'output'/'unit6'; OUT.mkdir(parents=True,exist_ok=True)
LIFT_OUT=[2.45,9.50,4.10,11.40]
LIFT_IN=[2.57,9.62,3.98,11.28]
DOOR_CENTER=10.45
DOOR_WIDTH=.95
floors=[]; vertical_assumptions=[]; room_zones=[]; upper_footprints={}
vertical_evidence=json.loads((ROOT/'unit6-vertical-verified.json').read_text())
verified_applied=[]
g.O.clear()

def rectpoly(b):
 x0,y0,x1,y1=b;return [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
def addbox(name,b,z0,z1,mat='plaster',cat='wall',status='原图平面定位',source=None):
 x0,y0,x1,y1=b
 if x1-x0<.0001 or y1-y0<.0001 or z1-z0<.0001:return
 o=g.box(name,(x0+x1)/2,(y0+y1)/2,(z0+z1)/2,x1-x0,y1-y0,z1-z0,mat,cat)
 o['geometryStatus']=status
 if source:o['source']=source.get('rootHandle',source.get('handle','原图')) if isinstance(source,dict) else source
 return o
def mesh_solid(name,poly,z0,z1,mat,cat='slab'):
 if poly.is_empty:return
 if poly.geom_type in ['MultiPolygon','GeometryCollection']:
  for i,p in enumerate(poly.geoms):
   if p.geom_type in ['Polygon','MultiPolygon']:mesh_solid(f'{name}_{i}',p,z0,z1,mat,cat)
  return
 vs=[];fs=[];lookup={}
 def v(x,y,z):
  p=(round(x,4),round(y,4),round(z,4))
  if p not in lookup:lookup[p]=len(vs);vs.append(p)
  return lookup[p]
 for tri in constrained_delaunay_triangles(poly).geoms:
  p=list(tri.exterior.coords)[:-1]
  fs.append([v(x,y,z1) for x,y in p]);fs.append([v(x,y,z0) for x,y in reversed(p)])
 for ring in [poly.exterior,*poly.interiors]:
  p=list(ring.coords)
  for a,b in zip(p,p[1:]):fs.append([v(*a,z0),v(*b,z0),v(*b,z1),v(*a,z1)])
 volume=0
 for face in fs:
  a=vs[face[0]]
  for i in range(1,len(face)-1):
   b,c=vs[face[i]],vs[face[i+1]]
   volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
 if volume<0:fs=[list(reversed(face)) for face in fs]
 b=poly.bounds
 g.add(name,'mesh',(0,0,0),(b[2]-b[0],b[3]-b[1],z1-z0),mat,cat,vertices=vs,faces=fs,collision=False)

def fullwall(name,b,h,status='原图平面定位',source=None,mat='plaster'):
 addbox(name,b,0,min(.90,h),mat,'wall-low',status,source)
 if h>.90:addbox(name,b,.90,h,mat,'wall-high',status,source)

def opening(op,h):
 op=dict(op);op.setdefault('name',op.get('id','原图门窗'))
 first_object=len(g.O)
 verified=None
 for item in vertical_evidence['verified']:
  if item['floor']!=g.F+1:continue
  same_id=op.get('id')==item['id']
  same_plan=(item.get('planA') is not None and op.get('code')==item['code']
   and all(abs(a-b)<.002 for a,b in zip(op['a'],item['planA']))
   and all(abs(a-b)<.002 for a,b in zip(op['b'],item['planB'])))
  if same_id or same_plan:
   verified=item;op['sill']=item['sill'];op['height']=item['height']
   verified_applied.append(item['id']);break
 a,b=op['a'],op['b'];axis=0 if abs(a[1]-b[1])<.002 else 1
 c=(a[1]+b[1])/2 if axis==0 else (a[0]+b[0])/2
 lo,hi=sorted([a[axis],b[axis]]);th=op.get('thickness',.24)
 bounds=[lo,c-th/2,hi,c+th/2] if axis==0 else [c-th/2,lo,c+th/2,hi]
 code=op.get('code') or '';match=re.search(r'(\d{2})(\d{2})',code)
 nominal_h=int(match.group(2))/10 if match else None
 door=op['type'] in ['door','entrance','door-window','door_window','doorWindow','glazed_door','passage'] or code.startswith('MLC')
 height=op.get('height') or nominal_h or (2.1 if door else 1.6)
 sill=op.get('sill')
 if sill is None:sill=0 if door else max(.25,2.60-height)
 height=min(height,h-.10-sill);top=sill+height
 if op.get('height') is None or op.get('sill') is None:
  vertical_assumptions.append({'floor':g.F+1,'name':op['name'],'code':code,'sill':round(sill,3),'height':round(height,3),'status':'高度按门窗编号推定、窗台为展示值，未获逐窗立面对应'})
 if sill:fullwall(op['name']+'窗下墙',bounds,sill,source=op.get('source'))
 addbox(op['name']+'过梁',bounds,top,h,'plaster','wall-high',source=op.get('source'))
 # Room doors remain open, exactly at the recorded opening. MLC assemblies retain sidelights.
 clear=(min(1.45,hi-lo-.10) if code.startswith('MLC') else hi-lo)
 split=(hi+lo)/2
 glass_intervals=[] if door else [(lo,hi)]
 if door and hi-lo>1.8:glass_intervals=[(lo,split-clear/2),(split+clear/2,hi)]
 for l,r in glass_intervals:
  if r-l<.03:continue
  bb=[l,c-.018,r,c+.018] if axis==0 else [c-.018,l,c+.018,r]
  addbox(op['name']+'玻璃',bb,sill+.025,top-.025,'glass','glazing',source=op.get('source'))
  count=max(1,round((r-l)/.75))
  for i in range(count+1):
   t=l+(r-l)*i/count
   bb=[t-.023,c-.028,t+.023,c+.028] if axis==0 else [c-.028,t-.023,c+.028,t+.023]
   addbox(op['name']+'窗框',bb,sill,top,'dark','glazing')
 for z in [sill,top]:
  if door and z==0:continue
  bb=[lo,c-.03,hi,c+.03] if axis==0 else [c-.03,lo,c+.03,hi]
  addbox(op['name']+'横框',bb,z-.023,z+.023,'oak' if door else 'dark','glazing')
 for t in [lo+.023,hi-.023]:
  bb=[t-.023,c-th/2,t+.023,c+th/2] if axis==0 else [c-th/2,t-.023,c+th/2,t+.023]
  addbox(op['name']+'门窗套',bb,0 if door else sill,top,'oak' if door else 'dark','glazing')
 if verified:
  for obj in g.O[first_object:]:
   obj['geometryStatus']=obj.get('geometryStatus','原图平面定位')+'；窗台及窗高按北立面核对'
   obj['verticalSource']=verified['sourceRootHandle']+':'+verified['id']

def proposed_partition(name,b,h,door=None,glass=False):
 if not door:fullwall(name,b,h,'新增内装',mat='glass' if glass else 'plaster');return
 x0,y0,x1,y1=b
 if x1-x0<y1-y0:
  for a,z in [(y0,door[0]),(door[1],y1)]:fullwall(name,[x0,a,x1,z],h,'新增内装',mat='glass' if glass else 'plaster')
  addbox(name+'门上收口',[x0,door[0],x1,door[1]],2.15,h,'oak','wall-high','新增内装')
 else:
  for a,z in [(x0,door[0]),(door[1],x1)]:fullwall(name,[a,y0,z,y1],h,'新增内装',mat='glass' if glass else 'plaster')
  addbox(name+'门上收口',[door[0],y0,door[1],y1],2.15,h,'oak','wall-high','新增内装')

def shell(fl):
 global floors
 f=fl.get('floorIndex',fl.get('id',1)-1);g.F=f
 elev=fl['elevation'];height=fl['ceilingElevation']-elev-.16
 boundary=fl['boundary'];indoor=fl.get('indoorBoundary',fl.get('ceilingBoundary',boundary))
 holes=[v['polygon'] for v in fl.get('voids',[]) if v.get('preserve',True)]
 if not fl.get('voids'):holes=fl.get('preservedHoles',[])
 void_geom=unary_union([Polygon(p) for p in holes]);footprint=Polygon(boundary).difference(void_geom);shaft=sbox(*LIFT_IN)
 interior=Polygon(indoor).difference(void_geom)
 terraces=[];surfaces=[]
 for t in fl.get('terraces',[]):
  p=t.get('polygon') if isinstance(t,dict) else t
  poly=Polygon(p).intersection(footprint)
  if poly.is_empty or poly.area<.01:continue
  level=t.get('floorElevation',elev) if isinstance(t,dict) else elev
  dz=level-elev;terraces.append(poly);surfaces.append({'polygon':p,'elevation':level})
  mesh_solid('原图露台楼板',poly,dz-.16,dz,'stone')
  mesh_solid('原图露台地面',poly,dz,dz+.012,'tile','floor-finish')
 terrace_geom=unary_union(terraces)
 mesh_solid('原图范围楼板_仅补原楼梯洞',footprint.difference(shaft).difference(terrace_geom),-.16,0,'stone')
 interior=interior.difference(terrace_geom)
 mesh_solid('室内木地面',interior.difference(shaft),0,.014,'floor','floor-finish')
 cap=interior.difference(shaft)
 if f in upper_footprints:cap=cap.difference(upper_footprints[f])
 mesh_solid('室内顶面_展示构造',cap,height,height+.10,'plaster','ceiling')
 if f==2:mesh_solid('主体屋顶_屋顶细部待核',interior.difference(shaft),2.98,3.03,'stone','roof')
 def subtract_rect(b,q):
  x0,y0,x1,y1=b;a0,b0,a1,b1=q
  if a0>=x1-.00001 or a1<=x0+.00001 or b0>=y1-.00001 or b1<=y0+.00001:return [b]
  a0=max(a0,x0);a1=min(a1,x1);b0=max(b0,y0);b1=min(b1,y1)
  return [p for p in [[x0,y0,a0,y1],[a1,y0,x1,y1],[a0,y0,a1,b0],[a0,b1,a1,y1]] if p[2]-p[0]>.00001 and p[3]-p[1]>.00001]
 for b in fl['boxes']:
  pieces=[b['bounds']]
  if b.get('role')!='column' and b.get('type')!='column' and 'column' not in b.get('method',''):
   for op in fl['openings']:
    a,z=op['a'],op['b'];th=op.get('thickness',.24)
    q=[min(a[0],z[0]),a[1]-th/2-.001,max(a[0],z[0]),a[1]+th/2+.001] if abs(a[1]-z[1])<.002 else [a[0]-th/2-.001,min(a[1],z[1]),a[0]+th/2+.001,max(a[1],z[1])]
    pieces=[sub for p in pieces for sub in subtract_rect(p,q)]
  for p in pieces:fullwall(b.get('name',b.get('id','原图墙柱')),p,height,source=b.get('source'))
 for op in fl['openings']:opening(op,height)
 for p in fl.get('parapets',[]):
  fullwall(p['name'],p['bounds'],p.get('height') or p.get('displayHeight',1.1),'原图平面定位；栏墙高度展示值',p.get('source'))
 # New shaft in the common circulation zone, with the same east-facing door on all levels.
 x0,y0,x1,y1=LIFT_OUT;ix0,iy0,ix1,iy1=LIFT_IN
 for n,b in [('西',[x0,y0,ix0,y1]),('南',[ix0,y0,x1,iy0]),('北',[ix0,iy1,x1,y1])]:
  fullwall('新增中央电梯井'+n,b,height,'用户指定电梯改造',mat='oaklight')
 for a,b in [(iy0,DOOR_CENTER-DOOR_WIDTH/2),(DOOR_CENTER+DOOR_WIDTH/2,iy1)]:
  fullwall('新增电梯门侧墙',[ix1,a,x1,b],height,'用户指定电梯改造',mat='oaklight')
 addbox('新增电梯门上墙',[ix1,DOOR_CENTER-DOOR_WIDTH/2,x1,DOOR_CENTER+DOOR_WIDTH/2],2.15,height,'oaklight','wall-high','用户指定电梯改造')
 g.label('中央电梯',sum(LIFT_IN[::2])/2,sum(LIFT_IN[1::2])/2,.03,1.15)
 floors.append({'id':f,'label':f'{f+1}F','elevation':elev,'boundary':boundary,'holes':holes,'rooms':[],'surfaces':surfaces})

def zone(name,b,polygon=None):
 p=polygon or rectpoly(b);floors[g.F]['rooms'].append({'name':name,'polygon':p})
 room_zones.append({'floor':g.F,'name':name,'polygon':p})
 g.label(name,(b[0]+b[2])/2,b[1]+.37,.038,min(2.1,b[2]-b[0]-.2))
def rug(name,x,y,w,d):g.box(name,x,y,.025,w,d,.022,'rug','rug')
def rotated(fn,x,y,angle,*args,**kwargs):
 i=len(g.O);fn(*args,**kwargs);g.transform_new(i,x,y,angle)
def sink(name,x,y,w=.65,d=.6):
 g.box(name+'柜',x,y,.42,w,d,.8,'oaklight');g.box(name+'台面',x,y,.86,w+.025,d+.025,.06,'stone')
 g.box(name+'盆',x,y,.897,w*.65,d*.66,.035,'white')
 g.cyl(name+'龙头',x,y+d*.29,1.0,.018,.23,'metal')
def bathroom(name,xoff=0):
 g.toilet(name,xoff+1.84,6.89)
 sink(name+'洗手台',xoff+.58,5.74,.69,.62)
 g.box(name+'淋浴区',xoff+.68,6.82,.025,1.07,.93,.034,'tile','floor-finish')
 g.cyl(name+'花洒',xoff+.26,7.04,1.2,.018,1.7,'metal')
 g.box(name+'顶喷',xoff+.39,7.04,2.07,.29,.23,.025,'metal')
 g.box(name+'淋浴侧屏',xoff+1.23,6.96,1.02,.022,.63,2.04,'glass','glazing')
def bedding(name,x,y,w,color):g.bed(name,x,y,w,color)

def interiors():
 g.F=0
 zone('父母卧室',[.12,1.22,3.48,5.18])
 rug('父母卧室地毯',1.65,3.10,2.65,2.7);bedding('父母',1.45,3.38,1.5,'sage')
 rotated(g.cabinet,3.13,2.35,-math.pi/2,'父母衣柜',3.13,2.35,1.65,.55,2.25)
 proposed_partition('父母卧室隐私隔断',[2.42,5.08,3.48,5.18],3.54,[2.5,3.38])
 proposed_partition('父母房东侧隐私隔断',[3.48,4.22,3.60,5.18],3.54)
 zone('客厅',[3.72,4.22,9.48,8.48]);rug('客厅地毯',6.9,6.05,3.9,2.85)
 g.sofa('家庭沙发',6.7,6.90,2.65);g.table('茶几',6.7,5.60,1.2,.7,.39,'oaklight')
 g.cabinet('电视柜',6.8,4.59,2.3,.4,.48,'oaklight',True)
 g.box('电视',6.8,4.57,1.38,1.72,.075,.99,'dark')
 g.box('电视画面',6.8,4.615,1.38,1.63,.012,.9,'screen')
 g.chair('窗边阅读椅',8.72,7.43,-.6,'sage');g.plant('客厅绿植',9.05,5.15,.63)
 zone('餐厅',[4.10,8.72,7.68,12.58]);g.table('六人餐桌',6.00,10.70,1.8,.85,.76)
 for x in [5.4,6,6.6]:g.chair('餐椅',x,9.92);g.chair('餐椅',x,11.48,math.pi)
 rotated(g.cabinet,9.20,7.48,-math.pi/2,'餐边收纳',9.20,7.48,1.25,.42,.92,'oaklight',True)
 zone('厨房',[4.32,12.82,7.68,14.78])
 proposed_partition('中厨玻璃隔断',[4.43,12.70,7.569,12.78],3.54,[5.40,6.60],True)
 g.box('厨房北地柜',6.04,14.42,.43,2.82,.64,.86,'oaklight')
 g.box('厨房北台面',6.04,14.42,.885,2.87,.67,.06,'stone');g.box('双槽水盆',5.93,14.41,.925,.73,.45,.025,'metal')
 g.box('水槽内',5.93,14.41,.943,.64,.37,.012,'water');g.cyl('厨房龙头',5.93,14.64,1.09,.019,.31,'metal')
 g.box('厨房东地柜',7.35,13.55,.43,.64,1.13,.86,'oaklight');g.box('灶台石材',7.35,13.55,.885,.67,1.15,.06,'stone')
 g.box('燃气灶',7.35,13.52,.928,.48,.76,.028,'dark')
 for y in [13.30,13.73]:g.cyl('炉头',7.35,y,.947,.14,.026,'metal')
 g.box('烟机',7.35,13.52,1.91,.65,.86,.23,'metal','wall-high')
 g.box('冰箱',4.72,13.29,1.02,.66,.73,2.04,'metal')
 g.box('冰箱把手',4.72,12.91,1.18,.025,.04,.61,'dark')
 zone('玄关',[1.82,12.82,4.08,14.78]);g.cabinet('玄关鞋柜',3.76,13.12,.46,.28,1.10)
 zone('爸爸操盘房',[.12,8.72,2.42,12.68]);g.desk('爸爸三屏操盘',1.04,10.83,1.48,True)
 rotated(g.shelf,.35,9.45,math.pi/2,'操盘资料柜',.35,9.45,1.08,.32,1.75)
 proposed_partition('操盘房玻璃隔断',[2.34,8.72,2.42,12.68],3.54,[11.62,12.52],True)
 bathroom('父母卫浴');zone('父母卫浴',[.12,5.3,2.3,7.28])
 g.toilet('玄关公卫',1.05,14.22);sink('公卫台盆',.50,13.23,.60,.57)
 zone('玄关公卫',[.12,12.82,1.72,14.78])

 g.F=1
 zone('夫妻主卧',[3.72,4.22,7.68,8.60]);rug('主卧地毯',5.45,6.33,3.1,3.30);bedding('夫妻',5.43,6.32,1.80,'sage')
 g.cabinet('主卧矮柜',5.55,4.65,1.75,.4,.74,'oaklight',True)
 zone('衣帽区',[4.32,8.72,7.68,11.08]);rotated(g.cabinet,6.25,9.2,math.pi,'夫妻衣柜',6.25,9.2,2.40,.55,2.28)
 # Lightweight interior screens follow the original dashed reference, and are recorded as new work.
 proposed_partition('主卧隐私屏',[3.50,4.22,3.60,8.60],3.04,[7.55,8.48])
 zone('儿童预留房',[.12,1.22,3.48,5.18]);rug('儿童地毯',1.8,2.75,2.5,2.4)
 bedding('儿童预留床',1.25,3.47,1.00,'blue')
 g.table('儿童学习桌',2.76,1.77,.9,.55,.73);g.chair('儿童学习椅',2.76,2.42,math.pi)
 rotated(g.cabinet,3.1,3.50,-math.pi/2,'儿童储物柜',3.1,3.50,1.2,.50,1.6)
 proposed_partition('儿童房隐私门',[2.42,5.08,3.48,5.18],3.04,[2.50,3.38])
 bathroom('儿童公卫');zone('儿童公卫',[.12,5.3,2.3,7.28])
 zone('家庭阅读区',[.12,8.72,2.42,12.68]);rotated(g.shelf,.35,11.55,math.pi/2,'家庭图书',.35,11.55,1.55,.34,1.9)
 g.chair('阅读椅',1.3,11.7,math.pi/2,'sage');g.table('阅读茶几',1.65,10.55,.52,.52,.49)
 g.box('洗衣机',.59,9.25,.46,.65,.64,.92,'white');g.box('烘干机',.59,9.25,1.43,.65,.64,.92,'white')
 for z in [.47,1.44]:
  o=g.cyl('洗烘圆门',.59,8.916,z,.21,.032,'dark');o['rotation']=[math.pi/2,0,0]
 g.cabinet('家政柜',1.46,9.15,.55,.5,1.85)
 zone('主卫',[4.32,11.2,7.68,13.48]);sink('主卫台盆',4.80,11.90,.65,.80)
 g.toilet('主卫',6.06,13.0);g.box('浴缸',7.15,12.25,.33,.74,1.62,.60,'white')
 g.box('浴缸内',7.15,12.25,.637,.56,1.39,.023,'water')
 g.box('主卫淋浴地盘',4.93,12.98,.025,1.04,.93,.04,'tile','floor-finish')
 g.cyl('主卫花洒',4.54,13.18,1.22,.018,1.7,'metal')

 g.F=2
 zone('妹妹卧室',[.12,1.22,3.48,5.18]);rug('妹妹地毯',1.67,3.22,2.5,2.7);bedding('妹妹',1.40,3.48,1.35,'rose')
 g.table('妹妹书桌',2.75,1.80,1.08,.55,.75);g.chair('妹妹书椅',2.75,2.45,math.pi,'rose')
 rotated(g.cabinet,3.15,3.65,-math.pi/2,'妹妹衣柜',3.15,3.65,1.20,.50,2.20)
 bathroom('妹妹卫浴');zone('妹妹卫浴',[.12,5.3,2.3,7.28])
 zone('书法房',[4.12,8.72,6.48,12.68]);g.table('书法长案',5.36,10.43,.90,1.94,.80,'walnut')
 g.box('宣纸',5.36,10.43,.853,.68,1.36,.007,'paper')
 for i in range(7):g.box('书法墨迹',5.28+(i%2)*.17,9.9+i*.15,.861,.027,.105,.004,'dark',rz=.2-i*.07)
 g.box('砚台',5.67,11.18,.882,.17,.23,.042,'dark');g.cyl('笔筒',5.05,11.17,.94,.055,.24,'walnut')
 for i in range(5):g.cyl('毛笔',5.02+.015*i,11.17,1.10,.005,.27,'walnut')
 g.cabinet('宣纸平放柜',4.58,12.37,.70,.44,.90,'oaklight',True)
 g.cabinet('书法藏书矮柜',5.9,12.42,.95,.34,.92,'oaklight')
 zone('妈妈毛线工作室',[.12,8.72,2.42,12.68]);g.table('编织工作台',1.25,11.68,1.65,.7,.76)
 g.chair('妈妈工作椅',1.25,10.96,0,'rose');g.box('编织作品',1.22,11.65,.82,.61,.38,.032,'rose')
 for i,c in enumerate(['sage','cream','blue','rose']):g.sphere('桌上毛线',1.87,11.48+i*.11,.89,.13,.13,.13,c)
 rotated(g.shelf,.34,9.8,math.pi/2,'防尘毛线柜',.34,9.80,1.45,.30,1.9,True)
 g.cabinet('室内花艺窗台架',1.25,12.43,1.40,.30,.73,'oaklight')
 for x in [.80,1.30,1.79]:g.plant('室内阳光花艺',x,12.41,.29,z=.77)
 zone('妈妈露台花园',[3.72,3.62,7.92,8.48],[[3.72,3.62],[7.92,3.62],[7.92,7.28],[6.48,7.28],[6.48,8.48],[3.72,8.48]])
 for i,(x,y) in enumerate([(4.18,3.99),(5.16,4.00),(6.29,4.00),(7.45,4.06),(7.46,5.14),(7.45,6.28)]):g.plant('露台花木',x,y,.60 if i%2 else .84,z=-.03)
 g.table('换盆台',7.36,6.76,.74,.54,.80,'oaklight');g.chair('露台休闲椅',4.43,6.1,.7,'sage')
 g.table('露台圆几',5.3,5.62,.64,.64,.46);g.plant('书房窗边盆栽',6.16,12.01,.48)

 for o in g.O:
  if o.get('category')=='furniture':o.setdefault('geometryStatus','新增家具与内装示意')

def main():
 raw=json.loads((ROOT/'unit6-floors12.json').read_text());ff=raw['floors'] if isinstance(raw,dict) else raw
 ff.append(json.loads((ROOT/'unit6-floor3.json').read_text()))
 ff=sorted(ff,key=lambda f:f['elevation'])
 for i in [0,1]:
  up=ff[i+1];voids=unary_union([Polygon(v['polygon']) for v in up.get('voids',[]) if v.get('preserve',True)])
  upper_footprints[i]=Polygon(up['boundary']).difference(voids).difference(sbox(*LIFT_IN))
 for fl in ff:shell(fl)
 assert set(verified_applied)=={v['id'] for v in vertical_evidence['verified']},verified_applied
 interiors()
 # Entry is inside the original north foyer, looking south into the house.
 data={'meta':{'title':'第6户 · 三层住宅漫游','unit':6,'width':9.84,'depth':15.0,'roof_elevation':9.9,
  'source':'02-10-20B#楼平立面图(1).dwg / E4户型；原图平面墙皮与洞口提取到毫米',
  'notes':['以第6户原图平面、门窗洞口、采光井、三层退台及主标高建立。','取消楼梯、原楼梯洞补板、新中央电梯和家具内装属于改造方案。','六处北侧窗的窗台及窗高已按原立面核对；其余门窗竖向、栏墙高度、顶面和板厚仍含展示参数。','三层花园使用原露台，保持露天；毛线工作室在室内。'],
  'blender':{'interior_view':{'floor':0,'position':[8.6,5.3,1.65],'target':[5.4,10.0,1.5],'lens':22}}},
  'materials':g.M,'objects':g.O,
  'walkthrough':{'floors':floors,'spawn':{'floor':0,'position':[3.12,13.63],'yaw':math.pi},
   'elevator':{'bounds':LIFT_IN,'stops':[0,1,2],'initialFloor':0,'door':{'side':'east','center':DOOR_CENTER,'width':DOOR_WIDTH}}}}
 (ROOT/'unit6-scene.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
 (OUT/'门窗展示参数.json').write_text(json.dumps(vertical_assumptions,ensure_ascii=False,indent=2))
 (OUT/'门窗立面核对.json').write_text(json.dumps(vertical_evidence,ensure_ascii=False,indent=2))
 print(f'Unit6 scene: {len(g.O)} objects; {len(floors)} floors; {len(vertical_assumptions)} provisional vertical details')
if __name__=='__main__':main()
