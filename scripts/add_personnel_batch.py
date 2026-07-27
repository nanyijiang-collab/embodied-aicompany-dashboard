# -*- coding: utf-8 -*-
import json

with open('data/personnel.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

existing_keys = set()
for entry in data:
    key = (entry.get('company', ''), entry.get('person_name', ''), entry.get('action', ''))
    existing_keys.add(key)

new_entries = [
    {
        "company": "腾讯",
        "person_name": "胡瀚",
        "action": "离职",
        "old_role": "腾讯混元多模态大模型负责人",
        "new_role": "独立创业（主攻具身大脑与世界模型赛道）",
        "title": "腾讯混元多模态负责人胡瀚离职创业，押注具身世界模型",
        "title_en": "Tencent Hunyuan Multimodal Lead Hu Han Resigns to Found Embodied World Model Startup",
        "summary": "胡瀚本科博士均就读清华大学，师从周杰教授，曾任职百度深度学习研究所、微软亚洲研究院视觉计算组（升任首席研究员）。2025年1月加入腾讯接替刘威负责混元多模态研发。2026年7月正式提出离职，将独立创业主攻具身大脑与世界模型赛道。原OpenAI研究员田永龙将接手其视觉语言模型研发工作。",
        "source": "OFweek维科网/新智元",
        "source_url": "https://znyj.m.ofweek.com/news/2026-07/ART-23013-8460-30695790.html",
        "date": "2026-07-24"
    },
    {
        "company": "小鹏汽车",
        "person_name": "米良川",
        "action": "离职",
        "old_role": "小鹏机器人业务负责人 / 副总裁 / AI技术委员会主席",
        "new_role": "离职（去向未明）",
        "title": "小鹏机器人负责人米良川离职，铁三角核心班底全员离场",
        "title_en": "Xpeng Robotics Head Mi Liangchuan Departs, Iron Triangle Core Team Fully Dissolved",
        "summary": "米良川本科毕业于中科大电气工程，美国爱荷华州立大学机器人硕士，曾在英伟达工作约15年，卡内基梅隆大学机器人研究所担任电气工程师。2021年加入小鹏任自动驾驶高级总监，2023年9月接管机器人事业部，后晋升副总裁并出任AI技术委员会主席。2026年7月确认离职，是小鹏机器人铁三角（米良川、施晓鑫、郑存远）最后一位离开的成员。何小鹏已亲自兼任机器人业务CEO。",
        "source": "职场Bonus/21世纪经济报道/新浪财经",
        "source_url": "https://finance.sina.com.cn/wm/2026-07-01/doc-ifiaeu6251272.shtml",
        "date": "2026-07-01"
    },
    {
        "company": "小鹏汽车",
        "person_name": "陆思渊",
        "action": "离职",
        "old_role": "小鹏AI基础架构部负责人",
        "new_role": "即将加入OpenAI参与具身机器人研发",
        "title": "小鹏AI架构负责人陆思渊离职，将加入OpenAI做人形机器人",
        "title_en": "Xpeng AI Infra Lead Lu Siyuan Departs for OpenAI Robotics",
        "summary": "陆思渊拥有南加州大学博士学位，深耕深度学习与算力优化领域，在小鹏主导搭建AI Infra体系，直管约200人团队，覆盖训练集群、芯片编译器、车端推理全链路技术。2026年7月正在办理工作交接，离职后将入职OpenAI参与具身机器人研发。这是近两月小鹏第三位出走的核心技术高管（此前施晓鑫、米良川已离职）。",
        "source": "OFweek机器人网/雷峰网",
        "source_url": "https://mp.ofweek.com/robot/a256714105627",
        "date": "2026-07-20"
    },
    {
        "company": "OpenAI",
        "person_name": "陆思渊",
        "action": "加入",
        "old_role": "小鹏汽车AI基础架构部负责人",
        "new_role": "OpenAI机器人事业部研究员",
        "title": "前小鹏AI架构负责人陆思渊加入OpenAI机器人部门",
        "title_en": "Former Xpeng AI Infra Lead Lu Siyuan Joins OpenAI Robotics Division",
        "summary": "OpenAI于2026年6月正式成立内部机器人事业部，由Sora、DALL-E研发负责人Aditya Ramesh统筹，卡内基梅隆大学博士何泰然作为核心研究员加入。陆思渊从小鹏离职后加入OpenAI机器人事业部，将利用其大规模算力调度和模型优化经验补齐机器人仿真训练底层算力短板。",
        "source": "OFweek机器人网/雷峰网",
        "source_url": "https://mp.ofweek.com/robot/a256714105627",
        "date": "2026-07-20"
    },
    {
        "company": "星动纪元",
        "person_name": "席悦",
        "action": "卸任",
        "old_role": "星动纪元联合创始人兼董事长 / 财务负责人",
        "new_role": "卸任董事长及财务负责人职务",
        "title": "星动纪元联合创始人席悦卸任董事长，石选阳接任",
        "title_en": "Robot Era Co-founder Xi Yue Steps Down as Chairman, Shi Xuanyang Succeeds",
        "summary": "星动纪元发生高层人事变动，联合创始人席悦卸任董事长及财务负责人职务。同时原董事沈源、王梦秋、郭其志、袁冰冰悉数退出；新增王志伟、张勃任董事。席悦通过合伙企业间接持股18.31%，为公司重要股东。星动纪元2026年以来完成多轮融资（3月10亿战略轮、4月超2亿美元、7月10亿新一轮），注册资本持续上调，公司类型已变更为股份有限公司。",
        "source": "泰山财经/中国能源网",
        "source_url": "https://www.cnenergynews.cn/article/4SHRIefhcuu",
        "date": "2026-07-06"
    },
    {
        "company": "星动纪元",
        "person_name": "石选阳",
        "action": "晋升",
        "old_role": "星动纪元运控算法负责人 / 董事",
        "new_role": "星动纪元董事长",
        "title": "星动纪元运控算法负责人石选阳升任董事长",
        "title_en": "Robot Era Motion Control Lead Shi Xuanyang Promoted to Chairman",
        "summary": "石选阳由董事调整为董事长，此前以公司运控算法负责人身份登上央视新闻。星动纪元是清华大学唯一持股的具身智能企业，2026年Q2开启千台级机器人交付，与中国邮政、顺丰等深度合作，已打通物流领域具身智能商业化闭环。",
        "source": "泰山财经/中国能源网",
        "source_url": "https://www.cnenergynews.cn/article/4SHRIefhcuu",
        "date": "2026-07-06"
    },
    {
        "company": "破壳机器人",
        "person_name": "刘硕",
        "action": "加入",
        "old_role": "美团无人机商业管理负责人 / 美团机器人研究院秘书长",
        "new_role": "破壳机器人首位商业合伙人（负责商业化、战略及业务拓展）",
        "title": "前美团无人机高管刘硕加入破壳机器人，出任首位商业合伙人",
        "title_en": "Former Meituan Drone Executive Liu Shuo Joins Poke Robotics as First Business Partner",
        "summary": "刘硕本科毕业于上海理工大学科技翻译专业，香港大学MBA。曾任职百度智能驾驶事业群生态合作总经理，后任翼健信息合伙人/副总裁，后入美团任无人机商业管理负责人及机器人研究院秘书长。2026年7月加入破壳机器人任首位商业合伙人。破壳机器人由许华哲（前星海图联创/首席科学家）创立，聚焦C端家庭场景轮式底盘+双臂形态具身机器人，4月完成数千万美元天使轮。",
        "source": "机器人前瞻/新浪网",
        "source_url": "https://k.sina.com.cn/article_7950358917_1d9e0d98502001eve6.html",
        "date": "2026-07-01"
    },
    {
        "company": "小鹏汽车",
        "person_name": "何小鹏",
        "action": "晋升",
        "old_role": "小鹏集团董事长兼CEO",
        "new_role": "小鹏集团董事长兼CEO + 机器人业务CEO + 机器人中心总负责人",
        "title": "何小鹏亲自兼任小鹏机器人业务CEO，全面接管机器人中心",
        "title_en": "He Xiaopeng Personally Takes Over as CEO of Xpeng Robotics Business",
        "summary": "2026年6月10日，何小鹏发布全员内部信，宣布亲自兼任机器人业务CEO及机器人中心总负责人，所有部门负责人直接向其汇报，取消中间总负责人层级。此举发生在施晓鑫离职后5天，旨在从集团最高层推动资金、产线、渠道、智驾技术全面向机器人倾斜，全力推动IRON人形机器人2026年底量产落地。",
        "source": "21世纪经济报道/今日头条",
        "source_url": "https://www.toutiao.com/article/7657391193710346752/",
        "date": "2026-06-10"
    },
    {
        "company": "小鹏汽车",
        "person_name": "郑存远",
        "action": "离职",
        "old_role": "小鹏机器人整机本体负责人（IRON从0到1搭建者之一）",
        "new_role": "离职创业（后以花名郑天乐加入超维动力）",
        "title": "小鹏机器人整机本体负责人郑存远离职创业，铁三角首名离场成员",
        "title_en": "Xpeng Robotics Hardware Lead Zheng Cunyuan Departs to Found Startup",
        "summary": "郑存远硕士毕业于哥伦比亚大学机械工程专业，曾在SpaceX实习、GE Research任研究员，加入小鹏前任拓斯达科技工业机器人研发负责人。在鹏行智能/小鹏机器人期间负责IRON整机技术架构，完成了最新一代IRON的总包集成。2025年5月底首个离开小鹏机器人铁三角。离职后朋友圈背景墙纸仍为IRON，2026年5月以花名郑天乐出现在超维动力发布会上。",
        "source": "职场Bonus/搜狐",
        "source_url": "https://m.sohu.com/a/1045502544_122014422",
        "date": "2025-05-31"
    },
    {
        "company": "超维动力",
        "person_name": "郑存远",
        "action": "创业加入",
        "old_role": "小鹏机器人整机本体负责人（花名Tyler）",
        "new_role": "超维动力联合创始人（花名郑天乐）",
        "title": "前小鹏机器人硬件负责人郑存远以花名郑天乐加入超维动力",
        "title_en": "Former Xpeng Robotics Hardware Lead Joins Chaowei Dynamics as Co-Founder",
        "summary": "郑存远从小鹏离职后，以花名郑天乐出现在超维动力的发布会和通稿中，经交叉验证确认其身份。通过深圳超维智联合伙持股79.17%，间接控制超维动力。",
        "source": "职场Bonus/搜狐",
        "source_url": "https://m.sohu.com/a/1045502544_122014422",
        "date": "2026-05-01"
    },
    {
        "company": "墨奇智能",
        "person_name": "黄青虬",
        "action": "创业",
        "old_role": "华为天才少年",
        "new_role": "墨奇智能联合创始人",
        "title": "前华为天才少年黄青虬创办墨奇智能，天使轮超10亿估值70亿",
        "title_en": "Former Huawei Genius Youth Huang Qingqu Found Moqi AI, Angel Round Exceeds 1B RMB",
        "summary": "黄青虬为前华为天才少年，与前华为资深高管高文礼联合创办墨奇智能。2026年7月宣布完成超10亿元天使轮系列融资，投后估值超70亿元。华为系已成为具身智能创业赛道重要力量，截至7月6日至少15位华为前高管离职加入或创办具身智能创企，9位曾入选华为天才少年，公开融资合计约77亿元。",
        "source": "智东西/36氪",
        "source_url": "https://www.toutiao.com/article/7659954781468787250",
        "date": "2026-07-06"
    },
    {
        "company": "墨奇智能",
        "person_name": "高文礼",
        "action": "创业",
        "old_role": "华为资深高管",
        "new_role": "墨奇智能联合创始人",
        "title": "前华为资深高管高文礼联合创办墨奇智能",
        "title_en": "Former Huawei Senior Executive Gao Wenli Co-founds Moqi AI",
        "summary": "高文礼为前华为资深高管，与前华为天才少年黄青虬联合创办墨奇智能。公司完成超10亿元天使轮系列融资，投后估值超70亿元。业务覆盖机器人本体、运动小脑、决策大脑等具身智能全产业链。",
        "source": "智东西/36氪",
        "source_url": "https://www.toutiao.com/article/7659954781468787250",
        "date": "2026-07-06"
    }
]

added = 0
skipped = 0
for entry in new_entries:
    key = (entry["company"], entry["person_name"], entry["action"])
    if key in existing_keys:
        print(f"SKIP (duplicate): {entry['company']} | {entry['person_name']} | {entry['action']}")
        skipped += 1
    else:
        data.append(entry)
        existing_keys.add(key)
        print(f"ADD: {entry['company']} | {entry['person_name']} | {entry['action']} | {entry['date']}")
        added += 1

with open('data/personnel.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal: {len(data)} entries ({added} added, {skipped} skipped)")
