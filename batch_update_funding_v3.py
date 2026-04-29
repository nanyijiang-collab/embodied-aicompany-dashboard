#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新 company.html 中的融资表格"""

import re
import json

# 手动定义融资数据（从 generated_funding.py 提取）
funding_data = {
    '星海图': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2024年3月', 'amount': '千万级美元', 'valuation': '—', 'investors': 'IDG资本、无限基金SEE Fund等'},
            {'round': 'Pre-A轮', 'date': '2024年11月', 'amount': '超¥2亿', 'valuation': '—', 'investors': '蚂蚁集团、高瓴创投（GL Ventures，联合领投）、无锡创投、同歌创业、FunPlus等'},
            {'round': 'A轮', 'date': '2025年2月', 'amount': '近¥3亿', 'valuation': '—', 'investors': '蚂蚁集团、凯辉基金（联合领投）、IDG资本、联想创投、百度风投等'},
            {'round': 'A+轮', 'date': '2025年7月', 'amount': '$1亿', 'valuation': '—', 'investors': '今日资本、美团龙珠、龙珠资本（联合领投）、IDG资本、中金资本、百度风投、凯辉基金等'},
            {'round': 'B轮', 'date': '2026年2月', 'amount': '¥10亿', 'valuation': '¥100亿', 'investors': '金鼎资本（领投）、北汽产投、碧鸿投资、正心谷资本、前海方舟、毅峰资本；老股东凯辉基金、美团龙珠、今日资本、襄禾资本、高瓴创投超额/满额追加'},
            {'round': 'B+轮', 'date': '2026年4月', 'amount': '近¥20亿', 'valuation': '>¥200亿', 'investors': '华登科技、蓝思科技、矽芯投资、时代伯乐、航发基金、修远资本、弘章投资、御海资本、金融街资本、金浦投资、北京科创、国元股权、中金资本、普华资本、洪泰基金、广发乾和等'}
        ],
        'fundingNote': '📌 成立于2023年9月，累计融资近¥50亿，估值突破¥200亿，是四家百亿独角兽中成立时间最短的企业。'
    },
    '至简动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2025年7月', 'amount': '$5000万', 'valuation': '—', 'investors': '元璟资本'},
            {'round': '连续4轮', 'date': '2025年下半年–2026年初', 'amount': '未披露（累计20亿）', 'valuation': '>$10亿（独角兽）', 'investors': '元璟资本、蓝驰创投、红杉中国、君联资本、中科创星、高榕创投（财务投资方）；腾讯、阿里巴巴（战略投资方，同轮入局）'}
        ],
        'fundingNote': '📌 成立于2025年7月，创始团队来自理想汽车核心班底。半年内连续完成5轮融资，累计¥20亿，成为具身智能赛道最年轻的独角兽。'
    },
    '逐际动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年10月', 'amount': '未披露', 'valuation': '—', 'investors': '峰瑞资本、智数资本、明势资本、昆仲资本'},
            {'round': 'Pre-A轮', 'date': '2023年10月', 'amount': '近¥2亿（天使+Pre-A合计）', 'valuation': '—', 'investors': '绿洲资本（领投）、联想创投'},
            {'round': '战略投资', 'date': '2024年5月', 'amount': '未披露', 'valuation': '—', 'investors': '阿里巴巴'},
            {'round': 'A轮', 'date': '2024年7月', 'amount': '数亿元', 'valuation': '—', 'investors': '阿里巴巴、招商局创投、尚颀资本（联合领投）；峰瑞资本、绿洲资本、明势资本跟投'},
            {'round': 'A+轮', 'date': '2025年3月', 'amount': '未披露（A轮系列累计¥5亿）', 'valuation': '—', 'investors': '阿里巴巴、招商局创投、尚颀资本、蔚来资本、联想创投、彼岸时代、纳爱斯集团、高捷资本、绿洲资本、明势创投、峰瑞资本、南山战新投'},
            {'round': 'B轮', 'date': '2026年2月', 'amount': '$2亿（~¥14.4亿）', 'valuation': '—', 'investors': '阿联酋磊石资本Stone Venture、东方富海、基石资本、天创资本、广发信德、合肥创新投、国泰君安创新投资、中信建投、唐兴资本、财鑫资本（机构投资方）；京东、中鼎股份、光洋股份、东土科技（战略产业投资方）；老股东尚颀资本、彼岸时代、蔚来资本、明势创投持续加码'}
        ],
        'fundingNote': '📌 成立于2022年，总部位于深圳，创始人张巍为南方科技大学长聘教授。深圳机器人"八大金刚"之一。2026年开年最大一笔人形机器人融资。'
    },
    '灵心巧手': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2025年8月', 'amount': '¥10亿', 'valuation': '—', 'investors': '京东（战略领投）'},
            {'round': 'B轮', 'date': '2026年3月', 'amount': '超¥10亿', 'valuation': '超¥100亿', 'investors': '黄浦江资本、凯泰资本、信安资本（重磅领投）；珠海科技产业集团、善达资本、海川基金等联合投资；北京某国资平台、广州市新兴基金、优利德、知来资本、LEO LION、南岭基金、相城金控等跟投；毅达资本等老股东超额加码'}
        ],
        'fundingNote': '📌 成立于2023年，专注灵巧手研发，产品覆盖腱绳、直驱、连杆三大技术路线。2026年新晋百亿估值独角兽。'
    },
    '傅利叶智能': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2016年', 'amount': '未披露', 'valuation': '—', 'investors': '松禾资本'},
            {'round': 'A轮', 'date': '2017年', 'amount': '未披露', 'valuation': '—', 'investors': '深创投'},
            {'round': 'B轮', 'date': '2018年', 'amount': '未披露', 'valuation': '—', 'investors': '腾讯投资'},
            {'round': 'C轮', 'date': '2019年', 'amount': '未披露', 'valuation': '—', 'investors': '洪泰基金'},
            {'round': '战略融资', 'date': '2021年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': '战略融资', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '蔚来资本'},
            {'round': '战略融资', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '华为哈勃投资'},
            {'round': '战略融资', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '中国移动'}
        ],
        'fundingNote': '📌 成立于2015年，最初专注康复机器人，后切入通用人形机器人。累计融资近¥10亿。计划科创板IPO。'
    },
    'Boston Dynamics': {
        'fundingTable': [
            {'round': '成立/早期', 'date': '1992年', 'amount': '—', 'valuation': '—', 'investors': '麻省理工学院衍生'},
            {'round': '收购', 'date': '2013年', 'amount': '—', 'valuation': '—', 'investors': 'Google（Alphabet）收购'},
            {'round': '收购', 'date': '2017年', 'amount': '—', 'valuation': '—', 'investors': 'SoftBank收购'},
            {'round': '收购', 'date': '2021年6月', 'amount': '$11亿', 'valuation': '$11亿', 'investors': 'Hyundai Motor Group（$8.8亿获80%）；郑义宣会长个人出资$2.2亿获20%'},
            {'round': '追加投资', 'date': '2025年', 'amount': '$6270万', 'valuation': '—', 'investors': 'Hyundai Glovis追加投资'}
        ],
        'fundingNote': '📌 估值从2021年$11亿飙升至2026年约$200亿。计划2027年初纳斯达克IPO。'
    },
    '小鹏鹏行': {
        'fundingTable': [
            {'round': '成立', 'date': '2016年', 'amount': '—', 'valuation': '—', 'investors': '何小鹏、小鹏汽车'},
            {'round': 'A轮', 'date': '2022年7月', 'amount': '$1亿', 'valuation': '—', 'investors': 'IDG Capital（领投）、小鹏汽车等'}
        ],
        'fundingNote': '📌 成立于2016年，小鹏汽车旗下仿生机器人公司。2025年融资约$1.5亿，估值超$10亿。'
    },
    '思灵机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2014年12月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2017年11月', 'amount': '¥4000万', 'valuation': '—', 'investors': '清控银杏（领投）、德联资本'},
            {'round': 'B轮', 'date': '2018年', 'amount': '未披露', 'valuation': '—', 'investors': '顺为资本（领投）'},
            {'round': 'C轮', 'date': '—', 'amount': '未披露', 'valuation': '—', 'investors': '深创投'},
            {'round': '战略轮', 'date': '2020年', 'amount': '未披露', 'valuation': '—', 'investors': '新希望集团'},
            {'round': '战略+轮', 'date': '2022年2月', 'amount': '¥4亿', 'valuation': '—', 'investors': '新希望集团'},
            {'round': '战略轮', 'date': '2023年4月', 'amount': '¥4亿', 'valuation': '—', 'investors': '国家制造业转型升级基金、邹城市新动能产业投资基金'},
            {'round': '战略+轮', 'date': '2024年4月', 'amount': '超¥5亿', 'valuation': '超¥40亿', 'investors': '国家制造业转型升级基金、邹城市新动能产业投资基金'}
        ],
        'fundingNote': '📌 成立于2016年，全球首台自适应机器人原创者。2025年1月战略孵化穹彻智能。'
    },
    '梅卡曼德': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2015年7月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2016年9月', 'amount': '¥1500万', 'valuation': '—', 'investors': '火山石投资、IDG资本、张江科投'},
            {'round': 'A轮', 'date': '2018年2月', 'amount': '¥3000万', 'valuation': '—', 'investors': '火山石投资、IDG资本、前海母基金'},
            {'round': 'B轮', 'date': '2019年7月', 'amount': '数千万', 'valuation': '—', 'investors': '旦恩资本、火山石投资、IDG资本'},
            {'round': 'B+轮', 'date': '2020年5月', 'amount': '数千万', 'valuation': '—', 'investors': '前海母基金'},
            {'round': 'C轮', 'date': '2020年10月', 'amount': '¥1亿', 'valuation': '—', 'investors': '前海母基金'},
            {'round': 'C++轮', 'date': '2021年3月', 'amount': '数千万', 'valuation': '—', 'investors': '临港科创投、元璟资本'},
            {'round': 'D轮', 'date': '2022年1月', 'amount': '¥4亿', 'valuation': '—', 'investors': '软银愿景基金2期（领投）；Prosperity7 Ventures、元璟资本'},
            {'round': 'E轮', 'date': '2025年1月', 'amount': '¥8亿', 'valuation': '—', 'investors': '国鑫投资、浦东创投、张江科投、Prosperity7 Ventures、华建函数投资、铭哲资产、张科垚坤、钧山'}
        ],
        'fundingNote': '📌 成立于2016年，北京，600名员工。工业3D视觉和AI机器人软件龙头。累计融资$3.14亿。'
    },
    'Field AI': {
        'fundingTable': [
            {'round': '早期VC', 'date': '2023年5月', 'amount': '$1亿', 'valuation': '—', 'investors': '—'},
            {'round': '早期VC', 'date': '2024年1月', 'amount': '$9100万', 'valuation': '—', 'investors': '—'},
            {'round': '加速器', 'date': '2025年4月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2025年7月', 'amount': '未披露', 'valuation': '—', 'investors': '—'}
        ],
        'fundingNote': '📌 成立于2023年，总部位于加州。专注野外AI技术，支持多形态机器人自主运行。累计融资$5.06亿。'
    },
    'Anybotics': {
        'fundingTable': [
            {'round': '大学衍生', 'date': '2015年1月', 'amount': '未披露', 'valuation': '—', 'investors': 'ETH Zurich孵化'},
            {'round': '加速器/孵化器', 'date': '2015年1月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': '种子轮', 'date': '2016年10月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2018年2月', 'amount': '$800万', 'valuation': '—', 'investors': 'Playground Global、Konstantin Othmer'},
            {'round': 'B轮', 'date': '2022年4月', 'amount': '$1.5亿', 'valuation': '—', 'investors': 'DCVC、Playground Global（领投）等'},
            {'round': 'C轮', 'date': '2024年10月', 'amount': '$1.1亿', 'valuation': '—', 'investors': 'Virginia Venture Partners、Y Combinator等'},
            {'round': 'C3轮', 'date': '2025年6月', 'amount': '$4亿', 'valuation': '~$21亿', 'investors': 'WP Global Partners（领投）；SoftBank、Amazon Industrial Innovation Fund等'}
        ],
        'fundingNote': '📌 成立于2016年，ETH Zurich衍生，专注AI驱动的自主四足工业巡检机器人。累计融资超$2.93亿。'
    },
    '乐聚机器人': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '经纬创投、蓝驰创投'},
            {'round': '天使轮', 'date': '2024年6月', 'amount': '¥7亿', 'valuation': '—', 'investors': '美团战投、北汽产投、商汤国香基金、讯飞基金、启明创投等'},
            {'round': '战略轮/A轮', 'date': '2024年11月', 'amount': '¥5亿', 'valuation': '—', 'investors': '上汽恒旭、香港投资公司HKIC、深创投、上海人工智能产业基金等'},
            {'round': 'B轮', 'date': '2025年6月', 'amount': '超¥11亿', 'valuation': '—', 'investors': '宁德时代（领投）、溥泉资本、国开科创等'}
        ],
        'fundingNote': '📌 成立于2016年，总部位于深圳。产品包括Aelos、Pando、Talos、Kavo等系列机器人。'
    },
    'Sunday Robotics': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2025年', 'amount': '$3500万', 'valuation': '—', 'investors': 'Benchmark、Conviction Partners（领投）'},
            {'round': 'B轮', 'date': '2026年3月', 'amount': '$1.65亿', 'valuation': '$11.5亿', 'investors': 'Coatue Management（领投）；Bain Capital Ventures、Fidelity Management等'}
        ],
        'fundingNote': '📌 成立于2024年，总部位于美国山景城。专注家用机器人Memo。累计融资近$2亿。'
    },
    '穹彻智能': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '水木创投、源码资本'},
            {'round': 'Pre-A+轮', 'date': '2024年7月', 'amount': '近¥1亿', 'valuation': '—', 'investors': '英诺天使基金、海国投'},
            {'round': 'A轮', 'date': '2025年7月', 'amount': '未披露', 'valuation': '—', 'investors': '—'}
        ],
        'fundingNote': '📌 成立于2023年11月，由非夕科技战略孵化。专注具身智能"大脑"系统Noematrix Brain。'
    },
    '加速进化': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '张科垚坤基金、伟创电气、柯力传感'},
            {'round': 'A轮', 'date': '2025年7月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A++轮', 'date': '2026年4月', 'amount': '亿元级', 'valuation': '—', 'investors': '赛富投资基金（领投）；诺力股份、民爆光电战略入股'}
        ],
        'fundingNote': '📌 成立于2023年，总部位于北京海淀。2024年8月在世界机器人大会亮相Booster T1人形机器人。'
    },
    '帕西尼感知': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A+轮', 'date': '2025年1月', 'amount': '未披露（A轮系列累计¥5亿）', 'valuation': '—', 'investors': '—'},
            {'round': 'B轮', 'date': '2026年3月', 'amount': '近¥10亿', 'valuation': '—', 'investors': '晨道资本（宁德时代系，领投）；国科投资、京国盛基金、九合创投等跟投'}
        ],
        'fundingNote': '📌 成立于2021年，专注机器人皮肤触觉智能。跻身中国具身智能"八大百亿估值俱乐部"之一。'
    },
    '它石智航': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2026年2月', 'amount': '数亿元', 'valuation': '—', 'investors': '红杉中国、鼎晖投资、BV百度风投、云锋基金、慕华科创、均普智能、灵初智能'},
            {'round': 'Pre-A轮', 'date': '2026年3月', 'amount': '累计¥20亿', 'valuation': '—', 'investors': '上海国资徐汇资本等基金（领投）；梁溪科创产业二期母基金、锡创投等地方国资；普丰资本、钛铭资本等市场化基金'}
        ],
        'fundingNote': '📌 成立于2025年2月，创始人团队来自百度自动驾驶和华为自动驾驶。成立仅一年，两轮累计融资近$7亿。'
    },
    '智平方': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '红杉中国、蚂蚁集团、浙江创新投资等'},
            {'round': 'A+轮', 'date': '2025年11月', 'amount': '数亿元', 'valuation': '¥16亿', 'investors': '东方富海、三七互娱、琥珀资本、九派资本、辰韬资本'}
        ],
        'fundingNote': '📌 成立于2023年，创始人郭彦东博士。拥有5位斯坦福全球前2%科学家加盟。'
    },
    '千寻智能': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年12月', 'amount': '数千万', 'valuation': '—', 'investors': '九合创投、联想之星'},
            {'round': 'A轮', 'date': '2025年5月', 'amount': '数亿元', 'valuation': '—', 'investors': '美团（领投）'},
            {'round': 'A+轮', 'date': '2025年9月', 'amount': '近¥10亿', 'valuation': '—', 'investors': '阿里云、国科投资（联合领投）'},
            {'round': 'A++轮', 'date': '2026年1月', 'amount': '¥10亿', 'valuation': '—', 'investors': '字节跳动、红杉中国（联合领投）'},
            {'round': '新融资', 'date': '2026年2月', 'amount': '数亿元', 'valuation': '超¥100亿', 'investors': '上汽金控、中金上汽基金（联合领投）；美团龙珠、红杉中国等老股东'}
        ],
        'fundingNote': '📌 成立于2023年，人形具身智能产线已在宁德时代中州基地投运。'
    },
    '自变量机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2024年12月', 'amount': '¥1.5亿', 'valuation': '—', 'investors': '追创投资（追觅科技关联基金，领投）、翼朴资本'},
            {'round': '战略融资', 'date': '2025年5月', 'amount': '数亿元', 'valuation': '—', 'investors': '禾创致远、芯联基金、华映资本等'},
            {'round': 'A轮', 'date': '2026年3月', 'amount': '超¥5亿', 'valuation': '—', 'investors': '天空工场创投基金、拓普集团、金雨茂物、苏大天宫、杰创智能、爱仕达、梁创投等'}
        ],
        'fundingNote': '📌 成立于2023年12月，国内唯一同时被阿里、美团、字节三家互联网大厂布局的具身智能企业。'
    },
    '魔法原子': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2025年Q2', 'amount': '$2.42亿（~¥17.5亿）', 'valuation': '—', 'investors': '—'},
            {'round': '天使+轮', 'date': '2025年7月', 'amount': '$1.22亿', 'valuation': '~¥50亿（投前）', 'investors': '启明创投等'},
            {'round': 'Pre-A轮', 'date': '2026年4月', 'amount': '$4.55亿（~¥30亿+）', 'valuation': '~¥150亿', 'investors': '高瓴创投、红杉中国（联合领投）；美团龙珠、中金资本等财务基金；美团战投（基石战略股东）'}
        ],
        'fundingNote': '📌 成立于2024年1月，约100人，80%以上为研发人员。2026年春晚亮相人形机器人。'
    },
    '光轮智能': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '三七互娱、学大教育、商汤科技、耀途资本、线性资本、清华SEE资本、银杏谷资本'},
            {'round': 'Pre-A轮（系列）', 'date': '2025年11月', 'amount': '¥2亿', 'valuation': '¥12亿', 'investors': '国方创新（上海国际集团旗下）、国泰海通、广发信德、滴滴出行、考拉基金等'}
        ],
        'fundingNote': '📌 成立于2023年，全球首家具身数据独角兽。专注合成数据解决方案。'
    },
    '坤维科技': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2018年', 'amount': '未披露', 'valuation': '¥2000万', 'investors': 'XBOTPARK基金（李泽湘系，领投）、啟赋资本、朗科投资、云泰创新投资'},
            {'round': 'B轮', 'date': '—', 'amount': '未披露', 'valuation': '¥18亿', 'investors': '高瓴创投、源码资本、清科产投、达晨财智、Brizan Ventures V'},
            {'round': 'C轮', 'date': '2025年5月', 'amount': '¥6000万', 'valuation': '¥40.48亿', 'investors': '高秉强、邝宇开、Brizan Ventures V'}
        ],
        'fundingNote': '📌 成立于2018年，源自航天技术积淀，专注六维力传感器及关节扭矩传感器。'
    },
    '卧安机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2017年10月', 'amount': '未披露', 'valuation': '¥2000万', 'investors': 'XBOTPARK基金（李泽湘系，领投）'},
            {'round': 'B轮', 'date': '—', 'amount': '未披露', 'valuation': '¥18亿', 'investors': '高瓴创投、源码资本、清科产投、达晨财智'},
            {'round': 'C轮', 'date': '2025年5月', 'amount': '¥6000万', 'valuation': '¥40.48亿', 'investors': '高秉强、邝宇开'},
            {'round': 'IPO', 'date': '2025年12月', 'amount': 'IPO发行', 'valuation': '164亿港元', 'investors': '港交所上市（6600.HK）'}
        ],
        'fundingNote': '📌 成立于2015年，"AI具身家庭机器人第一股"。IPO前估值从天使轮¥2000万涨至C轮¥40.48亿。'
    },
    'Mimic Robotics': {
        'fundingTable': [
            {'round': '大学衍生', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': 'ETH Zurich Soft Robotics Lab孵化'},
            {'round': '加速器/孵化器', 'date': '2024年1月', 'amount': '$5790', 'valuation': '—', 'investors': '—'},
            {'round': '种子轮', 'date': '2024年4月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': '早期VC（Seed）', 'date': '2025年11月', 'amount': '$1600万（€1380万）', 'valuation': '—', 'investors': 'Elaia Partners（领投）、Speedinvest、Founderful等'}
        ],
        'fundingNote': '📌 成立于2023年，ETH Zurich衍生。专注工业灵巧手及物理AI模型。累计融资超$2590万。'
    },
    '珞石机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2016年初', 'amount': '数百万', 'valuation': '—', 'investors': '米粒影业、金复创投、上海利龙投资、杭州璞程投资'},
            {'round': 'A轮', 'date': '2016年7月', 'amount': '未披露', 'valuation': '—', 'investors': '金复资本、米粒影业、易盛投资'}
        ],
        'fundingNote': '📌 成立于2014年，山东济宁，创始人庹华。轻型工业机器人+协作机器人。累计10轮融资。'
    },
    '地瓜机器人': {
        'fundingTable': [
            {'round': '分拆成立', 'date': '2024年1月', 'amount': '—', 'valuation': '—', 'investors': '地平线机器人AIoT部门分拆'},
            {'round': 'A轮', 'date': '2025年5月', 'amount': '$1亿', 'valuation': '—', 'investors': '高瓴创投、五源资本、线性资本、和暄资本、九合创投、Vertex Growth (淡马锡旗下)等'},
            {'round': 'B1轮', 'date': '2026年3月', 'amount': '$1.2亿', 'valuation': '~$12亿', 'investors': 'Synstellation Capital、滴滴、美团龙珠、北汽产投（产业资本）'},
            {'round': 'B2轮', 'date': '2026年4月', 'amount': '$1.5亿', 'valuation': '$15亿（~¥102.5亿）', 'investors': 'Prosperity7 Ventures、远景科技集团（战略投资方）'}
        ],
        'fundingNote': '📌 成立于2024年1月，由地平线机器人分拆独立。定位机器人软硬件通用底座提供商。累计融资$3.7亿+。'
    },
    '觅蜂科技': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2026年4月', 'amount': '未披露', 'valuation': '¥40亿', 'investors': 'IDG资本、峰瑞资本、真格基金'}
        ],
        'fundingNote': '📌 成立于2026年2月，智元机器人旗下孵化的具身智能数据平台公司。'
    },
    '大晓机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2026年3月', 'amount': '累计¥20亿', 'valuation': '—', 'investors': '国开金融、国中资本、央视融媒体产业投资基金（国家队）；某数千亿上市公司旗下战投'},
            {'round': 'Pre-A轮', 'date': '2026年3月', 'amount': '（同上，共¥20亿）', 'valuation': '—', 'investors': '上海国资徐汇资本等基金（领投）；梁溪科创产业二期母基金、锡创投等地方国资'}
        ],
        'fundingNote': '📌 成立于2025年7月，商汤科技"1+X"战略孵化的具身智能实体。董事长王晓刚。'
    },
    '七腾机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2010年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2021年', 'amount': '未披露', 'valuation': '—', 'investors': '红马资本、厚雪资本、安徽省铁路基金等'},
            {'round': 'B轮', 'date': '2022年5月', 'amount': '未披露', 'valuation': '—', 'investors': '中金浦成投资公司、安徽交控招商产业投资基金'},
            {'round': '战略融资', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': '增资', 'date': '2025年10月', 'amount': '¥1.3亿', 'valuation': '¥40亿（投前）', 'investors': '李起富（个人增资）'}
        ],
        'fundingNote': '📌 成立于2010年，重庆，专注特种机器人（防爆四足、消防灭火侦察等）。累计超10轮融资。'
    },
    '云深处': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2017年', 'amount': '未披露', 'valuation': '—', 'investors': '英诺天使基金'},
            {'round': 'A轮', 'date': '2018年', 'amount': '未披露', 'valuation': '—', 'investors': '元禾原点'},
            {'round': 'B轮', 'date': '2019年', 'amount': '未披露', 'valuation': '—', 'investors': '邦盛资本'},
            {'round': 'C轮', 'date': '2020年', 'amount': '未披露', 'valuation': '—', 'investors': '深智城产投'},
            {'round': 'D轮', 'date': '2022年', 'amount': '未披露', 'valuation': '—', 'investors': '方广资本'},
            {'round': 'C轮（重新定级）', 'date': '2025年7月', 'amount': '近¥5亿', 'valuation': '—', 'investors': '达晨财智、国新基金（联合领投）；北京机器人产业发展投资基金等'}
        ],
        'fundingNote': '📌 成立于2017年，杭州，"杭州六小龙"之一。累计7轮融资，总额超¥5.66亿。'
    },
    '戴盟机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '吴中金控、涌铧投资'},
            {'round': '新一轮', 'date': '2026年3月', 'amount': '近¥3亿', 'valuation': '—', 'investors': '中金汇融、洪山资本、广州产投、谢诺投资'}
        ],
        'fundingNote': '📌 成立于2023年，深圳，香港科技大学机器人研究院创始院长王煜教授与段江哗博士联合创办。'
    },
    '镜识科技': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2024年10月', 'amount': '数千万人民币', 'valuation': '¥1亿', 'investors': '深创投、方广资本、软通动力'}
        ],
        'fundingNote': '📌 成立于2024年5月，上海。核心产品："黑豹2.0"四足机器人（全球最快）。'
    },
    '优理奇智能': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': 'BV百度风投（领投）；Momenta、九识、星海图跟投'},
            {'round': '种子+轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '速腾聚创（领投）；BV百度风投跟投'},
            {'round': '天使轮', 'date': '2025年12月', 'amount': '未披露', 'valuation': '—', 'investors': '顺为资本（领投）；初心资本、BV百度风投超额跟投'}
        ],
        'fundingNote': '📌 成立于2024年，通用具身智能机器人公司。2025年底起持续实现单月交付量破百台。'
    },
    '松延动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '数千万', 'valuation': '—', 'investors': '昆仲资本（独投）'},
            {'round': '天使+轮', 'date': '2024–2025年', 'amount': '亿元级', 'valuation': '—', 'investors': '国中资本、金鼎资本、联想创投、招银国际'},
            {'round': '天使++轮', 'date': '2025年8月', 'amount': '亿元级', 'valuation': '—', 'investors': '招商局创投（领投）；东方嘉富、架桥资本跟投'},
            {'round': '战略轮', 'date': '2025年12月', 'amount': '亿元级', 'valuation': '—', 'investors': '中国移动链长基金（独家投资）'}
        ],
        'fundingNote': '📌 成立于2023年，北京。产品矩阵：N系列、E系列、"小布米"（首款万元级高性能人形机器人）。'
    },
    '开普勒人形机器人': {
        'fundingTable': [
            {'round': 'Pre-A轮', 'date': '2025年1月', 'amount': '数亿元', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2025年3月', 'amount': '数亿元', 'valuation': '—', 'investors': '—'},
            {'round': 'A+轮', 'date': '2025年9月', 'amount': '数亿元', 'valuation': '—', 'investors': '成都天投、中车资本、城濮投资、科晟基金、常州高新投'},
            {'round': 'B轮系列（5轮）', 'date': '2026年2月', 'amount': '超¥10亿', 'valuation': '超¥100亿', 'investors': '百度战投、中车资本、宇信科技、森麒麟、沄柏资本、国泰海通'}
        ],
        'fundingNote': '📌 成立于2023年8月，上海。产品"先行者K1/K2"人形机器人。'
    },
    '理工华汇': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2018年6月', 'amount': '未披露', 'valuation': '—', 'investors': '檀沐企业管理、时代聚创科技、启智投资等'},
            {'round': 'A轮', 'date': '2018年9月', 'amount': '数千万人民币', 'valuation': '¥1.5亿', 'investors': '和合资本、华盖资本'}
        ],
        'fundingNote': '📌 北京理工大学张伟民教授团队孵化，专注人形机器人及其核心部件。'
    },
    '卓益得机器人': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2025年6月', 'amount': '数千万元', 'valuation': '¥1.5亿', 'investors': '联想之星（领投）；智谱Z基金、燕缘创投、彬复资本跟投'}
        ],
        'fundingNote': '📌 成立于2021年，上海。产品："硅基少女"Moya（全球首款完全仿生具身智能机器人，定价¥120–150万）。'
    },
    '天链机器人': {
        'fundingTable': [
            {'round': 'A轮', 'date': '2017年12月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'B轮', 'date': '2018年8月', 'amount': '数千万美元', 'valuation': '—', 'investors': '芯动能投资（国家大基金发起，领投）；联想创投'},
            {'round': '定向增发', 'date': '2024年12月', 'amount': '¥8000万', 'valuation': '约¥8亿', 'investors': '浙江思考私募基金、嘉兴川龙股权投资等'}
        ],
        'fundingNote': '📌 成立于2012年，四川，新三板挂牌（川机器人）。主营谐波减速机、协作机器人、人形机器人。'
    },
    '青瞳视觉': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2016年初', 'amount': '数百万', 'valuation': '—', 'investors': '米粒影业、金复创投、上海利龙投资、杭州璞程投资'},
            {'round': 'A轮', 'date': '2016年7月', 'amount': '未披露', 'valuation': '—', 'investors': '金复资本、米粒影业、易盛投资'}
        ],
        'fundingNote': '📌 成立于2015年8月，上海。红外光学位置追踪系统研发商。'
    },
    '钛虎机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2022年3月', 'amount': '近千万美元', 'valuation': '—', 'investors': '松禾资本、真格基金'},
            {'round': 'Pre-A轮', 'date': '2022年10月', 'amount': '亿元级人民币', 'valuation': '—', 'investors': '联创资本（领投）'},
            {'round': '战略融资', 'date': '2024年5月', 'amount': '未披露', 'valuation': '—', 'investors': '联想创投（领投）'},
            {'round': 'A轮', 'date': '2025年1月', 'amount': '未披露', 'valuation': '—', 'investors': '清智资本、天鹰资本'},
            {'round': 'A1&A2轮', 'date': '2025年7月', 'amount': '数亿元', 'valuation': '—', 'investors': '成都科创投、洪泰基金（联合领投）'}
        ],
        'fundingNote': '📌 成立于2020年，上海。专注高性能轻量化关节模组。'
    },
    '爱动超越': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2017年6月', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '松禾资本（领投）'}
        ],
        'fundingNote': '📌 成立于2017年6月，北京。人工智能技术应用服务商。'
    },
    '灵宇宙': {
        'fundingTable': [
            {'round': '种子轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '英诺天使基金、水木校友种子基金、远镜创投'},
            {'round': '种子+轮', 'date': '2025年', 'amount': '未披露', 'valuation': '—', 'investors': '华映资本（领投）'},
            {'round': '天使轮', 'date': '2026年3月', 'amount': '数千万元', 'valuation': '—', 'investors': '银河创新资本（领投）；国海创新资本、天鹰资本等跟投'}
        ],
        'fundingNote': '📌 成立于2023年，上海。定位关系式交互大模型，从家庭场景消费级机器人切入。'
    },
    '无界动力': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2026年4月', 'amount': '数千万美元', 'valuation': '—', 'investors': '云启资本、顺为资本、弘晖基金、小米集团、星海图、百度风投、英诺天使基金、东方嘉富'},
            {'round': '连续融资', 'date': '2026年', 'amount': '未披露', 'valuation': '—', 'investors': '远景科技集团、Prosperity7 Ventures'}
        ],
        'fundingNote': '📌 成立于2025年3月，北京。聚焦构建机器人"通用大脑"与"操作智能"。'
    },
    '破壳机器人': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2026年2月10日', 'amount': '未披露', 'valuation': '—', 'investors': '蚂蚁集团（领投）、启明创投、金景资本、弘毅投资、联想创投、上海交大母基金菡源资产'}
        ],
        'fundingNote': '📌 家庭机器人研发生产商，技术路线：轮式底盘+双臂形态。'
    },
    '灵初智能': {
        'fundingTable': [
            {'round': '天使轮', 'date': '2023年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'Pre-A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A轮', 'date': '2024年', 'amount': '未披露', 'valuation': '—', 'investors': '—'},
            {'round': 'A+轮', 'date': '2025年1月', 'amount': '未披露（A轮系列累计¥5亿）', 'valuation': '—', 'investors': '—'}
        ],
        'fundingNote': '📌 成立于2024年9月，北京海淀。通用灵巧操作智能体，聚焦端到端VLA大模型。'
    }
}

def update_company_html():
    with open('company.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_count = 0
    not_found = []
    
    for company_name, data in funding_data.items():
        # 查找简单映射模式
        pattern = rf"('{company_name}':\s*\{{\s*name:\s*'{company_name}'"
        
        match = re.search(pattern, content)
        if match:
            start = match.start()
            line_end = content.find('\n', start)
            if line_end == -1:
                line_end = len(content)
            
            old_line = content[start:line_end]
            
            # 检查是否已有 fundingTable
            if 'fundingTable' not in old_line:
                # 提取 nameEn
                name_match = re.search(r"nameEn:\s*'([^']+)'", old_line)
                name_en = name_match.group(1) if name_match else company_name
                
                # 构建 fundingTable 字符串
                funding_table_str = json.dumps(data['fundingTable'], ensure_ascii=False)
                # 转换为 JavaScript 对象格式
                funding_table_js = funding_table_str.replace('"', '').replace(': ', ': ').replace(', ', ', ')
                
                new_line = f"'{company_name}': {{ name: '{company_name}', nameEn: '{name_en}', fundingTable: {funding_table_js}, fundingNote: '{data['fundingNote']}' }}"
                
                content = content[:start] + new_line + content[line_end:]
                updated_count += 1
                print(f"✓ 已更新: {company_name}")
            else:
                print(f"- 已有融资表格: {company_name}")
        else:
            not_found.append(company_name)
    
    with open('company.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n=== 更新完成 ===")
    print(f"成功更新: {updated_count} 家公司")
    if not_found:
        print(f"未找到: {len(not_found)} 家")
        for name in not_found[:15]:
            print(f"  - {name}")

if __name__ == '__main__':
    update_company_html()
