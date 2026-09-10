import bpy
from pathlib import Path
scene=bpy.data.scenes['00_整栋_完整墙体'];bpy.context.window.scene=scene
cats={'wall','wall-low','wall-high','slab','ceiling','roof','floor-finish','column'}
objects=[o for o in scene.objects if o.type=='MESH' and o.get('category') in cats]
print('UNION_INPUTS',len(objects),flush=True)
col=bpy.data.collections.new('QA_union_operands')
for o in objects[1:]:col.objects.link(o)
base=objects[0].copy();base.data=objects[0].data.copy();scene.collection.objects.link(base)
mod=base.modifiers.new('Exact_union_same_coordinates','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.operand_type='COLLECTION';mod.collection=col;mod.use_self=True
bpy.ops.object.select_all(action='DESELECT');base.select_set(True);bpy.context.view_layer.objects.active=base
bpy.ops.object.modifier_apply(modifier=mod.name)
print('UNION_OUTPUT',len(base.data.vertices),len(base.data.polygons),flush=True)
for o in objects:o.hide_render=True
scene.cycles.samples=12;scene.render.resolution_percentage=60;scene.render.filepath=str(Path(__file__).resolve().parent/'unit-six-union-interior.png')
bpy.ops.render.render(write_still=True,scene=scene.name)
