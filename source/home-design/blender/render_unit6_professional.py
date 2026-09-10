"""Build the evidence-preserving model, then render the configured real-model views."""
import argparse
import hashlib
import json
import math
import runpy
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--scene',type=Path,default=ROOT/'unit6-professional-scene.json')
parser.add_argument('--cameras',type=Path,default=ROOT/'unit6-professional-cameras.json')
parser.add_argument('--out',type=Path,default=ROOT.parent/'output'/'unit6-professional')
parser.add_argument('--samples',type=int,default=40)
parser.add_argument('--only',nargs='*',default=None)
parser.add_argument('--reuse-blend',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
source_hash=hashlib.sha256(args.scene.read_bytes()).hexdigest()
images=args.out/'图册'/'images';images.mkdir(parents=True,exist_ok=True)
model=args.out/'模型';model.mkdir(parents=True,exist_ok=True)
if args.reuse_blend:
    bpy.ops.wm.open_mainfile(filepath=str(model/'第6户_三层住宅.blend'))
else:
    sys.argv=['Blender','--','--scene',str(args.scene),'--out',str(model),'--skip-render','--samples',str(args.samples)]
    runpy.run_path(str(ROOT/'build_unit6_blender.py'),run_name='__main__')
record=json.loads(args.cameras.read_text())
full=bpy.data.scenes['00_整栋_完整墙体']
cut_scenes={i:next(sc for sc in bpy.data.scenes if sc.name.startswith(f'{i+1:02d}_')) for i in range(3)}
manifest=[]
for view in record['views']:
    scene=full if view['mode']=='full' else cut_scenes[view['floor']]
    name='专业图册_'+view['id']+'_'+view['title']
    camera=bpy.data.objects.get(name)
    if not camera:
        camera=bpy.data.objects.new(name,bpy.data.cameras.new(name));scene.collection.objects.link(camera)
    camera.location=view['position']
    direction=Vector(view['target'])-camera.location
    camera.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
    if abs(direction.x)<1e-8 and abs(direction.y)<1e-8:
        camera.rotation_euler=(0,0,0) # camera -Z looks down; image top is true +Y
    camera.data.type=view.get('cameraType','PERSP')
    camera.data.clip_start=.035;camera.data.clip_end=400
    camera.data.lens=view.get('lens',24)
    if camera.data.type=='ORTHO':camera.data.ortho_scale=view['orthoScale']
    camera['view_notes']=json.dumps(view,ensure_ascii=False)
    scene.camera=camera
    scene.cycles.samples=args.samples;scene.cycles.use_denoising=True
    scene.render.resolution_x,scene.render.resolution_y=view.get('resolution',[1600,1100])
    scene.render.resolution_percentage=100
    destination=images/f'{view["id"]}_{view["title"]}.png'
    scene.render.filepath=str(destination)
    if view['mode']=='cut':
        description='剖去上部墙体后的楼层俯视，展示实际模型内的房间与家具布置。'
    elif view['id'] in ('20','21'):
        description='南院完成面为-0.40m；相机眼高为绝对1.25m，展示休憩种植与连接南廊的坡道。'
    elif view['id'] in ('18','19'):
        description='三层退台与室内工作区；露台6.87m完成面为展示假设，待建筑节点深化。'
    elif view.get('eyeHeight'):
        description='完整墙体下的'+view.get('room','室内')+'视角，相机位于地面以上1.65m。'
    else:
        description='模型完整三层体量、真实退台与南院位置；保留屋面孔洞，不封填院落外的下沉空间。'
    manifest.append({**view,'image':str(destination.relative_to(args.out/'图册')),'file':str(destination.resolve()),'description':description})
    if args.only is None or view['id'] in args.only:
        bpy.context.window.scene=scene
        print('PROFESSIONAL_RENDER',view['id'],view['title'],flush=True)
        bpy.ops.render.render(write_still=True,scene=scene.name)
full.camera=bpy.data.objects.get('专业图册_06_客厅望向餐厅与中央电梯') or full.camera
bpy.context.window.scene=full
bpy.ops.wm.save_as_mainfile(filepath=str(model/'第6户_三层住宅.blend'),compress=True)
(args.out/'图册'/'视角清单.json').write_text(json.dumps({'scene':args.scene.name,'scene_sha256':source_hash,'views':manifest},ensure_ascii=False,indent=2))
print('PROFESSIONAL_RENDER_COMPLETE',len(manifest),flush=True)
