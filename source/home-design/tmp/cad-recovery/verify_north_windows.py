import ezdxf,json,logging
from ezdxf import disassemble,bbox
from pathlib import Path
logging.disable(logging.CRITICAL)
base=Path('/Users/howardwang/Desktop/Quick Projects/家装/home-design');p=ezdxf.readfile(base/'tmp/cad-recovery/oda-audited/original.dxf');root=p.entitydb['2AC16C'];xorg=608349.1237666766;zorg=995363.0944562624
results=[]
for e in disassemble.recursive_decompose([root]):
 if e.dxftype() not in ['LINE','LWPOLYLINE','POLYLINE','INSERT']:continue
 try:b=bbox.extents([e])
 except:continue
 if not b.has_data:continue
 bb=[(xorg-b.extmax.x)/1000,(b.extmin.y-zorg)/1000,(xorg-b.extmin.x)/1000,(b.extmax.y-zorg)/1000]
 if bb[2]-bb[0]<.7 or bb[3]-bb[1]<.7:continue
 targets=[('HC1012a',[-.1,.9,1.8,2.7]),('HC1212',[5.1,.9,6.9,2.7]),('LPC1915a',[.4,7.4,3.2,9.7]),('LPC1313b',[4.7,7.7,6.7,9.7]),('LPC2622',[4.2,3.8,7.2,6.7])]
 for code,w in targets:
  if bb[0]>w[0] and bb[1]>w[1] and bb[2]<w[2] and bb[3]<w[3]:
   s=e.source_of_copy
   rr={'code':code,'bounds':[round(v,6) for v in bb],'type':e.dxftype(),'layer':e.dxf.layer,'handle':e.dxf.get('handle'),'originalEntityHandle':s.dxf.get('handle') if s else None,'closed':getattr(e,'closed',None)};results.append(rr)
(base/'audit/unit6/vertical/north-window-source-entities.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
for r in results:print(r)
