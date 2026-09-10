"""Read-only verification of the saved Blender delivery against its source data."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import bpy

root=Path(__file__).resolve().parents[1]
source=root/'unit6-professional-scene.json'
data=json.loads(source.read_text())
floors={f['id']:f['elevation'] for f in data['walkthrough']['floors']}
scene=bpy.data.scenes['00_整栋_完整墙体']
objects=defaultdict(list)
for obj in scene.objects:
    if obj.get('model_source')==source.name:
        objects[(obj.get('source_name'),*(round(v,4) for v in obj.location))].append(obj)
checked=0
attributes=0
for item in data['objects']:
    if item.get('walkthroughRole')=='elevator-generated':
        continue
    floor=item.get('floor')
    base=floors.get(floor,data['meta']['roof_elevation'] if floor=='roof' else item.get('level_elevation',0))
    p=list(item['position']);p[2]+=base
    key=(item['name'],*(round(v,4) for v in p))
    candidates=objects.get(key,[])
    assert candidates, ('Missing or shifted source object',key)
    obj=candidates.pop()
    for field in ['geometryStatus','source','verticalSource']:
        if field in item:
            value=item[field]
            expected=json.dumps(value,ensure_ascii=False) if isinstance(value,(list,dict)) else str(value)
            assert obj.get(field)==expected, (item['name'],field)
            attributes+=1
    checked+=1
report={'passed':True,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'matchedSourceObjects':checked,'sourceAttributesChecked':attributes,'scenes':len(bpy.data.scenes),'defaultScene':scene.name}
(root/'qa'/'professional-model-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('PROFESSIONAL_MODEL_VALIDATED',json.dumps(report,ensure_ascii=False))
