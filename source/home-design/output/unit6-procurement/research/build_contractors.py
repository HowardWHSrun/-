import json
from pathlib import Path

OUT = Path(__file__).parent
DATE = '2026-09-10'
sources = []
def src(id, title, url, publisher, typ='企业官方', published=None, note=''):
    sources.append(dict(id=id,title=title,url=url,publisher=publisher,type=typ,accessedAt=DATE,publishedAt=published,limits=note))

src('C01','铭品装饰：企业简介','https://www.mpzs.com/about.html','浙江铭品装饰工程有限公司')
src('C02','铭品装饰：联系我们及城市分站','https://www.mpzs.com/contact.html','浙江铭品装饰工程有限公司',note='页面有默认计算器数值，没有输入本案数据，未将默认数字当报价。')
src('C03','铭品别墅大宅服务','https://www.mpzs.com/villa.html','浙江铭品装饰工程有限公司')
src('C04','富阳自建房793㎡温馨极简案例','https://www.mpzs.com/case/info_491.html','浙江铭品装饰工程有限公司',note='企业自述案例，面积非本案；未独立实地核验。')
src('C05','藏龙大境240㎡现代合院案例','https://www.mpzs.com/case/info_518.html','浙江铭品装饰工程有限公司',note='企业自述案例，不证明本案实际派出班组的能力。')
src('C06','2024年企业标准领跑者名单','https://www.cnis.ac.cn/ynbm/zhfy/tzgg/202501/P020250120387662984599.pdf','中国标准化研究院','官方机构','2025-01-20','列有浙江铭品装饰工程有限公司Q/MP102-2021；这不是当期营业/承包资质或履约保证。')
src('C07','南鸿装饰：品牌实力','https://www.nhzs.com/gywm/ppsl.html','浙江南鸿装饰股份有限公司')
src('C08','南鸿装饰官网联系资料','https://www.nhzs.cn/index.php/welcome.html','浙江南鸿装饰股份有限公司')
src('C09','南鸿1199整装套餐','https://www.nhzs.com/tc/1199tc.html','浙江南鸿装饰股份有限公司',note='公开套餐名称和部分材料类别；本案适用范围、计价面积、门窗/水电限额和增项条件尚未确认。')
src('C10','嘉绿名苑西区300㎡现代简约别墅案例','https://www.nhzs.com/info_anli/3014.html','浙江南鸿装饰股份有限公司','企业官方','2024-01-15','企业自述历史案例，套系标价不能视作2026年合同成交价。')
src('C11','市装协住宅装饰分会开展自律公约工地履行情况检查','https://www.hzzsxh.com/association-dynamics/1483.html','杭州市建筑装饰行业协会','行业协会',note='列明受检会员包括南鸿、铭品、圣都等；仅证明该次受检，不把报告总体问题归因给某一家，也不作质量评级。')
src('C12','都都装饰官网','https://www.duduzs.cn/','浙江都都装饰有限公司')
src('C13','都都别墅大宅服务','https://www.duduzs.cn/villamansion','浙江都都装饰有限公司',note='检索可读，直接抓取曾超时。')
src('C14','嘉悦府270㎡叠排现代港式案例','https://www.duduzs.cn/cases/788','浙江都都装饰有限公司',note='企业自述案例；风格与本案不同，主要用于查看叠排经验。')
src('C15','都都设计师黄金玲及杭州城西店','https://www.duduzs.cn/design/38','浙江都都装饰有限公司',note='企业页面列大华西溪风情320㎡现代简约及嘉悦府叠排；设计师当前档期和实际派出班组未确认。')
src('C16','尚层杭州品牌及服务区域','https://hz.shangceng.com.cn/about/','尚层装饰（北京）有限公司杭州分公司',note='该页地址写25楼，首页简介写24、26楼；只采用楼宇地址，具体接待楼层待电话确认。')
src('C17','尚层杭州案例与业主故事','https://hz.shangceng.com.cn/','尚层装饰（北京）有限公司杭州分公司',note='企业展示300㎡现代简约别墅和联排改造故事；未独立验证完工状态、承包金额或班组。')
src('C18','圣都整装杭州套餐与门店','https://shengdu.ke.com/hz/?cityId=330100&redirected_from=1&source=shengdu_baidu_sem','贝壳／圣都整装',note='检索页面显示A3s-140及公开门店，普通整装用于价格比较；本次未取得杭州三层别墅专属报价或具体同类案例。')
src('C19','拱墅区2022年度突出贡献企业通知','https://www.gongshu.gov.cn/art/2023/4/20/art_1229113461_1831127.html','杭州市拱墅区人民政府','政府','2023-04-20','列有圣都家居装饰有限公司；历史公开名称核对，不证明当前财务、信用或工地质量。')
src('C20','杭州市住宅室内装饰装修施工合同示范文本HT3301/SF021-2024','https://resource.hzzsxh.com/uploads/editor/20240318/1d6857b176c3cc311695b58387d39e10.pdf','杭州市建筑装饰行业协会','行业协会','2024-03-18','用于合同附件结构参考；具体合同仍须双方结合项目范围审定。')
src('E01','Cibes S80平台式家用电梯','https://www.cibeslift.cn/products/s80/','Cibes西柏思')
src('E02','三层家用电梯价格FAQ','https://www.cibeslift.cn/faq/home-lift-price/1486.html','Cibes西柏思','厂家价格参考','2026-05-30','20–35万元为厂家公开一般三层参考，未对应S80版本、尺寸和本案交付范围。')
src('E03','2026家用电梯价格与报价组成','https://www.cibeslift.cn/wenjian/home-elevator-price-guide.html','Cibes西柏思','厂家价格参考','2026-09-08','14.1万元起为品牌起价，不是本案三层配置承诺价。')
src('E04','Cibes中国官网联系资料','https://www.cibeslift.cn/','Cibes西柏思')
src('E05','Aritco HomeLift Access 2026数据表','https://www.aritco.com/wp-content/uploads/2026/02/Datasheet-Aritco-HomeLift-Access-English.pdf','Aritco Lift AB','厂家技术资料','2026-01','国际标准型号数据；中国销售配置、安装和本地服务须厂家确认。')
src('E06','Aritco Access 900×1480 AC安装平面','https://www.aritco.com/wp-content/uploads/2023/12/900x1480-AC.pdf','Aritco Lift AB','厂家技术资料',note='官网DWG下载目录仍链接此图；只作初选，不能代替本项目厂家签认安装图。')
src('E07','Aritco HomeLift 2026数据表','https://www.aritco.com/wp-content/uploads/2026/02/Datasheet-Aritco-HomeLift-English.pdf','Aritco Lift AB','厂家技术资料','2026-01','S12产品外形不是楼板开孔净尺寸。')
src('E08','Aritco官方型号图纸目录与中国联系资料','https://www.aritco.com/uk/products/dwg-files/','Aritco Lift AB')
src('E09','Aritco中国逸致款服务页面','https://www.aritco.com.cn/products/home-lifts/ahla/','ARITCO瑞特科中国')
src('E10','Cibes品牌三层整体报价参考','https://www.cibeslift.cn/faq/1370.html','Cibes西柏思','厂家价格参考','2025-12-27','Cibes品牌在常见住宅条件下25–35万元；价格分类页当前仍引用。区别于E02泛家用电梯20–35万元，仍非型号报价。')
src('P01','杭州市建筑工程劳务工种人工价格调研会','https://www.hangzhoujx.com/association-dynamics/2627.html','杭州市建筑业协会','行业协会',note='说明人工信息价需按市场采集调整；本次未取得适用2026年9月本案的小型私宅逐工种官方价表。')

common = {
 'contacted':False,'siteVisited':False,'formalQuoteReceived':False,
 'verificationStatus':'公开资料初筛；营业执照、当前资质范围与有效期、具体合同主体、派出工长及班组、近期信用状态均待现场采购阶段核验。',
 'price':{'currency':'CNY','asOf':DATE,'status':'待复测及正式询价','projectAmount':None},
}
def candidate(**kw):
    return {**common,**kw}

candidates = [
 candidate(id='T01',brand='铭品装饰',companyName='浙江铭品装饰工程有限公司',priority='首轮比价',
   website='https://www.mpzs.com/',phone='400-600-3007',address='杭州市上城区天城路295号（文晖大桥东）',
   serviceArea='杭州；官网明确列富阳分站。本小区现场服务、工人交通与售后响应待核实。',
   serviceMode='别墅全案／室内设计与施工；要求另报按本案清单的施工及辅材、主材、定制分项。',
   whyShortlisted='已有富阳极简住宅和现代合院官方案例，适合以现有P02方案为基础做结构边界、机电、定制统筹。',
   evidence=['C01','C02','C03','C04','C05','C06','C11'],
   caseLinks=[{'title':'富阳793㎡温馨极简住宅（面积大于本案）','url':'https://www.mpzs.com/case/info_491.html'},{'title':'藏龙大境240㎡现代合院','url':'https://www.mpzs.com/case/info_518.html'}],
   independentEvidence='2024企业标准领跑者官方名单有该企业；市装协公布受检名单有铭品。只作为存在和参与记录，不作履约保证。',
   uncertainties=['与现有方案衔接是否另收设计深化费','富阳在施工地可否由拟派同一项目经理带看','花园、防水和电梯界面由谁承担总协调','是否接受指定家具品牌和甲供主材，管理费如何计取']),
 candidate(id='T02',brand='南鸿装饰',companyName='浙江南鸿装饰股份有限公司',priority='首轮比价',
   website='https://www.nhzs.com/',phone='400-8800-618',address='杭州市拱墅区绍兴路59号',
   serviceArea='杭州及浙江部分城市；官网有富阳住宅案例，项目地址的服务边界待确认。',
   serviceMode='整装、定制、橱柜及舒适系统；请同时给清单报价与套餐差额对照。',
   whyShortlisted='有现代简约别墅案例，公开标准套餐便于检查费用边界，适合作为舒适实用方向的比价对象。',
   evidence=['C07','C08','C09','C10','C11'],
   caseLinks=[{'title':'嘉绿名苑西区300㎡现代简约别墅','url':'https://www.nhzs.com/info_anli/3014.html'}],
   independentEvidence='杭州市装协公开受检会员名单有南鸿；尚未取得本案班组的独立质量结论。',
   publicPriceEvidence=['R01'],
   uncertainties=['1199套餐对多层、面积、厨房卫生间数量的限制','旧房拆除、修补、跨楼层运输、机电、室外是否另计','装修工程专业承包资质官网自述与当期证书是否一致','使用甲供材料是否增加服务费']),
 candidate(id='T03',brand='都都装饰',companyName='浙江都都装饰有限公司',priority='首轮比价',
   website='https://www.duduzs.cn/',phone='400-600-5508',address='杭州市拱墅区祥富路2号联龙创鑫空间G座1–3层；城西店：西湖区文二西路295号',
   serviceArea='杭州站及杭州门店已核；富阳本小区接单、运输及售后范围待确认。',
   serviceMode='整装、软装定制及排屋别墅；本案施工清单须单独核价。',
   whyShortlisted='可用舒适家产品方向核对简约舒适配套，官网有270㎡叠排及320㎡现代简约住宅展示。',
   evidence=['C12','C13','C14','C15'],
   caseLinks=[{'title':'嘉悦府270㎡叠排现代港式','url':'https://www.duduzs.cn/cases/788'},{'title':'杭州团队及现代简约案例索引','url':'https://www.duduzs.cn/design/38'}],
   independentEvidence='本次取得的是企业官方资料；未获得当期独立信用或工地质检结论。',
   uncertainties=['套餐是否接受现有方案而不整体重做','三层旧改工长的最近案例及在建工地','花园和露台防水/排水是否自营或分包','官网零投诉等宣传未独立核验，不列为评分依据']),
 candidate(id='T04',brand='尚层别墅装饰·杭州',companyName='尚层装饰（北京）有限公司杭州分公司',priority='全案服务比较备选',
   website='https://hz.shangceng.com.cn/',phone='400-001-5820',address='杭州市上城区新业路8号UDC时代大厦A座；官网页面楼层不一致，接待楼层待确认',
   serviceArea='官网写大杭州及周边；富阳项目需书面确认。',
   serviceMode='别墅整体规划、施工、设备与家具定制全案。',
   whyShortlisted='可作为多专业协调能力及全案服务深度的比较对象；本案要求减少装饰造型、控制定制及品牌溢价。',
   evidence=['C16','C17'],
   caseLinks=[{'title':'杭州别墅案例目录','url':'https://hz.shangceng.com.cn/case/'}],
   independentEvidence='本次仅核企业官方服务和展示；未取得当期独立资信或本案班组记录。',
   uncertainties=['能否按简约舒适、明确总投资控制线接单','已有方案深化费、全案管理费与主材服务费是否重复','接受部分甲供家具家电的合同方式','具体合同主体与收款账户是否一致']),
 candidate(id='T05',brand='圣都整装·杭州',companyName='圣都家居装饰有限公司（杭州实际签约分支待确认）',priority='标准整装费用比较备选',
   website='https://shengdu.ke.com/hz/',phone='4001115699',address='圣都整装钱江新城店：杭州市上城区三新路37号中豪江河时代2F',
   serviceArea='杭州站和门店已核；富阳项目服务范围待确认。',
   serviceMode='标准整装；能否承接本案三层旧改及专业接口尚未确认。',
   whyShortlisted='公开A3s-140起价可作为标准整装边界参照，不能直接视作本案可用合同方案。',
   evidence=['C18','C19','C11'],caseLinks=[],
   independentEvidence='拱墅区政府历史企业名单有圣都家居装饰有限公司；市装协受检会员名单有圣都。',
   publicPriceEvidence=['R02'],
   uncertainties=['本次尚未核到足以证明同类三层别墅旧改的杭州具体案例，须先补齐后入围','标准套餐是否限制厨房/卫生间数量、层高与面积计量','电梯、花园、露台及结构合法性深化是否有责任主体']),
]

elevators = [
 dict(id='EL01',brand='Cibes西柏思',model='S80 雅致版（Elegance）',classification='平台式／螺杆驱动／自带一体化井道',
  scope='三层三站单一家庭使用；版本在售、门型和配置待厂家确认。',
  dimensionalEvidence={'minimumPublishedFootprintMm':[1070,940],'platformMm':None,'chosenFootprintMm':None,'openingMm':None,'pitMm':[50,70],'floors':[2,6]},
  interpretation='官网1070×940mm是系列最小尺寸，不是本案选定机身或安装孔。底坑可按厂家方案改为地坪抬高处理；需同时检查首层通行坡度及标高。',
  fitStatus='未适配确认。需厂方出三层立面、总行程、平台净尺寸、门净宽、开门方向、井道外轮廓、检修空间和反力图。',
  finishIntent='白色框体＋透明玻璃＋灰色地板；不选RGB氛围背景升级。',
  manufacturerContact={'phone':'400-9999-076','servicePhone':'400-9990-629','website':'https://www.cibeslift.cn/'},
  price={'currency':'CNY','asOf':DATE,'status':'型号无正式报价；Cibes品牌一般三层参考','low':250000,'high':350000,'referenceId':'R05','scope':'仅作品牌三层电梯系统预算区间，配置、运输、安装、税、服务逐项待确认；结构改造与土建另列。'},
  sources=['E01','E02','E03','E04','E10']),
 dict(id='EL02',brand='ARITCO瑞特科',model='HomeLift Access 逸致款／型号3／900×1480 AC',classification='平台式／螺杆驱动／一体化井道',
  scope='三层三站初选；国际2026规格，国内销售配置和本地安装方案待确认。',
  dimensionalEvidence={'platformMm':[900,1480],'exteriorMm':[1300,1600],'floorOpeningMm':[1305,1630],'openingToleranceMm':{'plus':15,'minus':0},'doorClearMm':800,'ratedLoadKg':410,'pitMm':50,'topHeightMinMm':2240,'floors':[2,6]},
  interpretation='孔口数值仅适用于所链接900×1480 AC标准安装图。现模型井道外1650×1900、净1410×1660mm，扣除孔口后净余量很小，且东开门方向与AC门型尚未核。不能据此断言可装。',
  fitStatus='未适配确认；先核合法性、原结构、每层测量、门前轮椅回转及救援通道，再由厂家签认土建条件。',
  finishIntent='白色RAL9016框体，透明玻璃，耐磨浅灰地板。',
  manufacturerContact={'phone':'400-6233-121','email':'info.china@aritco.com','website':'https://www.aritco.com.cn/'},
  price={'currency':'CNY','asOf':DATE,'status':'未发现国内本型号三层公开价，待厂家正式报价','low':None,'high':None,'scope':'不可把Cibes参考价写为Aritco型号报价；项目电梯系统统一预留需正式询价覆盖。'},
  sources=['E05','E06','E08','E09']),
 dict(id='EL03',brand='ARITCO瑞特科',model='HomeLift S12',classification='家用螺杆式／一体化井道',
  scope='三层三站初选；国际2026规格，国内配置待确认。',
  dimensionalEvidence={'carrierMm':[1000,1200],'exteriorMm':[1366,1250],'floorOpeningMm':None,'ratedLoadKg':400,'pitMm':37,'topHeightMinMm':2225,'floors':[2,6]},
  interpretation='1366×1250mm为产品外形，楼板孔口与装配间隙另需安装图。当前模型净宽1410mm，外形宽方向仅余44mm总间隙；不得据此锁定。S15外形宽1466mm已大于当前1410mm净宽，不能原样套入。',
  fitStatus='未适配确认；门型、轮椅使用舒适度、开门及检修路径、顶层高度需实测和厂家方案。',
  finishIntent='白色框体和浅色地板；普通暖白照明，控制装饰背景墙选配。',
  manufacturerContact={'phone':'400-6233-121','email':'info.china@aritco.com','website':'https://www.aritco.com.cn/'},
  price={'currency':'CNY','asOf':DATE,'status':'未发现国内本型号三层公开价，待厂家正式报价','low':None,'high':None,'scope':'价格须列机身、井道、三层门、运输、安装、税、维保、应急救援及土建分界。'},
  sources=['E07','E08']),
]

priceEvidence=[
 dict(id='R01',item='南鸿1199整装套餐',currency='CNY',unit='元/㎡',advertisedValue=1199,low=None,high=None,asOf=DATE,publishedAt=None,status='企业网站公开套餐标签／非本案报价',sourceIds=['C09'],scope='标准整装页面列瓷砖、地板、卫浴、橱柜、水槽等材料类别；计价面积、数量限额、拆改与多层附加未核。',use='仅用于核对询价量级和费用边界；不得乘本案模型地面面积当总造价。'),
 dict(id='R02',item='圣都杭州A3s-140',currency='CNY',unit='元/140㎡套餐起价',advertisedValue=156110,low=None,high=None,asOf=DATE,publishedAt=None,status='企业网站公开起价／非本案报价',sourceIds=['C18'],scope='官网列量房、设计、主材、辅料、基础施工、保洁、监管、质保；未证实电梯、庭院、空调、全屋定制及本案多层改造在内。',use='普通住宅标准整装参照，不推广为本案单价。'),
 dict(id='R03',item='三层家用电梯一般参考',currency='CNY',unit='元/套',advertisedValue=None,low=200000,high=350000,asOf=DATE,publishedAt='2026-05-30',status='厂家一般市场参考／非独立行情指数／非本案报价',sourceIds=['E02'],scope='一般三层家用电梯；层高、系列、尺寸、门型、安装条件与费用包含项仍未锁定。',use='保留与R05的来源口径差异。Cibes品牌预算优先R05的25–35万元，不取此较低泛参考充当型号价。'),
 dict(id='R04',item='Cibes品牌最新起售价',currency='CNY',unit='元/套起',advertisedValue=141000,low=None,high=None,asOf=DATE,publishedAt='2026-09-08',status='厂家品牌起价／配置待确认／非三层价',sourceIds=['E03'],scope='页面明确需按层数、尺寸、产品、安装及选配出方案，交付组成应逐项确认。',use='仅保留价格来源透明度；不用于压低本案三层预算。'),
 dict(id='R05',item='Cibes品牌三层整体参考',currency='CNY',unit='元/套',advertisedValue=None,low=250000,high=350000,asOf=DATE,publishedAt='2025-12-27',status='厂家品牌整体参考／非型号或本案报价',sourceIds=['E10'],scope='Cibes品牌常见住宅三层整体报价；比R03一般三层20–35万元的对象更具体，空间受限或特殊结构另核。',use='本案若以Cibes候选为基准，电梯系统建议先按25–35万元预留，三家报价后替换；厂家土建分界另列。'),
]

inquiryChecklist = [
 '首轮同发P02平面、点位、材料/家具清单及本采购预算，要求现场复测后逐项报数量、品牌型号、人工、辅材、主材、损耗、税、运杂、管理费。',
 '候选先确认实际城市与小区、房屋现状、物业施工时间和搬运路线，排屋/别墅是否可接；不提交私人联系方式到平台。',
 '核对签约主体营业执照、统一社会信用代码、当期资质及范围、收款账户、拟派项目经理、工长与水电/泥木油班组，不只看品牌。',
 '要求拟派同一工长的两个近两年多层住宅案例：一个在水电/防水阶段、一个已入住经历雨季；经业主同意后安排查看，不私取住户信息。',
 '询问是否接受现有设计和甲供家具家电，设计深化、采购服务费与施工管理费分别列项。',
 '撤除楼梯、楼板开孔、补板、承重及外立面改动先核合法性。施工队口头保证或厂家免底坑宣传不构成许可；未释放项列暂估/暂停，不能安排拆除。',
 '常规施工、机电、定制、家电、家具、花园、电梯七个包用同一界面表，逐项写谁设计、谁采购、谁安装、谁保修。',
 '电梯报价固定三层三站、约6.9m展示行程待复测；列净开门、载重、轮椅/婴儿车实际进入、紧急平层、门锁、安全边、断电救援、保修、年度保养与急修服务。',
 '电梯土建必须书面给设备反力、孔口、底坑、顶层净高、井道固定、机房/检修需求及电源；不要先砌1650×1900井道再选产品。',
 '所有厨房和卫生间分开计量，墙地防水、水路排水、闭水试验、取样和维修责任写清；中央空调、新风及除湿的负荷与风量由专业深化。',
 '南院47.504㎡、主南廊9.797㎡、三层露台18.684㎡为方案/来源边界，不是承包计价测量。室外包须含防水排水界面、轻质花箱、铺装及成品保护，不填天井。',
 '花园苗木写品种、容器规格、冠幅/株高、数量、土壤/基质、灌溉、养护周期与补苗条件，禁止以一项绿化造景费替代明细。',
 '把甲供家具包装尺寸、入户门和楼层搬运路线纳入报价；人工搬运、吊装如需另计，先核现场可实施条件。',
 '询价须明列拆旧清运、找平/基层修复、墙面铲除、瓷砖收口、异形、门套、插座回路、定制五金、开孔、进场保护及开荒的包含与不含项。',
 '付款与已验收工程量挂钩，约定停工/延期、设计变更、甲供延迟、成品损坏、保修留款。变更必须先书面报价并获业主确认；具体比例由双方审定。',
 '报价比较总价时同时比较计量规则和范围；暂估、未决和允许变更项单列，避免用低总价隐藏漏项。'
]

bidSchedule = [
 {'stage':1,'name':'确认地址和复测输入','durationWorkingDays':'2–5（计划假设）','output':'可量房范围、原始结构资料、物业边界、现场尺寸和高差照片','release':'具备现场进入授权'},
 {'stage':2,'name':'三家同口径现场询价','durationWorkingDays':'5–10（计划假设）','output':'分项工程量报价、主材型号、工长履历、现场工期和合同草稿','release':'地址和现场工况确认'},
 {'stage':3,'name':'电梯与关键专业并行深化','durationWorkingDays':'按合法性核验及厂家响应另排','output':'不可实施项、设备条件图、结构/机电责任人和追加成本','release':'先完成合法性和技术条件核实'},
 {'stage':4,'name':'技术澄清及候选对比','durationWorkingDays':'3–5（计划假设）','output':'统一范围比较表、删减/升级项、疑点闭环','release':'至少两份可比完整报价'},
 {'stage':5,'name':'签约和开工条件检查','durationWorkingDays':'随审批和专业出图条件','output':'双方签署合同/附件、品牌型号冻结、分阶段开工单','release':'相应工序合法并已取得所需可施工文件'}
]
scoring = [
 {'item':'合法性和专业边界','weight':25,'evidence':'明确拒绝未释放结构改动；提供负责专业及设备条件图'},
 {'item':'拟派班组的同类项目','weight':25,'evidence':'同一工长实地可核的多层住宅与防水/机电记录'},
 {'item':'报价完整和可比','weight':25,'evidence':'工程量、型号、范围、增项规则、税及管理费透明'},
 {'item':'现场组织与售后','weight':15,'evidence':'进度、人员、验收记录、保修主体与响应约定'},
 {'item':'简约舒适方案匹配','weight':10,'evidence':'在预算控制下保留动线、易清洁、收纳、适老舒适性'}
]

data = dict(schemaVersion='1.0',title='第6户：杭州暂定施工团队初筛与电梯询价依据',asOf=DATE,
 location={'assumedCity':'杭州（优先杭州/富阳服务范围）','basis':'原DWG题签杭州富春玫瑰园华墅地块二期二区','confirmedByUser':False},
 status='仅公开资料研究，未联系企业、未提交表单、未收到报价、未预订或付款。',
 recommendation='首轮邀请铭品、南鸿、都都按同一清单比价；尚层作为全案协调深度备选，圣都先补齐同类三层旧改案例再考虑入围。最终比较实际派出的工长和合同范围。',
 legalBoundary='此处并未确认撤梯、开井、补板等合法或可施工，当前仍不可据P02模型直接开工；须在合法性核验后由相关专业完成可施工文件。',
 measurementBoundary='现有模型是方案量；净井尺寸1410×1660mm和外井1650×1900mm均非已核厂方安装条件。',
 candidates=candidates,elevators=elevators,priceEvidence=priceEvidence,inquiryChecklist=inquiryChecklist,
 bidSchedule=bidSchedule,scoringFramework={'status':'建议评分框架，未给任何企业虚构得分','criteria':scoring},
 estimateGuidance={'currency':'CNY','asOf':DATE,'elevatorSystemAllowance':[250000,350000],'status':'基于E10的Cibes品牌常见三层整体参考预留；不是候选型号报价，也不当作Aritco价格','excluded':'拆梯、开孔补板、结构加固、合法性/专业设计、不可实施时的替代方案费用须单列。','constructionRates':'本次未获得适用本案且2026年9月有效的官方小型私宅逐项人工价格，不将营销文章自称的官方数据当事实。标准套餐仅做交付范围对比，工程预算按方案量与明确假设编制后由现场报价替换。'},
 sources=sources)
(OUT/'contractors.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# 第6户施工团队与电梯初筛',f'更新：{DATE}｜币种：人民币 CNY｜地点暂按杭州/富阳，尚待业主确认。','',data['status'],'',data['recommendation'],'','## 团队候选','',
 '| 候选 | 公开联系方式 | 适合本案的比较角度 | 当前报价 |','|---|---|---|---|']
for c in candidates:
    lines.append(f"| {c['id']} [{c['brand']}]({c['website']}) | {c['phone']}；{c['address']} | {c['whyShortlisted']} | 未获得本案报价 |")
lines+=['','以上为品牌/企业候选，并不等于已落实的施工班组。官网案例和宣传不作独立质量结论。以下首轮核验完毕才建议选定实际承包人。','']
for c in candidates:
    lines += [f"### {c['id']} {c['brand']}",'',f"公开主体：{c['companyName']}。服务：{c['serviceArea']}",'',c['independentEvidence'],'','待核：'+'；'.join(c['uncertainties'])+'。','']
    for ca in c['caseLinks']: lines.append(f"- [案例：{ca['title']}]({ca['url']})")
    lines.append('')
lines += ['## 能用来核对价格的公开信息','',
 '南鸿公开1199元/㎡整装套餐；圣都杭州A3s-140为156,110元起。这些是普通整装标签，不能直接按三层住宅面积换算本案总价；电梯、室外、防水修补、机电、甲供、定制和多层运输边界未核。',[f'- [{s["title"]}]({s["url"]})' for s in sources if s['id'] in ('C09','C18')][0], [f'- [{s["title"]}]({s["url"]})' for s in sources if s['id'] in ('C09','C18')][1],'',
 'Cibes官网泛家用电梯FAQ写一般三层20–35万元；针对Cibes品牌的三层整体报价页面写25–35万元，价格分类页当前仍引用。由于后者对象更具体，本案暂按25–35万元预留Cibes电梯系统；正式配置报价后替换。2026-09-08品牌14.1万元起并非三层保证价。以上均非本案或某一型号的正式报价，土建、结构、合法性及专业深化另列。',
 '- [Cibes品牌三层整体参考25–35万元](https://www.cibeslift.cn/faq/1370.html)',
 '- [三层参考价](https://www.cibeslift.cn/faq/home-lift-price/1486.html)', '- [最新品牌起价与费用组成](https://www.cibeslift.cn/wenjian/home-elevator-price-guide.html)','',
 '## 电梯候选：先确认条件，再锁型号','',
 '| 候选 | 官网尺寸/条件 | 本案适配和价格状态 |','|---|---|---|',
 '| Cibes S80雅致版 | 系列最小占地1070×940mm起；2–6层；底坑50–70mm或厂家认可的地坪处理 | 未选定尺寸与门型；25–35万元是Cibes品牌一般三层整体参考，非S80本案报价 |',
 '| Aritco HomeLift Access 型号3（900×1480 AC） | 平台900×1480；外形1300×1600；410kg；安装图楼板孔1305(+15/-0)×1630(+15/-0)；门净800；底坑50；顶层至少2240mm | 现净井1410×1660余量很小，门向/检修/反力未核；国内型号价待询 |',
 '| Aritco HomeLift S12 | 载台1000×1200；外形1366×1250；400kg；底坑37；顶层至少2225mm，具体工况另核 | 外形不是开孔尺寸，当前1410mm净宽仅比1366mm宽44mm；国内型号价待询 |','',
 '三层三站、东向入梯、家庭未来婴儿车和父母长期使用应写入询价。不得先按模型井道砌筑，再把任意电梯装进去；产品外形、楼板孔、井道、门洞与检修空间是不同尺寸。','']
for s in sources:
    if s['id'] in ('E01','E05','E06','E07','E08'): lines.append(f'- [{s["title"]}]({s["url"]})')
lines += ['','## 同口径询价与合同要点','']
for i,q in enumerate(inquiryChecklist,1): lines.append(f'{i}. {q}')
lines += ['','[杭州住宅装饰装修施工合同示范文本](https://resource.hzzsxh.com/uploads/editor/20240318/1d6857b176c3cc311695b58387d39e10.pdf)可作为附件结构参考；具体条款按本案审定。','',
 '## 初步询价推进顺序','']
for s in bidSchedule: lines.append(f"{s['stage']}. {s['name']}：{s['durationWorkingDays']}。交付：{s['output']}。前提：{s['release']}。")
lines += ['','## 来源与证据边界','']
for s in sources: lines.append(f"- {s['id']} [{s['title']}]({s['url']})｜{s['publisher']}｜访问{DATE}"+(f"；{s['limits']}" if s['limits'] else ''))
(OUT/'contractors.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'candidates':len(candidates),'elevatorModels':len(elevators),'sources':len(sources),'output':str(OUT/'contractors.json')},ensure_ascii=False))
