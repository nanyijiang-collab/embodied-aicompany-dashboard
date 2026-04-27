#!/usr/bin/env python3
import re

# Read the file
with open(r'c:\Users\ZhuanZ\WorkBuddy\20260422102414\company.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The new complete rankingData from index.html
new_rankingData = '''        // rankingData - 所有公司基础数据（与index.html同步）
        const rankingData = [
            { company: 'Figure AI', valuation: '390亿美元', valuationCNY: 390 * 7.2, currency: '美元', percentage: 100, latest: 'C轮10亿美元', latest_en: '$1B Series C', segment: '人形整机 / 仿真+遥操作', date: '2025.09', isOverseas: true },
            { company: 'Physical Intelligence', valuation: '56亿美元', valuationCNY: 56 * 7.2, currency: '美元', percentage: 80, latest: 'B轮6亿美元', latest_en: '$600M Series B', segment: 'VLA模型 / 视频学习', date: '2025.11', isOverseas: true },
            { company: '1X Technologies', valuation: '100亿美元', valuationCNY: 100 * 7.2, currency: '美元', percentage: 85, latest: '洽谈10亿美元', latest_en: '$1B in progress', segment: '人形整机 / 遥操作', date: '2025.09', isOverseas: true },
            { company: 'Skild AI', valuation: '140亿美元', valuationCNY: 140 * 7.2, currency: '美元', percentage: 88, latest: 'C轮14亿美元', latest_en: '$1.4B Series C', segment: 'VLA模型 / 物理世界', date: '2026.01', isOverseas: true },
            { company: 'Apptronik', valuation: '53亿美元', valuationCNY: 53 * 7.2, currency: '美元', percentage: 75, latest: 'A轮9.35亿美元', latest_en: '$935M Series A', segment: '人形整机 / 物理世界', date: '2026.02', isOverseas: true },
            { company: 'Agility Robotics', valuation: '17.5亿美元', valuationCNY: 17.5 * 7.2, currency: '美元', percentage: 55, latest: 'C轮1.5亿美元', latest_en: '$150M Series C', segment: '人形整机 / 物理世界', date: '2025.09', isOverseas: true },
            { company: 'Sanctuary AI', valuation: '约10亿美元', valuationCNY: 10 * 7.2, currency: '美元', percentage: 45, latest: 'B轮融资', latest_en: 'Series B', segment: '人形整机 / 遥操作', date: '2024.12', isOverseas: true },
            { company: 'Sunday Robotics', valuation: '11.5亿美元', valuationCNY: 82.8, currency: '美元', percentage: 50, latest: '1.65亿美元B轮', latest_en: '$165M Series B', segment: '人形整机 / 仿真', date: '2026.03', isOverseas: true },
            { company: 'Field AI', valuation: '约5亿美元', valuationCNY: 5 * 7.2, currency: '美元', percentage: 35, latest: 'A轮', latest_en: 'Series A', segment: 'VLA模型 / 视频学习', date: '2024.10', isOverseas: true },
            { company: 'Mimic Robotics', valuation: '约2亿美元', valuationCNY: 2 * 7.2, currency: '美元', percentage: 25, latest: '天使轮', latest_en: 'Angel Round', segment: '具身大脑 / 遥操作', date: '2024.06', isOverseas: true },
            { company: 'Anybotics', valuation: '约5亿美元', valuationCNY: 5 * 7.2, currency: '美元', percentage: 35, latest: 'B轮', latest_en: 'Series B', segment: '四足/特种 / 物理世界', date: '2024.08', isOverseas: true },
            { company: 'Skydio', valuation: '约10亿美元', valuationCNY: 10 * 7.2, currency: '美元', percentage: 45, latest: '战略投资', latest_en: 'Strategic Investment', segment: '无人机 / AI', date: '2024.05', isOverseas: true },
            { company: 'Hexagon', valuation: '约200亿美元', valuationCNY: 200 * 7.2, currency: '美元', percentage: 95, latest: '上市', latest_en: 'Listed', segment: '传感器/视觉 / 物理世界', date: '2026.04', isOverseas: true },
            { company: 'Boston Dynamics', valuation: '约15亿美元', valuationCNY: 15 * 7.2, currency: '美元', percentage: 50, latest: '被现代收购', latest_en: 'Acquired by Hyundai', segment: '人形整机/四足 / 物理世界', date: '2024.01', isOverseas: true },
            { company: 'Tesla Optimus', valuation: 'Tesla上市主体市值', valuationCNY: 0, currency: '美元', percentage: 100, latest: 'Self-funded', latest_en: 'Tesla Self-funded', segment: '人形整机 / 混合', date: '2026.04', isOverseas: true },
            { company: '英伟达 (NVIDIA)', valuation: '上市~2万亿美元', valuationCNY: 20000 * 7.2, currency: '美元', percentage: 100, latest: '上市', latest_en: 'Listed', segment: '芯片/平台 / 物理世界', date: '2026.04', isOverseas: true },
            { company: '宇树科技', valuation: '420亿人民币', valuationCNY: 420, currency: '人民币', percentage: 92, latest: 'IPO募资42亿', latest_en: 'IPO ¥4.2B Raised', segment: '人形整机 / 物理世界', date: '2026.03', isOverseas: false },
            { company: '灵心巧手', valuation: '240亿人民币', valuationCNY: 240, currency: '人民币', percentage: 85, latest: 'B轮15亿', latest_en: 'Series B ¥15B', segment: '灵巧手 / 物理世界', date: '2026.03', isOverseas: false },
            { company: '银河通用', valuation: '210亿人民币', valuationCNY: 210, currency: '人民币', percentage: 82, latest: 'B+轮25亿', latest_en: 'Series B+ ¥25B', segment: '人形整机 / 仿真+遥操作', date: '2026.03', isOverseas: false },
            { company: '它石智航', valuation: '216亿人民币', valuationCNY: 216, currency: '人民币', percentage: 83, latest: '4.55亿美元Pre-A', latest_en: '$455M Pre-A', segment: '人形整机 / 混合', date: '2026.04', isOverseas: false },
            { company: '星海图', valuation: '200亿人民币', valuationCNY: 200, currency: '人民币', percentage: 80, latest: 'B+轮20亿', latest_en: 'Series B+ ¥20B', segment: 'VLA模型 / 视频学习', date: '2026.04', isOverseas: false },
            { company: '星动纪元', valuation: '130亿+人民币', valuationCNY: 135, currency: '人民币', percentage: 78, latest: '2亿美元+10亿战略', latest_en: '$200M+¥1B Strategic', segment: '人形整机 / 遥操作', date: '2026.04', isOverseas: false },
            { company: '智元机器人', valuation: '150亿人民币', valuationCNY: 150, currency: '人民币', percentage: 75, latest: 'B轮融资', latest_en: 'Series B', segment: '人形整机 / 遥操作', date: '2025.03', isOverseas: false },
            { company: '傅利叶智能', valuation: '80亿人民币', valuationCNY: 80, currency: '人民币', percentage: 65, latest: 'E轮近8亿', latest_en: '~¥800M Series E', segment: '人形整机 / 物理世界', date: '2025.01', isOverseas: false },
            { company: '至简动力', valuation: '72亿+人民币', valuationCNY: 75, currency: '人民币', percentage: 62, latest: '半年20亿5轮', latest_en: '¥2B 5 Rounds', segment: '人形整机 / 混合', date: '2026.03', isOverseas: false },
            { company: '光轮智能', valuation: '70亿+人民币', valuationCNY: 75, currency: '人民币', percentage: 60, latest: '10亿A+++轮', latest_en: '¥1B Series A+++', segment: '数据平台 / 仿真', date: '2026.03', isOverseas: false },
            { company: '逐际动力', valuation: '100亿+人民币', valuationCNY: 105, currency: '人民币', percentage: 70, latest: '2亿美元B轮', latest_en: '$200M Series B', segment: '人形整机 / 混合', date: '2026.02', isOverseas: false },
            { company: '智平方', valuation: '100亿+人民币', valuationCNY: 100, currency: '人民币', percentage: 70, latest: 'B轮超10亿', latest_en: 'Series B ¥10B+', segment: '人形整机 / 混合', date: '2026.02', isOverseas: false },
            { company: '千寻智能', valuation: '100亿+人民币', valuationCNY: 100, currency: '人民币', percentage: 70, latest: '约30亿融资', latest_en: '¥30B Raised', segment: 'VLA模型 / 视频学习', date: '2026.04', isOverseas: false },
            { company: '自变量机器人', valuation: '100亿+人民币', valuationCNY: 100, currency: '人民币', percentage: 70, latest: 'B轮近20亿', latest_en: 'Series B ~¥20B', segment: '人形整机 / 遥操作', date: '2026.04', isOverseas: false },
            { company: '帕西尼感知', valuation: '100亿+人民币', valuationCNY: 100, currency: '人民币', percentage: 70, latest: 'B轮超10亿', latest_en: 'Series B ¥10B+', segment: '传感器/灵巧手 / 物理世界', date: '2026.03', isOverseas: false },
            { company: '普渡机器人', valuation: '100亿+人民币', valuationCNY: 100, currency: '人民币', percentage: 70, latest: '近10亿新融资', latest_en: '~¥1B New', segment: '服务机器人 / 物理世界', date: '2026.04', isOverseas: false },
            { company: '魔法原子', valuation: '100亿+人民币', valuationCNY: 100, currency: '人民币', percentage: 70, latest: 'A轮5亿+天使1.5亿', latest_en: 'Series A ¥500M', segment: '人形整机 / 遥操作', date: '2026.04', isOverseas: false },
            { company: '乐聚机器人', valuation: '90亿人民币', valuationCNY: 90, currency: '人民币', percentage: 68, latest: 'Pre-IPO轮15亿', latest_en: 'Pre-IPO ¥1.5B', segment: '人形整机 / 物理世界', date: '2025.10', isOverseas: false },
            { company: '加速进化', valuation: '70亿+人民币', valuationCNY: 72, currency: '人民币', percentage: 62, latest: 'C轮近10亿', latest_en: 'Series C ~¥1B', segment: '人形整机 / 遥操作', date: '2026.04', isOverseas: false },
            { company: '梅卡曼德', valuation: '30亿+人民币', valuationCNY: 30, currency: '人民币', percentage: 48, latest: 'D轮近5亿', latest_en: 'Series D ~¥500M', segment: '传感器/视觉 / 物理世界', date: '2025.08', isOverseas: false },
            { company: '灵初智能', valuation: '20亿+人民币', valuationCNY: 22, currency: '人民币', percentage: 42, latest: '天使+Pre-A共20亿', latest_en: '¥2B Angel+Pre-A', segment: '人形整机 / 混合', date: '2026.03', isOverseas: false },
            { company: '思灵机器人', valuation: '70亿+人民币', valuationCNY: 72, currency: '人民币', percentage: 62, latest: '累计超20亿', latest_en: '>$2B Total', segment: '机械臂/协作 / 物理世界', date: '2025.08', isOverseas: false },
            { company: '穹彻智能', valuation: '15亿+人民币', valuationCNY: 18, currency: '人民币', percentage: 38, latest: 'A轮数亿', latest_en: '¥100M+ Series A', segment: '具身大脑 / 混合', date: '2026.02', isOverseas: false },
            { company: '破壳机器人', valuation: '约4亿美元', valuationCNY: 28.8, currency: '美元', percentage: 40, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 遥操作', date: '2026.03', isOverseas: false },
            { company: '大晓机器人', valuation: '约10亿人民币', valuationCNY: 10, currency: '人民币', percentage: 32, latest: 'A轮融资', latest_en: 'Series A', segment: '人形整机 / 混合', date: '2025.06', isOverseas: false },
            { company: '七腾机器人', valuation: '约10亿人民币', valuationCNY: 10, currency: '人民币', percentage: 32, latest: 'B轮融资', latest_en: 'Series B', segment: '特种机器人 / 物理世界', date: '2025.08', isOverseas: false },
            { company: '觅蜂科技', valuation: '约10亿人民币', valuationCNY: 12, currency: '人民币', percentage: 35, latest: '种子+天使轮', latest_en: 'Seed+Angel', segment: '数据平台 / 仿真', date: '2026.02', isOverseas: false },
            { company: '跨维智能', valuation: '约8亿人民币', valuationCNY: 8, currency: '人民币', percentage: 28, latest: '天使轮', latest_en: 'Angel Round', segment: '传感器/视觉 / 物理世界', date: '2025.03', isOverseas: false },
            { company: '珞石机器人', valuation: '约20亿人民币', valuationCNY: 20, currency: '人民币', percentage: 42, latest: '战略投资', latest_en: 'Strategic', segment: '机械臂/协作 / 物理世界', date: '2025.09', isOverseas: false },
            { company: '镜识科技', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.05', isOverseas: false },
            { company: '优理奇智能', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 遥操作', date: '2025.04', isOverseas: false },
            { company: '优必选', valuation: '上市~550亿港元', valuationCNY: 500, currency: '人民币', percentage: 85, latest: '港股上市', latest_en: 'Listed HK', segment: '人形整机 / 物理世界', date: '2026.04', isOverseas: false },
            { company: '卧安机器人', valuation: '上市~255亿港元', valuationCNY: 230, currency: '港币', percentage: 75, latest: '港股上市', latest_en: 'Listed HK', segment: '服务机器人 / 物理世界', date: '2026.04', isOverseas: false },
            { company: '小鹏鹏行', valuation: '约50亿人民币', valuationCNY: 50, currency: '人民币', percentage: 58, latest: 'A轮融资', latest_en: 'Series A', segment: '人形整机 / 混合', date: '2025.06', isOverseas: false },
            { company: '云深处', valuation: '约10亿人民币', valuationCNY: 10, currency: '人民币', percentage: 32, latest: 'B轮', latest_en: 'Series B', segment: '四足/特种 / 物理世界', date: '2025.09', isOverseas: false },
            { company: '松延动力', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: 'A轮', latest_en: 'Series A', segment: '人形整机 / 混合', date: '2025.06', isOverseas: false },
            { company: '卓益得机器人', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.03', isOverseas: false },
            { company: '开普勒人形机器人', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.05', isOverseas: false },
            { company: '理工华汇', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: 'A轮', latest_en: 'Series A', segment: '人形整机 / 混合', date: '2025.08', isOverseas: false },
            { company: '天链机器人', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.04', isOverseas: false },
            { company: '青瞳视觉', valuation: '约2亿人民币', valuationCNY: 2, currency: '人民币', percentage: 15, latest: 'A轮', latest_en: 'Series A', segment: '传感器/视觉 / 物理世界', date: '2025.05', isOverseas: false },
            { company: '墨奇科技', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: 'B轮', latest_en: 'Series B', segment: '传感器/视觉 / 物理世界', date: '2025.07', isOverseas: false },
            { company: '国地具身智能', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.06', isOverseas: false },
            { company: '北京人形机器人创新中心', valuation: '非上市', valuationCNY: 0, currency: '人民币', percentage: 30, latest: '国研机构', latest_en: 'National Research Center', segment: '人形整机 / 混合', date: '2026.04', isOverseas: false },
            { company: '国家地方共建具身智能机器人创新中心', valuation: '非上市', valuationCNY: 0, currency: '人民币', percentage: 30, latest: '国研机构', latest_en: 'National Research Center', segment: '人形整机 / 混合', date: '2026.04', isOverseas: false },
            { company: '星尘智能', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.05', isOverseas: false },
            { company: '钛虎机器人', valuation: '约2亿人民币', valuationCNY: 2, currency: '人民币', percentage: 15, latest: 'Pre-A轮', latest_en: 'Pre-A Round', segment: '人形整机 / 混合', date: '2025.08', isOverseas: false },
            { company: '爱动超越', valuation: '约2亿人民币', valuationCNY: 2, currency: '人民币', percentage: 15, latest: 'A轮', latest_en: 'Series A', segment: '人形整机 / 混合', date: '2025.07', isOverseas: false },
            { company: '神源久机器人', valuation: '约1亿人民币', valuationCNY: 1, currency: '人民币', percentage: 10, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.06', isOverseas: false },
            { company: '千秒机器人', valuation: '约1亿人民币', valuationCNY: 1, currency: '人民币', percentage: 10, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.08', isOverseas: false },
            { company: '坤维科技', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: 'A轮', latest_en: 'Series A', segment: '传感器 / 物理世界', date: '2025.09', isOverseas: false },
            { company: '因时机器人', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: 'B轮', latest_en: 'Series B', segment: '灵巧手 / 物理世界', date: '2025.07', isOverseas: false },
            { company: '思特威', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 25, latest: '战略投资', latest_en: 'Strategic', segment: '传感器 / 物理世界', date: '2025.06', isOverseas: false },
            { company: '灵宇宙', valuation: '约2亿人民币', valuationCNY: 2, currency: '人民币', percentage: 15, latest: '天使轮', latest_en: 'Angel Round', segment: '具身大脑 / 混合', date: '2025.07', isOverseas: false },
            { company: '智平方机器人', valuation: '约10亿人民币', valuationCNY: 10, currency: '人民币', percentage: 32, latest: 'A轮', latest_en: 'Series A', segment: '人形整机 / 混合', date: '2025.08', isOverseas: false },
            { company: '简智机器人', valuation: '约10亿人民币', valuationCNY: 10, currency: '人民币', percentage: 32, latest: '累计近10亿', latest_en: '~¥1B Raised', segment: '数据平台 / 仿真', date: '2026.03', isOverseas: false },
            { company: '灵御智能', valuation: '约2亿人民币', valuationCNY: 2, currency: '人民币', percentage: 15, latest: '天使轮', latest_en: 'Angel Round', segment: '具身大脑 / 遥操作', date: '2025.06', isOverseas: false },
            { company: '智在无界', valuation: '约5亿人民币', valuationCNY: 5, currency: '人民币', percentage: 22, latest: '数千万元天使轮', latest_en: '¥10M+ Angel', segment: 'VLA模型 / 视频学习', date: '2025.06', isOverseas: false },
            { company: '地瓜机器人', valuation: '约20亿人民币', valuationCNY: 20, currency: '人民币', percentage: 42, latest: 'A轮', latest_en: 'Series A', segment: '芯片/算力 / 物理世界', date: '2025.10', isOverseas: false },
            { company: '星源智机器人', valuation: '约3亿人民币', valuationCNY: 3, currency: '人民币', percentage: 20, latest: '天使轮', latest_en: 'Angel Round', segment: '人形整机 / 混合', date: '2025.05', isOverseas: false },
            { company: '苏度科技', valuation: '约140亿人民币', valuationCNY: 140, currency: '人民币', percentage: 75, latest: '5亿美元Pre-A轮', latest_en: '$500M Pre-A', segment: 'VLA模型 / 仿真', date: '2026.04', isOverseas: false },
            { company: '超维动力', valuation: '新发布，估值待定', valuationCNY: 1, currency: '人民币', percentage: 15, latest: '新品发布', latest_en: 'Product Launch', segment: '人形整机 / 混合', date: '2026.04', isOverseas: false },
            { company: '自然意志', valuation: '约40亿人民币', valuationCNY: 40, currency: '人民币', percentage: 55, latest: '天使轮', latest_en: 'Angel Round', segment: '具身大脑 / 物理世界', date: '2026.01', isOverseas: false }
        ];'''

# Find and replace the rankingData
# Pattern: from "// rankingData - 所有公司基础数据" to the closing "];\n\n        // 公司名英文映射"
pattern = r'// rankingData - 所有公司基础数据.*?\n        \];(\n\n        // 公司名英文映射)'

replacement = new_rankingData + r'\1'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open(r'c:\Users\ZhuanZ\WorkBuddy\20260422102414\company.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done! rankingData updated with complete information.")
