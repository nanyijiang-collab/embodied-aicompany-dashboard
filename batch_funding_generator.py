#!/usr/bin/env python3
"""
批量更新融资表格脚本
从Word文档提取融资数据，添加到company.html
"""
from docx import Document
import re
import os

# 读取Word文档
doc = Document('C:/Users/ZhuanZ/Desktop/公司的融资轮次.docx')

# 提取所有表格数据
all_tables = []
for table in doc.tables:
    rows = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        rows.append(cells)
    all_tables.append(rows)

# 表格到公司的映射
table_to_company = {
    9: ('星海图', 'Galaxea'),
    10: ('至简动力', 'Simplexity Robotics'),
    11: ('逐际动力', 'LimX Dynamics'),
    13: ('灵心巧手', 'Linkhou'),
    14: ('坤维科技', 'Kunwei'),
    15: ('卧安机器人', 'Woan'),
    16: ('光轮智能', 'Lucid'),
    17: ('Anybotics', 'Anybotics'),
    18: ('Mimic Robotics', 'Mimic Robotics'),
    19: ('加速进化', 'RobotEra'),
    20: ('帕西尼感知', 'PaXini'),
    21: ('穹彻智能', 'Omni'),
    23: ('它石智航', 'T-Robot'),
    24: ('智平方', 'SmartSquare'),
    25: ('千寻智能', 'Seeker'),
    26: ('自变量机器人', 'X Square Robot'),
    27: ('魔法原子', 'Magic Atom'),
    28: ('乐聚机器人', 'Leju'),
    29: ('Sunday Robotics', 'Sunday Robotics'),
    30: ('傅利叶智能', 'Fourier'),
    32: ('Boston Dynamics', 'Boston Dynamics'),
    33: ('思灵机器人', 'Flexiv'),
    34: ('小鹏鹏行', 'Xpeng Robotics'),
    36: ('Field AI', 'Field AI'),
    37: ('梅卡曼德', 'Mech-Mind'),
    38: ('破壳机器人', 'Poke'),
    39: ('灵初智能', 'PsiBot'),
    40: ('珞石机器人', 'Ruoshi'),
    41: ('地瓜机器人', 'D-Robotics'),
    42: ('觅蜂科技', 'Meef'),
    43: ('大晓机器人', 'Daxiao'),
    44: ('七腾机器人', 'Qiteng'),
    45: ('云深处', 'DeepRobotics'),
    46: ('戴盟机器人', 'Daimeng'),
    49: ('镜识科技', 'In-Sight'),
    50: ('优理奇智能', 'UniX AI'),
    51: ('松延动力', 'Songyan'),
    52: ('开普勒人形机器人', 'Kepler'),
    53: ('理工华汇', 'Hui'),
    55: ('思特威', 'SmartSens'),
    57: ('卓益得机器人', 'Zhuoyi'),
    58: ('天链机器人', 'Tianlian'),
    59: ('青瞳视觉', 'Qingtong'),
    60: ('钛虎机器人', 'Tiger'),
    61: ('爱动超越', 'Aidong'),
    62: ('灵宇宙', 'Ling Universe'),
    65: ('无界动力', 'Wujie'),
}

# 公司融资总结（从Word文档段落提取）
company_summaries = {
    '星海图': '📌 成立于2023年9月，累计融资近¥50亿，估值突破¥200亿，是四家百亿独角兽中成立时间最短的企业。',
    '至简动力': '📌 成立于2025年7月，创始团队来自理想汽车核心班底。半年内连续完成5轮融资，累计¥20亿，成为具身智能赛道最年轻的独角兽。',
    '逐际动力': '📌 成立于2022年，总部深圳，创始人张巍为南方科技大学长聘教授。深圳机器人"八大金刚"之一。',
    '灵心巧手': '📌 成立于2023年，专注灵巧手研发，产品覆盖腱绳、直驱、连杆三大技术路线。2026年新晋百亿估值独角兽。',
    '光轮智能': '📌 成立于2023年，全球首家具身数据独角兽。专注合成数据解决方案。',
    'Anybotics': '📌 成立于2016年，ETH Zurich衍生，专注AI驱动的自主四足工业巡检机器人ANYmal。累计融资超$2.93亿。',
    'Mimic Robotics': '📌 成立于2023年，ETH Zurich衍生。专注工业灵巧手及物理AI模型。累计融资超$2590万。',
    '加速进化': '📌 成立于2023年，总部北京海淀。2024年8月在世界机器人大会亮相Booster T1人形机器人。',
    '帕西尼感知': '📌 成立于2021年，专注机器人皮肤触觉智能。跻身中国具身智能"八大百亿估值俱乐部"之一。',
    '穹彻智能': '📌 成立于2023年11月，由非夕科技战略孵化。专注具身智能"大脑"系统Noematrix Brain。',
    '它石智航': '📌 成立于2025年2月，创始团队来自百度自动驾驶和华为自动驾驶。成立仅一年，两轮累计融资近$7亿。',
    '智平方': '📌 成立于2023年，创始人郭彦东博士。拥有5位斯坦福全球前2%科学家加盟。',
    '千寻智能': '📌 成立于2023年，人形具身智能产线已在宁德时代中州基地投运。',
    '自变量机器人': '📌 成立于2023年12月，国内唯一同时被阿里、美团、字节三家大厂布局的具身智能企业。累计融资超¥30亿。',
    '魔法原子': '📌 成立于2024年1月，约100人。2026年春晚亮相人形机器人。',
    '乐聚机器人': '📌 成立于2016年，总部深圳。产品包括Aelos、Pando、Talos、Kavo等系列机器人。',
    'Sunday Robotics': '📌 成立于2024年，总部美国山景城。专注家用机器人Memo。累计融资近$2亿。',
    '傅利叶智能': '📌 成立于2015年，最初专注康复机器人，后切入通用人形机器人。累计融资近¥10亿。',
    'Boston Dynamics': '📌 估值从2021年$11亿飙升至2026年约$200亿。计划2027年初纳斯达克IPO。',
    '思灵机器人': '📌 成立于2016年，全球首台自适应机器人原创者。2025年1月战略孵化穹彻智能。',
    '小鹏鹏行': '📌 成立于2016年，小鹏汽车旗下仿生机器人公司。2025年融资约$1.5亿，估值超$10亿。',
    'Field AI': '📌 成立于2023年，总部加州。专注野外AI技术。累计融资$5.06亿，181名员工。',
    '梅卡曼德': '📌 成立于2016年，北京，600名员工。工业3D视觉和AI机器人软件龙头。累计融资$3.14亿。',
    '破壳机器人': '📌 家庭机器人研发生产商，技术路线：轮式底盘+双臂形态。',
    '灵初智能': '📌 成立于2024年9月，北京海淀。通用灵巧操作智能体。创始人王启斌博士。',
    '珞石机器人': '📌 成立于2014年，山东济宁。轻型工业机器人+协作机器人，2023年出货量超5000台。',
    '地瓜机器人': '📌 成立于2024年1月，由地平线机器人分拆独立。累计融资$3.7亿+，估值$15亿。',
    '觅蜂科技': '📌 专注具身智能，核心产品为Alpha系列机器人。',
    '大晓机器人': '📌 专注机器人研发。',
    '七腾机器人': '📌 专注工业巡检机器人。',
    '云深处': '📌 专注四足机器人研发。',
    '戴盟机器人': '📌 专注具身智能。',
    '镜识科技': '📌 专注机器人视觉。',
    '优理奇智能': '📌 专注具身智能。',
    '松延动力': '📌 专注人形机器人。',
    '开普勒人形机器人': '📌 专注人形机器人研发。',
    '理工华汇': '📌 专注机器人。',
    '思特威': '📌 成立于2011年，高性能CMOS图像传感器芯片设计公司。',
    '卓益得机器人': '📌 成立于2021年，上海。产品"硅基少女"Moya。',
    '天链机器人': '📌 成立于2012年，四川，新三板挂牌（川机器人）。主营谐波减速机、协作机器人、人形机器人。',
    '青瞳视觉': '📌 成立于2015年8月，上海。红外光学位置追踪系统研发商。',
    '钛虎机器人': '📌 成立于2020年，上海。专注高性能轻量化关节模组。',
    '爱动超越': '📌 成立于2017年6月，北京。人工智能技术应用服务商。',
    '灵宇宙': '📌 成立于2023年，上海。创始人顾嘉唯。定位关系式交互大模型。',
    '无界动力': '📌 成立于2025年3月，北京。创始人张玉峰（前地平线副总裁）。',
}

def table_to_funding_js(company_name, table_idx, summary):
    """将表格数据转换为JavaScript fundingTable代码"""
    if table_idx >= len(all_tables):
        return None
    
    table = all_tables[table_idx]
    if not table or len(table) < 2:
        return None
    
    # 跳过表头
    rows = table[1:]
    
    funding_rows = []
    for row in rows:
        if len(row) >= 5:
            round_name = row[0] if row[0] else '—'
            date = row[1] if row[1] else '—'
            amount = row[2] if row[2] else '—'
            valuation = row[3] if row[3] else '—'
            investors = row[4] if row[4] else '—'
            
            # 转义引号
            round_name = round_name.replace("'", "\\'").replace('"', '\\"')
            investors = investors.replace("'", "\\'").replace('"', '\\"')
            
            funding_rows.append(f"{{ round: '{round_name}', date: '{date}', amount: '{amount}', valuation: '{valuation}', investors: '{investors}' }}")
    
    if not funding_rows:
        return None
    
    code = f"""                    fundingTable: [
                        {', '.join(funding_rows)}
                    ],
                    fundingNote: '{summary}'"""
    
    return code

# 生成所有融资数据
print("=" * 60)
print("批量融资数据生成")
print("=" * 60)
print()

generated = {}
for table_idx, (company, name_en) in table_to_company.items():
    summary = company_summaries.get(company, f'📌 {company}融资数据。')
    code = table_to_funding_js(company, table_idx, summary)
    if code:
        generated[company] = code
        print(f"✅ {company} (表格{table_idx})")

print()
print(f"共生成 {len(generated)} 家公司融资数据")

# 保存到文件
with open('c:/Users/ZhuanZ/WorkBuddy/20260422102414/generated_funding.py', 'w', encoding='utf-8') as f:
    f.write("#!/usr/bin/env python3\n")
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("\"\"\"Generated funding data\"\"\"\n\n")
    f.write(f"generated_funding = {repr(generated)}")

print()
print("✅ 融资数据已保存到 generated_funding.py")
