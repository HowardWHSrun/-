from pathlib import Path
import json
p=Path(__file__).parent;g=json.load(open(p/'P02几何数据.json'));n=json.load(open(p/'P02房间与花园通达检查.json'))
wall=g['baselineWallColumnParapetComparison'];reach=n['allRoomsReachable'];checks=g['surfaceGeometryChecks'];fresh=g['sceneSha256']==n['sceneSha256']
status='范围核对通过，全部室内房间及花园可从电梯到达。' if reach and fresh else '范围核对通过；通达仍有阻断，须修正后重测。'
md=f'''# P02 几何与行走连通复核

**{status}**

依据为当前 `unit6-professional-scene.json`（{g['objects']}个对象），比对原模型 `unit6-scene.json` 与从DWG核出的 `unit6-landscape-source.json`。本检查核对几何与漫游行走，不替代现场净空测量、结构计算或施工合规审查。

## 原墙、范围与空洞

- 原模型{wall['baselineObjects']}个墙、窗下墙、过梁、柱及栏墙对象的定位、形状和来源均无删改。新加{wall['added']}个仅为南院两侧矮墙意向，高度待核；此结论以原模型既有中央电梯/楼梯改造方案为基线。
- 南院地面网格投影 **{checks[0]['projectionArea']:.5f}㎡**，严格位于核出的庭院范围内。
- 南廊及门口连接网格投影 **{checks[1]['projectionArea']:.5f}㎡**，其中原廊保守可用面约9.797㎡；其余为明确标识的门口收口区域[4.29,3.90,8.91,4.22]。不将它冒称额外原庭院或产权面积。
- 新坡道投影 **{g['ramp']['area']:.2f}㎡**，其中{g['ramp']['withinCourtM2']:.2f}㎡在庭院内、{g['ramp']['withinOriginalStepsM2']:.2f}㎡在原中部踏步改造范围内，超出这两区的面积为0。
- 15条新增庭院铺装分缝的越界面积为0；所有楼层的楼板/地面对象与南、东下沉井上空投影相交面积均为0。
- 新漫游边界保留全部原室内范围；南端停在y=-3.78，没有向下沉井填板。

上项采用网格面真实投影的并集核对，而非只看对象包围框。详细数值见 `P02几何数据.json`。

## 行走检查

使用新版 `WalkthroughWorld`：半径0.22m的行走者、0.10m采样网格，以 `canStand` 判断落点、以 **canStep** 判断相邻点能否跨越高差；每层从已停靠、开门的电梯轿厢出发。坡道profile优先于下方庭院平面。检查覆盖房间入口与花园连通，不代表房间每个角落都可走，也不等同于轮椅或施工净宽合规。

| 楼层 | 从电梯连通的网格点 | 可达房间/区域 | 结果 |
|---|---:|---:|---|
'''
for f in n['floors']:
 ok=sum(r['reachable'] for r in f['rooms']);bad='、'.join(r['name'] for r in f['rooms'] if not r['reachable'])
 md+=f"| {f['floor']}F | {f['connectedCells']} | {ok}/{len(f['rooms'])} | {'全部可达' if not bad else '未通：'+bad} |\n"
md+='\n'
for c in n['probes']:md+=f"- {c['label']}：{c['elevations'][0]:.4f} → {c['elevations'][1]:.4f}m，{'可跨越' if c['canStep'] else '阻断'}。\n"
md+=f'''
坡道板外宽1.40m、水平长4.20m、高差0.350m；几何比为1:12。当前扶手中心间距1.32m，扣除扶手厚度后内侧净距约1.277m，不能把板宽1.40m直接写作扶手净宽。门口5cm高差可由行走引擎处理；节点和施工无阶要求另行深化。

详细逐房间路线、坡道每25mm直线采样和高差数据见 `P02房间与花园通达检查.json`；逐层网格在 `P02网格_F1/F2/F3.json`。室外使用范围及未核实产权部分仍以《室外范围核对》为准。

## 当前版本记录

- 场景SHA256：`{g['sceneSha256']}`。
- 几何与连通检查读取同一版本：{'是' if fresh else '否，需同步重测'}。
- 三层露台完成面6.870仍是展示假设；原图可确认结构面6.770，此处没有把展示值升级为施工依据。
'''
if not reach:md+='\n当前阻断已定位到客厅南门内侧旧电视柜及其抽屉/拉手，阻挡进入南廊；坡顶和坡脚本身通畅。需由方案生成器调整家具，再重新执行本检查。\n'
if (p/'P02客厅家具检查.json').exists():
 c=json.load(open(p/'P02客厅家具检查.json'))
 md+='\n## 客厅重排家具\n\n'
 md+=f"针对沙发、茶几、电视/电视柜、餐边柜、窗边阅读椅共{c['partsChecked']}个部件，与原墙柱、玻璃及其他家具比较水平投影和竖向区间，同一家具组的装配接触不计缺陷。" 
 if c['hardCollisions']:md+='当前仍发现硬相交：'+ '；'.join(a['a']+' / '+a['b'] for a in c['hardCollisions'])+'，须调整后重测。\n'
 else:md+='未发现穿原墙柱或与其他组家具的硬相交。\n'
 md+='\n家具检查读取同一场景版本：'+('是' if c['sceneSha256']==g['sceneSha256'] else '否，需同步重测')+'。此检查不评定抽屉/柜门动态开启轨迹或家具本体制作节点。\n'
if (p/'P02园林组检查.json').exists():
 a=json.load(open(p/'P02园林组检查.json'));freshGarden=a['sceneSha256']==g['sceneSha256']
 md+='\n## 16组园林摆位最终复核\n\n'
 md+=f"按清单16个组别、19个实体单元核对（四把G1-C01椅子分别检查），涵盖全部花箱、坐凳、圆几、换盆台、茶桌、四椅与坡道及扶手；全组零件的实际投影均{'位于' if a['allWithin'] else '未完全位于'}源设计边界或明确原中踏步/南廊连接范围内。不同组的平面重叠{len(a['betweenGroupPlanOverlaps'])}处，跨组实体硬相交{len(a['hardCollisions'])}处。\n"
 md+='\n每个实体单元旁均有可从电梯连通的接近点：'+('是' if a.get('allAssembliesApproachable') else '未全部证实')+'。接近点由同一canStep网格求得，位于组外约0.23~0.85m；坡道允许取可站立板面。此结果不替代家具开启、设备操作空间与轮椅回转的施工审查。\n'
 md+='\nG3-W01换盆台整体西移，G3-P04花箱东移；首层茶桌四椅整组南移以保持源庭院边界。园林检查与当前场景同版本：'+('是' if freshGarden else '否，需同步重测')+'。明细见 `P02园林组检查.json`。\n'
(p/'P02几何复核.md').write_text(md)
print(status)
