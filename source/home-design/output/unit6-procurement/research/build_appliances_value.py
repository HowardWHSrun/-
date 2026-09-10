"""Add the value plan while retaining the earlier source research unchanged."""
import copy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
path=ROOT/'appliances.json'
data=json.loads(path.read_text(encoding='utf-8'))
old={x['id']:x for x in data['items']}
sources={x['id']:x for x in data['sources']}
date='2026-09-10'
def source(key,title,url,kind='官方产品页/型号线索，地区供货待核'):
    sources[key]={'id':key,'title':title,'url':url,'type':kind,'checked_date':date}
source('v_toilet_main','九牧11396系列：11396KD版本；网页活动过期且库存待选，不采用促销价','https://www.ejomoo.com.cn/item/11396.htm')
source('v_toilet_other','九牧11370KE普通坐便器；坑距与含安装版本可选','https://www.ejomoo.com.cn/item/11370.htm')
source('v_toilet_list','九牧官方普通坐便器目录：用于确认在列型号，不能当本地供货承诺','https://www.ejomoo.com/items/products.htm?categoryUuid=mtzq')
source('v_shower_main','九牧26195恒温淋浴：选26195，不混入26209升级版','https://www.ejomoo.com/item/26195.htm')
source('v_shower_other','九牧36669普通淋浴：亮银版不含安装，需单列人工','https://www.ejomoo.com/item/36669.htm')
source('v_tap','九牧32846面盆龙头：亮银1B候选，网页338元不能代表本地现货','https://www.ejomoo.com/item/32846.htm')
source('v_jomoo_company','九牧官方商城公司及服务主体：九牧厨卫（厦门）有限公司','https://www.ejomoo.com.cn/')
source('v_lights','米家吸顶灯L60/D40/D30套系中国官方入口；直接打开标题一致，无有效当前售价','https://www.mi.com/shop/buy/detail?cfrom=search&product_id=22569')
source('v_ac_wall','海尔 KFR-35GW/EC1-1：2026年款1.5匹一级变频，参考2599元','https://www.haier.com/air_conditioners/20260707_292886.shtml','官方规格与参考价')
source('v_ac_floor','海尔 KFR-72LW/E1-1：3匹一级变频，参考6399元','https://www.haier.com/air_conditioners/20250213_255574.shtml','官方规格与参考价')
source('v_hotwater','海尔 JSQ38-20HT5DPXGU1：20升天然气热水器，参考3599元','https://www.haier.com/water_heaters/rqrsq/20241216_254014.shtml','官方规格与参考价')

recommended=[copy.deepcopy(x) for x in data['items'] if x['required']]
idx={x['id']:x for x in recommended}
def edit(id,base,low,high,**kwargs):
    r=idx[id]
    r.update(kwargs)
    r['unit_price_cny']=base;r['low_unit_price_cny']=low;r['high_unit_price_cny']=high
    for k,v in [('total_cny',base),('low_total_cny',low),('high_total_cny',high)]:r[k]=round(r['quantity']*v,2)
    r['price_checked_date']=date
    r['price_is_binding_quote']=False
    if 'source_ids' in kwargs:r['sources']=[sources[s] for s in kwargs['source_ids']]
    r['purchase_status']='推荐预算候选；须完成现场复尺、厂家安装图、中国版本/本地库存和书面含税报价确认。'
    return r

edit('A07',5600,4500,7200,quantity=1,unit='组',
 name='五套普通节水坐便器，父母/主卫与其他房间分档',
 model='九牧11396KD ×2（父母/主卫）；11370KE ×3（公卫/儿童/妹妹），305/400坑距逐间实测选版',
 price_basis='整组预算：2×1300+3×1000；不是九牧现价，未使用过期618价、国补或满件折扣',
 source_ids=['v_toilet_main','v_toilet_other','v_toilet_list','v_jomoo_company'],
 dimensions={'overall_mm':None,'pit_variants_mm':[305,400]},
 model_fit='保留5个原卫浴内的坐便功能；候选国产普通马桶无电控。完整外廓尚未取得厂家尺寸图，现模型不得据此缩减净空。父母/主卫先试坐确认座圈尺寸和起坐高度。',
 installation_dependencies=['每间按完成墙面量坑距、排污中心、前方及侧方净空，再确定305或400版本','官网11396有KC、KD和含/不含安装版本，主选明确11396KD；11370主选11370KE，不接受泛写11370系列','商家须提供缓降座圈、水件、密封件及安装的完整包含清单；网页显示库存0且未选地址，须确认杭州供货','不为适配马桶迁移原排污立管或破坏已验收防水；智能盖仅预留合规电源不计入本期'],
 included='五套普通坐便器、普通缓降座圈、常规密封安装附件的预算；地方安装若不含须从预算明确分摊',
 excluded='智能盖板、坑距移位、结构开孔和防水返工；未取得可直接下单的本地套餐报价',
 components=[{'model':'九牧11396KD','quantity':2,'unit_allowance_cny':1300,'total_cny':2600,'assignment':'R102父母/R203主卫'},
 {'model':'九牧11370KE','quantity':3,'unit_allowance_cny':1000,'total_cny':3000,'assignment':'R103公卫/R205儿童/R302妹妹'}])
edit('A09',350,280,450,name='五只国产面盆龙头',model='九牧32846 亮银1B',
 price_basis='每只预算350元；官网商品页曾显示338元，未选地区/库存0，不能标为已核实可成交现价',
 source_ids=['v_tap'],dimensions={'overall_mm':None,'hole_diameter_mm':None},
 model_fit='继续搭配原候选TVÄLLEN陶瓷盆，但单孔直径、龙头高度和水流落点尚待厂家图与样品复核。',
 installation_dependencies=['确认单孔台盆安装孔径、台面厚度和出水嘴投影，防止水流冲盆沿','冷热水角阀保留检修，按确切型号核对连接软管规格及是否随箱','选亮银1B，避免把不同颜色或活动起价当同一SKU；不要使用已失效的首页239元秒杀链接'],
 included='5只龙头设备预算；标准连接件是否随箱须书面确认',excluded='角阀、安装人工和加长软管按合同另核')
edit('A11',7000,5400,9200,quantity=1,unit='组',name='四处淋浴分档配置',
 model='九牧26195恒温款×2（父母/主卫）；36669亮银1B普通款×2（儿童/妹妹）',
 price_basis='套组预算：2×2400+2×1100；网页促销/颜色/安装条件不一致，未把低起价当四套安装总价',
 source_ids=['v_shower_main','v_shower_other'],
 dimensions={'overall_mm':None,'main_shower_shelf_width_mm':360,'main_top_shower_diameter_mm':300,'required_dynamic_pressure_MPa':None},
 model_fit='保持4处原淋浴位置。父母和主卫采用恒温、带手持的26195；其他两间采用可维护的普通混水花洒。公卫不加淋浴。',
 installation_dependencies=['26195页面列36厘米置物台与30厘米顶喷；勿把26209的45厘米台/32厘米顶喷误当26195，完整安装图仍待厂家提供','36669亮银1B在官网明确不包安装，预算须留出人工；不可只看枪灰包安装标题','取得整套手持、软管、阀体清单和冷热管距/高度图，按三楼动态水压及实际热水能力确定是否可用恒温款','普通混水花洒与热源控温一起调试，设置家庭合适热水温度并试用，不假定省掉恒温阀即可忽略烫伤风险'],
 included='两套26195恒温完整花洒与两套36669普通完整花洒及基础安装附件的整组预算',
 excluded='淋浴玻璃、地漏、防水、结构钻孔；原14,000元四套TOTO预算仅作为升级备选，不与本项相加',
 components=[{'model':'九牧26195','quantity':2,'unit_allowance_cny':2400,'total_cny':4800,'assignment':'父母/主卫'},
 {'model':'九牧36669 亮银1B','quantity':2,'unit_allowance_cny':1100,'total_cny':2200,'assignment':'儿童/妹妹；包含人工预留，官网亮银版不包安装'}])
edit('A13',8990,7100,11600,name='30个基础灯位：国产简洁主灯及适用湿区/户外灯',
 model='室内干区米家D40×4、D30×14作可调光系列候选；厨房/卫浴/户外按防护选型',
 price_basis='细项设计预算：D40 4×430+D30 14×330+厨房2×200+卫浴5×200+户外5×250；并非厂家当前报价',
 source_ids=['v_lights'],
 dimensions={'D40_China_version_mm':None,'D30_China_version_mm':None,'final_lumen_calculation':None},
 model_fit='保留P02全部30个基础灯位，不统一每处装同样大的灯。18个干区以国产D系列作为供货候选，按原位逐区计算照度后确定D30/D40数量组合；4+14是数量预算，不是已验证照度。',
 installation_dependencies=['官方入口已确认L60、D40和D30套系存在，未取得有效单灯现价；上述430/330为预算，不沿用2024首发价','干区候选需供应商提交准确中国版本、外形、光通量、调光调色和安装说明；不将港台版参数直接用于大陆采购','湿区和户外仍独立预算并核安装分区防护，米家普通干区灯不能替代；厨房/卫浴灯宜简洁易清洁','不做无主灯满吊顶，不增加装饰线性灯；保留足够照度、好显色与可维护接线。开关/驱动兼容性须按最终型号确认'],
 included='30套基础灯具预算；每个功能位置保留，有效减少品牌/装饰溢价',
 excluded='照明电线、开关插座和人工归施工合同；A14工作灯、A15床头灯、A19补光另计',
 components=[{'name':'较大干区主灯','model':'米家D40中国版候选','quantity':4,'unit_allowance_cny':430,'total_cny':1720},
 {'name':'其他干区主灯','model':'米家D30中国版候选','quantity':14,'unit_allowance_cny':330,'total_cny':4620},
 {'name':'厨房基础灯','model':'防护/清洁性与照度选型待定','quantity':2,'unit_allowance_cny':200,'total_cny':400},
 {'name':'卫浴基础灯','model':'按湿区安装分区选型','quantity':5,'unit_allowance_cny':200,'total_cny':1000},
 {'name':'花园基础灯','model':'合格防雨灯，优先IP65并核实际工况','quantity':5,'unit_allowance_cny':250,'total_cny':1250}])
edit('A16',4500,3500,6500,
 name='四处淋浴暖风排风+公卫排风，功能实用款',
 model='国内常规暖风/排风机型待浴室风量、湿区与吊顶净空选型',
 price_basis='数量拆分预算：四套900元+公卫300元+常规管道止逆安装600元；未取得项目设备报价',
 dimensions={'heated_bathrooms':4,'powder_rooms':1,'final_airflow_m3h':None,'fan_size_mm':None},
 included='4套普通暖风排风、1套公卫排风、常规风管止逆和安装的预算',
 excluded='专用电源线路由电气施工计；需要长管/高阻力或特殊吊顶时重新核报价，不削减必要风量',
 components=[{'name':'淋浴间暖风排风','quantity':4,'unit_allowance_cny':900,'total_cny':3600},
 {'name':'公卫排风','quantity':1,'unit_allowance_cny':300,'total_cny':300},
 {'name':'常规风管/止逆/安装','quantity':1,'total_cny':600}])
edit('A17',30592,28000,42000,
 name='按八个使用分区预留的独立分体空调',
 model='七个房间挂机+一个公共区柜机的数量预算；海尔KFR-35GW/EC1-1及KFR-72LW/E1-1仅为价格/安装尺寸锚点',
 price_basis='七台挂机官方参考2599×7=18193；一台柜机官方参考6399；附加安装及容量调整预留6000，共30592。尚未做热负荷选型。',
 source_ids=['v_ac_wall','v_ac_floor','hvac_install'],
 dimensions={'provisional_indoor_unit_count':8,'provisional_outdoor_unit_count':8,'wall_reference_mm':{'indoor_W':845,'indoor_D':205,'indoor_H':300,'outdoor_W':820,'outdoor_D':325,'outdoor_H':550},'floor_reference_mm':{'indoor_W':364,'indoor_D':424,'indoor_H':1830,'outdoor_W':889,'outdoor_D':355,'outdoor_H':643},'final_room_loads_kW':None},
 room_ids=['R101','R108','R201','R204','R301','R303','R304','R104/R105'],
 model_fit='按父母、操盘、夫妻、未来儿童、妹妹、书法、毛线七个可关门房间及客餐公共区共八分区列预算。原图外立面能否容纳八台室外机尚未确认，不代表已批准机位；衣帽区和走廊不另机械加空调。',
 installation_dependencies=['逐房按围护/玻璃、朝向遮阳、层高、人员电脑及通风计算夏季冷负荷和冬季热负荷；不能凭2599元价格把七间强定为1.5匹','客厅与餐厅是否能用同一公共区机组由实测连通性、送风路径和负荷决定；不足时调整数量/容量，从预留并重新报价','八台室外机的合法机位、维护通道、散热短路、外观/邻户噪声和冷凝排水需先确认；不足则比较小多联或局部风管，不能挡门窗','设备参考总价24592与安装预留6000分列；标准安装若本已包含不得再次收同项，超长铜管、支架、墙孔等按实际明细','未来儿童房若暂空置可先做套管、电源和排水，延后购一台；主推荐为长期预算仍保留该台，不虚报节约'],
 included='8个使用分区的设备参考预算及6000元附加安装/容量调整预留；其中冷媒管与排水必须按实际长度结算',
 excluded='新风、地暖、全屋除湿、电表增容和外墙结构施工；中央/多联系统作为替换升级方案，不叠加',
 components=[{'name':'七个房间挂机参考','model':'KFR-35GW/EC1-1，容量待逐房核定','quantity':7,'unit_reference_cny':2599,'total_cny':18193,'rooms':['R101','R108','R201','R204','R301','R303','R304']},
 {'name':'公共区柜机参考','model':'KFR-72LW/E1-1，容量与一机覆盖条件待核','quantity':1,'unit_reference_cny':6399,'total_cny':6399,'rooms':['R104','R105']},
 {'name':'附加安装与容量调整','model':'按实际管长、支架、检修及最终容量核算','quantity':1,'allowance_cny':6000,'total_cny':6000}])
edit('A18',10000,8500,16000,
 name='三层生活热水：单热源+必要保温/按需回水预算',
 model='有合适天然气条件时，以海尔JSQ38-20HT5DPXGU1 20L为价格/尺寸候选；系统最终容量待同时用水计算',
 price_basis='单机官方参考3599+按需回水/阀控预留2400+安装排烟附材1500+保温/调试/能力调整2501；共10000元。非全屋性能承诺。',
 source_ids=['v_hotwater'],
 dimensions={'reference_H_mm':540,'reference_W_mm':340,'reference_D_mm':175,'reference_nominal_output_L_min':20,'reference_nominal_gas_heat_input_kW':37.5,'final_simultaneous_flow_L_min':None},
 model_fit='毛坯阶段优先把热水管与可行回水路径、保温一起设计，减少三层等待。仍保留4个淋浴点，但20L单机不是四淋浴可同时开放的保证；如果家庭要求冬季两/三处持续同时淋浴，需升容或改储热系统。',
 installation_dependencies=['确认入户天然气容量、合法排烟位置和最不利三楼动态水压；若无燃气，改空气能储热方案并按机位/负荷重新报价，不套用本主预算','按冬季进水温度与设定出水温差、两人同时用水期望和实际花洒流量计算；标称20L/min取决于标准测试温升，现场可用流量会变','回水采用按需控制，厂家须书面确认本机能配所选循环方案，不随意外加泵；若不兼容则更换同等级合适热源并重核价','公共热水长支路做合理保温和维护口；无需自动全天循环、全屋每点都追求瞬热，不以省钱取消必要控温','保留当前四处淋浴供水但不强制全部同时；若用户明确同时用水需求超出单热源能力，要在采购冻结前调整'],
 included='一种热源、按需循环/阀控的必要设备预留及常规安装/排烟附材、保温和调试',
 excluded='给水总包若已含管路/保温须扣重；燃气开户/增容、外立面工程、异常大储热系统；不是指定20L一定够用',
 components=[{'name':'热源尺寸/价格参考','model':'JSQ38-20HT5DPXGU1','quantity':1,'official_reference_cny':3599,'total_cny':3599},
 {'name':'按需回水及阀控','model':'按最终厂家兼容方案选定','quantity':1,'allowance_cny':2400,'total_cny':2400},
 {'name':'安装与排烟附材','quantity':1,'allowance_cny':1500,'total_cny':1500},
 {'name':'保温/调试/能力调整','quantity':1,'allowance_cny':2501,'total_cny':2501}])

for r in recommended:
    r['original_research_id']=r['id']
    r['scope_decision']='retain' if r['total_cny']==old[r['id']]['total_cny'] else 'replace_with_value_choice'
    r['saving_vs_original_cny']=round(old[r['id']]['total_cny']-r['total_cny'],2)
    r.setdefault('price_status',('public_reference_or_display_not_binding' if '预算' not in r['price_basis'] else 'budget_allowance_not_quote'))
deferred=[copy.deepcopy(x) for x in data['items'] if not x['required']]
for r in deferred:
    r['scope_decision']='defer_until_after_move_in'
    r['deferral_reason']='先用现有设备，入住后按实际湿度、清洁或办公需要购买；未计入价值版必配总额。'
    if r['id'] in ['O01','O02']:
        r['source_verification_note']='本轮搜索摘要识别为目标商品，但直接打开相同product_id存在标题不一致/缓存差异；作为型号检索线索，不能当已验证可直接下单链接。'
        r['purchase_status']='延期；先重新核对中国版本型号和官方有效商品页。'
def totals(rows):return {k:round(sum(r[k] for r in rows),2) for k in ['low_total_cny','total_cny','high_total_cny']}
t={'recommended_goods_excluding_systems':totals([x for x in recommended if x['category']!='systems']),
   'recommended_systems':totals([x for x in recommended if x['category']=='systems']),
   'recommended_all':totals(recommended),'deferred_optional':totals(deferred),
   'by_category':{c:totals([r for r in recommended if r['category']==c]) for c in sorted(set(r['category'] for r in recommended))}}
savings=[{'id':r['id'],'name':r['name'],'original_cny':old[r['id']]['total_cny'],'recommended_cny':r['total_cny'],'saving_cny':r['saving_vs_original_cny'],'method':r['price_basis']} for r in recommended if r['saving_vs_original_cny']]
value={
 'version':'2026-09-10-value-1','title':'毛坯长期自住：钱花在使用频率和维护上','user_context':['毛坯','预算不太多，但需要的地方要花','长期自住','当前4名家人，未来妻子与孩子属于预留'],
 'status':'新的推荐预算；旧items与totals保留为来源研究，不应用旧合计作为当前主方案。',
 'recommendedItems':recommended,'excludedDeferred':deferred,'totals':t,'savings':savings,
 'total_saving_vs_original_required_cny':round(data['totals']['required_all']['total_cny']-t['recommended_all']['total_cny'],2),
 'source_notes':['九牧官方页能核对型号/版本，但含过期活动、未选择地区和库存0提示；未把网页低促销价当杭州可成交价，使用明确预算。','米家主灯官方22569入口直接打开标题可核，仅证实套系名称；没有把2024新闻首发价写成2026现价，也没有把港台版本外形移用到大陆。','部分小米可选商品搜索结果与直接页标题不一致，列为延期并等待再次核验。'],
 'value_principles':['不削减五卫功能、必要防水/水电、检修、接地和排风。','父母/主卫保留恒温淋浴和合适座圈体验；其他卫生间用普通可靠功能。','工作照明A14、床头A15、镜前/厨房补光/夜灯A19保留，基础主灯减少装饰溢价。','按八个实际使用分区列空调数量预算，型号容量未冻结；独立维修的分体为主，小多联/中央系统是机位不够时的替换比较。','未来儿童房设备可延后，但本长期主推荐仍预留其必要空调与照明；不靠省略未来功能凑预算。'],
 'conditional_defer_options':[{'item':'未来儿童房单台挂机设备','reference_saving_cny':2599,'condition':'该房短期不使用且用户确认；套管/电源/排水先落实，安装预留金额按实际重算。','included_in_current_recommended':True}],
 'upgrade_alternatives_not_added':[{'item':'全屋多联/中央空调','basis':'原研究A17的55,000元系统预留仅作升级比较，先拿独立分体实际机位与负荷结果比；二选一。'},{'item':'四处TOTO恒温花洒','basis':'原A11 14,000元，可选升级但不与九牧分档主方案相加。'},{'item':'更高并发热水/空气能储热','basis':'若气源不具备或同时淋浴需求较高，按储热和运行费用重新设计报价；不是在10,000元上任意声称已经包含。'}],
 'new_sources':[v for k,v in sources.items() if k.startswith('v_')]}
data['valuePlan']=value
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'appliances-value.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 毛坯长期自住：家电、卫浴与灯具价值版',f'核查日期：{date}。本版为最新推荐；原始采购研究保留供比较。','',
 f"必配采购与机电系统合计 **¥{t['recommended_all']['total_cny']:,.0f}**，比原研究方案少 **¥{value['total_saving_vs_original_required_cny']:,.0f}**。这是本子表预算，不是整个房子的装修总价。公开参考价与估算分开，未把过期促销、国补或会员价当承诺。",'',
 '|范围|低位预算|推荐预算|高位预算|','|---|---:|---:|---:|']
for key,label in [('recommended_goods_excluding_systems','必配商品'),('recommended_systems','空调、热水与浴室通风'),('recommended_all','本表推荐合计'),('deferred_optional','延期可选项，不含在推荐合计')]:
    z=t[key];lines.append(f"|{label}|¥{z['low_total_cny']:,.0f}|¥{z['total_cny']:,.0f}|¥{z['high_total_cny']:,.0f}|")
lines+=['','## 省在哪里','', '|调整|原研究|新推荐|差额|','|---|---:|---:|---:|']
for s in savings:lines.append(f"|{s['name']}|¥{s['original_cny']:,.0f}|¥{s['recommended_cny']:,.0f}|¥{s['saving_cny']:,.0f}|")
lines+=['','不是把同样东西的报价随意打折：坐便/花洒/龙头改为明确国产候选并按常用房间分档；空调变成能逐项核对的分体设备加安装预算；取消高价装饰灯的倾向。工作照明、防水、电气保护、维护空间与多层热水等待问题继续保留。','',
 '## 推荐采购明细','', '|编号|项目与准确候选|数量|预算小计|价格状态|','|---|---|---|---:|---|']
for r in recommended:lines.append(f"|{r['id']}|{r['name']}：{r['model']}|{r['quantity']}{r['unit']}|¥{r['total_cny']:,.0f}|{r['price_basis']}|")
lines+=['','## 空调和热水不能省略的确认','',
 '空调预算按7个可关门房间+客餐公共区共8区拆分：7×2599+6399+6000=30592元。七台1.5匹和一台3匹仅用于形成可审查的设备价锚点，不能视为已经按每间负荷选定。逐房负荷、客餐厅连通性、八个合法室外机位和冷凝排水必须确认后才下单。若外立面放不下，应比较小多联等方案，不占窗、不挤消防和检修通道。',
 '', '热水按3599元20升热源参考，加必要按需回水/保温、阀控和安装调试预留到10000元。20升标称产率受标准温升约束，冬季实际可用总流量会下降，不能保证四淋浴或高流量双淋浴同时使用。毛坯阶段先解决气源容量、最高层动态水压、回水管与保温；热源和回水控制必须由厂家确认兼容。无燃气或要求高并发则重新比较储热方案。','',
 '## 变更项目的具体规格、安装与来源','']
for r in recommended:
    if r['scope_decision']=='retain':continue
    lines += [f"### {r['id']} {r['name']}",'',r['model_fit'],'','规格核查：'+json.dumps(r['dimensions'],ensure_ascii=False)+'。null表示未取得可施工的准确参数。','']
    lines += ['- '+x for x in r['installation_dependencies']]
    lines += ['','包含：'+r['included']+'。','未包含：'+r['excluded']+'。','']
    if r['components']:lines+=['组内预算：']+['- '+json.dumps(c,ensure_ascii=False) for c in r['components']]+['']
    if r['sources']:lines+=['来源：'+'；'.join(f"[{s['title']}]({s['url']})" for s in r['sources'])+'。','']
lines+=['## 可以后买','',
 '除湿机、扫拖机器人、新增三屏与UPS合计预算10205元，先不买。先用现有设备；入住后按湿度、清洁和办公需要再补。未来儿童房的独立空调也可在该房暂不用时延期，但本版长期推荐仍保留它的2599元设备参考，没有将这笔当已发生节省。','',
 '九牧多款页面显示未选地区且库存0；部分小米可选商品的搜索摘要与直接页标题不一致。这些候选要经杭州供货渠道核对真实在售版本、到手价和安装图后才能冻结。没有采购、付款或联系商家。']
(ROOT/'appliances-value.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'totals':t,'saving':value['total_saving_vs_original_required_cny']},ensure_ascii=False,indent=2))
