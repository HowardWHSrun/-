"""Create the budget/procurement supplement from one published dataset."""
import json,math
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,KeepTogether
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output/unit6-procurement'
D=json.loads((OUT/'采购预算整合.json').read_text());C=json.loads((OUT/'research/contractors.json').read_text());F=json.loads((OUT/'research/furniture.json').read_text());A=json.loads((OUT/'research/appliances.json').read_text())
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/Supplemental/Songti.ttc',subfontIndex=6));pdfmetrics.registerFont(TTFont('CNB','/System/Library/Fonts/Supplemental/Songti.ttc',subfontIndex=1))
W,H=297*mm,210*mm;M=15*mm;CW=W-2*M
INK=colors.HexColor('#263D38');MUT=colors.HexColor('#64736C');LINE=colors.HexColor('#D9DED6');PALE=colors.HexColor('#EFF2EA');OAK=colors.HexColor('#A67443')
styles={k:ParagraphStyle(k,fontName=('CNB' if k in ['title','h','head'] else 'CN'),fontSize=size,leading=leading,textColor=(colors.white if k=='head' else INK),wordWrap='CJK',spaceAfter=space) for k,size,leading,space in [('title',25,32,13),('h',16,22,9),('body',11,17,7),('small',9,13,5),('cell',9.1,13.6,0),('head',9.5,14,0)]}
styles['h'].keepWithNext=True
S=[];MD=[];refs={};refrows=[]
def txt(x):return str(x if x is not None else '').replace('–','-').replace('—','-').replace('\n','<br/>')
def p(x,sty='body'):return Paragraph(txt(escape(str(x))).replace('&lt;br/&gt;','<br/>'),styles[sty])
def para(x,sty='body'):S.append(p(x,sty));MD.append(str(x)+'\n')
def title(n,t):
 if S:S.append(PageBreak())
 S.append(p(f'{n} / {t}','title'));MD.append('\n## '+str(n)+' / '+t+'\n')
def table(head,rows,widths,small=False):
 padding=5 if head[0]=='分项' else 6
 content=[[p(x,'head') for x in head]]+[[p(x,'cell') for x in row] for row in rows]
 t=Table(content,colWidths=[CW*v/sum(widths) for v in widths],repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),padding),('BOTTOMPADDING',(0,0),(-1,-1),padding),('LINEBELOW',(0,0),(-1,0),.7,INK),('LINEBELOW',(0,1),(-1,-1),.35,LINE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE])]))
 S.append(KeepTogether([t]) if head[0]=='比较项' else t);S.append(Spacer(1,8));MD.append('| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+'\n'.join('| '+' | '.join(str(x).replace('\n',' / ').replace('|','/') for x in row)+' |' for row in rows)+'\n')
def ref(url,label):
 if not url:return ''
 if url not in refs:
  refs[url]=f'S{len(refs)+1:03}';refrows.append((refs[url],label,url))
 return '['+refs[url]+']'
def yuan(x):return f'¥{x:,.2f}'
def rowamt(r):return r['quantity']*r['budgetUnitPrice']
def source(r):return ref(r.get('sourceUrl'),r['name'])
t=D['totals']
title('01','毛坯长期自住 · 预算与采购')
para('第6户 / 简约舒适 / 采购补充 V1 / 2026.09.10','small')
para('四位常住成员：父母、你、妹妹。先做好耐久的基础工程与每天使用的家具，预留未来夫妻及儿童生活。项目地区暂按原图杭州富阳；实际城市区县仍待确认。')
table(['已计主方案，含12%预备费','其中电梯及对应预备费','不含电梯的已计方案'],[[yuan(t['mainWithContingency']),yuan(t['elevatorWithContingency']),yuan(t['withoutElevator'])]],[1,1,1])
para('电梯设备暂按18万元采购目标询价，不是厂家报价。撤梯、开井、补板、加固等未知工程未计；12%预备费不覆盖这些未计项目。此金额不能作为包干或封顶承诺。')
img=ROOT/'output/第6户_住宅与花园_P02_完整交付包/图册/images/01_完整建筑与庭院鸟瞰.png'
if img.exists():
 from PIL import Image as PI
 im=PI.open(img);hh=57*mm;S.append(Image(str(img),width=hh*im.width/im.height,height=hh,hAlign='LEFT'))
para('图像为P02原方案示意，非本版品牌家具实物效果。原图边界与P02模型本次未改；选型仍须完成尺寸和安装条件复核。','small')
title('02','预算总览与可调整范围')
cat=t['categories'];table(['分项','金额 / 元','计价说明'],[[k,yuan(v),('18万元采购目标，未获报价；土建另计' if k=='电梯暂列' else '模型量与工程预算假设' if k in ['室内硬装','花园工程','前期与验收'] else '公开参考/显示价与预算额度混合，逐行标注')] for k,v in cat.items()]+[['已计范围小计',yuan(t['subtotal']),'只加计入=1的行'],['12%预备费',yuan(t['contingency']),'覆盖已计范围的一般数量与价格波动'],['已计主方案',yuan(t['mainWithContingency']),'不含后文未知工程'],['未勾选后添及升级',yuan(t['optionalBeforeContingency']),'另计；不自动叠加主方案，也未加预备费']],[1.1,1,3])
para('Excel浅黄色单元格可改数量、预算单价、正式报价与计入开关。正式报价留空时用预算值；填写0是有效的零报价。电梯及其预备费单列，便于比较有无电梯的支出。网站预算试算也可调整，保存于当前浏览器。','small')
title('03','哪些钱该花，哪些先省')
table(['先做 / 保留','落实方式','避免多花'],[
['隐蔽工程与可检修性','验收毛坯防水与门窗；给排水、电气回路、节点与检修图先定，隐蔽前留照片及试验记录。','不为省钱覆盖缺陷；开发商交付问题先明确整改责任。'],
['睡眠与长时间工作','父母、夫妻、妹妹三张床和床垫；保留实际工作的椅子。书法双工作灯、毛线高显色工作照明。','床垫椅子本人试躺试坐；不盲目追求豪华床架与灯具数量。'],
['空间与饰面','暖白墙、浅木地面、米灰织物、少量灰绿。普通平顶，必要部位局部吊顶。','不做大面积电视石材背景、复杂吊顶、满墙展示柜、电动帘等默认升级。'],
['稳定的设备与维护','先比较可在本地维护的国产电梯、独立分体冷暖；卫浴按房间频率分档。','单价低不等于系统省钱；须核可用外机位、管路、安装及维保总成本。'],
['妈妈花园与工作室','先4组轻型花箱、基础防护排水、露台坐凳和换盆台；人工浇水。','其余6花箱、户外餐桌椅、自动滴灌入住后决定。露台保持原开敞边界。']],[1,2.1,1.9])
para('本版没有封闭玻璃阳光房的材料或报价。妈妈工作室与开敞露台共同满足园艺、毛线使用；若要封闭阳光房，需要另核允许范围、结构和防结露排水，再单列预算。')
table(['家具采购阶段','预算','范围'],[[x['name'],yuan(x['budgetCny']),x['scope']] for x in D['furniturePhases']],[1.2,.8,3])
title('04','工程量基础与报价口径')
q=D['quantityBasis'];para('室内参考量来自原图边界、墙体投影及P02当前孔洞/电梯方案计算，约216.9㎡；不是产权面积，也不是可直接结算的施工实测量。')
table(['预算用量','数值','说明'],[['室内参考合计',f"{q['interiorApproxM2']:.3f}㎡",'最终地面面积按现场完成面、门槛及设备占位复核'],['干区 / 厨卫地面',f"{q['dryFloorApproxM2']:.3f} / {q['wetFloorApproxM2']:.3f}㎡",'五卫一厨，地板和湿区地砖分列'],['南院 / 主南廊 / 露台','47.504 / 9.797 / 18.684㎡','室外合计75.985㎡，只计原核边界内'],['墙面 / 湿区墙砖 / 防水展开','430 / 125 / 150㎡','设计预算占位，未从墙面施工展开图精算'],['橱柜地柜 / 吊柜','4.4 / 2.2延米','预算占位；洗碗机与冰箱重排后按柜体拆单计价'],['门 / 开关插座','9套 / 约70位','均为暂估，38处洞口或62展示点不等于采购数量']],[1.3,1.3,2.5])
para('工程单价是本项目预算假设，不是已取得的施工报价或当地官方定额。按拟含税工料总支出规划；施工方必须拆清人工、主材、辅材、损耗、管理费、税及甲供服务费，不能在含税零售价上机械再叠一遍税。')
para('常住家具和家电按官网型号资料筛选，但页面存在不代表杭州库存或送装条件已确认。型号候选、预算预留、官方参考价和商品显示价已分行记录；未采用过期活动或假定补贴。')
title('05','硬装与花园 · 逐项预算')
para('数字为预算；“后添”不计入当前主方案。施工前必须复测、深化并核对合法性。','small')
rs=D['construction'];table(['编号 / 状态','项目','数量 × 单价','行金额 / 元','供货施工范围及边界'],[[r['id']+('\n已计' if r['included'] else '\n后添'),r['name'],f"{r['quantity']:g}{r['unit']} × {r['budgetUnitPrice']:,.0f}",yuan(rowamt(r)),r['scope']+'\n'+r['fitStatus']] for r in rs],[.6,1.1,1,.8,3])
title('06','成品家具 · 型号、货号与尺寸')
para('保留常住三间卧室和实际工作需要。首次采购约7.06万元，包含后续章节定制与配送预留。官方页面已查日期均为2026-09-10；未设置收货地址，库存与送装须单独核实。','small')
rs=[r for r in D['furniture'] if r['category']=='成品家具'];table(['编号 / 状态','房间 / 商品 / 货号','数量 × 单价','行金额','尺寸及采购条件'],[[r['id']+('\n已计' if r['included'] else '\n延后'),r['room']+'\n'+r['name']+'\n'+r['model']+' '+source(r),f"{r['quantity']:g} × {r['budgetUnitPrice']:,.2f}",yuan(rowamt(r)),r['fitStatus']] for r in rs],[.6,2.0,.8,.8,2.5])
title('07','定制家具与附加费用')
para('以下是尺寸规格和询价额度，没有虚构成品型号。定制均先现场复尺与材料样板确认，签收安装图后加工；原梯区家具须等可实施方案确定。','small')
rs=[r for r in D['furniture'] if r['category']!='成品家具'];table(['编号 / 状态','房间 / 项目','数量 × 单价','行金额','尺寸 / 供货边界'],[[r['id']+('\n已计' if r['included'] else '\n延后'),r['room']+'\n'+r['name'],f"{r['quantity']:g} × {r['budgetUnitPrice']:,.0f}",yuan(rowamt(r)),r['fitStatus']+'\n'+r['scope']] for r in rs],[.6,1.3,.8,.8,3])
title('08','家电、卫浴、照明与设备')
para('必配21组共114913元（含网络与叠放配件1700元），后添3组10205元另计。为保持完整的五卫使用条件，儿童卫浴和该房空调目前仍预留，儿童家具则延后。设备选择须服从现场容量、通风、排水及检修条件。','small')
table(['编号 / 状态','房间 / 商品与型号','数量 × 单价','行金额','价格口径 / 安装条件'],[[r['id']+('\n已计' if r['included'] else '\n延后'),r['room']+'\n'+r['name']+'\n'+r['model']+' '+source(r),f"{r['quantity']:g} × {r['budgetUnitPrice']:,.0f}",yuan(rowamt(r)),r['priceStatus']+'\n'+r['fitStatus']] for r in D['appliances']],[.6,2.1,.8,.8,2.8])
title('09','设备组合拆分与施工界面')
for r in D['appliances']:
 if not r.get('components') or not r['included']:continue
 group_start=len(S)
 S.append(p(r['id']+' '+r['name'],'h'));MD.append('### '+r['name'])
 comps=[]
 for x in r['components']:
  price=next((x[k] for k in ['unit_allowance_cny','unit_reference_cny','official_reference_cny','price_cny','allowance_cny'] if k in x),None)
  amount=x.get('total_cny',price*x.get('quantity',1) if price is not None else None)
  comps.append([x.get('model') or x.get('name',''),str(x.get('quantity',1)),yuan(amount) if amount is not None else '组内预算，不重复加计',x.get('assignment','') or '按最终厂家清单与安装图核定'])
 table(['组合项','数量','组内金额','分配 / 说明'],comps,[2.1,.5,1,2])
 para('已含：'+r['scope']+'；此拆分只解释上一章总额，不再加一次。','small')
 S[group_start:]=[KeepTogether(S[group_start:])]
title('10','施工团队候选与筛选顺序')
para('按原图杭州/富阳区域初筛。建议先向铭品、南鸿、都都要同范围书面报价；尚层作全案对照，圣都作标准整装范围对照。名单依据公开官网案例和服务渠道，未联系、未量房、未取得本案报价，也未核实拟派工长质量。')
for r in C['candidates']:
 S.append(p(r['brand']+' / '+r['priority'],'h'));MD.append('### '+r['brand'])
 refcode=ref(r['website'],r['brand']+'官网')
 table(['主体 / 公开联系','适合本案的依据','需要核对'],[[r['companyName']+'\n'+r['phone']+'\n'+r['serviceArea']+' '+refcode,r['whyShortlisted']+'\n'+r['serviceMode'],'；'.join(r['uncertainties'])]],[1.8,2.2,2])
 for case in r['caseLinks']:para('案例线索：'+case['title']+' '+ref(case['url'],r['brand']+'：'+case['title']),'small')
para('品牌不是具体工班。入围后要求同一拟派工长的近期多层住宅案例、隐蔽验收记录和在建现场；营业执照、资质适用范围、合同收款主体、分包及售后责任逐项核验。若实际城市不同，重筛当地名单，不把杭州总部自动当作可跨城服务。')
title('11','电梯候选：本地服务与总成本')
para('先询国产标准款，不选豪华轿厢或屏幕作为必配。三层三站采购目标15-20万元，主预算暂填18万元；公开资料没有本案成交价。预算目标可被现场条件推高。')
for r in C.get('domesticElevatorCandidates',[]):
 contact=r['manufacturerContact'];para(r['brand']+' / '+r['model'],'h')
 table(['联系与服务核验','本案选择理由','尺寸与价格条件'],[[contact.get('localPhone') or contact.get('nationalPhone',''),r['whyThisProject'],r['fitStatus']+'\n价格：未报价。']],[1,1.7,2.6])
 para(contact['serviceVerification'],'small')
 for sid in r.get('sourceIDs',[])[:2]:
  src=next((s for s in C.get('domesticElevatorSources',[]) if s['id']==sid),None)
  if src:para(ref(src['url'],src['title'])+' '+src['title'],'small')
para('进口对照：Cibes品牌公开三层参考25-35万元；该区间不是S80本案报价，也不能套作ARITCO价格。若以30万元替换当前18万元，仅已计预算增加13.44万元（含12%预备费），土建仍未计。 '+ref('https://www.cibeslift.cn/faq/1370.html','Cibes三层家用梯价格FAQ'),'small')
para('当前井道外1650×1900mm、内净1410×1660mm。各系列宣传最小尺寸、单一机身外廓或载重，均不足以证明可以装入。要求厂家出本案总行程、门方向与净宽、底坑、顶层净高、反力、安装运输、检修及停电救援图。')
title('12','下单与开工前的尺寸闭环')
table(['编号 / 项目','当前判断','具体行动'],[[r['id']+' '+r['item'],r['condition'],r['action']] for r in D['fitIssues']],[1.1,2.3,2.6])
title('13','未计范围与报价接口')
table(['项目','未计原因 / 处理方式'],[[r['id']+' '+r['name'],r['why']] for r in D['excludedUnpriced']],[1.3,3])
para('结构、建筑与设备专业的可行性意见不自动替代当地允许施工的条件；若撤梯或开井属于禁止范围，应修改方案。普通家用电梯也不能凭模型设定替代获准的疏散路径。')
table(['可能重计位置','本版计法','正式报价如何扣重'],[
['厨房','H23-26柜体台面17430元；AP-A12水槽龙头1848元','若整装橱柜套餐含槽龙头，应扣相应甲供项；核抽屉、拉篮、开孔与转角'],
['五卫盆柜','AP-A08盆柜附件6400、A09龙头1750、A10镜柜1995','木作不能再加同一盆柜；镜前灯在A19，浴室主灯在A13'],
['安装','H21为未被商家覆盖的安装协调预留；空调热水排风组含部分安装','设备合同已包的施工人工、风管和附材须从H21/H03/H04对应范围扣回'],
['花园','G01-09铺装/修复/防护/首期花箱；户外灯体在AP-A13','花箱不在家具重算；换盆台、坐凳在家具；排水检查修复只归G02'],
['可选系统','地暖、新风、软水和后添设备为计入0','替代基础系统时先减被替代项目，避免把两个完整系统一起相加']],[1,1.8,2.2])
title('14','施工与采购顺序')
para('下面是施工组织建议，用于询价与工序交接，具体做法和工期须由承担责任的专业人员与施工团队按现场出图确认。现阶段不发布撤梯、楼板或承重构件的操作步骤。')
table(['阶段 / 计划时长','现场工作与采购','交接后才能继续'],[
['准备 / 约2-4周','毛坯交付验收、原图和结构资料、合法性核查；三家同图报价；电梯/热水/空调提前给条件图。','问题清单关闭；明确可以施工的范围及各专业责任人。审批/结构评估可能延长。'],
['放线与隐蔽 / 约3-5周','完成面与柜体设备放样；回路和给排水施工；按厂家图预留套管接口；材料进场核批次与型号。','设计负责人确认无冲突；隐蔽试验合格、照片和变更图归档后封闭。'],
['防水与湿作 / 约3-5周','基层与防水系统按技术要求施工、节点样板、试验；找坡、铺贴、养护；先检查原开发商防水。','水试验及排水检查记录；无渗漏和积水，复核实际墙地完成面。'],
['木作与涂饰 / 约3-5周','只做必要局部吊顶与检修口；墙顶饰面；橱柜与定制现场二次复尺，板材/五金样板封存。','柜体加工图签认、门洞复尺；涂饰基层状态符合材料要求后续工序。'],
['设备与家具 / 约2-3周','空调/热水/卫浴、厨房家电、门、柜、灯与地板按保护顺序安装；床垫沙发按搬运条件送装。','设备单机与联合调试；五金、开门、检修、冷凝水/热水末端验证。'],
['验收与入住准备 / 约1-2周以上','分房验收、维修、保洁、环境检测安排；使用培训、保修票据、设备型号序列号和竣工记录移交。','按适用检测要求及实际结果安排入住，不能以固定通风天数保证空气合格。']],[1.1,2.5,2.1])
para('整体可按约16-24周作初期排期参考，工序可局部交叉，但不是工期承诺；结构、许可、电梯定制交期、返工或梅雨环境可能拉长。电梯运输/生产/安装计划应独立列出，未经条件确认不付定制生产款。','small')
title('15','验收与维护：钱花在长期使用上')
table(['节点','应留下的证据','验收关注点'],[
['材料与样板','进场清单、型号批次、合格资料、封样照片','板材/涂料/胶与合同一致；不以笼统“环保板”代替等级和检测资料。'],
['水电隐蔽','管线照片带尺寸、试验记录、配电回路表','适用试验方法由设计/产品标准确定；热冷水、排水、接地保护和绝缘逐项记录。'],
['厨卫与露台','防水节点照片、试水和排水记录','闭水/淋水条件与时间按系统及当地要求约定；不自行省略门槛、地漏、穿管节点。'],
['定制与家电','竣工尺寸、调试表、保修与说明书','柜体固定防倾覆、抽屉开合、五金、边角、设备散热及检修可达。'],
['电梯与专业设备','厂家验收、用户培训、救援/维保合同','按设备分类确认适用手续；书面约定响应时限、备件、维保频率及收费，不只听销售承诺。'],
['入住后','保修问题台账、过滤器和排水口维护计划','换季检查空调冷凝水、花园排水及密封；花箱不堵排水，防水层不随意钻孔。']],[1,1.4,2.8])
title('16','三家同口径询价包')
para('本页是可交给候选施工方的询价内容，尚未发出。请先确认实际城市、现场进入和联系人，再由业主安排量房；公开资料整理不等于厂家或施工方已承接本案。')
for i,item in enumerate(C['inquiryChecklist'],1):para(f'{i:02d}. {item}','small')
para('建议采用杭州2024版住宅装饰装修施工合同示范文本及对应附件作为合同核对框架，适用时再由双方完善具体条款。定制家具同时核对浙江定制家具合同示范文本。'+ref('https://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web3246/site/attach/0/64186cb270a04ec19b154e67c0c4cad6.pdf','杭州2024住宅装饰装修施工合同示范文本')+' '+ref('https://htsfwb.samr.gov.cn/View?id=eb70112b-103d-47ec-97b0-01abbabeb18b','浙江定制家具合同示范文本2024'),'small')
table(['比较项','建议权重','要求提供的证据'],[[r['item'],str(r['weight'])+'%',r['evidence']] for r in C['scoringFramework']['criteria']],[1.3,.7,3])
para('付款按双方约定的已验收节点安排，分别写定金、进度款、尾款、变更和保修处理；不在没有合同范围和工程量时预设某个百分比为法定标准。报价最低者不自动中标，应先排除缺项和无法实施的承诺。','small')
title('17','项目总结与本次交付')
para(f'本次把P02住宅与花园方案推进到“可比较报价、可复尺选品”的采购阶段：毛坯基准、{sum(len(D[k]) for k in ['construction','furniture','appliances'])}行预算、26种成品家具原始型号研究、非标定制规格、家电卫浴组合、5家施工企业候选及3家国产电梯系列。所有主方案金额由同一整合数据汇总，Excel可替换真实报价。')
para('当前最先要办的事：确认城市区县；完成毛坯交付及现场复测；查清撤梯/开井方案能否实施；让至少两家电梯厂家和三家施工方用同一范围报价。厨房柜格、空调机位、洗烘位置和热水并发能力是下单前的重点。')
para('模型仍保持P02原图边界与尺度意向，未换入品牌实物模型。本采购补充不将家具货号、预算单价或平面示意当作可以直接开工的专业签章图。未知结构费用、完整换窗/屋面整修和封闭阳光房均未被藏入“全包”承诺。')
para('交付文件：PDF用于阅读与询价沟通；Excel用于替换正式报价和调整数量；CSV用于商家分项回填；JSON保留可追溯数据与来源；在线页面支持搜索型号与试算。旧P02图册、源图、Blender和漫游继续保留。')
# Record remaining evidence even if composite first link was sufficient in the budget table.
for r in D['appliances']:
 for e in r.get('sources',[]):ref(e['url'],e['title'])
for e in C.get('domesticElevatorSources',[]):ref(e['url'],e['title'])
title('18','来源索引与价格日期')
para('核对日期：2026-09-10。家具采用中国大陆商品详情页显示价，设备多为官网参考价或明确预算。官网公开页面支持型号与企业渠道；不构成第三方工地质量评价或本地库存、安装和成交承诺。链接可点击。','small')
for code,label,url in refrows:
 S.append(Paragraph(f'<b>{code}</b> {escape(label)}<br/><link href="{escape(url)}" color="#397A79">{escape(url)}</link>',styles['small']));S.append(Spacer(1,1));MD.append(f'{code} [{label}]({url})\n')
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(LINE);canvas.line(M,12*mm,W-M,12*mm);canvas.setFont('CN',8);canvas.setFillColor(MUT);canvas.drawString(M,7.8*mm,'第6户 / 采购补充 V1 / 2026.09.10 / 供复尺、深化与询价');canvas.drawRightString(W-M,7.8*mm,f'{doc.page}');canvas.restoreState()
file=OUT/'第6户_预算采购与施工询价.pdf'
SimpleDocTemplate(str(file),pagesize=(W,H),rightMargin=M,leftMargin=M,topMargin=13*mm,bottomMargin=17*mm,title='第6户 毛坯长期自住预算采购与施工询价',author='Howard Wang / Project team').build(S,onFirstPage=footer,onLaterPages=footer)
(OUT/'项目预算与采购总结.md').write_text('# 第6户 毛坯长期自住预算采购与施工询价\n'+ '\n'.join(MD))
r=PdfReader(file);texts=[p.extract_text() for p in r.pages];assert all(x.strip() for x in texts);assert f"{t['mainWithContingency']:,.2f}" in texts[0];print('PDF',len(r.pages),'pages',file.stat().st_size,'bytes; sources',len(refrows))
(OUT/'采购报告校验.json').write_text(json.dumps({'pages':len(r.pages),'mainBudget':t['mainWithContingency'],'rows':sum(len(D[k]) for k in ['construction','furniture','appliances']),'sources':len(refrows),'allPagesHaveText':True},ensure_ascii=False,indent=2))
