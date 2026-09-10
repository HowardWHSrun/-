# -*- coding: utf-8 -*-
import json, pathlib, hashlib
OUT=pathlib.Path(__file__).parent
DATE='2026-09-10'
BASE='https://www.ikea.cn/cn/zh/p/'
items=[]
def add(id,name,sku,color,cm,price,rooms,url,includes,fit,stage='复尺后成品采购',excludes='配送、上楼、组装和额外墙体固定件另核'):
    q=sum(rooms.values())
    items.append(dict(id=id,category='成品家具',brand='IKEA 宜家',name=name,model=name.split(' ')[0],sku=sku,color=color,dimensionsCm=cm,quantity=q,rooms=rooms,unitPriceCny=price,totalPriceCny=round(price*q,2),priceBasis='大陆官网商品详情页显示价；非锁价合同，不计过期会员/优惠价',checkedDate=DATE,sourceUrl=BASE+url,includes=includes,excludes=excludes,fitReview=fit,procurementStage=stage,availability='未设置收货地址；页面存在不代表杭州有库存，付款前由供应商确认本货号、交期与配送'))

add('F01','TARVA 塔瓦 床架 / LURÖY 鲁瑞 150','091.985.15','松木 / 鲁瑞',[160,209,92],1299,{'R101':1},'tarva-ta-wa-chuang-jia-song-mu-lu-rui-s09198515/','150×200床架、鲁瑞床板架、SKORVA床中挺；独立包装','按套装页较大外宽160控制；单床架303.544.67页标158，厂家需书面统一。模型床框160×215，长减6；床垫150×200另列。',excludes='床垫、床品、木材涂装、配送上楼及组装另计')
add('F02','TARVA 塔瓦 床架 / LURÖY 鲁瑞 180','891.985.78','松木 / 鲁瑞',[188,209,92],1499,{'R201':1},'tarva-ta-wa-chuang-jia-song-mu-lu-rui-89198578/','180×200床架、鲁瑞床板架及SKORVA床中挺','模型床框190×215；成品宽减2、长减6。床垫180×200单列。',excludes='床垫、床品、木材涂装、配送上楼及组装另计')
add('F03','TARVA 塔瓦 床架 / LURÖY 鲁瑞 120','191.984.78','松木 / 鲁瑞',[128,209,92],999,{'R301':1},'tarva-ta-wa-chuang-jia-song-mu-lu-rui-19198478/','120×200床架及鲁瑞床板架','妹妹模型床框145×215；成品128×209可减占地，床垫由意向135改120。若坚持135，另做总外宽不大于145的定制床并重新复核；不能直接替换150床。',excludes='床垫、床品、木材涂装、配送上楼及组装另计')
add('F04','NESTTUN 奈斯顿 床架 / LURÖY 鲁瑞 90','691.580.26','白色 / 鲁瑞',[96,207,86],699,{'R204':1},'nesttun-nai-si-dun-chuang-jia-bai-se-lu-rui-69158026/','90×200床架及鲁瑞床板架','模型儿童预留床框110×215；成品96×207。按弹性客卧/较大儿童后期家具作预算，不作为婴儿床或幼儿防坠方案。','未来房间按实际年龄再定',excludes='床垫、床品及适龄安全配件另列；配送上楼组装另计')
add('F05','VALEVÅG 瓦勒沃格 袋装弹簧床垫 150','304.506.71','硬型 / 浅蓝色',[150,200,24],1799,{'R101':1},'valevag-wa-le-wo-ge-dai-zhuang-dan-huang-chuang-dian-ying-xing-qian-lan-se-30450671/','单张床垫','匹配F01的床垫尺寸；硬度为商品标签，父母须共同试躺，不按年龄推断必须睡最硬。',excludes='床架、床板、床褥、保护垫、床品及配送另计')
add('F06','VALEVÅG 瓦勒沃格 袋装弹簧床垫 180','804.700.06','加硬 / 浅蓝色',[180,200,24],2299,{'R201':1},'valevag-wa-le-wo-ge-dai-zhuang-dan-huang-chuang-dian-jia-ying-qian-lan-se-80470006/','单张床垫','匹配F02；夫妻应共同试躺确认硬度、翻身干扰及床沿坐感。',excludes='床架、床板、床褥、保护垫、床品及配送另计')
add('F07','VALEVÅG 瓦勒沃格 袋装弹簧床垫 120','004.699.07','加硬 / 浅蓝色',[120,200,24],1499,{'R301':1},'valevag-wa-le-wo-ge-dai-zhuang-dan-huang-chuang-dian-jia-ying-qian-lan-se-00469907/','单张床垫','匹配F03，不能将120床垫作为135床垫采购；试躺后可同尺寸换硬度货号。',excludes='床架、床板、床褥、保护垫、床品及配送另计')
add('F08','VALEVÅG 瓦勒沃格 袋装弹簧床垫 90','404.700.27','加硬 / 浅蓝色',[90,200,24],1299,{'R204':1},'valevag-wa-le-wo-ge-dai-zhuang-dan-huang-chuang-dian-jia-ying-qian-lan-se-40470027/','单张床垫','匹配F04；该项为未来弹性客卧预算，儿童实际使用时按年龄和床架安全要求复选。','未来房间按实际年龄再定',excludes='床架、床板、床褥、保护垫、床品及配送另计')
add('F09','TONSTAD 图恩斯塔 床头桌','605.100.08','灰白',[40,40,59],599,{'R101':2,'R201':2,'R301':1},'tonstad-tu-en-si-ta-chuang-tou-zhuo-hui-bai-60510008/','床头桌及抽屉','父母模型48×48，夫妻/妹妹需按床位现场纸样；59高需与最终床面高度试取物，插座不能被柜挡。')
add('F10','VIMLE 维姆勒 三人沙发','393.990.32','刚纳瑞德 米黄色',[241,98,83],2999,{'R104':1},'vimle-wei-mu-le-san-ren-sha-fa-gang-na-rui-de-mi-huang-se-s39399032/','三人框架、两扶手、相应米色可拆洗罩套及坐靠垫；非仅罩套','模型265×约92；成品较短24、深增加约6。维持朝东并复核沙发前通道；须以整体98深纸样复核，当前漫游并未替换为该SKU。',excludes='头枕、脚凳、装饰靠枕、配送组装另计')
add('F11','LISABO 利萨伯 茶几','103.530.63','白蜡木贴面',[118,50,50],799,{'R104':1},'lisabo-li-sa-bo-cha-ji-bai-zha-mu-tie-mian-10353063/','茶几','模型约120×70，平面占地减小；台高由展示意向约39升至50，配48高沙发座，宜现场试坐取物。')
add('F12','BRIMNES 百灵 电视柜','504.098.93','白色',[180,41,53],799,{'R104':1},'brimnes-bai-ling-dian-shi-gui-bai-se-50409893/','电视柜及抽屉','模型230×40×48；长缩50、深增1、高增5。沿东墙保留原室外门；电视型号/脚座跨度和重量另核；网页柜顶承重30kg。',excludes='电视、支架、设备、墙体固定件及配送组装另计')
add('F13','EKEDALEN 伊克多兰 伸缩型餐桌','503.408.13','橡木',[180,80,75],1999,{'R105':1},'ekedalen-yi-ke-duo-lan-shen-suo-xing-can-zhuo-xiang-mu-50340813/','伸缩桌及1块加长板','收拢120×80、展开180×80；按6人展开180计，占地小于模型180×85。六椅采用两侧各2、两端各1，拉椅后核电梯/厨房通路。不要照搬模型同侧3把椅子的摆法。',excludes='餐椅、保护脚垫及配送组装另计')
add('F14','EKEDALEN 伊克多兰 软垫椅','203.410.22','橡木 / 欧斯塔 淡灰色',[45,51,95],499,{'R105':6,'R303':1},'ekedalen-yi-ke-duo-lan-yi-zi-xiang-mu-ou-si-ta-dan-hui-se-20341022/','椅架、座垫和所选罩套','座高48。餐厅比模型约47×45深6；布置改2+2+1+1并留后撤。书法椅为坐姿短时使用，站写时移靠墙。',excludes='额外罩套、地板保护垫及配送组装另计')
add('F15','MARKUS 马库斯 人体工学办公椅 小号','805.887.94','威索尔 深灰色',[64,64,129],799,{'R108':1,'R304':1,'R301':1,'R204':1},'markus-ma-ku-si-ban-gong-yi-wei-suo-er-shen-hui-se-80588794/','办公椅，含产品配套头枕/扶手','高度118–129、座高43–54、底盘64×64；比模型普通椅大，必须按真实底盘、后仰及退椅走样；先试坐再定大小号。儿童房这把仅为未来客卧/较大儿童预算，不按幼儿适用宣称。','R108/R304须先确认原梯区方案可实施；R204延后；R301复尺后',excludes='脚踏、地板保护垫及配送组装另计')
add('F16','MICKE 米克 书桌 73','803.542.81','白色',[73,50,75],399,{'R204':1},'micke-desk-white-80354281/','小书桌及抽屉','模型90×55；成品73×50可留更多通路。固定75高并不适合所有年龄，儿童实际启用时按身高换桌椅组合。','未来房间按实际年龄再定')
add('F17','MICKE 米克 书桌 105','803.542.76','白色',[105,50,75],699,{'R301':1},'micke-desk-white-80354276/','书桌及抽屉/柜；不带高架','模型108×55，成品105×50；只买75高版本，不能换成带高架的140高套装。抽屉方向与书桌椅退让现场确认。')
add('F18','BILLY 毕利 矮书架','905.220.38','白色',[40,28,106],199,{'R206':3,'R108':2},'billy-bookcase-white-90522038/','单体书架与配套层板','R206三件并排120×28，低于原155×34×190；R108两件并排80。沿原实墙布置，不能堆叠；降低储书量换取通透和可移动性。','原梯区可实施条件明确后定位',excludes='柜门、额外层板、防倾倒基层固定件、配送组装另计')
add('F19','BILLY 毕利 / OXBERG 奥克伯 带门书柜','795.283.48','白色 / 玻璃',[40,30,202],449,{'R304':3},'billy-bi-li-oxberg-ao-ke-bo-dai-ban-bo-li-men-shu-gui-bai-se-bo-li-s79528348/','书架与所选板/玻璃门套装','三件120×30×202，较模型毛线柜145×30×190更窄但高12；靠西实墙复核窗帘和墙面电点。柜门有缝，不能称密封柜；毛线加带盖盒。','原梯区可实施条件明确后定位',excludes='额外内配、防倾倒基层固定件、配送组装另计')
add('F20','SAMLA 萨姆拉 附盖储物盒 5L','194.408.48','透明',[28,20,14],9.99,{'R304':12,'R204':6},'samla-box-with-lid-transparent-19440848/','盒体与盖，合计9.99；不重复加盖价','用于按线色/小件分类；横向28、进深20放入30深书柜，每格1盒为基准。非密封防潮箱，勿湿线入柜。','R304方案批准后；R204按需延后',excludes='标签、干燥剂及配送另计')
add('F21','POÄNG 波昂 单人扶手椅','192.407.88','桦木贴面 / 基尼萨 浅米色',[68,83,100],499,{'R104':1,'R206':1},'poaeng-bo-ang-dan-ren-sha-fa-fu-shou-yi-hua-mu-tie-mian-ji-ni-sa-dan-mi-se-s19240788/','椅框及所选椅垫','真实68×83明显大于模型窗边普通椅，列有条件替代，预留约80×100静态区并核前方起身空间；不得直接声称模型已验证。座高40，对父母须试起坐；如偏低改中高座扶手椅另询价。','现场纸样通过后；R206功能条件先明确',excludes='脚凳及配送组装另计')
add('F22','GLADOM 格拉登 托盘边桌','503.378.20','白色',[45,45,53],79.99,{'R104':1,'R206':1},'gladom-tray-table-white-50337820/','托盘与桌架','室内阅读角可移动边桌，圆形直径45；与POÄNG同时做纸样，不能占主通路。未用作户外耐候家具。','现场纸样通过后；R206功能条件先明确')
add('F23','NÄMMARÖ 耐玛瑞 户外桌','805.112.00','着浅褐色漆',[140,75,75],999,{'R109':1},'naemmaroe-nai-ma-rui-zhuo-zi-hu-wai-zhao-qian-he-se-qi-80511200/','户外木桌','平面140×75小于模型G1-T01的145×78；高度改75餐桌高，配45座高四椅，保留长边两侧各2。不是模型低茶几高度。','南院产权、承载、防水、排水及坡道位置确认后',excludes='椅子、家具罩、养护油、配送组装另计')
add('F24','NÄMMARÖ 耐玛瑞 户外折叠椅','705.103.43','着浅褐色漆',[49,50,81],299,{'R109':4},'70510343/','折叠木椅','座高45；比示意普通椅略大，配F23复核4把拉椅后到坡道的通路；不用躺椅替换。','南院范围及防水承载条件确认后',excludes='坐垫、家具罩、养护油及配送另计')
add('F25','KUDDARNA 库达那 户外椅垫','805.472.23','浅米灰色',[36,32,6],29.99,{'R109':4},'kuddarna-ku-da-na-yi-dian-hu-wai-qian-mi-hui-se-80547223/','单件椅垫','放在44×44的椅座居中系紧，垫小于椅座；雨后收纳晾干；坐高增加约6，须实坐确认。','随F24采购')
add('F26','NÄMMARÖ 耐玛瑞 户外长椅','105.103.41','着浅褐色漆',[120,40,45],499,{'R305':1},'naemmaroe-nai-ma-rui-chang-yi-hu-wai-zhao-qian-he-se-qi-10510341/','木长椅','替代G3-B01意向坐凳；按120×40沿原长向放置。与花箱、排水口及门区联合复尺，不贴近边缘形成攀爬踏脚。','露台结构、防水、排水与防护条件确认后',excludes='坐垫、家具罩、养护油及配送组装另计')

custom=[]
def cust(id,name,room,cm,low,mid,high,note,tag='木作定制预算（总造价中仅计一次）'):
    custom.append(dict(id=id,name=name,rooms={room:1},quantity=1,model='定制尺寸规格，无成品型号',brand=None,sku=None,dimensionsCm=cm,color='浅木色 / 哑光米白',priceBasis='设计概算额度，非供应商报价；需同图同材询价',unitPriceLowCny=low,unitPriceBaseCny=mid,unitPriceHighCny=high,sourceUrl=None,checkedDate=DATE,scopeTag=tag,requirement=note))
cust('C01','爸爸操盘桌','R108',[148,80,76],1800,2500,3500,'保留原意向外廓；承重底架、显示器支臂夹具加强、后部线槽、可拆检修和圆角。三屏真实尺寸与支架载荷到货前深化。原梯区未获合法实施条件，不下固定桌订单。','活动定制家具')
cust('C02','妈妈编织工作台','R304',[165,70,76],1600,2200,3000,'哑光易擦台面、圆角、桌面下净膝空间；不做妨碍退椅的满深柜。原梯区未明确实施条件，不下固定桌订单。','活动定制家具')
cust('C03','书法长案','R303',[194,90,80],3000,4200,6000,'194沿模型南北长向；整张哑光稳定台面、可换防墨毡、钢木底架，不靠薄台板直接夹重物。本人站写/坐写确认最终高度；不把概念194尺寸当加工净尺。','活动定制家具')
cust('C04','父母衣柜','R101',[165,55,225],3000,4000,5000,'模型55为外深，须把背板/门后实际挂衣净深画出来；必要用侧向拉出挂衣杆，不能直接加深压床侧路。')
cust('C05','夫妻衣柜','R202',[240,55,228],5000,6500,8500,'本预算包含基础柜体、门、常规铰链和挂衣/层板；不含奢侈五金、复杂灯控。55外深不保证常规平挂净深，内部系统和主卫门开启须深化。')
cust('C06','妹妹衣柜','R301',[120,50,220],2400,3200,4500,'保持沿东墙方向；50外深用侧向挂衣及折叠分区，未经重排不放60深标准衣柜。')
cust('C07','儿童预留柜','R204',[120,50,160],1800,2200,3000,'低柜及防倾倒固定，儿童年龄和使用方式未定，延后采购；不可作为攀爬阶梯。')
cust('C08','宣纸与作品收纳柜','R303',[70,44,90],1800,2400,3500,'原模型70×44无法平放模型中68×136的完整宣纸；只可放折纸/册页。完整大纸采用另行设计的立式卷轴筒或在194×90案下设可拆卷存模块，供应商先拿实际纸样；本项不宣称整张平放。')
cust('C09','书法北窗矮柜','R303',[95,34,92],1500,2000,2800,'保持低于已核110窗台；防潮、避日晒，窗帘与窗扇净距复核。')
cust('C10','玄关窄鞋柜','R107',[46,28,110],600,900,1500,'原模型外形仅46×28×110，不足全家全部鞋量；做常用鞋倾斜层板和钥匙收纳，季节鞋进入其他柜体。本项仅这只窄柜。')
cust('C11','露台轻型换盆台','R305',[80,46,85],700,1200,1800,'按最新定位与花箱错开；可拆耐候台面、带沿托盘、收土盒，供水只用经核接口。需承载、防水、排水批准后订。','园林固定/定制设施（勿与园林造价重复）')
cust('C12','露台小圆茶桌','R305',[56,56,49],400,600,1000,'直径56小于模型G3-T01约58，台高49延续示意；耐候可移动，不未经复尺换65方桌。','活动定制家具')

allowances=[
dict(id='A01',name='四床枕被、保护垫与床品',quantity=1,lowCny=3000,baseCny=5000,highCny=8000,basis='设计预算；未指定虚构型号。3常住床+1未来床，各人睡感、材质与季节确定后配单；未来床部分可延后。'),
dict(id='A02',name='成品送货、上楼、组装与基层固定',quantity=1,lowCny=1500,baseCny=2500,highCny=4500,basis='项目预算额度；不是宜家官方服务报价，按地址、楼层、搬入路线和商品工作量结算。'),
dict(id='A03',name='户外家具罩、维护用品与标签脚垫',quantity=1,lowCny=600,baseCny=1000,highCny=1800,basis='项目预算额度；实际家具罩需要按组合外形选择，不预填错误尺寸。'),
]
sum_standard=round(sum(x['totalPriceCny'] for x in items),2)
data=dict(version='P03-采购研究-1.0',title='第6户｜简约舒适家具型号与定制规格',checkedDate=DATE,currency='CNY',style=dict(base='哑光米白、自然浅木色、米灰织物，少量柔和绿色点缀',principles=['优先可拆洗面料、直线柜面和可维修五金','卧室保证通道和床垫睡感，不为成品促销改变原图结构','功能工作桌按个人姿势和真实设备定制','户外木家具需维护；花箱荷载、防水和排水仍待专业确认']),sourceModel='home-design/blender/unit6-professional-scene.json',sourceModelSha256=hashlib.sha256(pathlib.Path('home-design/blender/unit6-professional-scene.json').read_bytes()).hexdigest(),scopeNote='采购建议与设计概算，未购买、未联系商家、未锁库存。当前P02三维模型使用意向家具，不代表已套入本次全部商品。成品型号定稿后须替换外廓复核通道，家具不能用来证明拆梯、开井等改造可以实施。',pricePolicy='以核对日打开的大陆官网详情页显示价记录，不使用已过期促销、境外币种或二手价。网页可能未选收货地区，库存交期须复核；价格是可复查预算锚点，不承诺成交。',fitPolicy='床框与床垫分别核算。表中外廓小于意向家具只说明初步平面尺寸关系，不代替墙面完成面、门扇、拉椅、抽屉、运输、安装与防倾倒检查。所有新增功能房是否可实施先依施工交接文件确认。',items=items,customItems=custom,allowances=allowances,totals=dict(standardProductsCny=sum_standard,customLowCny=sum(x['unitPriceLowCny'] for x in custom),customBaseCny=sum(x['unitPriceBaseCny'] for x in custom),customHighCny=sum(x['unitPriceHighCny'] for x in custom),allowanceLowCny=sum(x['lowCny'] for x in allowances),allowanceBaseCny=sum(x['baseCny'] for x in allowances),allowanceHighCny=sum(x['highCny'] for x in allowances)),countingRules=['成品床架价格已包含所列床板/中挺，不再重复加购计价。','床垫独立列项；不能把床架价视为整套寝具到家价。','C04–C10如已计入全屋木作/柜体预算，须从家具汇总中剔除一份。','C11如已计入园林换盆台预算，须剔除重复；花箱和铺装未计入本家具成品小计。','本列表包含未来儿童房与原梯区条件性布置额度；分期采购可暂缓，不代表现在都应付款。','电器、电脑显示器、灯具、厨房橱柜、卫浴柜、全屋窗帘、地毯、花箱和园林施工不在这份成品家具小计内，须由对应预算表另列。'],releaseChecklist=['现场复尺并用胶带标出家具整体外廓，门/柜/椅同时开启走样','父母试床垫及起坐，三位工作使用者试办公椅与桌高','确认床架套装构成、真实货号、颜色、库存、运输包件和售后','供应商提供定制材料、封边、五金品牌型号、加工图、安装条件与分项报价','不以活动家具订单提前锁定尚未获准的拆梯、楼板及电梯井改造'])
data['totals']['furnitureAllInBaseCny']=round(sum_standard+data['totals']['customBaseCny']+data['totals']['allowanceBaseCny'],2)
data['totals']['furnitureAllInLowCny']=round(sum_standard+data['totals']['customLowCny']+data['totals']['allowanceLowCny'],2)
data['totals']['furnitureAllInHighCny']=round(sum_standard+data['totals']['customHighCny']+data['totals']['allowanceHighCny'],2)
(OUT/'furniture.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 第6户｜简约舒适家具型号与定制规格',f'核对日期：{DATE}；货币：人民币。',data['scopeNote'],data['pricePolicy'],data['fitPolicy'],'## 建议风格',data['style']['base'],'\n'.join('- '+p for p in data['style']['principles']),'## 预算汇总',f'26条成品SKU，按房间数量合计 **¥{sum_standard:,.2f}**。定制规格预算 **¥{data["totals"]["customBaseCny"]:,.0f}**，服务与床品等额度 **¥{data["totals"]["allowanceBaseCny"]:,.0f}**。本家具范围基准 **¥{data["totals"]["furnitureAllInBaseCny"]:,.2f}**，概算区间 **¥{data["totals"]["furnitureAllInLowCny"]:,.2f}–{data["totals"]["furnitureAllInHighCny"]:,.2f}**。这不是装修总价，且须按下方去重规则与全屋预算合并。','## 成品家具','|编号 / 房间及数量|型号 / 货号 / 颜色|外廓cm|官网显示单价|小计|','|---|---|---|---:|---:|']
for x in items:
    room='、'.join(k+'×'+str(v) for k,v in x['rooms'].items())
    lines.append(f'|{x["id"]} · {room}|[{x["name"]}]({x["sourceUrl"]}) / {x["sku"]} / {x["color"]}|'+ '×'.join(map(str,x['dimensionsCm']))+f'|¥{x["unitPriceCny"]:,.2f}|¥{x["totalPriceCny"]:,.2f}|')
lines+=['## 每项适配与包含范围']
for x in items:
    lines += [f'### {x["id"]} {x["name"]}',f'包含：{x["includes"]}。另计：{x["excludes"]}。',x['fitReview'],f'采购节点：{x["procurementStage"]}。']
lines+=['## 定制尺寸规格（没有虚构成品型号）','以下均为概算额度，不是供应商报价；不能直接按此下加工订单。','|编号 / 房间|定制项目|意向外廓cm|低 / 基准 / 高预算|','|---|---|---|---:|']
for x in custom:
    lines.append(f'|{x["id"]} / {next(iter(x["rooms"]))}|{x["name"]}|'+ '×'.join(map(str,x['dimensionsCm']))+f'|¥{x["unitPriceLowCny"]:,} / {x["unitPriceBaseCny"]:,} / {x["unitPriceHighCny"]:,}|')
for x in custom:lines +=[f'**{x["id"]} {x["name"]}：** {x["requirement"]}']
lines+=['## 未定型号的合理预留']
for x in allowances:lines +=[f'- {x["name"]}：基准¥{x["baseCny"]:,}，范围¥{x["lowCny"]:,}–{x["highCny"]:,}。{x["basis"]}']
lines+=['## 与总装修预算合并时的规则']+['- '+p for p in data['countingRules']]+['## 下单前逐项释放']+['- '+p for p in data['releaseChecklist']]
md='\n\n'.join(lines)
while '|\n\n|' in md: md=md.replace('|\n\n|','|\n|')
(OUT/'furniture.md').write_text(md,encoding='utf-8')
print(json.dumps(data['totals'],ensure_ascii=False,indent=2))

# Keep the original researched products and prices; allocate their actual quantities by phase.
defer_rooms={
 'F04':{'R204':1}, 'F08':{'R204':1}, 'F16':{'R204':1},
 'F15':{'R204':1}, 'F20':{'R204':6},
 'F22':{'R104':1,'R206':1},
 'F23':{'R109':1}, 'F24':{'R109':4}, 'F25':{'R109':4},
}
recommended_rows=[]; deferred_rows=[]
for x in items:
    late=defer_rooms.get(x['id'],{})
    now={r:q-late.get(r,0) for r,q in x['rooms'].items() if q-late.get(r,0)>0}
    for target, allocation in [(recommended_rows,now),(deferred_rows,late)]:
        if not allocation: continue
        qty=sum(allocation.values())
        target.append(dict(id=x['id'],name=x['name'],sku=x['sku'],rooms=allocation,quantity=qty,unitPriceCny=x['unitPriceCny'],totalPriceCny=round(qty*x['unitPriceCny'],2)))

additional=[
 dict(id='C13',name='主卧矮柜',rooms={'R201':1},quantity=1,model='定制尺寸规格，无成品型号',dimensionsCm=[175,40,74],baseCny=2200,lowCny=1500,highCny=3500,priceBasis='设计概算占位，非供应商报价',note='补回模型已有但旧采购表漏列的柜体；保持床尾通行，按完成面复尺。若总木作合同已含本柜，只计一次。'),
 dict(id='C14',name='家政用品柜',rooms={'R206':1},quantity=1,model='定制尺寸规格，无成品型号',dimensionsCm=[55,50,185],baseCny=1500,lowCny=900,highCny=2500,priceBasis='设计概算占位，非供应商报价',note='仅干式清洁用品柜，不含洗烘机包柜或接水改造。原梯区可实施条件明确后订制；若需另找原合法可用墙面，先重新布置。'),
 dict(id='C15',name='完整宣纸与卷轴轻放收纳模块',rooms={'R303':1},quantity=1,model='按实际纸样定制，无成品型号',dimensionsCm=None,baseCny=800,lowCny=400,highCny=1500,priceBasis='设计概算占位，非供应商报价',note='完整未书写宣纸只作宽松卷存预案：大直径圆芯/外套筒和独立分格，不紧卷、不捆压、不以其他物品压纸，避潮、避阳光及热源；实际纸性不适宜卷存或已完成作品，应采用相应平放/装裱收纳并另深化。原70×44柜仅收折纸、册页和小幅纸，不宣称可平放68×136整纸。'),
]
phase1_standard=round(sum(x['totalPriceCny'] for x in recommended_rows),2)
phase2_standard=round(sum(x['totalPriceCny'] for x in deferred_rows),2)
phase2_custom=custom[6]['unitPriceBaseCny']+custom[11]['unitPriceBaseCny']
phase1_custom=sum(x['unitPriceBaseCny'] for x in custom)-phase2_custom
additional_total=sum(x['baseCny'] for x in additional)
phase1_allowance=7500
phase2_allowance=1000
phase1_total=round(phase1_standard+phase1_custom+additional_total+phase1_allowance,2)
phase2_total=round(phase2_standard+phase2_custom+phase2_allowance,2)
valuePlan=dict(
 title='毛坯长期自住｜先把常住生活做好，按实际需要分期添置',
 basis='保留26条成品研究和原显示价，不虚构折扣。预算优化来自推迟尚未需要的数量，不压低父母/夫妻床垫和三位实际工作者的工作椅。',
 recommendedIds=[x['id'] for x in recommended_rows],
 deferredIds=[x['id'] for x in deferred_rows],
 partialIds=['F15','F20'],
 idRule='F15、F20同时出现在推荐和延后列表，仅因为儿童房份额延后；必须按下列rooms/quantity分配汇总，不能按整条总量重复计。',
 recommendedProducts=recommended_rows,deferredProducts=deferred_rows,
 recommendedCustomIds=[x['id'] for x in custom if x['id'] not in ['C07','C12']],
 deferredCustomIds=['C07','C12'],
 additionalItems=additional,
 allowanceAllocation=[
  dict(id='A01',name='床品与保护垫',recommendedBaseCny=4000,deferredBaseCny=1000,note='原5000预算中，为未来儿童床划出1000延后；这是预算分配，不是某SKU的核实售价。'),
  dict(id='A02',name='家具配送、上楼、组装与基层固定',recommendedBaseCny=2500,deferredBaseCny=0,note='送装不因少买几件自动等比例下降；分期可能产生第二次配送费，付款前单独核价。'),
  dict(id='A03',name='维护、保护与收纳小件',recommendedBaseCny=1000,deferredBaseCny=0,note='保留户外坐凳及常用物件的必要保护维护额度，不提前购买未下单桌椅的专用家具罩。'),
 ],
 budget=dict(originalFullResearchBaseCny=data['totals']['furnitureAllInBaseCny'],additionalOmissionsBaseCny=additional_total,recommendedStandardCny=phase1_standard,recommendedOriginalCustomCny=phase1_custom,recommendedAllowanceCny=phase1_allowance,recommendedPhase1BaseCny=phase1_total,deferredStandardCny=phase2_standard,deferredCustomCny=phase2_custom,deferredAllowanceCny=phase2_allowance,deferredTotalBaseCny=phase2_total,fullIncludingAdditionalBaseCny=round(phase1_total+phase2_total,2)),
 phases=[
  dict(name='一期｜常住和实际工作需要',budgetCny=phase1_total,scope='父母、夫妻、妹妹三张床及床垫，三间常用卧室床头柜；客餐厅；父亲、母亲、妹妹三把工作椅；书法、编织和操盘工作台、必要柜体及书柜；妈妈露台坐凳和换盆台。补主卧矮柜、家政柜和整纸收纳。原梯区功能及露台项目仍按施工交接的可实施条件释放。'),
  dict(name='二期｜有实际儿童使用需求再选',budgetCny=6455.94,scope='儿童床699、床垫1299、书桌399、该房工作椅799、6只收纳盒59.94、儿童柜2200、床品预算1000。启用时按实际年龄重新确认；这套成人尺寸客卧预案不是婴幼儿专用配置。'),
  dict(name='后添｜园中用餐与装饰边桌',budgetCny=3074.94,scope='南院桌999、四椅1196、四坐垫119.96；露台圆几600；室内两只托盘边桌159.98。先入住体验动线和使用频率，再决定是否需要。'),
 ],
 valueOptimizations=[
  '父母/夫妻床垫、已经实际使用的三把工作椅不降级；本人试躺试坐后在同价级别内定软硬和椅型。',
  '保留成品矮书架与带门毛线柜，不再同位置追加一套定制展示柜；节约来自避免重复，而不是凭空给定制折价。',
  '非标55/50深衣柜、书法案及真实设备桌保留复尺定制，不能为买便宜60深标准柜挤占原图通道。',
  '妹妹床先按外廓已核的120床垫方案；若本人明确需要135，只做局部替换核算，不同时算两张床。',
  '不增加无必要整面电视造型柜、全屋高柜、复杂桌面和成套装饰；现模型摆件不意味着全部都要买。',
 ],
 exclusions='厨房地柜、台面等已由总预算H23–H26计17430元，本valuePlan不再加厨房。五卫盆柜镜龙头在家电卫浴表，花箱/铺装/排水在园林表，均不重复。',
 caution='分期金额按2026-09-10已记录公开价与设计概算计算，只表示今天规划的支出时点；未来价格、库存和二次配送可能变化，不承诺未来以当前价格购得。当前3D仍是P02示意。'
)
assert round(phase1_standard+phase2_standard,2)==sum_standard
assert round(phase1_total+phase2_total,2)==round(data['totals']['furnitureAllInBaseCny']+additional_total,2)
assert round(sum(p['budgetCny'] for p in valuePlan['phases']),2)==valuePlan['budget']['fullIncludingAdditionalBaseCny']
data['valuePlan']=valuePlan
(OUT/'furniture.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
value_md='\n\n## 毛坯长期自住的分期采购（更新）\n\n'+valuePlan['basis']+'\n\n'
value_md+=f'补入漏项主卧矮柜、家政柜和整纸收纳共¥{additional_total:,}后，全量家具预算为 **¥{valuePlan["budget"]["fullIncludingAdditionalBaseCny"]:,.2f}**。一期建议 **¥{phase1_total:,.2f}**；可延后 **¥{phase2_total:,.2f}**。厨房与卫浴不在此重复增加。\n\n'
for p in valuePlan['phases']: value_md+=f'- **{p["name"]}：¥{p["budgetCny"]:,.2f}。** {p["scope"]}\n'
value_md+='\n整纸收纳：'+additional[2]['note']+'\n\n'+valuePlan['caution']+'\n'
md=(OUT/'furniture.md').read_text(encoding='utf-8')
(OUT/'furniture.md').write_text(md+value_md,encoding='utf-8')
(OUT/'furniture-value-plan.md').write_text('# 家具分期与价值优化\n'+value_md,encoding='utf-8')
print('valuePlan',json.dumps(valuePlan['budget'],ensure_ascii=False))
