import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/Users/howardwang/Desktop/Quick Projects/家装/home-design')
SOURCE = {'file': 'home-design/tmp/cad-recovery/oda-audited/original.dxf',
          'rootHandle': '8B1CB', 'block': 'ERTGVVV',
          'method': 'paired transformed straight wall-face endpoints, rounded to 1 mm'}

def src(layers, note=''):
    return dict(SOURCE, layers=layers if isinstance(layers, list) else [layers], note=note)

boxes=[]
def wall(name,bounds,layer='E4-FL03$0$AUDIT_I_171201172723-4'):
    boxes.append({'name':name,'bounds':bounds,'source':src(layer),'role':'wall'})

wall('西侧分户墙',[-.12,.98,.12,12.92],['E4-FL03$0$A-WALL','E1-FL03$0$A-WALL'])
wall('南窗西墙垛',[.12,.98,.48,1.22])
wall('南窗东墙垛',[3.12,.98,3.72,1.22])
for name,b in [('卧室东墙南段',[3.48,1.22,3.72,1.77]),
               ('卧室东墙两窗间',[3.48,2.77,3.72,4.58]),
               ('卧室东墙北窗间',[3.48,6.72,3.72,7.33]),
               ('走廊东墙北段',[3.48,7.993,3.72,8.72]),
               ('书房南墙门西',[3.72,8.48,4.48,8.72]),
               ('书房南墙门东',[5.92,8.48,6.72,8.72]),
               ('书房东墙窗南',[6.48,8.72,6.72,9.055]),
               ('书房东墙窗北',[6.48,12.345,6.72,12.92]),
               ('书房北墙西端',[.12,12.68,.805,12.92]),
               ('书房北墙两窗间',[2.795,12.68,5.03,12.92]),
               ('书房北墙东端',[6.37,12.68,6.48,12.92])]:wall(name,b)
for name,b in [('卫生间南墙',[.12,5.18,2.42,5.30]),
               ('卫生间东墙门南',[2.30,5.30,2.42,5.42]),
               ('卫生间东墙门北',[2.30,6.22,2.42,7.28]),
               ('卫生间北窗西墙',[.12,7.28,.44,7.52]),
               ('卫生间北窗东墙',[1.21,7.28,2.30,7.52]),
               ('采光井东南墙角',[2.30,7.28,2.42,7.52]),
               ('采光井东窗南墙',[2.18,7.52,2.42,7.625]),
               ('采光井东窗北墙',[2.18,8.375,2.42,8.48]),
               ('采光井北墙',[.12,8.48,2.42,8.72])]:wall(name,b,'WALL')
wall('卧室入口门西墙垛',[2.42,7.28,2.46,7.40],'WALL-MOVE')
wall('卧室入口门东墙垛',[3.36,7.23,3.48,7.35],'WALL-MOVE')

openings=[]
def opening(name,kind,a,b,code=None,layer=None,notes=''):
    openings.append({'name':name,'type':kind,'a':a,'b':b,'thickness':.24 if name!='卫生间门' else .12,
                     'sill':None,'height':None,'verticalStatus':'待立面/门窗表核对；平面编号不直接当作已核实净高',
                     'code':code,'source':src(layer or 'E4-FL03$0$AUDIT_I_171201172723-4',notes)})
opening('卧室南窗','window',[.48,1.10],[3.12,1.10],'LPC2615',notes='墙皮洞宽2.64m；尺寸标注名义2600。')
opening('卧室东小窗','window',[3.60,1.77],[3.60,2.77],'SC0909',notes='结构两端1.77/2.77；框内尺寸标注1.82/2.72=900。')
opening('卧室东大窗','window',[3.60,4.58],[3.60,6.72],'LPC2123',notes='此处平面标窗，不擅自改为露台门；名义尺寸2100。')
opening('走廊东窗','window',[3.60,7.33],[3.60,7.993],'LPC0723',notes='采用两侧墙皮实际端点；图中另有700名义窗框尺寸，不与净洞混同。')
opening('书房至露台双门','door',[4.48,8.60],[5.92,8.60],'MLC1423',notes='结构洞1.44m；双扇开启弧明确，名义门宽1400。')
opening('书房东长窗','window',[6.60,9.055],[6.60,12.345],'LPC3213ab',notes='结构洞3.29m；名义框尺寸3250。')
opening('书房北西窗','window',[.805,12.80],[2.795,12.80],'LPC1915a',notes='结构洞1.99m；名义框尺寸1950。')
opening('书房北东窗','window',[5.03,12.80],[6.37,12.80],'LPC1313b',notes='结构洞1.34m；名义框尺寸1300。')
opening('卫生间采光井窗','window',[.44,7.40],[1.21,7.40],'LPC0716a',layer='WALL',notes='框标注750，采光井相邻墙；不得当成外侧房间门。')
opening('走廊采光井窗','window',[2.30,7.625],[2.30,8.375],'LPC0716a',layer='WALL')
opening('卫生间门','door',[2.36,5.42],[2.36,6.22],'M0821',layer=['WALL','E1-FL03$0$A-DOOR'])
opening('卧室入口门','door',[2.46,7.34],[3.36,7.34],layer=['WALL-MOVE','E1-BS01-18-19$0$A-ANNO-NPLT'],notes='原图有开启弧和0.9m门洞；两门垛Y端点略错位，采用洞口中线。')
openings[-1]['thickness']=.12
for o in openings:
    if o['type']=='door':o['sill']=0

indoor=[[-.12,.98],[3.72,.98],[3.72,8.48],[6.72,8.48],[6.72,12.92],[-.12,12.92]]
boundary=[[-.12,.98],[3.72,.98],[3.72,3.38],[8.16,3.38],[8.16,7.52],[6.72,7.52],[6.72,12.92],[-.12,12.92]]
terrace=[[3.72,3.38],[8.16,3.38],[8.16,7.52],[6.72,7.52],[6.72,8.48],[3.72,8.48]]
well=[[.12,7.52],[2.18,7.52],[2.18,8.48],[.12,8.48]]
stairhole=[[1.17,9.77],[2.77,9.77],[2.77,11.63],[1.17,11.63]]
parapets=[]
for name,b in [('露台南栏墙',[3.72,3.38,8.16,3.62]),('露台东栏墙',[7.92,3.62,8.16,7.52]),
               ('露台东北退台栏墙',[6.72,7.28,7.92,7.52]),('露台北段东栏墙',[6.48,7.52,6.72,8.48])]:
    parapets.append({'name':name,'bounds':b,'height':None,'displayHeight':1.10,'role':'parapet',
                     'source':src('E4-FL03$0$A-SLAB-OTLN','平面墙皮0.24m；1.10m仅展示值，需将立面/7.900结构标注核对到具体墙顶。')})

def room(name,bounds,position,polygon=None):
    r={'name':name,'bounds':bounds,'labelPosition':position,'source':{'file':'home-design/audit/recovered/F3-texts-decoded.json','rootGeometryHandle':'8B1CB','labelLayer':'DZ-TEXT-FL01$0$A-ROOM-IDEN'}}
    if polygon:r['polygon']=polygon
    return r
data={'id':3,'floorIndex':2,'name':'第6户 三层 / 原图户型E4','units':'m',
      'meta':{'originDwgMm':[658498.48,567027.2316627398],'coordinateRoundingMeters':.001,
              'sourceDwgSha256':'f8b152616a5b38dbc866076aca374d165bd5aefeea2e49652542c0df8c4b477b'},
      'elevation':6.9,'ceilingElevation':9.9,
      'boundary':boundary,'boundarySource':src(['E4-FL03$0$A-WALL','E4-FL03$0$AUDIT_I_171201172723-4','E4-FL03$0$A-SLAB-OTLN'],'主体外墙和可达露台外边线的并集；不含坡屋面、悬挑檐口、设备平台和下沉庭院上空。'),
      'indoorBoundary':indoor,'ceilingBoundary':indoor,
      'holes':[well,stairhole],
      'voids':[{'name':'采光井上空','polygon':well,'preserve':True,'source':src(['WALL','E1-FL03$0$A-HOLE'])},
               {'name':'原楼梯中空','polygon':stairhole,'preserve':False,'source':src(['E1-FL03$0$A-HRAL','E1-FL03$0$A-STRS']),'note':'原状记录；用户指定拆楼梯后是否补板由改造模型明确处理。'}],
      'terraces':[{'name':'露台','polygon':terrace,'bounds':[3.72,3.38,8.16,8.48],
                   'floorElevation':6.87,'structuralElevation':6.77,
                   'source':src('E4-FL03$0$A-SLAB-OTLN','原露台文字在[5.592,6.078]，6.870/6.770结构标注在露台西南及相邻位置；保持露天。')}],
      'boxes':boxes,'wallBoxes':boxes,'openings':openings,'parapets':parapets,
      'originalStairBounds':[.12,8.72,2.47,12.68],
      'originalStairSource':src(['E1-FL03$0$A-STRS','E1-FL02$0$A-STRS','E1-FL03$0$A-HRAL']),
      'originalStairHole':stairhole,
      'rooms':[room('卧室',[.12,1.22,3.48,5.18],[1.586,2.824],[[.12,1.22],[3.48,1.22],[3.48,7.23],[2.42,7.23],[2.42,5.18],[.12,5.18]]),
               room('卫',[.12,5.30,2.30,7.28],[1.490,5.979]),
               room('书房',[2.47,8.72,6.48,12.68],[3.897,11.007]),
               room('露台',[3.72,3.38,8.16,8.48],[5.592,6.078],terrace)],
      'circulation':[{'name':'原卧室入口通道','bounds':[2.42,5.18,3.48,7.28]},
                     {'name':'采光井东侧交通','bounds':[2.42,7.40,3.48,8.72]},
                     {'name':'原楼梯区域','bounds':[.12,8.72,2.47,12.68]}],
      'excludedZones':[{'name':'北侧设备平台','labelPosition':[.94,14.174],'walkable':False,'reason':'没有从三层室内直接出入门；仅用于设备，不当作室内或生活露台。'},
                       {'name':'东侧下沉庭院上空','labelPosition':[9.0,11.0],'walkable':False,'reason':'此层为空，不铺楼板。'},
                       {'name':'露台周边坡屋面/檐口','walkable':False,'reason':'多组6.900/7.150标注及屋面线并不代表连续可走地板。'}],
      'proposedLiftCandidate':{'bounds':[2.50,8.90,4.35,10.90],'status':'仅三层避开原露台双门洞的建议；须与1/2F统一，由根代理改造层决定'},
      'notes':['这是原状几何提取，尚未应用取消楼梯和新增电梯。',
               'full-height boxes不得封闭openings；需按原门窗位置补窗下墙、过梁并保留可穿行门洞。',
               '门窗高度与窗台未获立面/门窗表逐项对应，null不是0；展示值须单独标为假设。',
               'boundary包含露台外边但ceilingBoundary仅限室内；不得给露台加屋顶。',
               '原楼梯孔可在指定改造中补板，但采光井应保留。',
               '同根块里的装饰线与屋面线未当作实墙；本稿主要墙皮按1mm取整。']}
(BASE/'blender/unit6-floor3.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))

# Draw a geometric QA overlay directly from CAD line data and extracted polygons.
S=150; xmin=-.8;ymax=16.0;ymin=-1.0;xmax=10.4
im=Image.new('RGB',(int((xmax-xmin)*S),int((ymax-ymin)*S)),'white')
d=ImageDraw.Draw(im,'RGBA')
def pt(p):return ((p[0]-xmin)*S,(ymax-p[1])*S)
def poly(p,fill,outline):d.polygon([pt(a) for a in p],fill=fill,outline=outline,width=3)
poly(boundary,(227,229,225,255),(74,97,101,255));poly(indoor,(232,226,213,255),(91,89,79,255));poly(terrace,(206,224,203,255),(59,103,53,255))
for v in data['voids']:poly(v['polygon'],(238,241,249,255),(92,111,156,255))
for n in range(0,11):d.line([pt([n,ymin]),pt([n,ymax])],fill=(172,194,203,170),width=1)
for n in range(0,16):d.line([pt([xmin,n]),pt([xmax,n])],fill=(172,194,203,170),width=1)
for r in json.load(open(BASE/'audit/unit6/F3-segments-local.json')):d.line([pt(r['a']),pt(r['b'])],fill=(78,87,93,70),width=1)
for b in boxes:
    x1,y1,x2,y2=b['bounds'];d.rectangle([pt([x1,y2]),pt([x2,y1])],fill=(40,48,56,255))
for b in parapets:
    x1,y1,x2,y2=b['bounds'];d.rectangle([pt([x1,y2]),pt([x2,y1])],fill=(93,122,87,255))
for o in openings:d.line([pt(o['a']),pt(o['b'])],fill=(10,135,178,255) if o['type']=='window' else (218,117,21,255),width=7)
font=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',23)
for r in data['rooms']:d.text(pt(r['labelPosition']),r['name'],font=font,fill=(20,66,96,255))
for n in range(0,11):d.text(pt([n,15.7]),f'{n}m',font=font,fill=(58,86,101,255))
for n in range(0,16):d.text(pt([-.7,n+.2]),str(n),font=font,fill=(58,86,101,255))
d.text((20,20),'第6户三层 | 实墙/原门窗洞提取核对 | 蓝=窗 橙=门 绿=露台 白蓝=洞',font=font,fill=(20,45,62,255))
im.save(BASE/'audit/unit6/F3-unit6-extraction-check.png')
print('saved unit6-floor3.json',len(boxes),'walls',len(openings),'openings')
