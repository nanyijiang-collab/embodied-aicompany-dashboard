#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新 company.html 中的融资表格 - 简化版"""

import json
import re

# 手动定义融资数据
funding_data = {
    '星海图': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2024年3月', 'amount': '千万级美元', 'valuation': '—', 'investors': 'IDG资本、无限基金SEE Fund等'},
            {'round': 'Pre-A轮', 'date': '2024年11月', 'amount': '超¥2亿', 'valuation': '—', 'investors': '蚂蚁集团、高瓴创投等'},
            {'round': 'A轮', 'date': '2025年2月', 'amount': '近¥3亿', 'valuation': '—', 'investors': '蚂蚁集团、凯辉基金等'},
            {'round': 'A+轮', 'date': '2025年7月', 'amount': '$1亿', 'valuation': '—', 'investors': '今日资本、美团龙珠等'},
            {'round': 'B轮', 'date': '2026年2月', 'amount': '¥10亿', 'valuation': '¥100亿', 'investors': '金鼎资本（领投）等'},
            {'round': 'B+轮', 'date': '2026年4月', 'amount': '近¥20亿', 'valuation': '>¥200亿', 'investors': '华登科技、蓝思科技等'}
        ],
        'fundingNote': '📌 成立于2023年9月，累计融资近¥50亿，估值突破¥200亿。'
    },
    '至简动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2025年7月', 'amount': '$5000万', 'valuation': '—', 'investors': '元璟资本'},
            {'round': '连续4轮', 'date': '2025年下半年–2026年初', 'amount': '累计20亿', 'valuation': '>$10亿', 'investors': '元璟资本、蓝驰创投、红杉中国等'}
        ],
        'fundingNote': '📌 成立于2025年7月，创始团队来自理想汽车。半年内连续完成5轮融资。'
    },
    '逐际动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年10月', 'amount': '未披露', 'valuation': '—', 'investors': '峰瑞资本等'},
            {'round': 'Pre-A轮', 'date': '2023年10月', 'amount': '近¥2亿', 'valuation': '—', 'investors': '绿洲资本（领投）、联想创投'},
            {'round': '战略投资', 'date': '2024年5月', 'amount': '未披露', 'valuation': '—', 'investors': '阿里巴巴'},
            {'round': 'A轮', 'date': '2024年7月', 'amount': '数亿元', 'valuation': '—', 'investors': '阿里巴巴等'},
            {'round': 'B轮', 'date': '2026年2月', 'amount': '$2亿', 'valuation': '—', 'investors': '阿联酋磊石资本等'}
        ],
        'fundingNote': '📌 成立于2022年，深圳。创始人张巍为南方科技大学长聘教授。'
    },
    '傅利叶智能': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2016年', 'amount': '未披露', 'valuation': '—', 'investors': '松禾资本'},
            {'round': 'A轮', 'date': '2017年', 'amount': '未披露', 'valuation': '—', 'investors': '深创投'},
            {'round': 'B轮', 'date': '2018年', 'amount': '未披露', 'valuation': '—', 'investors': '腾讯投资'},
            {'round': '战略融资', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '蔚来资本'},
            {'round': '战略融资', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '华为哈勃投资'},
            {'round': '战略融资', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '中国移动'}
        ],
        'fundingNote': '📌 成立于2015年，累计融资近¥10亿。计划科创板IPO。'
    },
    'Boston Dynamics': {
        'fundingTable': [
            {'round': '成立', 'date': '1992年', 'amount': '—', 'valuation': '—', 'investors': 'MIT衍生'},
            {'round': '收购', 'date': '2013年', 'amount': '—', 'valuation': '—', 'investors': 'Google收购'},
            {'round': '收购', 'date': '2017年', 'amount': '—', 'valuation': '—', 'investors': 'SoftBank收购'},
            {'round': '收购', 'date': '2021年6月', 'amount': '$11亿', 'valuation': '$11亿', 'investors': 'Hyundai Motor Group收购80%'},
            {'round': '追加投资', 'date': '2025年', 'amount': '$6270万', 'valuation': '—', 'investors': 'Hyundai Glovis'}
        ],
        'fundingNote': '📌 估值从2021年$11亿飙升至2026年约$200亿。计划2027年纳斯达克IPO。'
    },
    '小鹏鹏行': {
        'fundingTable': [
            {'round': '成立', 'date': '2016年', 'amount': '—', 'valuation': '—', 'investors': '何小鹏、小鹏汽车'},
            {'round': 'A轮', 'date': '2022年7月', 'amount': '$1亿', 'valuation': '—', 'investors': 'IDG Capital（领投）'}
        ],
        'fundingNote': '📌 成立于2016年，小鹏汽车旗下仿生机器人公司。估值超$10亿。'
    },
    '思灵机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2014年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2017年11月', 'amount': '¥4000万', 'valuation': '—', 'investors': '清控银杏（领投）'},
            {'round': 'B轮', 'date': '2018年', 'amount': '未披露', 'valuation': '—', 'investors': '顺为资本（领投）'},
            {'round': '战略轮', 'date': '2020年', 'amount': '未披露', 'valuation': '—', 'investors': '新希望集团'},
            {'round': '战略+轮', 'date': '2022年2月', 'amount': '¥4亿', 'valuation': '—', 'investors': '新希望集团'},
            {'round': '战略+轮', 'date': '2024年4月', 'amount': '超¥5亿', 'valuation': '超¥40亿', 'investors': '国家制造业转型升级基金'}
        ],
        'fundingNote': '📌 成立于2016年，全球首台自适应机器人原创者。'
    },
    '梅卡曼德': {
        'fundingTable': [
            {'round': 'Pre-A轮', 'date': '2016年9月', 'amount': '¥1500万', 'valuation': '—', 'investors': '火山石投资、IDG资本'},
            {'round': 'A轮', 'date': '2018年2月', 'amount': '¥3000万', 'valuation': '—', 'investors': '火山石投资、IDG资本'},
            {'round': 'B轮', 'date': '2019年7月', 'amount': '数千万', 'valuation': '—', 'investors': '旦恩资本等'},
            {'round': 'C轮', 'date': '2020年10月', 'amount': '¥1亿', 'valuation': '—', 'investors': '前海母基金'},
            {'round': 'D轮', 'date': '2022年1月', 'amount': '¥4亿', 'valuation': '—', 'investors': '软银愿景基金2期（领投）'},
            {'round': 'E轮', 'date': '2025年1月', 'amount': '¥8亿', 'valuation': '—', 'investors': '国鑫投资等'}
        ],
        'fundingNote': '📌 成立于2016年，工业3D视觉和AI机器人软件龙头。累计融资$3.14亿。'
    },
    'Anybotics': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2016年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2018年2月', 'amount': '$800万', 'valuation': '—', 'investors': 'Playground Global'},
            {'round': 'B轮', 'date': '2022年4月', 'amount': '$1.5亿', 'valuation': '—', 'investors': 'DCVC等'},
            {'round': 'C轮', 'date': '2024年10月', 'amount': '$1.1亿', 'valuation': '—', 'investors': 'Virginia Venture Partners等'},
            {'round': 'C3轮', 'date': '2025年6月', 'amount': '$4亿', 'valuation': '~$21亿', 'investors': 'WP Global Partners（领投）'}
        ],
        'fundingNote': '📌 成立于2016年，ETH Zurich衍生。累计融资超$2.93亿。'
    },
    '乐聚机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2024年6月', 'amount': '¥7亿', 'valuation': '—', 'investors': '美团战投、北汽产投等'},
            {'round': '战略轮', 'date': '2024年11月', 'amount': '¥5亿', 'valuation': '—', 'investors': '上汽恒旭、深创投等'},
            {'round': 'B轮', 'date': '2025年6月', 'amount': '超¥11亿', 'valuation': '—', 'investors': '宁德时代（领投）'}
        ],
        'fundingNote': '📌 成立于2016年，深圳。产品包括Aelos、Pando、夸父等系列机器人。'
    },
    'Sunday Robotics': {
        'fundingTable': [
            {'round': 'A轮', 'date': '2025年', 'amount': '$3500万', 'valuation': '—', 'investors': 'Benchmark等'},
            {'round': 'B轮', 'date': '2026年3月', 'amount': '$1.65亿', 'valuation': '$11.5亿', 'investors': 'Coatue Management（领投）'}
        ],
        'fundingNote': '📌 成立于2024年，美国山景城。专注家用机器人Memo。'
    },
    'Field AI': {
        'fundingTable': [
            {'round': '早期VC', 'date': '2023年5月', 'amount': '$1亿', 'valuation': '—', 'investors': '—'},
            {'round': '早期VC', 'date': '2024年1月', 'amount': '$9100万', 'valuation': '—', 'investors': '—'}
        ],
        'fundingNote': '📌 成立于2023年，加州。专注野外AI技术。累计融资$5.06亿。'
    },
    '加速进化': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '经纬创投、蓝驰创投'},
            {'round': 'Pre-A轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '张科垚坤基金等'},
            {'round': 'A++轮', 'date': '2026年4月', 'amount': '亿元级', 'valuation': '—', 'investors': '赛富投资基金（领投）'}
        ],
        'fundingNote': '📌 成立于2023年，北京海淀。Booster T1人形机器人。'
    },
    '帕西尼感知': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'B轮', 'date': '2026年3月', 'amount': '近¥10亿', 'valuation': '—', 'investors': '晨道资本（领投）'}
        ],
        'fundingNote': '📌 成立于2021年，专注机器人皮肤触觉智能。百亿估值俱乐部成员。'
    },
    '光轮智能': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '三七互娱、商汤科技等'},
            {'round': 'Pre-A轮', 'date': '2025年11月', 'amount': '¥2亿', 'valuation': '¥12亿', 'investors': '国方创新等'}
        ],
        'fundingNote': '📌 成立于2023年，全球首家具身数据独角兽。专注合成数据。'
    },
    'Mimic Robotics': {
        'fundingTable': [
            {'round': '早期VC', 'date': '2025年11月', 'amount': '$1600万', 'valuation': '—', 'investors': 'Elaia Partners等'}
        ],
        'fundingNote': '📌 成立于2023年，ETH Zurich衍生。专注工业灵巧手。'
    },
    '地瓜机器人': {
        'fundingTable': [
            {'round': 'A轮', 'date': '2025年5月', 'amount': '$1亿', 'valuation': '—', 'investors': '高瓴创投等'},
            {'round': 'B1轮', 'date': '2026年3月', 'amount': '$1.2亿', 'valuation': '~$12亿', 'investors': 'Synstellation Capital等'},
            {'round': 'B2轮', 'date': '2026年4月', 'amount': '$1.5亿', 'valuation': '$15亿', 'investors': 'Prosperity7 Ventures等'}
        ],
        'fundingNote': '📌 成立于2024年1月，地平线分拆。机器人软硬件通用底座。累计融资$3.7亿+。'
    },
    '七腾机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2010年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2021年', 'amount': '未披露', 'valuation': '—', 'investors': '红马资本等'},
            {'round': '增资', 'date': '2025年10月', 'amount': '¥1.3亿', 'valuation': '¥40亿', 'investors': '李起富（个人）'}
        ],
        'fundingNote': '📌 成立于2010年，重庆。专注特种机器人。累计超10轮融资。'
    },
    '云深处': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2017年', 'amount': '未披露', 'valuation': '—', 'investors': '英诺天使基金'},
            {'round': 'A轮', 'date': '2018年', 'amount': '未披露', 'valuation': '—', 'investors': '元禾原点'},
            {'round': 'C轮', 'date': '2025年7月', 'amount': '近¥5亿', 'valuation': '—', 'investors': '达晨财智、国新基金（联合领投）'}
        ],
        'fundingNote': '📌 成立于2017年，杭州，"杭州六小龙"之一。产品"绝影"系列四足机器人。'
    },
    '戴盟机器人': {
        'fundingTable': [
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '吴中金控、涌铧投资'},
            {'round': '新一轮', 'date': '2026年3月', 'amount': '近¥3亿', 'valuation': '—', 'investors': '中金汇融等'}
        ],
        'fundingNote': '📌 成立于2023年，深圳。专注高分辨率视触觉感知与灵巧操作。'
    },
    '镜识科技': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2024年10月', 'amount': '数千万', 'valuation': '¥1亿', 'investors': '深创投、方广资本、软通动力'}
        ],
        'fundingNote': '📌 成立于2024年5月，上海。"黑豹2.0"四足机器人（全球最快）。'
    },
    '优理奇智能': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': 'BV百度风投（领投）'},
            {'round': '天使轮', 'date': '2025年12月', 'amount': '未披露', 'valuation': '—', 'investors': '顺为资本（领投）'}
        ],
        'fundingNote': '📌 成立于2024年，通用具身智能机器人公司。'
    },
    '松延动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '数千万', 'valuation': '—', 'investors': '昆仲资本（独投）'},
            {'round': '天使+轮', 'date': '2024–2025年', 'amount': '亿元级', 'valuation': '—', 'investors': '国中资本、金鼎资本等'},
            {'round': '战略轮', 'date': '2025年12月', 'amount': '亿元级', 'valuation': '—', 'investors': '中国移动链长基金'}
        ],
        'fundingNote': '📌 成立于2023年，北京。"小布米"（首款万元级高性能人形机器人）。'
    },
    '开普勒人形机器人': {
        'fundingTable': [
            {'round': 'A+轮', 'date': '2025年9月', 'amount': '数亿元', 'valuation': '—', 'investors': '成都天投、中车资本等'},
            {'round': 'B轮', 'date': '2026年2月', 'amount': '超¥10亿', 'valuation': '超¥100亿', 'investors': '百度战投、中车资本等'}
        ],
        'fundingNote': '📌 成立于2023年8月，上海。产品"先行者K1/K2"人形机器人。'
    },
    '理工华汇': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2018年6月', 'amount': '未披露', 'valuation': '—', 'investors': '檀沐企业管理等'},
            {'round': 'A轮', 'date': '2018年9月', 'amount': '数千万', 'valuation': '¥1.5亿', 'investors': '和合资本、华盖资本'}
        ],
        'fundingNote': '📌 北京理工大学张伟民教授团队孵化。'
    },
    '天链机器人': {
        'fundingTable': [
            {'round': 'B轮', 'date': '2018年8月', 'amount': '数千万美元', 'valuation': '—', 'investors': '芯动能投资（领投）、联想创投'},
            {'round': '定向增发', 'date': '2024年12月', 'amount': '¥8000万', 'valuation': '约¥8亿', 'investors': '浙江思考私募基金等'}
        ],
        'fundingNote': '📌 成立于2012年，四川，新三板挂牌（川机器人）。'
    },
    '青瞳视觉': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2016年', 'amount': '数百万', 'valuation': '—', 'investors': '米粒影业等'},
            {'round': 'A轮', 'date': '2016年7月', 'amount': '未披露', 'valuation': '—', 'investors': '金复资本等'}
        ],
        'fundingNote': '📌 成立于2015年，上海。红外光学位置追踪系统研发商。'
    },
    '钛虎机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2022年3月', 'amount': '近千万美元', 'valuation': '—', 'investors': '松禾资本、真格基金'},
            {'round': 'Pre-A轮', 'date': '2022年10月', 'amount': '亿元级', 'valuation': '—', 'investors': '联创资本（领投）'},
            {'round': 'A1&A2轮', 'date': '2025年7月', 'amount': '数亿元', 'valuation': '—', 'investors': '成都科创投、洪泰基金（联合领投）'}
        ],
        'fundingNote': '📌 成立于2020年，上海。专注高性能轻量化关节模组。'
    },
    '无界动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2026年4月', 'amount': '数千万美元', 'valuation': '—', 'investors': '云启资本、顺为资本、弘晖基金等'}
        ],
        'fundingNote': '📌 成立于2025年3月，北京。聚焦机器人"通用大脑"。'
    }
}

def simple_update():
    with open('company.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated = []
    not_found = []
    
    for i, line in enumerate(lines):
        for company_name, data in funding_data.items():
            # 简单字符串匹配
            if f"'{company_name}':" in line and 'name:' in line and 'nameEn:' in line:
                # 检查是否已有 fundingTable
                if 'fundingTable' not in line:
                    # 构建新的公司定义
                    funding_rows = []
                    for row in data['fundingTable']:
                        funding_rows.append(f"{{ round: '{row['round']}', date: '{row['date']}', amount: '{row['amount']}', valuation: '{row['valuation']}', investors: '{row['investors']}' }}")
                    
                    funding_table_str = '[' + ', '.join(funding_rows) + ']'
                    note = data['fundingNote']
                    
                    new_line = line.rstrip()
                    if new_line.endswith(','):
                        new_line = new_line[:-1]
                    new_line = new_line.rstrip() + f", fundingTable: {funding_table_str}, fundingNote: '{note}' }}\n"
                    
                    lines[i] = new_line
                    updated.append(company_name)
                    print(f"✓ 已更新: {company_name}")
                    break
    
    with open('company.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n=== 更新完成 ===")
    print(f"成功更新: {len(updated)} 家公司")
    
    # 检查未处理的
    for company_name in funding_data:
        if company_name not in updated:
            print(f"- 未找到: {company_name}")

if __name__ == '__main__':
    simple_update()
