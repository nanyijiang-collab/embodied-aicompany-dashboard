#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新剩余公司的融资表格"""

def update_remaining():
    with open('company.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 剩余公司的融资数据
    remaining_data = {
        '灵心巧手': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
                {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
                {'round': 'A轮', 'date': '2025年8月', 'amount': '¥10亿', 'valuation': '—', 'investors': '京东（战略领投）'},
                {'round': 'B轮', 'date': '2026年3月', 'amount': '超¥10亿', 'valuation': '超¥100亿', 'investors': '黄浦江资本、凯泰资本等'}
            ],
            'fundingNote': '📌 成立于2023年，专注灵巧手研发。2026年新晋百亿估值独角兽。'
        },
        '穹彻智能': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
                {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '水木创投、源码资本'},
                {'round': 'Pre-A+轮', 'date': '2024年7月', 'amount': '近¥1亿', 'valuation': '—', 'investors': '英诺天使基金、海国投'},
                {'round': 'A轮', 'date': '2025年7月', 'amount': '未披露', 'valuation': '—', 'investors': '—'}
            ],
            'fundingNote': '📌 成立于2023年11月，由非夕科技战略孵化。专注具身智能"大脑"系统。'
        },
        '它石智航': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2026年2月', 'amount': '数亿元', 'valuation': '—', 'investors': '红杉中国、鼎晖投资、百度风投等'},
                {'round': 'Pre-A轮', 'date': '2026年3月', 'amount': '累计¥20亿', 'valuation': '—', 'investors': '上海国资徐汇资本（领投）等'}
            ],
            'fundingNote': '📌 成立于2025年2月，创始人团队来自百度、华为。累计融资近$7亿。'
        },
        '智平方': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
                {'round': 'A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '红杉中国、蚂蚁集团等'},
                {'round': 'A+轮', 'date': '2025年11月', 'amount': '数亿元', 'valuation': '¥16亿', 'investors': '东方富海、三七互娱等'}
            ],
            'fundingNote': '📌 成立于2023年，创始人郭彦东博士。5位斯坦福全球前2%科学家加盟。'
        },
        '千寻智能': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2023年12月', 'amount': '数千万', 'valuation': '—', 'investors': '九合创投、联想之星'},
                {'round': 'A轮', 'date': '2025年5月', 'amount': '数亿元', 'valuation': '—', 'investors': '美团（领投）'},
                {'round': 'A+轮', 'date': '2025年9月', 'amount': '近¥10亿', 'valuation': '—', 'investors': '阿里云、国科投资（联合领投）'},
                {'round': 'A++轮', 'date': '2026年1月', 'amount': '¥10亿', 'valuation': '—', 'investors': '字节跳动、红杉中国（联合领投）'},
                {'round': '新融资', 'date': '2026年2月', 'amount': '数亿元', 'valuation': '超¥100亿', 'investors': '上汽金控、中金上汽基金（联合领投）'}
            ],
            'fundingNote': '📌 成立于2023年，人形具身智能产线已在宁德时代投运。'
        },
        '自变量机器人': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2024年12月', 'amount': '¥1.5亿', 'valuation': '—', 'investors': '追创投资（领投）、翼朴资本'},
                {'round': '战略融资', 'date': '2025年5月', 'amount': '数亿元', 'valuation': '—', 'investors': '禾创致远、芯联基金、华映资本等'},
                {'round': 'A轮', 'date': '2026年3月', 'amount': '超¥5亿', 'valuation': '—', 'investors': '天空工场创投基金、拓普集团等'}
            ],
            'fundingNote': '📌 成立于2023年12月，唯一同时被阿里、美团、字节布局的具身智能企业。'
        },
        '魔法原子': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2025年Q2', 'amount': '$2.42亿', 'valuation': '—', 'investors': '—'},
                {'round': '天使+轮', 'date': '2025年7月', 'amount': '$1.22亿', 'valuation': '~¥50亿', 'investors': '启明创投等'},
                {'round': 'Pre-A轮', 'date': '2026年4月', 'amount': '$4.55亿', 'valuation': '~¥150亿', 'investors': '高瓴创投、红杉中国（联合领投）'}
            ],
            'fundingNote': '📌 成立于2024年1月，约100人。2026年春晚亮相人形机器人。'
        },
        '坤维科技': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2018年', 'amount': '未披露', 'valuation': '¥2000万', 'investors': 'XBOTPARK基金（领投）'},
                {'round': 'B轮', 'date': '—', 'amount': '未披露', 'valuation': '¥18亿', 'investors': '高瓴创投、源码资本等'},
                {'round': 'C轮', 'date': '2025年5月', 'amount': '¥6000万', 'valuation': '¥40.48亿', 'investors': '高秉强等'}
            ],
            'fundingNote': '📌 成立于2018年，源自航天技术积淀，专注六维力传感器。'
        },
        '卧安机器人': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2017年10月', 'amount': '未披露', 'valuation': '¥2000万', 'investors': 'XBOTPARK基金（领投）'},
                {'round': 'B轮', 'date': '—', 'amount': '未披露', 'valuation': '¥18亿', 'investors': '高瓴创投、源码资本等'},
                {'round': 'C轮', 'date': '2025年5月', 'amount': '¥6000万', 'valuation': '¥40.48亿', 'investors': '高秉强等'},
                {'round': 'IPO', 'date': '2025年12月', 'amount': 'IPO发行', 'valuation': '164亿港元', 'investors': '港交所上市（6600.HK）'}
            ],
            'fundingNote': '📌 成立于2015年，"AI具身家庭机器人第一股"。'
        },
        '珞石机器人': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2016年', 'amount': '数百万', 'valuation': '—', 'investors': '米粒影业、金复创投等'},
                {'round': 'A轮', 'date': '2016年7月', 'amount': '未披露', 'valuation': '—', 'investors': '金复资本等'}
            ],
            'fundingNote': '📌 成立于2014年，山东济宁。轻型工业机器人+协作机器人。累计10轮融资。'
        },
        '觅蜂科技': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2026年4月', 'amount': '未披露', 'valuation': '¥40亿', 'investors': 'IDG资本、峰瑞资本、真格基金'}
            ],
            'fundingNote': '📌 成立于2026年2月，智元机器人旗下孵化的具身智能数据平台公司。'
        },
        '大晓机器人': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2026年3月', 'amount': '累计¥20亿', 'valuation': '—', 'investors': '国开金融、国中资本、央视融媒体基金等'},
                {'round': 'Pre-A轮', 'date': '2026年3月', 'amount': '（同上）', 'valuation': '—', 'investors': '上海国资徐汇资本（领投）等'}
            ],
            'fundingNote': '📌 成立于2025年7月，商汤科技"1+X"战略孵化。董事长王晓刚。'
        },
        '灵初智能': {
            'fundingTable': [
                {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
                {'round': 'A+轮', 'date': '2025年1月', 'amount': '未披露（A轮系列累计¥5亿）', 'valuation': '—', 'investors': '—'}
            ],
            'fundingNote': '📌 成立于2024年9月，北京海淀。通用灵巧操作智能体。'
        },
        '戴盟': {
            'fundingTable': [
                {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '吴中金控、涌铧投资'},
                {'round': '新一轮', 'date': '2026年3月', 'amount': '近¥3亿', 'valuation': '—', 'investors': '中金汇融、洪山资本、广州产投等'}
            ],
            'fundingNote': '📌 成立于2023年，深圳。专注高分辨率视触觉感知与灵巧操作。'
        }
    }
    
    updated = []
    
    for company_name, data in remaining_data.items():
        # 构建 fundingTable JavaScript 代码
        funding_rows = []
        for row in data['fundingTable']:
            funding_rows.append(f"{{ round: '{row['round']}', date: '{row['date']}', amount: '{row['amount']}', valuation: '{row['valuation']}', investors: '{row['investors']}' }}")
        
        funding_table_str = '[' + ', '.join(funding_rows) + ']'
        note = data['fundingNote']
        
        # 查找并替换
        old_pattern = f"'{company_name}': {{ name: '{company_name}'"
        if old_pattern in content and 'fundingTable' not in content[content.find(old_pattern):content.find(old_pattern)+200]:
            # 找到简单映射
            idx = content.find(old_pattern)
            # 找到这一行的结束
            line_end = content.find('\n', idx)
            old_line = content[idx:line_end]
            
            # 提取 nameEn
            import re
            name_match = re.search(r"nameEn:\s*'([^']+)'", old_line)
            name_en = name_match.group(1) if name_match else company_name
            
            # 构建新行
            new_line = f"'{company_name}': {{ name: '{company_name}', nameEn: '{name_en}', fundingTable: {funding_table_str}, fundingNote: '{note}' }}"
            
            content = content[:idx] + new_line + content[line_end:]
            updated.append(company_name)
            print(f"✓ 已更新: {company_name}")
    
    with open('company.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n=== 补充更新完成 ===")
    print(f"成功更新: {len(updated)} 家公司")

if __name__ == '__main__':
    update_remaining()
