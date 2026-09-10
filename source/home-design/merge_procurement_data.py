import json,csv
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'output/unit6-procurement'
read=lambda f:json.loads((OUT/f).read_text())
d=read('预算基础数据.json');f=read('research/furniture.json');a=read('research/appliances.json');c=read('research/contractors.json')
rooms={'R101':'父母卧室','R102':'父母卫浴','R103':'一层公卫','R104':'客厅','R105':'餐厅','R106':'厨房','R108':'爸爸操盘房','R109':'南院','R201':'主卧','R203':'主卫','R204':'未来儿童房','R205':'儿童卫浴','R206':'二层休闲/家政区','R301':'妹妹卧室','R302':'妹妹卫浴','R303':'书法房','R304':'妈妈毛线工作室','R305':'露台花园'}
def roomstr(rs):return '、'.join(f'{k} {rooms.get(k,k)}'+(f'×{v}' if v!=1 else '') for k,v in (rs.items() if isinstance(rs,dict) else ((r,1) for r in rs)))
def dims(x):return '×'.join(map(str,x))+' cm' if x else '待按实物/纸样定尺寸'
rows=[];v=f['valuePlan'];original={r['id']:r for r in f['items']}
for phase,key in [(True,'recommendedProducts'),(False,'deferredProducts')]:
 for p in v[key]:
  r=original[p['id']];rows.append(dict(id='FN-'+r['id']+('' if phase else '-D'),category='成品家具',room=roomstr(p['rooms']),name=r['name']+('' if phase else '（延后）'),model=f"{r['brand']} {r['model']} / {r['sku']}",quantity=p['quantity'],unit='件',budgetUnitPrice=p['unitPriceCny'],included=phase,priceStatus=r['priceBasis'],priceDate=r['checkedDate'],sourceUrl=r['sourceUrl'],scope=r['includes']+'；另计：'+r['excludes'],fitStatus=dims(r['dimensionsCm'])+'；'+r['fitReview'],notes=r['availability'],sourceId=r['id']))
for r in f['customItems']:
 phase=r['id'] in v['recommendedCustomIds'];rows.append(dict(id='FN-'+r['id'],category='定制家具',room=roomstr(r['rooms']),name=r['name']+('' if phase else '（延后）'),model=r['model'],quantity=r['quantity'],unit='件',budgetUnitPrice=r['unitPriceBaseCny'],included=phase,priceStatus=r['priceBasis'],priceDate=r['checkedDate'],sourceUrl='',scope=r['scopeTag']+'；'+r['color'],fitStatus=dims(r['dimensionsCm'])+'；'+r['requirement'],notes='',sourceId=r['id']))
for r in v['additionalItems']:
 rows.append(dict(id='FN-'+r['id'],category='定制家具',room=roomstr(r['rooms']),name=r['name'],model=r['model'],quantity=r['quantity'],unit='件',budgetUnitPrice=r['baseCny'],included=True,priceStatus=r['priceBasis'],priceDate=d['asOf'],sourceUrl='',scope=r['note'],fitStatus=dims(r['dimensionsCm']),notes='',sourceId=r['id']))
for r in v['allowanceAllocation']:
 for key,phase in [('recommendedBaseCny',True),('deferredBaseCny',False)]:
  if r[key]:rows.append(dict(id='FN-'+r['id']+('' if phase else '-D'),category='家具附加',room='全屋',name=r['name']+('' if phase else '（延后）'),model='预算额度，具体清单待采购',quantity=1,unit='批',budgetUnitPrice=r[key],included=phase,priceStatus='预算预留，非商家报价',priceDate=d['asOf'],sourceUrl='',scope=r['note'],fitStatus='地址、物品数量及服务范围待核',notes='',sourceId=r['id']))
d['furniture']=rows;ap=[]
addon=read('research/network-addendum.json')
a['valuePlan']['recommendedItems']+=addon['recommendedItems']
for phase,key in [(True,'recommendedItems'),(False,'excludedDeferred')]:
 for r in a['valuePlan'][key]:
  component='；'.join((x.get('model') or x.get('name',''))+f" ×{x.get('quantity',1)}" for x in r.get('components',[]))
  ap.append(dict(id='AP-'+r['id'],category={'appliances':'生活家电','sanitary':'卫浴洁具','lighting':'照明','systems':'冷暖热水排风','optional_appliances':'可选设备','network':'生活家电','installation_accessories':'生活家电','accessories':'生活家电','appliance_accessory':'生活家电'}.get(r['category'],r['category']),room=roomstr(r['room_ids']),name=r['name']+('' if phase else '（延后）'),model=r['model'],quantity=r['quantity'],unit=r['unit'],budgetUnitPrice=r['unit_price_cny'],included=phase,priceStatus=r['price_basis'],priceDate=r['price_checked_date'],sourceUrl=r['sources'][0]['url'] if r['sources'] else '',scope=r['included']+'；另计：'+r['excluded']+('；组成：'+component if component else ''),fitStatus=r['model_fit']+'；'+ '；'.join(r['installation_dependencies']),notes=r.get('source_verification_note','')+r['purchase_status'],dimensions=r['dimensions'],components=r['components'],sources=r['sources'],sourceId=r['id']))
d['appliances']=ap;d['contractors']=c['candidates'];d['elevators']=c['elevators'];d['domesticElevatorCandidates']=c.get('domesticElevatorCandidates',[])
d['fitIssues']=[
 {'id':'F01','item':'电梯与原楼梯','condition':'模型井道外1650×1900mm、内净1410×1660mm；东侧门。型号和孔口未签认；无楼梯仅为方案意向。','action':'先核撤梯、开井、补板是否允许及疏散方案，再由结构/建筑/电梯厂家协同出图；未确认前不下电梯或梯区定制单。'},
 {'id':'F02','item':'厨房600mm洗碗机','condition':'模型520mm面板不是安装净孔；15套S1需重排柜格。厨房4.4延米只为预算占位。','action':'在原厨房边界内复尺，厂家与橱柜厂同图确认净孔、门板、踢脚、上下水；放不下则更换型号重新核价。'},
 {'id':'F03','item':'冰箱与搬运','condition':'候选海尔595×600×1906mm，模型占位660×730×2040mm；机体小于占位不等于可安装。','action':'核散热、开门抽屉、插座及整条搬运路线；原图墙体和洞口不得为家电擅改。'},
 {'id':'F04','item':'妹妹床与卧室通道','condition':'妹妹用120×200床垫及TARVA外廓128×209cm；150床架不适合直接套用原145cm床框。','action':'现场按完成面、柜门开启和床头通道放样；本人试躺后锁货号。'},
 {'id':'F05','item':'沙发/电视柜与75寸电视','condition':'VIMLE沙发241×98cm，比原示意占位深约6cm；成品电视柜比原230cm示意短。','action':'放样通道，核所选75D50真实机宽/底座支承范围及固定方法，勿以屏幕对角线判断可摆。'},
 {'id':'F06','item':'完整宣纸收纳','condition':'原70×44cm柜无法平放68×136cm整纸。','action':'原柜只放小幅纸/册页，新增800元轻放收纳预留；纸样不宜卷存则另做净内尺寸足够的平放方案。'},
 {'id':'F07','item':'五卫卫浴与热水','condition':'坐便坑距、盆柜固定基层、四淋浴水压未测；20L候选不保证冬季多人同时洗浴。','action':'按最不利用水点、温升、气源和并发需求核热源；确定回水、止回与检修；淋浴按每间实测选择。'},
 {'id':'F08','item':'空调室外机与负荷','condition':'预算8个分区暂列7挂机+1柜机，非负荷计算结果；8台外机合法机位、散热、噪声未确认。','action':'先核原预留机位与物业条件，再比较分体/多联配置；安装、铜管、排水和最终容量重新报价。'},
 {'id':'F09','item':'洗烘机位置','condition':'现家政区域并非已核湿区；地漏、排水、防水和楼板条件未确认。','action':'优先复核原合法湿区可用洗衣位置；H30仅常规配套暂列，禁止未经设计在干区穿板接排水，移动后重核柜体与动线和追加费用。'},
 {'id':'F10','item':'门窗与吊顶','condition':'38处模型洞口中32处竖向未完整核实；门数9套、窗帘等均暂估。','action':'毛坯逐洞验收，合格开发商门窗保留；按完成面洞口表订门和窗帘，不从模型直接下料。'},
 {'id':'F11','item':'庭院/露台与花房','condition':'南院47.504㎡、南廊9.797㎡、露台18.684㎡；仅开敞轻型园艺，无新增封闭阳光房预算。','action':'确认防水排水、饱水荷载、抗风及临空防护；先4花箱。若需玻璃封闭阳光房，须另核允许范围并专项设计报价。'},
 {'id':'F12','item':'灯光与电气','condition':'62展示点不是完整电气点表；18干区/2厨/5卫/5室外主灯为采购预算。','action':'核照度、眩光、开关逻辑、湿区防护与末端回路；书法/毛线台灯实测，不靠总瓦数替代照度。'},
 {'id':'F13','item':'同范围报价去重','condition':'H21安装预留；AP系统已含部分安装。厨房H23–26已计17430，五卫盆柜龙头镜柜在AP，花箱在G06。','action':'签约前做甲供乙供界面表，重复安装/柜体费扣除；所有增项先明确工程量、单价与批准记录。'},
 {'id':'F14','item':'原图一致性','condition':'本版没有改变P02模型和原图边界；采购产品也尚未替换到三维模型。','action':'保持已核墙体/边界，在原图内复尺布置并更新施工图；不得把选品清单当作准确品牌实物模型或加工图。'}]
allrows=d['construction']+rows+ap;cats=defaultdict(float)
for r in allrows:
 r['lineTotal']=round(r['quantity']*r['budgetUnitPrice'],2)
 if r['included']:cats[r['category']]+=r['lineTotal']
subtotal=round(sum(cats.values()),2);elev=cats['电梯暂列'];total=round(subtotal*(1+d['contingencyRate']),2)
d['totals']={'categories':{k:round(v,2) for k,v in cats.items()},'subtotal':subtotal,'contingency':round(subtotal*d['contingencyRate'],2),'mainWithContingency':total,'elevatorWithContingency':round(elev*(1+d['contingencyRate']),2),'withoutElevator':round((subtotal-elev)*(1+d['contingencyRate']),2),'optionalBeforeContingency':round(sum(r['lineTotal'] for r in allrows if not r['included']),2),'furniturePhase1':round(sum(r['lineTotal'] for r in rows if r['included']),2),'appliancesPhase1':round(sum(r['lineTotal'] for r in ap if r['included']),2),'furnitureDeferred':v['budget']['deferredTotalBaseCny']}
assert abs(d['totals']['furniturePhase1']-v['budget']['recommendedPhase1BaseCny'])<.01
assert abs(d['totals']['appliancesPhase1']-a['valuePlan']['totals']['recommended_all']['total_cny']-1700)<.01
assert len({r['id'] for r in allrows})==len(allrows)
d['furniturePhases']=v['phases'];d['sourceNotes']=d['notes'];d['pricingCaution']='所有金额人民币；模型量及工程单价是预算假设。未获现场正式报价，未知结构工程未计，不能视为封顶总价。'
(OUT/'采购预算整合.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
for name,rs in [('硬装与花园',d['construction']),('家具与定制',rows),('家电与卫浴',ap)]:
 with (OUT/f'{name}.csv').open('w',encoding='utf-8-sig',newline='') as fh:
  w=csv.writer(fh);w.writerow(['编号','类别','房间','项目','型号货号','数量','单位','预算单价元','初期计入','行金额元','价格类型','核对日期','来源','供货界面','尺寸安装条件','备注'])
  for r in rs:w.writerow([r[k] for k in ['id','category','room','name','model','quantity','unit','budgetUnitPrice','included','lineTotal','priceStatus','priceDate','sourceUrl','scope','fitStatus','notes']])
print(json.dumps(d['totals'],ensure_ascii=False,indent=2));print('Rows',len(allrows))
