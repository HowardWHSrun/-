from pathlib import Path
import json,sys,math,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tmp/geometry-libs'))
from shapely.geometry import Polygon
from shapely.ops import unary_union
raw=(R/'blender/unit6-professional-scene.json').read_bytes();d=json.loads(raw);out=Path(__file__).parent
prefixes={'sofa':['家庭沙发'],'coffee_table':['茶几'],'tv':['电视'],'sideboard':['餐边收纳'],'reading_chair':['窗边阅读椅']}
def group(o):
 for g,p in prefixes.items():
  if any(o['name'].startswith(s) for s in p):return g
 return None
def poly(o):
 x,y,z=o['position'];w,l,h=o['size'];a=o['rotation'][2];c,s=math.cos(a),math.sin(a)
 pts=[(math.cos(i*math.tau/128)*w/2,math.sin(i*math.tau/128)*l/2) for i in range(128)] if o['kind']=='cylinder' else [(-w/2,-l/2),(w/2,-l/2),(w/2,l/2),(-w/2,l/2)]
 return Polygon([(x+xx*c-yy*s,y+xx*s+yy*c) for xx,yy in pts])
obs=[o for o in d['objects'] if o['floor']==0 and o['kind'] in ['box','cylinder'] and o.get('category') not in ['label','text','ceiling','slab','floor-finish','rug']]
selected=[o for o in obs if group(o)];targets=[o for o in obs if o.get('category') in ['wall','wall-low','wall-high','column','furniture','glazing']]
collisions=[]
for a in selected:
 for b in targets:
  if a is b or group(a)==group(b):continue
  za=a['position'][2];ha=a['size'][2];zb=b['position'][2];hb=b['size'][2]
  dz=min(za+ha/2,zb+hb/2)-max(za-ha/2,zb-hb/2)
  if dz<=.001:continue
  area=poly(a).intersection(poly(b)).area
  if area>1e-6:collisions.append({'a':a['name'],'b':b['name'],'intersectionM2':area,'heightOverlapM':dz})
groups={g:unary_union([poly(o) for o in selected if group(o)==g]) for g in prefixes}
gaps=[]
keys=list(groups)
for i,g in enumerate(keys):
 for h in keys[i+1:]:gaps.append({'between':[g,h],'planMinimumGapM':groups[g].distance(groups[h])})
report={'sceneSha256':hashlib.sha256(raw).hexdigest(),'method':'upright parts: rotated polygon overlap plus vertical interval; compare changed living-room assemblies against source wall/column/glazing and other furniture; ignore overlap within same assembly','partsChecked':len(selected),'hardCollisions':collisions,'assemblyGaps':gaps,'limits':['投影最小间距不必然位于人行通路，也不代表所有间隙必须可通行。','同一组家具零件之间的相交视作装配接触，不作碰撞缺陷。','本检查不评定抽屉/柜门动态开启轨迹或家具本体制作节点。']}
(out/'P02客厅家具检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
