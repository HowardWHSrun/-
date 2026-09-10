"""Append researched domestic options without replacing the original research fields."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DAY = "2026-09-10"
path = HERE / "contractors.json"
data = json.loads(path.read_text())
original = json.loads(path.read_text())

sources = [
    {"id":"D01","title":"康力中文官网家用电梯产品页","publisher":"康力电梯股份有限公司","url":"https://www.canny-elevator.com/product/show-491.html","accessed":DAY,"notes":"当前家用产品与安全/救援功能说明；本页未给出完整井道土建参数。"},
    {"id":"D02","title":"CANNY KLJ Home Use Elevator","publisher":"康力电梯股份有限公司","url":"https://en.canny-elevator.com/product/show-893.html","accessed":DAY,"notes":"确认KLJ产品系列名；英文页功能和配置须由中国销售合同复核。"},
    {"id":"D03","title":"康力营销网络：浙江分公司","publisher":"康力电梯股份有限公司","url":"https://www.canny-elevator.com/marketing-16.html","accessed":DAY,"notes":"官网公开0571-89971040，杭州市拱墅区新天地商务中心806、807室。"},
    {"id":"D04","title":"西奥SIND及SINDII家用别墅梯","publisher":"杭州西奥电梯有限公司","url":"https://www.xiolift.com/products/productsinfo4/4/4.html","accessed":DAY,"notes":"当前家用系列、钢带曳引、可选儿童锁/物联网；家用咨询0571-81028788。"},
    {"id":"D05","title":"西奥官网与杭州总部、客户服务","publisher":"杭州西奥电梯有限公司","url":"https://www.xiolift.com/","accessed":DAY,"notes":"总部地址浙江省杭州市临平经济技术开发区宏达路168号；服务400-826-9998。"},
    {"id":"D06","title":"快意VILLUX家用别墅电梯产品页","publisher":"快意电梯股份有限公司","url":"https://www.ifelift.com/VILLUXbieshudianti/82-27.html","accessed":DAY,"notes":"官网当前在售产品系列入口，不含本案三层合同报价。"},
    {"id":"D07","title":"快意VILLUX系列产品册202501版","publisher":"快意电梯股份有限公司","url":"https://www.ifelift.com/uploads/202601/695b21c533ff3.pdf","accessed":DAY,"documentVersion":"202501版，官网2026年1月上传路径","notes":"已把原厂PDF第3、21、22、23页渲染逐图核读；技术参数主要见PDF第22页右半（印刷页42）；井道宽深以变量表达，未给本案固定净井匹配结论。"},
    {"id":"D08","title":"快意官网及全球服务网络","publisher":"快意电梯股份有限公司","url":"https://www.ifelift.com/quanqiuwangluo.html","accessed":DAY,"notes":"官网公开公司电话0769-8207-8888、服务400-6789-443；此页面未核到杭州具体服务地址。"},
    {"id":"D09","title":"家用电梯价格差距为什么这么大","publisher":"Cibes西柏思","url":"https://www.cibeslift.cn/wenjian/jiayongdianti-jiage-chaju-weishenme-zheme-da-2026.html","published":"2026-04-24","accessed":DAY,"notes":"品牌科普页面自述曳引式12–25万元含安装、曳引维保约3000–5000元/年；不是独立市场统计，不指向康力、西奥或快意，不能当作三层具体型号正式报价。"},
    {"id":"D10","title":"快意2025年半年度报告","publisher":"快意电梯股份有限公司","url":"https://www.ifelift.com/uploads/202512/694b40789497b.pdf","accessed":DAY,"notes":"确认制造业务和全国分支网络；全国网络不等于本案富阳到场服务承诺。"},
]

def price():
    return {"currency":"CNY","asOf":DAY,"status":"未报价","quotedAmount":None,"publicThreeStopModelPrice":None,"scope":"三层三站、提升高度与门向待现场确定；未联系厂家，未取得含税到场安装报价。","source":"本次官方公开资料检索，无本案报价"}

common_fit = "未核定。模型外井1650×1900mm、净井1410×1660mm仅为方案占位，厂家须给本案平面、剖面、荷载和门洞图并签认；不能直接下单或开井。"
data["domesticElevatorCandidates"] = [
    {
        "id":"DE01","brand":"康力 CANNY","manufacturer":"康力电梯股份有限公司","model":"KLJ 家用电梯系列",
        "classification":"国内电梯制造企业的家用系列；具体出厂型号、产地及配置以合格证明和合同为准",
        "priority":"第一轮询价",
        "whyThisProject":"官网可核杭州浙江分公司，可先核家用梯与本地安装、救援、配件供应是否由同一责任主体承担；适合毛坯阶段先做土建接口方案与标准饰面询价。",
        "scope":"要求三层三站、标准轿厢与自动门；当前网页不能证明本案净井、提升高度和救援条件均满足。",
        "dimensionalEvidence":{"sourceIDs":["D01","D02"],"minimumShaftMm":None,"pitDepthMm":None,"minimumHeadroomMm":None,"notes":"官网当前公开页未取得完整土建尺寸表；不能将早年KLJ/VF参数套在2026年采购上。"},
        "verifiedFeatures":["中文官网列出断电应急救援、故障自动救援、电动松闸救援","中文官网说明光幕保护、一键呼救；具体标配/选配须列合同"],
        "manufacturerContact":{"localOffice":"浙江分公司","localPhone":"0571-89971040","localAddress":"杭州市拱墅区新天地商务中心806、807室","nationalPhone":"400-188-2367","sourceIDs":["D03"],"serviceVerification":"杭州公开分公司已核；富阳上门时限、家用型号专属团队、授权状态和收费未确认"},
        "fitStatus":common_fit,"price":price(),"sourceIDs":["D01","D02","D03"],
        "uncertainties":["KLJ具体配置单、三层土建条件和门净宽","全国服务电话不构成本案救援时限承诺","未独立验证实际工班质量或客户长期故障记录"]
    },
    {
        "id":"DE02","brand":"西奥 XIOLIFT","manufacturer":"杭州西奥电梯有限公司","model":"SIND / SINDII 家用别墅梯系列",
        "classification":"杭州本地电梯制造企业的家用系列；订单型号、制造地与所用部件须合同列明",
        "priority":"第一轮询价",
        "whyThisProject":"杭州总部、家用业务专线可直接核；用标准钢带曳引系列与康力做同范围报价比较，重点审本地服务与备件。",
        "scope":"要求三层三站；优先询常规自动门、浅色标准饰面，不以豪华轿厢或语音屏幕作为必选。",
        "dimensionalEvidence":{"sourceIDs":["D04"],"minimumShaftMm":None,"pitDepthMm":None,"minimumHeadroomMm":None,"notes":"当前官方产品页确认SIND/SINDII系列，但未公开可直接用于本案的完整井道尺寸表；经销商旧册和两层商城起价不作为三层订货依据。"},
        "verifiedFeatures":["当前官网说明钢带曳引技术","物联网、儿童锁、语音呼梯列为可配置项；报价需区分选配费用"],
        "manufacturerContact":{"localOffice":"杭州总部 / 家用电梯业务","localPhone":"0571-81028788","localAddress":"浙江省杭州市临平经济技术开发区宏达路168号","nationalPhone":"400-826-9998","sourceIDs":["D04","D05"],"serviceVerification":"总部及家用业务专线已核；须明确本案由厂家或哪家授权商安装维保，富阳响应时限未确认"},
        "fitStatus":common_fit,"price":price(),"sourceIDs":["D04","D05"],
        "uncertainties":["SIND与SINDII适用本案的具体子型号及2026订货图","额定载重、速度、底坑、顶层净高和自动门净宽未获本案核定","品牌总部在杭州不等于承诺由总部直营安装或长期免费维保"]
    },
    {
        "id":"DE03","brand":"快意 IFE","manufacturer":"快意电梯股份有限公司","model":"VILLUX 基础系列；VILLUX-Pro作结构条件备选",
        "classification":"国内电梯制造企业的钢带曳引家用系列",
        "priority":"第二轮技术与价格对照；杭州本地服务主体确认后入围",
        "whyThisProject":"现行原厂册公开土建参数较完整，可用于提前判断顶层和底坑；先比较基础VILLUX，不默认采用Max旗舰或Mini平台式。",
        "scope":"拟询基础VILLUX、400kg、0.4m/s、三层三站、单侧自动门；载重不是本案可容纳4人的承诺，最终容量和轿厢尺寸以制造商为准。",
        "dimensionalEvidence":{"sourceIDs":["D07"],"documentVersion":"202501版，PDF第22页右半/印刷页42","ratedLoadKg":400,"requestedSpeedMps":0.4,"drive":"钢带2:1曳引、永磁同步无齿轮","maximumTravelM":27,"minimumShaftMm":None,"minimumHeadroomRearCounterweightMm":2900,"minimumHeadroomSideCounterweightMm":2950,"minimumPitPvcMm":200,"minimumPitMarbleMm":225,"standardPower":"单相220V，可选380V；电源与线路仍按本案安装图设计","door":"VVVF自动门可中分、旁开、中分双折，净开门宽尚未核定","notes":"上述顶层数据仅对应本册VILLUX的0.4/0.63m/s配置。厂册以SW/SD表示井道宽深，不能据此判定1410×1660mm净井可装。旧2022册1350×1350mm最小井宣传不作为现行订货依据。"},
        "verifiedFeatures":["现行厂册列光幕、门锁保护、超载保护","现行厂册列自动救援、一键紧急呼叫、电动松闸；儿童锁列为可选"],
        "manufacturerContact":{"localOffice":None,"localPhone":None,"localAddress":None,"nationalPhone":"400-6789-443","companyPhone":"0769-8207-8888","sourceIDs":["D08","D10"],"serviceVerification":"已核全国服务渠道；官网公开文本未核到杭州具体家用梯服务点，须厂家给出在地授权公司、工班及救援/备件安排后再列合格投标人"},
        "fitStatus":common_fit,"price":price(),"sourceIDs":["D06","D07","D08","D10"],
        "uncertainties":["杭州/富阳服务网点及到场时限待核","厂册尺寸必须由制造商按实际楼层、井道、基础条件重出安装图","3层总行程在27m以内不代表其他安装条件均满足"]
    }
]

data["domesticElevatorPriceGuidance"] = {
    "currency":"CNY","asOf":DAY,
    "status":"项目采购目标与前期暂列建议；不是厂家报价或市场成交保证",
    "mainApproach":"毛坯、长期自住且控制预算，先让康力KLJ与杭州西奥SIND/SINDII按同清单报价，快意VILLUX作技术与价格对照；待确认尺寸及本地服务后择优。",
    "inquiryTargetLow":150000,"inquiryTargetHigh":200000,
    "inquiryTargetMeaning":"15–20万元为项目方希望实现的三层三站标准配置设备系统交付目标，包含设备、需要的井架/围护、标准内饰、运输、安装调试及税费。目标尚未得到上述三家报价验证。结构土建和室内收口另列，不能拿纯设备价冒充这个目标。",
    "planningPlaceholder":180000,
    "planningPlaceholderStatus":"18万元可作可编辑初期暂列额；若报价或净井条件超出目标，应调整预算/技术方案，不能削减必需保护与维保条件，也不能承诺18万元必然买到。",
    "publicReference":{"low":120000,"high":250000,"sourceID":"D09","published":"2026-04-24","quoteStatus":"另一厂家科普页对曳引技术路线的含安装粗范围，不是候选品牌价表或具体三层价","scope":"未限定型号、层站、井道材质、税费与本案条件；只辅助设定询价方向，不直接计入总预算"},
    "importComparison":{"low":250000,"high":350000,"sourceID":"E10","quoteStatus":"Cibes官网常见三层品牌整体参考，非型号报价；保留作进口品牌路线对照，不再作为毛坯节制预算主方案","currency":"CNY","asOf":DAY},
    "annualMaintenanceReference":{"low":3000,"high":5000,"sourceID":"D09","currency":"CNY/year","asOf":DAY,"status":"品牌科普页的曳引式维护粗参考，不是任一候选厂家报价","scope":"拟合同须另问质保后每年保养次数、应急到场、配件/电池/钢带是否含；不得简单将此作为10年包干价"},
    "requiredQuoteLines":["完整型号与版本、制造厂、载重、速度、3层3站、提升高度、门向与净宽","现场净井与外井、底坑/顶层、每层门洞、钢结构/混凝土井道责任界面","电梯本体、3层门系统、井架与围护、标准内饰分别列价","运输、卸货吊装、安装调试、含税交付分别列价","断电自动救援、紧急通信、门保护、必要检测及交付文件逐项列入","整机与关键部件质保、易耗件排除项、故障应急到场与困人救援责任","质保后1年及5年维护方案，钢带/电池/门机/控制器更换价格口径","现场结构专业设计、审批、土建、电源和收口另列，不与18万元暂列重复计算"],
    "durabilityPriorities":["先核本地安装维保团队及备件渠道，再比较品牌装饰配置","三层家庭询0.4m/s标准配置；是否可用由厂家结合标准、型号与现场确认","简洁耐用轿厢、易清洁地面、实际乘坐噪音体验，比大屏和豪华饰面优先","当次演示停电救援、紧急呼叫；交付时培训家人，维保合同写清响应和收费"],
    "noContactMade":True
}
data["domesticElevatorSources"] = sources
data["ownerUpdate"] = {
    "asOf":DAY,"housingCondition":"毛坯房（用户本轮已明确）","budgetIntent":"预算不要太多，但该花要花，长期自住",
    "interpretation":"此补充优先指导当前采购。旧版施工候选中提及的旧改经历仅作为复杂工序能力参考，不说明本房是旧改；不再默认需要成套拆旧。",
    "primaryElevatorBudgetField":"domesticElevatorPriceGuidance",
    "olderImportAllowanceField":"estimateGuidance.elevatorSystemAllowance保留原始研究；当前仅为进口品牌路线对照，不与国产暂列额相加"
}

for key, value in original.items():
    if key not in {"domesticElevatorCandidates","domesticElevatorPriceGuidance","domesticElevatorSources","ownerUpdate"}:
        assert data[key] == value, f"Unexpected alteration: {key}"
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")

section = '''
## 毛坯长期自住更新：先询国产厂家标准家用梯

用户已明确本房为毛坯，希望节制预算、该花的钱花在长期使用上。本补充优先指导当前采购；前文进口家用梯25–35万元仍保留为对照，**不再作为主方案默认采购额，也不与国产暂列重复相加**。施工候选前文的旧改案例仅能说明其自述复杂工序经验，本案不应预设整套拆旧。

| 先询的真实系列 | 制造商与已核杭州渠道 | 可用技术依据 | 正式三层报价 |
|---|---|---|---|
| 康力 KLJ | 康力电梯股份有限公司；浙江分公司0571-89971040，拱墅区新天地商务中心806、807室 | 当前官网确认家用系列及断电/故障救援功能；完整井道、底坑、顶层参数待厂方出图 | 未报价 |
| 西奥 SIND / SINDII | 杭州西奥电梯有限公司；家用业务0571-81028788，临平经济技术开发区宏达路168号；服务400-826-9998 | 当前官网确认钢带曳引家用系列；具体子型号和土建条件待出图 | 未报价 |
| 快意 VILLUX基础系列 | 快意电梯股份有限公司；全国400-6789-443，公司0769-8207-8888；杭州具体家用服务商未核定 | 现行原厂册400kg/0.4m/s：后对重顶层≥2900mm、侧对重≥2950mm；PVC地板底坑≥200mm，大理石≥225mm | 未报价 |

先让康力与杭州西奥用同一范围报价；快意补齐杭州/富阳具体授权服务主体后参加比价。厂家和系列可查并不代表实际施工班组质量已经过独立验证。总部/分公司存在也不等于已取得富阳到场时限或直营安装承诺。[康力产品与杭州网络](https://www.canny-elevator.com/marketing-16.html)、[KLJ系列](https://en.canny-elevator.com/product/show-893.html)、[西奥家用系列](https://www.xiolift.com/products/productsinfo4/4/4.html)、[快意原厂册](https://www.ifelift.com/uploads/202601/695b21c533ff3.pdf)

建议把**15–20万元作为三层三站标准配置的询价目标**，18万元可作为预算里可编辑的初期暂列额，三家均未确认这个价能成交。目标范围应统一包含设备、所需井架/围护、标准内饰、运输、安装调试和税费；结构设计、相关审批、土建、电源与室内收口另列。现有18万元暂列须在收到现场正式报价后替换。

价格依据只是一项弱参考：Cibes于2026-04-24的科普页自述曳引式含安装12–25万元，未限定层站、品牌或井道交付，不是独立市场统计，更不是康力/西奥/快意的报价。因此15–20万元是项目方采购目标，不能宣传成这些型号的厂家指导价。同页曳引维保约3000–5000元/年也仅是粗参考；合同须明确保养次数、应急服务、易耗件与主要部件更换，不能视为十年包干保证。[价格范围原文](https://www.cibeslift.cn/wenjian/jiayongdianti-jiage-chaju-weishenme-zheme-da-2026.html)

模型**外井1650×1900mm、净井1410×1660mm**还没有被厂家接受。快意202501版册的井道宽深是变量，不提供本案固定净井适配结论；旧版1350×1350mm最小井宣传不能拿来保证2026订单可装。所有候选都要先提供本案的井道平面/剖面、轿厢及门净宽、底坑/顶层要求、楼层荷载与救援条件。三层总行程在产品范围以内，也不等于其他安装条件满足。

长期使用优先比较本地维保工班、故障救援和配件供应；标准轿厢、常规自动门和好清洁饰面足够。儿童锁、停电救援、紧急通信等应在配置单中写明。采购合同应给出整机/核心部件质保、1年和5年维保方案以及电池、门机、钢带、控制器等更换价格口径。语音大屏、豪华金属饰面、额外观光玻璃不默认列必选。

本次没有联系任何厂家、施工队或销售，也没有提交询价表单；所有三层价格均为“未报价”。资料访问日期：2026-09-10。新增机器可读数据位于JSON的domesticElevatorCandidates、domesticElevatorPriceGuidance及domesticElevatorSources字段；旧字段保留用于追溯。
'''
mdpath=HERE/"contractors.md"
md=mdpath.read_text()
marker="## 毛坯长期自住更新：先询国产厂家标准家用梯"
if marker in md:
    md=md.split(marker)[0].rstrip()+"\n"
mdpath.write_text(md+"\n"+section)
assert len(data['domesticElevatorCandidates'])==3
assert all(x['price']['quotedAmount'] is None for x in data['domesticElevatorCandidates'])
print("Appended 3 domestic candidates and guidance; original fields preserved.")
