from pathlib import Path
import json,math,hashlib,sys,itertools
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tmp/geometry-libs'))
from shapely.geometry import Polygon,MultiPoint,Point
from shapely.ops import unary_union
out=Path(__file__).parent;raw=(R/'blender/unit6-professional-scene.json').read_bytes();d=json.loads(raw);src=json.load(open(R/'blender/unit6-landscape-source.json'));z={q['id']:q for q in src['zones']};items=json.load(open(out/'方案点位与定制清单.json'))['gardenItems'];ids=[q['id'] for q in items]
chair=0;groups={};softnames=['叶','花瓣','花心','枝','香草冠']
def classify(o):
 global chair
 n=o['name']
 if n.startswith('G1-C01'):
  if '坐垫' in n:chair+=1
  return 'G1-C01#'+str(chair)
 for gid in ids:
  if n.startswith(gid):return gid
 if n.startswith(('换盆台支架','换盆台下层','换盆工具桶')):return 'G3-W01'
 if n.startswith(('新增南院模块坡道','坡道扶手')):return 'G1-R01'
 if n.startswith('南院茶桌果盘'):return 'G1-T01'
 return None
def geometry(o):
 pos=o['position'];sx,sy,sz=o['size'];rx,ry,rz=o.get('rotation',[0,0,0]);cx,snx,cy,sny,cz,snz=math.cos(rx),math.sin(rx),math.cos(ry),math.sin(ry),math.cos(rz),math.sin(rz)
 mat=[[cy*cz,-cy*snz,sny],[cx*snz+snx*sny*cz,cx*cz-snx*sny*snz,-snx*cy],[snx*snz-cx*sny*cz,snx*cz+cx*sny*snz,cx*cy]]
 if o['kind']=='mesh':
  vv=[[v[i]+pos[i] for i in range(3)] for v in o['vertices']];ps=[]
  for f in o['faces']:
   p=Polygon([(vv[i][0],vv[i][1]) for i in f])
   if p.is_valid and p.area>1e-10:ps.append(p)
  poly=unary_union(ps)
 else:
  if o['kind'] in ['cylinder','sphere'] and abs(rx)+abs(ry)<1e-9:
   coords=[(math.cos(i*math.tau/128)*sx/2,math.sin(i*math.tau/128)*sy/2) for i in range(128)]
   poly=Polygon([(pos[0]+xx*cz-yy*snz,pos[1]+xx*snz+yy*cz) for xx,yy in coords]);vv=[[0,0,pos[2]-sz/2],[0,0,pos[2]+sz/2]]
  else:
   vv=[[pos[i]+sum(mat[i][j]*v[j] for j in range(3)) for i in range(3)] for v in itertools.product([-sx/2,sx/2],[-sy/2,sy/2],[-sz/2,sz/2])];poly=MultiPoint([(v[0],v[1]) for v in vv]).convex_hull
 return poly,[min(v[2] for v in vv),max(v[2] for v in vv)]
for i,o in enumerate(d['objects']):
 gid=classify(o)
 if not gid:continue
 p,zz=geometry(o);groups.setdefault(gid,[]).append(dict(index=i,name=o['name'],floor=o['floor'],poly=p,z=zz,soft=any(k in o['name'] for k in softnames)))
court=Polygon(z['south_courtyard']['polygon']);terrace=Polygon(z['third_floor_terrace']['polygon']);rampallow=unary_union([court,Polygon(z['south_main_steps']['polygon']),Polygon(z['south_main_porch']['polygon'])]);report={'sceneSha256':hashlib.sha256(raw).hexdigest(),'inventoryGroups':len(ids),'physicalInstances':len(groups),'method':'actual object part polygons, 128-point ellipse for round parts; Euler rotation for boxes; mesh face projection union; chairs checked as 4 separate physical instances','groups':[],'betweenGroupPlanOverlaps':[],'hardCollisions':[]}
for gid,ps in groups.items():
 floor=ps[0]['floor'];allow=rampallow if gid=='G1-R01' else terrace if floor==2 else court
 full=unary_union([p['poly'] for p in ps]);hard=unary_union([p['poly'] for p in ps if not p['soft']]);outside=full.difference(allow)
 report['groups'].append({'id':gid,'inventoryId':gid.split('#')[0],'floor':floor+1,'parts':len(ps),'bounds':list(full.bounds),'visualOutsideAllowedM2':outside.area,'hardOutsideAllowedM2':hard.difference(allow).area,'outsideParts':[p['name'] for p in ps if p['poly'].difference(allow).area>1e-7],'polygon':list(full.exterior.coords) if full.geom_type=='Polygon' else None})
keys=list(groups)
for i,a in enumerate(keys):
 for b in keys[i+1:]:
  if groups[a][0]['floor']!=groups[b][0]['floor']:continue
  fa=unary_union([p['poly'] for p in groups[a]]);fb=unary_union([p['poly'] for p in groups[b]]);area=fa.intersection(fb).area
  if area>1e-7:report['betweenGroupPlanOverlaps'].append({'a':a,'b':b,'visualPlanOverlapM2':area})
  for pa in groups[a]:
   if pa['soft']:continue
   for pb in groups[b]:
    if pb['soft']:continue
    dz=min(pa['z'][1],pb['z'][1])-max(pa['z'][0],pb['z'][0]);over=pa['poly'].intersection(pb['poly']).area
    if dz>.001 and over>1e-7:report['hardCollisions'].append({'a':a,'b':b,'partA':pa['name'],'partB':pb['name'],'overlapM2':over,'heightOverlapM':dz})
report['allWithin']=all(g['visualOutsideAllowedM2']<1e-7 for g in report['groups']);report['noHardCollisions']=not report['hardCollisions'];report['noBetweenGroupPlanOverlaps']=not report['betweenGroupPlanOverlaps'];report['limits']=['不同组的平面投影相交与实体硬相交分开报告，避免把允许的上下错层误称穿模。','同组零件装配/花卉自身重叠不作为组间碰撞。','边界采用源图设计面；仅坡道允许落在原中踏步及南廊衔接内。','本项未认证结构荷载、护栏安全、可攀爬性或柜门动态开启净空。']
navpath=out/'P02房间与花园通达检查.json'
if navpath.exists() and json.load(open(navpath))['sceneSha256']==report['sceneSha256']:
 grids={f:json.load(open(out/f'P02网格_F{f+1}.json')) for f in [0,2]}
 for g in report['groups']:
  fid=g['floor']-1;gr=grids[fid];shape=unary_union([p['poly'] for p in groups[g['id']]])
  targets=[]
  for idx,reached in enumerate(gr['seen']):
   if not reached:continue
   x=gr['xmin']+(idx%gr['nx'])*gr['step'];y=gr['ymin']+(idx//gr['nx'])*gr['step'];dist=shape.distance(Point(x,y))
   if (.23<=dist<=.85) or (g['id']=='G1-R01' and shape.contains(Point(x,y))):targets.append((dist,x,y))
  targets.sort();g['reachableApproachPoint']=[round(v,3) for v in targets[0][1:]] if targets else None;g['reachableApproachCount']=len(targets)
 report['allAssembliesApproachable']=all(g['reachableApproachPoint'] is not None for g in report['groups']);report['approachMethod']='reachable canStep grid point 0.23..0.85m outside actual group projection; ramp also permits reachable on-deck point'
else:report['allAssembliesApproachable']=None
(out/'P02园林组检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='groups'},ensure_ascii=False,indent=2));print('out-of-bounds',[(g['id'],g['visualOutsideAllowedM2'],g['outsideParts']) for g in report['groups'] if g['visualOutsideAllowedM2']>1e-7])
