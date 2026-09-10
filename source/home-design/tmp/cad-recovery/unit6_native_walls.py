from pathlib import Path
import ezdxf,json,math,collections,logging
from ezdxf import disassemble,bbox,path
logging.disable(logging.CRITICAL)
base=Path('/Users/howardwang/Desktop/Quick Projects/家装/home-design');out=base/'audit/unit6';p=ezdxf.readfile(base/'tmp/cad-recovery/oda-audited/original.dxf')
for fid,y0 in [('F1',725212.6429989272),('F2',647269.5110587726)]:
 ss=json.load(open(out/f'{fid}-segments-local.json'));handles=sorted(set(s['source_handle'] for s in ss if (s['layer'].upper()=='WALL' or s['layer'].upper().endswith('A-WALL') or 'COL' in s['layer'].upper()) and s['source_handle'] in p.entitydb));lines=[];dashed=[];columns=[]
 for h in handles:
  for e in disassemble.recursive_decompose([p.entitydb[h]]):
   l=e.dxf.get('layer','');lu=l.upper();iswall=(lu=='WALL' or lu.endswith('A-WALL')) and 'WALL-TYPE' not in lu;iscol=lu.startswith('0-COL')
   if not(iswall or iscol) or e.dxftype() not in ['LINE','LWPOLYLINE']:continue
   try: vv=[e.dxf.start,e.dxf.end] if e.dxftype()=='LINE' else list(path.make_path(e).flattening(.01))
   except:continue
   vv=[(round((v.x-658498.48)/1000,3),round((v.y-y0)/1000,3)) for v in vv]
   if not vv:continue
   xmn=min(v[0] for v in vv);xmx=max(v[0] for v in vv);ymn=min(v[1] for v in vv);ymx=max(v[1] for v in vv)
   if xmx<-.121 or xmn>9.721 or ymx<.979 or ymn>15.5:continue
   lt=e.dxf.get('linetype','BYLAYER')
   if lt.upper()=='BYLAYER':
    try:lt=p.layers.get(l).dxf.linetype
    except:pass
   hid=any(k in lt.upper() for k in ['HIDDEN','DASH'])
   if iscol and e.dxftype()=='LWPOLYLINE' and e.closed and xmx-xmn>.05 and ymx-ymn>.05 and xmx-xmn<1 and ymx-ymn<1:
    cols={'bounds':[xmn,ymn,xmx,ymx],'polygon':vv,'source':[h],'layers':[l],'role':'column','method':'source closed column polyline bounds','status':'plan_geometry'}
    if xmn>=-.3 and xmx<=9.9:columns.append(cols)
   if iswall:
    for a,b in zip(vv,vv[1:]):
     if abs(a[0]-b[0])<.002 and abs(a[1]-b[1])>.025:q=dict(axis='v',c=a[0],lo=min(a[1],b[1]),hi=max(a[1],b[1]),source=h,layer=l,linetype=lt)
     elif abs(a[1]-b[1])<.002 and abs(a[0]-b[0])>.025:q=dict(axis='h',c=a[1],lo=min(a[0],b[0]),hi=max(a[0],b[0]),source=h,layer=l,linetype=lt)
     else:continue
     (dashed if hid else lines).append(q)
 boxes={}
 for i,a in enumerate(lines):
  for b in lines[i+1:]:
   if a['axis']!=b['axis'] or round(abs(a['c']-b['c']),3) not in [.12,.24]:continue
   lo=max(a['lo'],b['lo']);hi=min(a['hi'],b['hi'])
   if hi-lo<.025:continue
   c0=min(a['c'],b['c']);c1=max(a['c'],b['c']);bounds=[c0,lo,c1,hi] if a['axis']=='v' else [lo,c0,hi,c1]
   if bounds[0]<-.121 or bounds[2]>9.721 or bounds[1]<.97:continue
   boxes[tuple(bounds)]={'bounds':bounds,'source':sorted(set([a['source'],b['source']])),'layers':sorted(set([a['layer'],b['layer']])),'method':'paired native continuous wall skins; 120/240 mm','status':'plan_geometry'}
 bs=list(boxes.values());bs=[a for i,a in enumerate(bs) if not any(i!=j and a['bounds'][0]>=b['bounds'][0] and a['bounds'][1]>=b['bounds'][1] and a['bounds'][2]<=b['bounds'][2] and a['bounds'][3]<=b['bounds'][3] and a['bounds']!=b['bounds'] for j,b in enumerate(bs))]
 (out/f'{fid}-native-wall-boxes.json').write_text(json.dumps(bs,ensure_ascii=False,indent=2));(out/f'{fid}-native-columns.json').write_text(json.dumps(columns,ensure_ascii=False,indent=2));(out/f'{fid}-dashed-wall-references.json').write_text(json.dumps(dashed,ensure_ascii=False,indent=2));(out/f'{fid}-native-wall-lines.json').write_text(json.dumps(lines,ensure_ascii=False,indent=2))
 print(fid,'boxes',len(bs),'columns',len(columns),'dashed',len(dashed),'sourcehandles',handles,flush=True)
