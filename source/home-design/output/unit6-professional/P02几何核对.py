from pathlib import Path
import json,math,collections,sys,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tmp/geometry-libs'))
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
out=Path(__file__).parent
raw=(R/'blender/unit6-professional-scene.json').read_bytes();d=json.loads(raw);old=json.load(open(R/'blender/unit6-scene.json'));src=json.load(open(R/'blender/unit6-landscape-source.json'));z={q['id']:q for q in src['zones']}
# Mesh face projections are unioned, including only non-zero area faces. No bounds-only shortcut.
def footprint(o):
 if o['kind']=='mesh':
  ps=[];vs=o.get('vertices',[]);px,py,_=o['position']
  for face in o.get('faces',[]):
   p=Polygon([(vs[i][0]+px,vs[i][1]+py) for i in face])
   if p.is_valid and p.area>1e-10:ps.append(p)
  return unary_union(ps)
 x,y,_=o['position'];sx,sy,_=o['size'];r=o.get('rotation',[0,0,0])[2];c,s=math.cos(r),math.sin(r)
 return Polygon([(x+dx*c-dy*s,y+dx*s+dy*c) for dx,dy in [(-sx/2,-sy/2),(sx/2,-sy/2),(sx/2,sy/2),(-sx/2,sy/2)]])
def ckey(o):return json.dumps({k:o.get(k) for k in ['name','kind','floor','position','size','rotation','vertices','faces','category','source']},ensure_ascii=False,sort_keys=True)
sourceobjs=lambda os:[o for o in os if o.get('category') in ['wall','wall-low','wall-high','column','parapet']]
a,b=collections.Counter(map(ckey,sourceobjs(old['objects']))),collections.Counter(map(ckey,sourceobjs(d['objects'])))
unchanged={'baselineObjects':sum(a.values()),'newObjects':sum(b.values()),'removedOrChanged':sum((a-b).values()),'added':sum((b-a).values()),'baselineGeometryPreserved':sum((a-b).values())==0,'exactGeometryUnchanged':a==b,'addedObjects':[json.loads(k) for k in (b-a).elements()],'comparison':'name/type/floor/position/size/rotation/mesh/category/source multiset against unit6-scene.json; proposed lift/stair treatment already in baseline'}
court=Polygon(z['south_courtyard']['polygon']);porch=Polygon(z['south_main_porch']['polygon']);steps=Polygon(z['south_main_steps']['polygon']);threshold=box(4.29,3.9,8.91,4.22)
allow=unary_union([court,porch,steps,threshold]);checks=[]
for prefix,allowed in [('原图南院完成面',court),('原图南廊完成面',unary_union([porch,threshold])),('新增南院模块坡道',unary_union([court,steps]))]:
 for o in d['objects']:
  if o['name'].startswith(prefix):
   p=footprint(o);checks.append({'name':o['name'],'projectionArea':p.area,'outsideAllowedArea':p.difference(allowed).area,'geometryWithinSourceOrDeclaredAlteration':p.difference(allowed).area<1e-6,'status':o.get('geometryStatus'),'zRange':[min(v[2] for v in o['vertices']),max(v[2] for v in o['vertices'])]})
finish_checks=[]
for o in d['objects']:
 if o['floor']==0 and o['name'].startswith('南院铺装分缝'):
  p=footprint(o);finish_checks.append({'name':o['name'],'outsideCourtArea':p.difference(court).area})
voids={k:Polygon(z[k]['polygon']) for k in ['south_sunken_void','east_sunken_void']};voidchecks=[]
for fid in [0,1,2]:
 flooros=[o for o in d['objects'] if o['floor']==fid and o['category'] in ['slab','floor-finish']]
 union=unary_union([footprint(o) for o in flooros]);detail=[]
 for key,v in voids.items():
  intrusions=[{'name':o['name'],'area':footprint(o).intersection(v).area} for o in flooros if footprint(o).intersection(v).area>1e-6]
  detail.append({'void':key,'slabProjectionOverlapM2':union.intersection(v).area,'intrusions':intrusions})
 voidchecks.append({'floor':fid+1,'checks':detail})
# Compare walkthrough boundary with the established interior plus newly permitted source surfaces.
orig=Polygon(old['walkthrough']['floors'][0]['boundary']);new=Polygon(d['walkthrough']['floors'][0]['boundary'])
boundary={'outsideOriginalOrNewAllowedM2':new.difference(unary_union([orig,allow])).area,'removedOriginalAreaM2':orig.difference(new).area,'newSouthMinY':new.bounds[1],'southVoidNorthEdge':-4.02,'sourceGardenSouthEdge':-3.78}
ramp=Polygon(d['landscape']['rampPolygon']);p=d['walkthrough']['floors'][0]['surfaces'][0]['profile'];rampinfo={'polygon':d['landscape']['rampPolygon'],'area':ramp.area,'withinCourtM2':ramp.intersection(court).area,'withinOriginalStepsM2':ramp.intersection(steps).area,'outsideCourtAndStepsM2':ramp.difference(unary_union([court,steps])).area,'slopeRiseMeters':abs(p['startElevation']-p['endElevation']),'runMeters':abs(p['start']-p['end']),'slopeRatio':abs(p['start']-p['end'])/abs(p['startElevation']-p['endElevation']),'widthMeters':ramp.bounds[2]-ramp.bounds[0]}
report={'sceneSha256':hashlib.sha256(raw).hexdigest(),'objects':len(d['objects']),'baselineWallColumnParapetComparison':unchanged,'surfaceGeometryChecks':checks,'paverSegmentsChecked':len(finish_checks),'paverOutsideAreaTotal':sum(q['outsideCourtArea'] for q in finish_checks),'voidChecks':voidchecks,'walkthroughBoundary':boundary,'ramp':rampinfo,'limits':['客厅门口连接区[4.29,3.90,8.91,4.22]是新增收口；非原图庭院或产权扩张。','源图结构断面/荷载/坡道审批/无障碍合规未因几何通过而验证。','本次对新增地面与洞口采用精确二维投影并集；家具叶片投影和渲染细节不据此认证为施工净空。']}
(out/'P02几何数据.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
