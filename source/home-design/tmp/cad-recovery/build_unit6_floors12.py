from pathlib import Path
import json,math
base=Path('/Users/howardwang/Desktop/Quick Projects/家装/home-design');src=base/'audit/unit6';out=base/'blender';out.mkdir(exist_ok=True)
def poly(b):x0,y0,x1,y1=b;return [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
def opening(id,a,b,type,code=None,height=None,source=None,notes=None,leaf=None):
 o={'id':id,'a':a,'b':b,'width':round(math.dist(a,b),3),'thickness':.24,'type':type,'code':code,'sill':None if type not in ['door','glazed_door','passage'] else 0,'height':height,'heightStatus':'identifier_nominal_interpretation_not_window_schedule' if code else 'unverified','planStatus':'source_wall_gap_and_window_or_door_symbol','source':source or [],'notes':notes or []}
 if leaf:o['walkableLeaf']=leaf
 return o
f1open=[
 opening('F1-entrance',[2.22,14.9],[4.04,14.9],'glazed_door',None,None,['8B9E1'],['Door leaf itself runs approximately x2.38–3.88; full masonry/frame aperture is wider.'],[[2.38,14.9],[3.88,14.9]]),
 opening('F1-public-wc-north',[.43,14.9],[1.48,14.9],'window','HC1012a',1.2,['8B9E1','3C65CA'],['North window symbol glazing x0.48–1.43. Audited overlapping wall detail extends into aperture and must be trimmed to window when constructing 3D.']),
 opening('F1-kitchen-north',[5.4,14.9],[6.6,14.9],'window','HC1212',1.2,['8B9E1']),
 opening('F1-south-west',[.615,1.1],[2.985,1.1],'glazed_door','MLC2228a',2.8,['8B9E1'],['Retain bay/porch projection separately; opening width measured between wall skins differs from nominal code.'],[[1.05,1.1],[2.55,1.1]]),
 opening('F1-south-living',[4.29,4.1],[8.91,4.1],'glazed_door','MLC4528',2.8,['8B9E1'],[],[[5.85,4.1],[7.35,4.1]]),
 opening('F1-courtyard-west',[7.8,9.34],[7.8,12.06],'window','LPC2619',1.9,['8B9E1']),
 opening('F1-courtyard-south',[8.315,8.6],[9.085,8.6],'window','LPC0619a',1.9,['8B9E1']),
 opening('F1-lightwell-south',[.45,7.4],[1.2,7.4],'window','LPC0720a',2.0,['8B9E1']),
 opening('F1-lightwell-east',[2.3,7.625],[2.3,8.375],'window','LPC0720a',2.0,['8B9E1']),
 opening('F1-public-wc-door',[1.8,12.9],[1.8,13.7],'door','M0821',2.1,['8B9E1']),
 opening('F1-south-wc-door',[2.36,5.42],[2.36,6.22],'door','M0821',2.1,['8B9E1']),
 opening('F1-kitchen-south',[5.1,12.74],[6.9,12.74],'passage',None,None,['8B9E1'],['Kitchen south flank lines are DASHED2 reference geometry; not treated as existing full-height solid wall.'])]
f2open=[
 opening('F2-south-west',[.775,1.1],[2.825,1.1],'window','LPC1921ab',2.1,['8B8EE']),
 opening('F2-south-main',[4.4,4.1],[7.24,4.1],'window','LPC2826',2.6,['8B8EE']),
 opening('F2-east-1',[7.8,4.6],[7.8,5.35],'window','LPC0617a',1.7,['8B8EE']),
 opening('F2-east-2',[7.8,7.35],[7.8,8.1],'window','LPC0617a',1.7,['8B8EE']),
 opening('F2-east-3',[7.8,9.51],[7.8,10.26],'window','LPC0617a',1.7,['8B8EE']),
 opening('F2-east-4',[7.8,11.81],[7.8,12.56],'window','LPC0617a',1.7,['8B8EE'],['Window symbol placed over continuous WALL outline; aperture must cut those overlapping wall boxes at selected sill/header elevations.']),
 opening('F2-north-main-bath',[4.38,13.7],[7.02,13.7],'window','LPC2622',2.2,['8B8EE'],['Cut overlapping wall detail in window band.']),
 opening('F2-north-stair-1',[.5,12.8],[1.25,12.8],'window','LPC0617a',1.7,['8B8EE']),
 opening('F2-north-stair-2',[2.39,12.8],[3.16,12.8],'window','LPC0617a',1.7,['8B8EE']),
 opening('F2-lightwell-south',[.45,7.4],[1.2,7.4],'window','LPC0718a',1.8,['8B8EE']),
 opening('F2-lightwell-east',[2.3,7.625],[2.3,8.375],'window','LPC0718a',1.8,['8B8EE']),
 opening('F2-south-wc-door',[2.36,5.42],[2.36,6.22],'door','M0821',2.1,['8B8EE']),
 opening('F2-main-bath-door',[5.2,11.24],[6.0,11.24],'door','M0821',2.1,['8B8EE']),
 opening('F2-dressing-west',[4.2,9.58],[4.2,11.08],'door',None,None,['8B8EE'],['Large door symbol; lower west-wall flank is HIDDEN reference. Central lift east door centered y10.45 falls inside this opening.'])]
meta=[
 dict(id=1,label='一层',origin=[658498.48,725212.6429989272],elevation=0,ceilingElevation=3.7,boundary=[[-.12,.98],[3.72,.98],[3.72,3.98],[9.72,3.98],[9.72,15.02],[-.12,15.02]],terraces=[poly([-.12,.38,3.72,.98]),poly([3.48,2.18,9.72,3.98]),poly([2.,15.02,4.26,16.35])],openings=f1open,rooms=[{'name':'原南西开敞空间','bounds':[.12,1.22,3.48,5.18],'proposedUse':'父母卧室','status':'privacy partition is new interior design, not source wall'},{'name':'原客厅','bounds':[3.72,4.22,9.48,8.48]},{'name':'原餐厅','bounds':[2.77,8.72,7.68,12.68]},{'name':'厨房','bounds':[4.32,12.8,7.68,14.78]},{'name':'玄关','bounds':[1.86,12.8,4.08,14.78]},{'name':'公卫','bounds':[.12,12.8,1.74,14.78]},{'name':'南侧卫生间','bounds':[.12,5.3,2.3,7.28]}],voids=[{'name':'采光井上空','bounds':[.14,7.54,2.16,8.46],'polygon':poly([.14,7.54,2.16,8.46]),'source':['8B9E1']},{'name':'东侧下沉庭院上空','bounds':[7.92,8.72,9.48,14.78],'polygon':poly([7.92,8.72,9.48,14.78]),'source':['8B9E1']}]),
 dict(id=2,label='二层',origin=[658498.48,647269.5110587726],elevation=3.7,ceilingElevation=6.9,boundary=[[-.12,.98],[3.72,.98],[3.72,3.98],[7.92,3.98],[7.92,13.82],[3.48,13.82],[3.48,12.92],[-.12,12.92]],terraces=[poly([.12,12.92,3.48,14.78])],flatRoofs=[{'name':'东侧平屋面','bounds':[7.92,4.1,9.48,8.48],'polygon':poly([7.92,4.1,9.48,8.48]),'elevation':3.7,'source':['8B8EE'],'status':'roof access is not implied'}],openings=f2open,rooms=[{'name':'南西卧室','bounds':[.12,1.22,3.48,5.18]},{'name':'南侧卫生间','bounds':[.12,5.3,2.3,7.28]},{'name':'主卧','bounds':[3.6,4.22,7.68,8.6]},{'name':'更衣','bounds':[4.32,8.72,7.68,11.18]},{'name':'主卫','bounds':[4.32,11.3,7.68,13.58]},{'name':'原楼梯区','bounds':[.12,8.72,2.77,12.68]}],voids=[{'name':'采光井上空','bounds':[.14,7.54,2.16,8.46],'polygon':poly([.14,7.54,2.16,8.46]),'source':['8B8EE']},{'name':'东侧下沉庭院上空','bounds':[7.92,8.72,9.48,14.78],'polygon':poly([7.92,8.72,9.48,14.78]),'source':['8B8EE']},{'name':'南廊上空','bounds':[3.74,2.445,9.095,3.98],'polygon':poly([3.74,2.445,9.095,3.98]),'source':['8B8EE']}])]
for f in meta:
 fid='F'+str(f['id']);walls=json.load(open(src/f'{fid}-native-wall-boxes.json'));cols=json.load(open(src/f'{fid}-native-columns.json'));cols=list({tuple(c['bounds']):c for c in cols}.values())
 for i,b in enumerate(walls):b['id']=f'{fid}-W{i+1:03}'
 for i,b in enumerate(cols):b['id']=f'{fid}-C{i+1:03}'
 f.update(boxes=walls+cols,wallBoxes=walls,columns=cols,dashedReferenceWalls=json.load(open(src/f'{fid}-dashed-wall-references.json')),originalStairBounds=[.12,8.72,2.77,12.68],originalStairVoid={'bounds':[1.17,9.77,2.77,11.63],'source':['8B9E1' if f['id']==1 else '8B8EE'],'status':'original A-HOLE, removed/infilled as part of user central lift alteration'},proposedLiftCandidate={'bounds':[2.45,9.5,4.10,11.4],'innerBounds':[2.57,9.62,3.98,11.28],'door':{'side':'east','center':[4.1,10.45],'width':.95},'status':'proposed alteration; root finalizes'},notes=['Do not generate original stairs; user requested their removal.','Boundary describes main conditioned outer envelope; subtract void polygons and new lift shaft. Original stair void may be infilled for proposed layout.','Terraces and flat roofs are original outdoor/projected boundaries, not extra indoor rooms. North entry terrace is traced from entry stair projection; user requested stair removal, so level access needs a separate alteration.','Source wall boxes describe plan material below cut plane; carve every opening through intersecting wall boxes at the chosen vertical aperture; preserve source structural columns and reconcile any opening-column overlap, rather than adding transparent planes in front of solid walls.','Window sill heights and finished ceiling underside heights are not confirmed by plan. Elevation is floor datum; ceilingElevation is next structural floor datum.','DASHED/HIDDEN wall references are deliberately separate from existing solid boxes. Do not turn dashed strokes into rows of wall fragments.','Some room boundaries are functional labels in an open plan; new privacy walls must be marked as proposed interior design.','All coordinates in metres relative to source origin; wall skins rounded to 1 mm.'])
result={'units':'m','unit':6,'sourceDrawing':'02-10-20B#楼平立面图(1).dwg','sourceDXF':str(base/'tmp/cad-recovery/oda-audited/original.dxf'),'schema':'floors with source-plan boxes/opening axes; separate original voids and proposed lift','floors':meta}
(out/'unit6-floors12.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(out/'unit6-floors12.json')
