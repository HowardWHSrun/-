"""Build verified unit-6 geometry. Run Blender --background --python THIS -- [options].

Reads materials/objects plus explicit walkthrough floor datums. No V1 dimensions,
uniform storey height or footprint is inferred. Does not change the input scene.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--scene', type=Path, default=ROOT / 'unit6-scene.json')
parser.add_argument('--out', type=Path, default=ROOT.parent / 'output' / 'unit6')
parser.add_argument('--skip-render', action='store_true')
parser.add_argument('--samples', type=int, default=32)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
D = json.loads(args.scene.read_text())
NAV = D.get('walkthrough', {})
FLOORS = {f['id']: f for f in NAV.get('floors', [])}
if len(FLOORS) != 3 or any('elevation' not in f or not f.get('boundary') for f in FLOORS.values()):
    raise ValueError('Unit-6 requires exactly three explicit floor elevations and actual per-floor boundaries.')
if not NAV.get('spawn') or NAV['spawn']['floor'] not in FLOORS:
    raise ValueError('A verified entry spawn is required for the interior view.')
ORDER = sorted(FLOORS, key=lambda f: FLOORS[f]['elevation'])
META = D.get('meta', {})
args.out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)


def linear(v):
    return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4


def rgb(h):
    return tuple(linear(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))


materials = {}
for name, source in D.get('materials', {}).items():
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    c = rgb(source.get('color', '#d8cfc0'))
    alpha = source.get('alpha', 1)
    mat.diffuse_color = (*c, alpha)
    p = mat.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*c, 1)
    p.inputs['Roughness'].default_value = source.get('roughness', .7)
    p.inputs['Metallic'].default_value = source.get('metallic', 0)
    if alpha < 1:
        p.inputs['Alpha'].default_value = alpha
        p.inputs['Transmission Weight'].default_value = .55
        p.inputs['IOR'].default_value = 1.45
        if hasattr(mat, 'surface_render_method'):
            mat.surface_render_method = 'DITHERED'
    if name in ('oak', 'oaklight', 'walnut', 'floor'):
        nt = mat.node_tree
        coordinates = nt.nodes.new('ShaderNodeTexCoord')
        scale = nt.nodes.new('ShaderNodeVectorMath')
        scale.operation = 'MULTIPLY'
        scale.inputs[1].default_value = (3, 42, 5)
        noise = nt.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 3
        noise.inputs['Detail'].default_value = 2
        bump = nt.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = .10
        bump.inputs['Distance'].default_value = .025
        nt.links.new(coordinates.outputs['Generated'], scale.inputs[0])
        nt.links.new(scale.outputs[0], noise.inputs['Vector'])
        nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], p.inputs['Normal'])
    materials[name] = mat
if not materials:
    raise ValueError('The input scene must provide actual design materials.')
fallback = next(iter(materials.values()))


def base_elevation(source):
    f = source.get('floor')
    if f in FLOORS:
        return FLOORS[f]['elevation']
    if f == 'roof':
        z = META.get('roof_elevation', NAV.get('roof', {}).get('elevation'))
        if z is None:
            raise ValueError('floor:"roof" requires meta.roof_elevation or walkthrough.roof.elevation.')
        return z
    if source.get('coordinateSpace') == 'world':
        return 0
    if 'level_elevation' in source:
        return source['level_elevation']
    raise ValueError(f'Object {source.get("name")} has an undefined floor datum: {f!r}')


def create_mesh(source):
    kind = source['kind']
    sx, sy, sz = source.get('size', [1, 1, 1])
    if kind == 'mesh':
        # Mesh vertices are already metre coordinates relative to position.
        # size is only metadata/bounds and must not scale the geometry again.
        vertices = source['vertices']
        faces = source['faces']
        if not vertices or not faces or any(len(v) != 3 for v in vertices):
            raise ValueError(f'Invalid explicit mesh: {source["name"]}')
        if any(len(face) < 3 or any(i < 0 or i >= len(vertices) for i in face) for face in faces):
            raise ValueError(f'Invalid face indices: {source["name"]}')
    elif kind == 'box':
        vertices = [(x * sx / 2, y * sy / 2, z * sz / 2) for x, y, z in
                    [(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
                     (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)]]
        faces = [(0, 2, 6, 4), (1, 5, 7, 3), (0, 4, 5, 1), (2, 3, 7, 6), (0, 1, 3, 2), (4, 6, 7, 5)]
    elif kind == 'cylinder':
        n = 24
        vertices = [(math.cos(i * math.tau / n) * sx / 2, math.sin(i * math.tau / n) * sy / 2, z * sz / 2)
                    for z in (-1, 1) for i in range(n)]
        faces = [tuple(reversed(range(n))), tuple(range(n, n * 2))] + [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
    elif kind == 'sphere':
        n, rings = 16, 8
        vertices = [(math.sin(math.pi * r / rings) * math.cos(i * math.tau / n) * sx / 2,
                     math.sin(math.pi * r / rings) * math.sin(i * math.tau / n) * sy / 2,
                     math.cos(math.pi * r / rings) * sz / 2) for r in range(rings + 1) for i in range(n)]
        faces = [(r * n + i, r * n + (i + 1) % n, (r + 1) * n + (i + 1) % n, (r + 1) * n + i)
                 for r in range(rings) for i in range(n)]
    else:
        raise ValueError(f'Unsupported geometry kind: {kind}')
    mesh = bpy.data.meshes.new(source['name'])
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(materials.get(source.get('material'), fallback))
    normals = bmesh.new()
    normals.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(normals, faces=list(normals.faces))
    normals.to_mesh(mesh)
    normals.free()
    mesh.update()
    if kind in ('sphere', 'cylinder'):
        for polygon in mesh.polygons:
            polygon.use_smooth = True
    return mesh


def new_collection(name):
    return bpy.data.collections.new(name)


full_collections = {f: new_collection(f'{FLOORS[f].get("label", str(f))}_完整空间') for f in ORDER}
roof_collection = new_collection('屋顶_独立几何')
environment_collection = new_collection('其他经确认的室外几何')
sources = {f: [] for f in ORDER}
font = None
for font_path in ['/System/Library/Fonts/Supplemental/Songti.ttc', '/System/Library/Fonts/PingFang.ttc']:
    if Path(font_path).exists():
        font = bpy.data.fonts.load(font_path)
        break


def add_source(source):
    f = source.get('floor')
    is_roof = f == 'roof' or source.get('category') == 'roof'
    collection = roof_collection if is_roof else full_collections.get(f, environment_collection)
    if source['kind'] == 'text':
        curve = bpy.data.curves.new(source['name'], 'FONT')
        curve.body = source.get('text', source['name'])
        if font:
            curve.font = font
        curve.align_x = 'CENTER'
        curve.align_y = 'CENTER'
        curve.size = min(.23, source.get('size', [2])[0] / max(1, len(curve.body)))
        curve.extrude = .0005
        curve.materials.append(materials.get(source.get('material', 'dark'), fallback))
        obj = bpy.data.objects.new(source['name'], curve)
    else:
        obj = bpy.data.objects.new(source['name'], create_mesh(source))
    collection.objects.link(obj)
    obj.location = source.get('position', [0, 0, 0])
    obj.location.z += base_elevation(source)
    obj.rotation_euler = source.get('rotation', [0, 0, 0])
    obj['floor'] = str(f)
    obj['category'] = source.get('category', '')
    obj['source_name'] = source.get('name', '')
    obj['model_source'] = str(args.scene.name)
    for key in ('geometryStatus', 'source', 'verticalSource'):
        if key in source:
            value = source[key]
            obj[key] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
    if source.get('sourceRef'):
        obj['source_reference'] = json.dumps(source['sourceRef'], ensure_ascii=False)
    if source.get('collision') is False:
        obj['walkthrough_collision'] = False
    if source['kind'] == 'box' and source.get('category') == 'furniture' and min(source.get('size', [0])) > .055:
        bevel = obj.modifiers.new('家具边缘', 'BEVEL')
        bevel.width = min(.02, min(source['size']) / 6)
        bevel.segments = 2
        obj.modifiers.new('家具法线', 'WEIGHTED_NORMAL')
    if f in sources and not is_roof:
        sources[f].append(obj)
    return obj


for i, source in enumerate(D.get('objects', [])):
    if source.get('walkthroughRole') == 'elevator-generated':
        continue
    add_source(source)
    if i % 300 == 0:
        print('SOURCE_OBJECTS', i, flush=True)


def add_elevator_visuals():
    """Matches the viewer's cabin and sliding landing doors, using configured bounds."""
    e = NAV.get('elevator')
    if not e:
        return
    b = e['bounds']
    d = e['door']
    initial = e.get('initialFloor', e['stops'][0])
    horizontal = d['side'] in ('south', 'north')
    low, high = (b[0], b[2]) if horizontal else (b[1], b[3])
    center = d.get('center', (low + high) / 2)
    width = d.get('width', .95)

    def box(f, name, pos, size, mat='oaklight'):
        return add_source({'name': name, 'kind': 'box', 'floor': f, 'position': pos, 'size': size,
                           'material': mat, 'category': 'elevator', 'geometryStatus': '新增电梯设备展示',
                           'source': '与漫游电梯参数一致的轿厢和层门；位置与净空来自输入模型配置'})

    box(initial, '电梯轿厢地板', [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2, -.035], [b[2] - b[0], b[3] - b[1], .07], 'stone')
    roof = box(initial, '电梯轿厢顶板', [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2, 2.32], [b[2] - b[0], b[3] - b[1], .06])
    roof['category'] = 'ceiling'
    walls = []
    if d['side'] != 'south':
        walls.append((b[0], b[1], b[2], b[1]))
    if d['side'] != 'north':
        walls.append((b[0], b[3], b[2], b[3]))
    if d['side'] != 'west':
        walls.append((b[0], b[1], b[0], b[3]))
    if d['side'] != 'east':
        walls.append((b[2], b[1], b[2], b[3]))
    if horizontal:
        y = b[1] if d['side'] == 'south' else b[3]
        walls.extend([(b[0], y, center - width / 2, y), (center + width / 2, y, b[2], y)])
    else:
        x = b[0] if d['side'] == 'west' else b[2]
        walls.extend([(x, b[1], x, center - width / 2), (x, center + width / 2, x, b[3])])
    for index, (x1, y1, x2, y2) in enumerate(walls):
        box(initial, f'电梯轿厢围护{index + 1}', [(x1 + x2) / 2, (y1 + y2) / 2, 1.15], [max(.06, x2 - x1), max(.06, y2 - y1), 2.3])
    for f in e['stops']:
        for side in (-1, 1):
            slide = side * (width / 4 + (width / 2 if f == initial else 0))
            if horizontal:
                pos, size = [center + slide, b[1] if d['side'] == 'south' else b[3], 1.075], [width / 2, .045, 2.15]
            else:
                pos, size = [b[0] if d['side'] == 'west' else b[2], center + slide, 1.075], [.045, width / 2, 2.15]
            box(f, f'电梯{FLOORS[f].get("label", f)}层门{side}', pos, size, 'metal')


add_elevator_visuals()

# Resolve transforms and convert text once, so every saved file is font portable.
assembly = bpy.data.scenes.new('_构建临时场景')
for collection in [*full_collections.values(), roof_collection, environment_collection]:
    assembly.collection.children.link(collection)
bpy.context.window.scene = assembly
bpy.context.view_layer.update()
for obj in list(assembly.objects):
    if obj.type == 'FONT':
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')
bpy.context.view_layer.update()


def clipped_copy(obj, plane_z):
    copy = obj.copy()
    copy.data = obj.data.copy()
    if copy.type != 'MESH':
        return copy
    bm = bmesh.new()
    bm.from_mesh(copy.data)
    matrix = obj.matrix_world.copy()
    bmesh.ops.transform(bm, matrix=matrix, verts=list(bm.verts))
    geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
    bmesh.ops.bisect_plane(bm, geom=geom, dist=.00001, plane_co=(0, 0, plane_z), plane_no=(0, 0, 1), clear_outer=True)
    rim = [edge for edge in bm.edges if edge.is_boundary and all(abs(v.co.z - plane_z) < .0001 for v in edge.verts)]
    if rim:
        bmesh.ops.holes_fill(bm, edges=rim, sides=0)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bmesh.ops.transform(bm, matrix=matrix.inverted(), verts=list(bm.verts))
    bm.to_mesh(copy.data)
    bm.free()
    copy.data.update()
    return copy


cut_collections = {}
architecture = {'wall', 'wall-low', 'wall-high', 'glazing', 'column', 'door', 'elevator', 'railing', 'partition'}
for f in ORDER:
    cut = new_collection(f'{FLOORS[f].get("label", str(f))}_剖开展示副本')
    cut_collections[f] = cut
    for obj in sources[f]:
        category = obj.get('category', '')
        if category in ('ceiling', 'roof'):
            continue
        if category in architecture or category.startswith('wall'):
            copy = clipped_copy(obj, FLOORS[f]['elevation'] + 1.1)
            if copy.type == 'MESH' and not len(copy.data.vertices):
                bpy.data.objects.remove(copy)
                continue
        else:
            copy = obj.copy()
            copy.data = obj.data
        copy.name = '剖开_' + obj.name
        cut.objects.link(copy)

all_xy = [p for f in FLOORS.values() for p in f['boundary']]
min_x, max_x = min(p[0] for p in all_xy), max(p[0] for p in all_xy)
min_y, max_y = min(p[1] for p in all_xy), max(p[1] for p in all_xy)
center_x, center_y = (min_x + max_x) / 2, (min_y + max_y) / 2
span = max(max_x - min_x, max_y - min_y)
highest = max(f['elevation'] for f in FLOORS.values())
geometry_top = max((obj.matrix_world @ Vector(corner)).z for obj in assembly.objects if obj.type == 'MESH' for corner in obj.bound_box)
world = bpy.data.worlds.new('暖白自然环境')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (.80, .78, .74, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = .75


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def area_light(scene, name, location, target, energy, size):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = energy
    ld.color = (1.0, .93, .83)
    ld.shape = 'DISK'
    ld.size = size
    light = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(light)
    light.location = location
    aim(light, target)
    return light


def scene_base(name):
    scene = bpy.data.scenes.new(name)
    scene.world = world
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.length_unit = 'METERS'
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1200
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'AgX'
    scene['source_scene'] = str(args.scene.name)
    scene['floor_datums'] = json.dumps({str(f): FLOORS[f]['elevation'] for f in ORDER}, ensure_ascii=False)
    scene['source_metadata'] = json.dumps(META, ensure_ascii=False)
    camera_data = bpy.data.cameras.new(name + '_相机')
    camera = bpy.data.objects.new(name + '_相机', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    sun_data = bpy.data.lights.new(name + '_日光', 'SUN')
    sun_data.energy = 1.6
    sun_data.angle = .3
    sun = bpy.data.objects.new(name + '_日光', sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(25), math.radians(-22), math.radians(-30))
    return scene, camera


full, camera = scene_base('00_整栋_完整墙体')
for collection in [*full_collections.values(), roof_collection, environment_collection]:
    full.collection.children.link(collection)
interior = META.get('blender', {}).get('interior_view')
if interior:
    datum = FLOORS[interior['floor']]['elevation']
    camera.location = interior['position']
    camera.location.z += datum
    target = Vector(interior['target']) + Vector((0, 0, datum))
    camera.data.lens = interior.get('lens', 24)
else:
    spawn = NAV['spawn']
    z = FLOORS[spawn['floor']]['elevation'] + 1.65
    camera.location = (*spawn['position'], z)
    yaw = spawn.get('yaw', 0)
    target = camera.location + Vector((math.sin(yaw), math.cos(yaw), 0))
    camera.data.lens = 24
camera.data.type = 'PERSP'
camera.data.clip_start = .04
aim(camera, target)
# Area lights placed at explicitly provided room interior points, never fabricated rooms.
for f in ORDER:
    room_list = FLOORS[f].get('rooms', []) + [r for r in NAV.get('rooms', []) if r.get('floor') == f]
    for index, room in enumerate(room_list):
        polygon = room.get('polygon', [])
        if not polygon:
            continue
        point = room.get('labelPosition') or room.get('center') or [sum(p[0] for p in polygon) / len(polygon), sum(p[1] for p in polygon) / len(polygon)]
        next_floor = min((floor['elevation'] for floor in FLOORS.values() if floor['elevation'] > FLOORS[f]['elevation']), default=META.get('roof_elevation', geometry_top))
        lamp_z = next_floor - .4
        area_light(full, f'{FLOORS[f].get("label", f)}_{room.get("name", index)}_室内柔光', (point[0], point[1], lamp_z), (point[0], point[1], FLOORS[f]['elevation']), 160, 1.8)
area_light(full, '入口柔光', camera.location + Vector((0, 0, .8)), target, 90, 1.1)
full.render.filepath = str(args.out / '04_室内人眼视角.png')

scenes = [full]
for index, f in enumerate(ORDER, 1):
    scene, cam = scene_base(f'{index:02d}_{FLOORS[f].get("label", f)}_剖开')
    scene.collection.children.link(cut_collections[f])
    boundary = FLOORS[f]['boundary']
    x0, x1 = min(p[0] for p in boundary), max(p[0] for p in boundary)
    y0, y1 = min(p[1] for p in boundary), max(p[1] for p in boundary)
    cx, cy, extent = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0)
    elevation = FLOORS[f]['elevation']
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = extent * 1.35
    cam.location = (cx + extent * 1.2, cy - extent * 1.35, elevation + extent * 1.65)
    aim(cam, (cx, cy, elevation + .45))
    area_light(scene, scene.name + '_柔光', (cx, cy, elevation + extent), (cx, cy, elevation), 1800, extent * .8)
    scene.render.filepath = str(args.out / f'{index:02d}_{FLOORS[f].get("label", f)}_剖开.png')
    scenes.append(scene)

exploded, cam = scene_base('05_三层展开')
gap = max(2.4, span * .18)
for i, f in enumerate(ORDER):
    collection = new_collection(f'{FLOORS[f].get("label", f)}_展开副本')
    exploded.collection.children.link(collection)
    for source in cut_collections[f].objects:
        copy = source.copy()
        copy.data = source.data
        copy.location.z += i * gap
        collection.objects.link(copy)
total_height = highest + (len(ORDER) - 1) * gap
cam.data.type = 'ORTHO'
cam.data.ortho_scale = max(span * 1.65, total_height * 1.35)
cam.location = (center_x + span * 1.8, center_y - span * 2.0, total_height + span)
aim(cam, (center_x, center_y, total_height / 2))
area_light(exploded, '展开主光', (center_x, center_y, total_height + span), (center_x, center_y, total_height / 2), 2200, span)
scenes.append(exploded)


def repair_coplanar_wall_rendering(scene):
    """Same-coordinate exact unions only for Cycles; retain every source object.

    Adjacent CAD wall rectangles overlap at columns and corners. Their coincident
    top faces can turn black in a cutaway render. Group by original material to
    preserve timber/plaster assignments, and never move a plan vertex.
    """
    bpy.context.window.scene = scene
    groups = {}
    for obj in list(scene.objects):
        category = obj.get('category', '')
        if obj.type != 'MESH' or not (category.startswith('wall') or category in ('column', 'partition')):
            continue
        key = tuple(material.name if material else '' for material in obj.data.materials)
        groups.setdefault(key, []).append(obj)
    for index, objects in enumerate(groups.values()):
        if len(objects) < 2:
            continue
        operands = bpy.data.collections.new(f'_渲染并集输入_{scene.name}_{index}')
        for source in objects[1:]:
            operands.objects.link(source)
        union = objects[0].copy()
        union.data = objects[0].data.copy()
        union.name = f'仅渲染_原坐标墙体并集_{scene.name}_{index}'
        scene.collection.objects.link(union)
        modifier = union.modifiers.new('原坐标精确并集_消除共面', 'BOOLEAN')
        modifier.operation = 'UNION'
        modifier.solver = 'EXACT'
        modifier.operand_type = 'COLLECTION'
        modifier.collection = operands
        modifier.use_self = True
        bpy.ops.object.select_all(action='DESELECT')
        union.select_set(True)
        bpy.context.view_layer.objects.active = union
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        if not len(union.data.polygons):
            raise RuntimeError(f'Empty wall union in {scene.name}; refusing to hide original geometry.')
        for source in objects:
            source.hide_render = True
        union.hide_viewport = True
        union.hide_render = False
        union.hide_select = True
        union['geometryStatus'] = '仅渲染用精确并集；原对象、位置和来源全部保留'
        union['source'] = json.dumps([source.name for source in objects], ensure_ascii=False)
        union['category'] = 'render-union-only'
        print('RENDER_WALL_UNION', scene.name, len(objects), len(union.data.polygons), flush=True)
        bpy.data.collections.remove(operands)


for scene in scenes:
    repair_coplanar_wall_rendering(scene)

for scene in list(bpy.data.scenes):
    if scene not in scenes:
        bpy.data.scenes.remove(scene)
bpy.context.window.scene = full
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.shading.type = 'MATERIAL'
            space.region_3d.view_perspective = 'CAMERA'
            space.overlay.show_overlays = False

notes = bpy.data.texts.new('从这里开始_第6户模型说明')
notes.write('第6户三层住宅\n\n')
notes.write('输入文件：' + str(args.scene.name) + '\n')
notes.write('标高：' + json.dumps({FLOORS[f].get('label', str(f)): FLOORS[f]['elevation'] for f in ORDER}, ensure_ascii=False) + ' 米\n\n')
notes.write('默认场景保留完整墙体。顶部Scene菜单可切换整栋、三层各自剖开图、三层展开图。\n剖开场景使用单独展示副本，原模型的墙、楼板、屋面未被切削。屋顶位于独立集合。\n')
notes.write('为避免CAD墙柱交接共面导致渲染黑块，Cycles使用同材质、同坐标的精确并集。原始墙对象与来源仍保留且在编辑视口可见；GLB导出原始模型。\n')
notes.write('模型材料、家具和空间以输入场景为准。第一人称网页提供碰撞步行与交互电梯；GLB为完整模型静态交换文件。\n\n')
notes.write('输入场景元数据与图纸核对说明：\n' + json.dumps(META, ensure_ascii=False, indent=2) + '\n')
notes.write('\n各层实际边界与导航配置：\n' + json.dumps(NAV, ensure_ascii=False, indent=2) + '\n')
blend_path = args.out / '第6户_三层住宅.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path), compress=True)
print('BLEND_SAVED', blend_path, 'OBJECTS', len(bpy.data.objects), flush=True)
bpy.ops.export_scene.gltf(filepath=str(args.out / '第6户_三层住宅.glb'), export_format='GLB', use_visible=True,
                          use_active_scene=True, export_cameras=False, export_lights=False)
if not args.skip_render:
    for scene in [*scenes[1:4], full]:
        bpy.context.window.scene = scene
        print('RENDER', scene.name, scene.render.filepath, flush=True)
        bpy.ops.render.render(write_still=True, scene=scene.name)
bpy.context.window.scene = full
print('UNIT6_BUILD_COMPLETE', flush=True)
