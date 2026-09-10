"""Shared, metre-based conceptual geometry for Blender and the interactive viewer."""
import json,math,random
from pathlib import Path
R=Path(__file__).resolve().parent
R.mkdir(exist_ok=True)
random.seed(8)
M={
 'plaster':{'color':'#eee9df','roughness':.9},'oak':{'color':'#ad8055','roughness':.62},
 'oaklight':{'color':'#d1b18c','roughness':.7},'walnut':{'color':'#72503a','roughness':.62},
 'floor':{'color':'#c9b08f','roughness':.78},'tile':{'color':'#d6d6cb','roughness':.62},
 'stone':{'color':'#eeeae0','roughness':.45},'cream':{'color':'#e3d9c7','roughness':.94},
 'sage':{'color':'#8d9c82','roughness':.94},'rose':{'color':'#c69d93','roughness':.94},
 'blue':{'color':'#7a919e','roughness':.94},'dark':{'color':'#26342f','roughness':.5},
 'metal':{'color':'#737c77','roughness':.28,'metallic':.65},'white':{'color':'#f5f1e7','roughness':.8},
 'glass':{'color':'#b4d6d5','roughness':.12,'alpha':.20},'water':{'color':'#678f94','roughness':.2},
 'leaf':{'color':'#547452','roughness':.9},'leaflight':{'color':'#7d9360','roughness':.9},
 'terracotta':{'color':'#b87956','roughness':.9},'paper':{'color':'#f6eed9','roughness':1},
 'screen':{'color':'#152c32','roughness':.25},'chartup':{'color':'#80b49a','roughness':.5},
 'chartdown':{'color':'#bf8370','roughness':.5},'brass':{'color':'#b9a16f','roughness':.25,'metallic':.65},
 'garden':{'color':'#c5c8b3','roughness':.95},'rug':{'color':'#c9c1ac','roughness':1}
}
O=[];F=0
def add(name,kind,pos,size,mat='oak',cat='furniture',rot=(0,0,0),**kw):
 o={'name':name,'kind':kind,'floor':F,'position':[round(v,4) for v in pos],'size':[round(v,4) for v in size],'rotation':list(rot),'material':mat,'category':cat,**kw};O.append(o);return o
def box(n,x,y,z,dx,dy,dz,m='oak',cat='furniture',rz=0):return add(n,'box',(x,y,z),(dx,dy,dz),m,cat,(0,0,rz))
def cyl(n,x,y,z,r,h,m='oak',cat='furniture'):return add(n,'cylinder',(x,y,z),(r*2,r*2,h),m,cat)
def sphere(n,x,y,z,dx,dy,dz,m='leaf'):return add(n,'sphere',(x,y,z),(dx,dy,dz),m)
def label(n,x,y,z=.06,size=1.9):return add(n,'text',(x,y,z),(size,.31,.01),'dark','label',text=n)
def table(n,x,y,w=1.8,d=.85,h=.76,m='oak'):
 box(n+'台面',x,y,h,w,d,.09,m)
 for a in [-1,1]:
  for b in [-1,1]:box(n+'桌腿',x+a*(w/2-.1),y+b*(d/2-.1),h/2,.07,.07,h-.04,m)
def chair(n,x,y,rz=0,m='sage'):
 idx=len(O)
 box(n+'坐垫',x,y,.46,.47,.45,.11,m)
 box(n+'靠背',x,y-.2,.72,.47,.09,.47,m)
 for a in [-1,1]:
  for b in [-1,1]:box(n+'椅腿',x+a*.17,y+b*.16,.23,.045,.045,.43,'oak')
 if rz:
  for o in O[idx:]:
   u,v=o['position'][0]-x,o['position'][1]-y;o['position'][0]=x+u*math.cos(rz)-v*math.sin(rz);o['position'][1]=y+u*math.sin(rz)+v*math.cos(rz);o['rotation'][2]+=rz
def bed(n,x,y,w=1.8,m='sage'):
 box(n+'床框',x,y,.26,w+.1,2.15,.34,'oak')
 box(n+'床垫',x,y,.49,w,2.06,.24,'cream')
 box(n+'被子',x,y-.22,.64,w-.04,1.46,.09,m)
 box(n+'床头',x,y+1.1,.74,w+.14,.12,1.26,'oak')
 for xx in [-w/4,w/4]:box(n+'枕头',x+xx,y+.7,.65,w*.41,.4,.14,'white')
 for xx in [-1,1]:box(n+'床头柜',x+xx*(w/2+.32),y+.75,.28,.48,.48,.52,'oaklight')
def cabinet(n,x,y,w,d=.55,h=2.25,m='oaklight',drawers=False):
 box(n,x,y,h/2,w,d,h,m)
 if drawers:
  for zz in [.22,.4,.58,.76]:
   box(n+'抽屉线',x,y-d/2-.01,zz,w-.07,.012,.012,'walnut')
   box(n+'抽屉拉手',x,y-d/2-.035,zz+.05,.16,.045,.022,'brass')
 else:
  count=max(1,round(w/.55))
  for j in range(count):
   xx=x-w/2+(j+.5)*w/count
   box(n+'分缝',xx+w/count/2,y-d/2-.008,h/2,.012,.012,h-.03,'walnut')
   box(n+'把手',xx+.1,y-d/2-.03,1.1,.02,.045,.24,'brass')
def shelf(n,x,y,w=1.5,d=.32,h=1.8,yarn=False):
 box(n+'背板',x,y+d/2,h/2,w,.06,h,'oak')
 for xx in [-w/2,w/2]:box(n+'侧板',x+xx,y,h/2,.06,d,h,'oak')
 for k in range(5):
  zz=.12+k*(h-.16)/4;box(n+'层板',x,y,zz,w,d,.04,'oak')
  if k<4:
   for j in range(5):
    xx=x-w*.39+j*w*.19
    if yarn:sphere(n+'毛线团',xx,y-.015,zz+.16,.18,.20,.18,['cream','sage','rose','blue'][int(j+k)%4])
    else:box(n+'书册',xx,y-.04,zz+.16,.10+random.random()*.035,.20,.26+random.random()*.07,['cream','sage','dark','rose'][int(j+k)%4])
 if yarn:box(n+'玻璃柜门',x,y-d/2-.02,h/2,w,.03,h,'glass')
def plant(n,x,y,s=1,z=0):
 cyl(n+'花盆',x,y,z+.23*s,.23*s,.46*s,'terracotta')
 cyl(n+'枝干',x,y,z+.64*s,.025*s,.88*s,'walnut')
 for i in range(7):
  a=i*2.4;rr=.18*s
  sphere(n+'叶簇',x+math.cos(a)*rr,y+math.sin(a)*rr,z+(.64+i*.085)*s,.4*s,.29*s,.35*s,'leaf' if i%2 else 'leaflight')
def sofa(n,x,y,w=2.4):
 box(n+'底座',x,y,.23,w,.90,.35,'oak')
 for dx in [-w/3,0,w/3]:box(n+'坐垫',x+dx,y-.06,.47,w/3-.04,.79,.20,'cream')
 box(n+'靠背',x,y+.40,.72,w,.19,.64,'cream')
 for xx in [-1,1]:box(n+'扶手',x+xx*(w/2-.09),y,.62,.18,.92,.43,'cream')
def toilet(n,x,y):
 box(n+'水箱',x,y+.24,.58,.40,.22,.69,'white')
 sphere(n+'坐便器',x,y,.31,.44,.64,.57,'white');sphere(n+'坐圈',x,y-.07,.52,.37,.47,.06,'stone')
def bath(n,x0,y0,x1,y1):
 w=x1-x0;d=y1-y0
 box(n+'淋浴地盘',x0+.65,y1-.7,.035,1.12,1.17,.06,'tile')
 box(n+'淋浴玻璃',x0+1.22,y1-.7,1.03,.035,1.3,2.05,'glass','wall-high')
 cyl(n+'花洒杆',x0+.17,y1-.6,1.23,.018,1.65,'metal')
 box(n+'顶喷',x0+.37,y1-.6,2.08,.43,.26,.035,'metal')
 toilet(n,x1-.56,y1-.55)
 box(n+'台盆柜',x1-.52,y0+.63,.42,.68,.95,.78,'oaklight')
 box(n+'台面',x1-.52,y0+.63,.85,.77,1.03,.08,'stone')
 box(n+'面盆',x1-.52,y0+.63,.91,.47,.60,.035,'water')
def desk(n,x,y,w=1.8,trading=False):
 table(n,x,y,w,.80)
 chair(n+'座椅',x,y-.73,0,'dark' if trading else 'sage')
 if trading:
  for k in [-1,0,1]:
   xx=x+k*.56;cyl(n+'支架',xx,y+.12,1.02,.018,.49,'metal')
   box(n+'显示器边框',xx,y+.17,1.20,.57,.07,.37,'dark')
   box(n+'屏幕',xx,y+.127,1.20,.52,.012,.32,'screen')
   for j in range(13):
    zz=1.12+.06*math.sin(j*.7+k)+j*.004
    box(n+'行情',xx-.23+j*.037,y+.118,zz,.012,.008,.035+random.random()*.03,'chartup' if j%3 else 'chartdown')
  box(n+'键盘',x,y-.18,.829,.52,.18,.025,'dark')
  box(n+'鼠标',x+.39,y-.17,.84,.075,.13,.04,'dark')
 else:
  box(n+'电脑',x,y+.19,1.1,.55,.05,.34,'dark')
  box(n+'电脑屏',x,y+.155,1.1,.50,.012,.29,'screen')

def shell_wall(n,axis,coord,a,b,openings=(),th=.16):
 """Opening entries {a,b,type:'door'|'window',bottom,top}. Split at real voids."""
 cuts=sorted(set([a,b]+[v for q in openings for v in [q['a'],q['b']] if a<v<b]))
 for aa,bb in zip(cuts[:-1],cuts[1:]):
  mid=(aa+bb)/2;op=next((q for q in openings if q['a']<=mid<=q['b']),None)
  intervals=[(0,3.0)] if not op else ([(0,op.get('bottom',.86)),(op.get('top',2.55),3.0)] if op.get('type')=='window' else [(2.25,3.0)])
  for bot,top in intervals:
   for lo,hi in [(bot,min(top,.88)),(max(bot,.88),top)]:
    if hi-lo<.002:continue
    cat='wall-low' if hi<=.88 else 'wall-high'
    x,y=((aa+bb)/2,coord) if axis=='x' else (coord,(aa+bb)/2)
    dx,dy=(bb-aa,th) if axis=='x' else (th,bb-aa)
    box(n,x,y,(lo+hi)/2,dx,dy,hi-lo,'plaster',cat)
  if op and op.get('type')=='window':
   bot=op.get('bottom',.86);top=op.get('top',2.55)
   x,y=((aa+bb)/2,coord) if axis=='x' else (coord,(aa+bb)/2)
   dx,dy=(bb-aa,.035) if axis=='x' else (.035,bb-aa)
   box(n+'玻璃',x,y,(bot+top)/2,dx,dy,top-bot,'glass','glazing')
   for zz in [bot,top]:box(n+'窗框',x,y,zz,dx+.05,dy+.05,.055,'dark','glazing')
   for p in [aa,bb]:
    xx,yy=(p,coord) if axis=='x' else (coord,p)
    box(n+'竖窗框',xx,yy,(bot+top)/2,.05,.05,top-bot,'dark','glazing')
  elif op and op.get('type')=='door':
   # Flat oak threshold and jambs; no door leaf blocks an actual route in cutaway.
   x,y=((aa+bb)/2,coord) if axis=='x' else (coord,(aa+bb)/2)
   dx,dy=(bb-aa,.17) if axis=='x' else (.17,bb-aa)
   box(n+'门槛标识',x,y,.016,dx,dy,.018,'oaklight','furniture')
   for p in [aa,bb]:
    xx,yy=(p,coord) if axis=='x' else (coord,p)
    box(n+'门套',xx,yy,1.14,.07,.07,2.28,'oak','wall-high')

def stairs():
 # 20 risers: 9 treads + landing per flight; 0.16m rise, 0.27m going.
 riser=.16;run=.27
 box('楼梯楼层平台',1.70,4.40,-.01,3.0,1.10,.10,'tile','stair')
 for i in range(9):
  yy=3.715-i*run;z=(i+1)*riser
  box('上行第一跑',2.45,yy,z/2,1.20,run+.008,z,'oaklight','stair')
 box('半层平台',1.70,.82,1.6-.10,2.7,1.20,.20,'oaklight','stair')
 for i in range(9):
  yy=1.555+i*run;z=1.6+(i+1)*riser
  box('上行第二跑',.95,yy,z-.09,1.20,run+.008,.18,'oaklight','stair')
 box('到达上层平台',1.70,4.40,3.1,3.0,1.10,.20,'oaklight','stair')
 angle=math.atan(.16/.27)
 for xx in [.5,1.40]:add('上跑支承梁','box',(xx,2.635,2.24),(.13,2.825,.22),'oak','stair',(angle,0,0))
 # Discrete inner guard posts and rails that show the route without a solid obstruction.
 for i in range(9):
  z=(i+1)*riser;yy=3.715-i*run
  cyl('楼梯内扶手立柱',1.86,yy,z+.48,.018,.96,'metal','stair')
  z2=1.6+(i+1)*riser;yy2=1.555+i*run
  cyl('返跑扶手立柱',1.54,yy2,z2+.48,.018,.96,'metal','stair')
 add('第一跑连续扶手','box',(1.86,2.635,1.76),(.05,2.55,.05),'oak','stair',(-angle,0,0))
 add('第二跑连续扶手','box',(1.54,2.635,3.36),(.05,2.55,.05),'oak','stair',(angle,0,0))
def floor_slab():
 # Slab split around stairs and lift shafts. Holes remain real mesh voids.
 if F==0:box('首层地坪',4.8,7.45,-.14,9.6,14.9,.28,'stone','slab')
 else:
  box('主体楼板',4.8,9.925,-.12,9.6,9.95,.24,'stone','slab')
  box('前右楼板',7.5,2.475,-.12,4.2,4.95,.24,'stone','slab')
  box('候梯与平台楼板',4.3,3.675,-.12,2.2,2.55,.24,'stone','slab')
  box('前边梁',2.7,.10,-.12,5.4,.20,.24,'stone','slab')
  box('楼梯左边梁',.10,2.575,-.12,.20,4.75,.24,'stone','slab')

def transform_new(idx,x,y,angle):
 for o in O[idx:]:
  u,v=o['position'][0]-x,o['position'][1]-y
  o['position'][0]=round(x+u*math.cos(angle)-v*math.sin(angle),4)
  o['position'][1]=round(y+u*math.sin(angle)+v*math.cos(angle),4)
  o['rotation'][2]+=angle

def furnishings(room):
 n=room['name'];rid=room['id']
 for f in room.get('furniture',[]):
  x0,y0,x1,y1=f['rect'];x=(x0+x1)/2;y=(y0+y1)/2;w=x1-x0;d=y1-y0;k=f['kind'];idx=len(O)
  if k in ['double_bed','bed']:
   side=f.get('headboard_wall','back');bed(n,x,y,d if side in ['left','right'] else w,'sage' if rid in ['parents','couple'] else ('rose' if rid=='sister' else 'blue'))
   if side in ['left','right']:transform_new(idx,x,y,math.pi/2 if side=='left' else -math.pi/2)
  elif k=='trading_desk':desk(n,x,y,d,True);transform_new(idx,x,y,-math.pi/2)
  elif k=='desk':desk(n,x,y,w,False)
  elif k in ['chair','nightstand']:continue
  elif k=='dining_table':
   table(n,x,y,w,d)
   for dx in [-.62,0,.62]:chair('餐椅',x+dx,y-.79);chair('餐椅',x+dx,y+.79,math.pi)
  elif k=='worktable':
   table('毛线工作台',x,y,w,d);chair('妈妈工作椅',x,y-.76)
   box('编织作品',x-.1,y,.817,.62,.37,.025,'rose')
   for j in range(4):sphere('工作台毛线',x+.55,y-.13+j*.11,.88,.13,.13,.13,['sage','cream','blue','rose'][j])
  elif k=='calligraphy_table':
   table('书法长案',x,y,d,w,.78,'walnut');transform_new(idx,x,y,math.pi/2)
   box('宣纸',x,y,.838,.79,1.52,.008,'paper')
   for i in range(5):
    box('墨迹意向',x-.19+(i%2)*.24,y-.49+i*.22,.846,.035,.16,.004,'dark',rz=(-.3+i*.21))
   box('砚台',x+.33,y-.73,.87,.17,.23,.045,'dark')
   cyl('笔筒',x-.32,y+.84,.93,.06,.24,'oak')
   for i in range(5):cyl('毛笔',x-.35+i*.015,y+.84,1.09,.005,.25,'walnut')
   cyl('书法圆凳',x,y-1.44,.45,.23,.12,'oak');cyl('圆凳脚',x,y-1.44,.23,.05,.43,'oak')
  elif k=='sofa':sofa(n,x,y,w)
  elif k=='coffee_table':table(n,x,y,w,d,.4,'oaklight');cyl('茶盘',x,y,.48,.19,.03,'walnut')
  elif k=='media_console':
   cabinet('电视矮柜',x,y,w,d,.47,'oaklight',True)
   box('电视落地背板',x,y+.1,1.14,2.20,.11,1.38,'oak')
   box('电视',x,y+.18,1.22,1.62,.04,.86,'dark')
  elif k in ['wardrobe','cabinet','linen','pantry']:
   cabinet(n,x,y,w if w>d else d,min(w,d),2.23,'oaklight')
   if w<d:transform_new(idx,x,y,math.pi/2 if x<4.8 else -math.pi/2)
  elif k in ['bookshelf','bookcase','yarn_closed_cabinets']:
   shelf(n,x,y,max(w,d),min(w,d),1.95,k=='yarn_closed_cabinets')
   if w<d:transform_new(idx,x,y,math.pi/2 if x<4.8 else -math.pi/2)
  elif k in ['sideboard','dresser','flat_paper_drawers']:
   cabinet(n,x,y,max(w,d),min(w,d),.9,'oaklight',True)
   if w<d:transform_new(idx,x,y,math.pi/2 if x<4.8 else -math.pi/2)
  elif k in ['armchair','lounge_chair']:
   chair(n,x,y,math.pi/4,'cream');box(n+'软坐垫',x,y,.47,.56,.53,.14,'sage')
  elif k in ['bench','reading_bench']:box(n+'长凳基座',x,y,.23,w,d,.4,'oak');box(n+'长凳坐垫',x,y,.47,w-.03,d-.03,.10,'sage')
  elif k=='fridge':
   box('冰箱',x,y,1.04,w,d,2.06,'metal');box('冰箱门缝',x,y+d/2+.01,1.12,w-.03,.01,.02,'dark')
  elif k=='kitchen_counter':
   box('中厨地柜',x,y,.44,w,d,.85,'oaklight');box('石材操作面',x,y,.89,w+.025,d,.055,'stone')
   box('双槽水盆',x,y0+.55,.924,.45,.65,.015,'metal');box('盆内',x,y0+.55,.933,.35,.51,.009,'water')
   box('灶台',x,y1-.65,.926,.53,.75,.015,'dark')
   for dy in [-.18,.18]:cyl('炉头',x,y1-.65+dy,.947,.14,.015,'metal')
   box('油烟机',x,y1-.65,1.88,.55,.80,.20,'metal','wall-high')
   k0=len(O);cabinet('吊柜',x,y0+.65,.51,1.10,.7,'oaklight')
   for o in O[k0:]:o['position'][2]+=1.55;o['category']='wall-high'
  elif k in ['utility_sink','vanity','brush_wash_station']:
   box(n+'台柜',x,y,.4,w,d,.79,'oaklight');box(n+'台面',x,y,.83,w+.015,d+.015,.06,'stone')
   if k!='brush_wash_station':box(n+'盆',x,y,.87,min(w-.1,.56),min(d-.1,.44),.025,'metal')
   else:cyl('移动洗笔盆',x,y,.93,.17,.16,'white')
  elif k=='washer_dryer':
   for yy in [y-.38,y+.38]:
    box('洗烘设备',x,yy,.46,w,.68,.90,'white')
    o=cyl('设备圆门',x+w/2+.01,yy,.47,.22,.025,'metal');o['rotation']=[0,math.pi/2,0]
    o=cyl('设备玻璃门',x+w/2+.035,yy,.47,.16,.026,'dark');o['rotation']=[0,math.pi/2,0]
  elif k=='toilet':toilet(n,x,y)
  elif k=='shower':
   box(n+'淋浴底盘',x,y,.036,w,d,.055,'tile')
   box(n+'玻璃隔屏',x1,y,1.05,.025,d,2.1,'glass','wall-high')
   cyl(n+'花洒立杆',x0+.11,y,1.25,.014,1.65,'metal')
   box(n+'顶喷',x0+.28,y,2.09,.35,.28,.03,'metal')

def walls_for_floor(fl):
 segs={};ops={}
 def wall(axis,c,a,b):
  key=(axis,round(c,3));segs.setdefault(key,[]).append((a,b))
 def opening(axis,c,q):ops.setdefault((axis,round(c,3)),[]).append(q)
 for r in fl['rooms']:
  x0,y0,x1,y1=r['rect'];edges={'left':('y',x0-.1,y0-.1,y1+.1),'right':('y',x1+.1,y0-.1,y1+.1),'front':('x',y0-.1,x0-.1,x1+.1),'back':('x',y1+.1,x0-.1,x1+.1)}
  for side,e in edges.items():
   if r.get('open_to_corridor') and side=='left':continue
   if F==0 and ((r['id']=='dining' and side=='back') or (r['id']=='living' and side=='front')):continue
   if r['id']=='foyer' and side=='left':continue
   wall(*e)
  for typ,q in [('door',r.get('door')),('garden_door',r.get('garden_door'))]+[('window',q) for q in r.get('windows',[])]:
   if not q:continue
   axis,c,a,b=edges[q['wall']];oa,ob=q['range']
   opening(axis,c,{'a':oa,'b':ob,'type':'window' if typ in ['window','garden_door'] else 'door','bottom':0 if typ=='garden_door' else .85,'top':2.45})
 # Perimeter and service core; no party-wall exterior windows.
 for e in [('y',.1,.1,14.8),('y',9.5,.1,14.8),('x',.1,.1,9.5),('x',14.8,.1,9.5),('y',3.3,.1,5.05),('x',5.05,.1,3.3),('x',2.3,3.3,5.5),('y',5.5,.1,2.3)]:wall(*e)
 opening('y',3.3,{'a':3.95,'b':4.85,'type':'door'})
 opening('x',2.3,{'a':3.85,'b':4.95,'type':'door'})
 opening('x',.1,{'a':.55,'b':2.95,'type':'window','bottom':1.15,'top':2.55})
 if F==0:opening('x',5.05,{'a':7.4,'b':8.4,'type':'door'})
 for (axis,c),intervals in segs.items():
  intervals.sort();merged=[]
  for a,b in intervals:
   if merged and a<=merged[-1][1]+.005:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
   else:merged.append((a,b))
  for a,b in merged:shell_wall('概念隔墙',axis,c,a,b,ops.get((axis,c),[]),.20)

def main():
 global F
 layout=json.loads((R/'layout_proposal.json').read_text())
 short={'foyer':'玄关','kitchen':'中厨','bath1':'首层公卫','utility1':'家务储藏','dining':'餐厅','yarn':'毛线工作室','living':'客厅','trading':'爸爸操盘房','laundry':'洗烘家政','parents_bath':'父母卫浴','family_landing':'阅读与收纳','sister_bath':'妹妹卫浴','parents':'父母卧室','sister':'妹妹卧室','couple':'夫妻主卧','bath3':'公卫','child_storage':'儿童储藏','couple_dressing':'衣帽区','couple_bath':'主卫','child':'儿童预留房','calligraphy':'书法房'}
 for fl in layout['floors']:
  F=fl['level']-1;floor_slab();walls_for_floor(fl)
  box('走廊地面',4.9,9.83,.012,1.3,9.73,.024,'tile','floor-finish')
  box('候梯厅地面',4.45,3.63,.012,2.15,2.65,.024,'tile','floor-finish')
  box('楼层平台饰面',1.70,4.40,.013,3,1.1,.026,'tile','floor-finish')
  if F<2:stairs()
  # Lift cage intentionally diagrammatic, separately readable from the stair.
  box('拟设电梯平台',4.4,1.2,.055,1.73,1.73,.11,'metal','lift')
  box('电梯后壁',4.4,.34,1.13,1.73,.035,2.15,'glass','wall-high')
  for xx in [3.55,5.25]:box('电梯侧壁',xx,1.2,1.13,.035,1.73,2.15,'glass','wall-high')
  box('电梯示意门',4.4,2.22,1.07,1.03,.035,2.08,'glass','wall-high')
  label('拟设电梯',4.4,1.2,.13,1.50)
  label('楼梯',1.7,4.44,.08,1.2)
  if F==2:
   for yy in [1,2.2,3.4]:cyl('顶层楼梯洞口护栏',3.08,yy,.53,.018,1.05,'metal','stair')
   box('顶层洞口扶手',3.08,2.05,1.08,.045,3.48,.045,'oak','stair')
   for xx in [1.72,2.30,2.95]:cyl('平台洞口护栏',xx,3.86,.53,.018,1.05,'metal','stair')
   box('平台洞口扶手',2.36,3.86,1.08,1.43,.045,.045,'oak','stair')
   box('电梯井顶示意',4.4,1.2,3.02,2,2,.12,'plaster','wall-high')
  for r in fl['rooms']:
   x0,y0,x1,y1=r['rect'];wet=any(k in r['id'] for k in ['bath','laundry','kitchen','utility'])
   box(r['name']+'地面',(x0+x1)/2,(y0+y1)/2,.016,x1-x0,y1-y0,.026,'tile' if wet else 'floor','floor-finish')
   # Fine plank joints provide human scale without image textures.
   if not wet:
    for j in range(int((x1-x0)/.24)):
     xx=x0+(j+1)*.24
     box('木地板拼缝',xx,(y0+y1)/2,.032,.006,y1-y0,.001,'oaklight','floor-finish')
   furnishings(r)
   label(short[r['id']],(x0+x1)/2,y0+.48,.06,min(2.35,(x1-x0)*.85))
  if F==0:
   plant('客厅盆栽',9.03,14.3,.65)
   box('玄关换鞋凳',3.78,2.85,.25,.55,.85,.45,'oak','furniture')
  elif F==1:plant('操盘房绿植',6.05,.73,.56)
  else:
   plant('书法房小绿植',9.05,14.32,.55)
 F=-1
 box('条件式后院露台',4.8,16,-.06,9.2,2.2,.12,'garden','garden')
 for j in range(4):box('露台铺装',4.8,15.05+j*.56,.011,9.2,.015,.012,'tile','garden')
 for i,(x,y) in enumerate([(1,16.55),(2.1,16.55),(3.3,16.45),(6.0,16.5),(7.2,16.5),(8.8,16.5)]):plant('条件式庭院植物',x,y,.65 if i%2 else .9)
 table('换盆台',.64,15.8,.65,1.1,.8,'oaklight')
 label('条件式植物庭院',5.0,15.45,.04,3.2)
 data={'meta':{'width':9.6,'depth':14.9,'floor_height':3.2,'title':'家庭住宅三维概念 V1','assumptions':layout['assumptions']},'materials':M,'objects':O}
 (R/'scene.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
 print(f'{len(O)} primitive objects; scene.json {(R/"scene.json").stat().st_size} bytes')
 return data

if __name__=='__main__':
 main()
