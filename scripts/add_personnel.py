#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加人事动态事件到 events.json
"""

import json
import os
import re
from datetime import datetime
from difflib import SequenceMatcher

def load_events():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def generate_id(company, date, idx=0):
    """生成唯一ID"""
    prefix = company[:2]
    date_part = date.replace('-', '')[:6]
    return f"{prefix}{date_part}{idx:02d}"

def normalize_text(text):
    """标准化文本"""
    if not text:
        return ''
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower().strip()

def similarity(a, b):
    """计算相似度"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def deduplicate_events(events):
    """三层去重"""
    seen = {}  # key: (company, date, title) -> event
    unique = []
    removed = 0
    
    for e in events:
        company = e.get('company', '')
        date = e.get('date', '')[:10]
        title = normalize_text(e.get('title', ''))
        event_id = e.get('id', '')
        
        key = (company, date, title)
        
        if key in seen:
            removed += 1
            continue
        
        # 相似度检查
        is_dup = False
        for existing_key in list(seen.keys()):
            ec, ed, et = existing_key
            if ec == company and ed == date and similarity(title, et) >= 0.8:
                is_dup = True
                removed += 1
                break
        
        if not is_dup:
            seen[key] = e
            unique.append(e)
    
    if removed > 0:
        print(f"  [Dedup] Removed {removed} duplicates")
    return unique

# 人事动态数据（搜索到的真实新闻）
personnel_events = [
    {
        "company": "众擎机器人",
        "person_name": "李力耘",
        "action": "加入",
        "old_role": "小鹏汽车副总裁",
        "new_role": "CTO",
        "title": "前小鹏汽车副总裁李力耘加入众擎机器人，出任CTO",
        "title_en": "Former XPeng VP Li Liyun Joins Zhongqing Robotics as CTO",
        "summary": "李力耘本科毕业于清华大学电子工程系，博士毕业于纽约大学计算机系。曾任小鹏汽车副总裁，主导自动驾驶团队\"产品+技术\"的AI化转型。在小鹏工作6年零4个月后，于2025年10月离职，2026年4月21日正式加入众擎机器人。",
        "source": "机器人大讲堂",
        "source_url": "https://news.qq.com/rain/a/20260422A05N6N00",
        "date": "2026-04-21"
    },
    {
        "company": "众擎机器人",
        "person_name": "李力耘",
        "action": "离职",
        "old_role": "小鹏汽车副总裁",
        "new_role": "-",
        "title": "小鹏汽车副总裁李力耘离职，曾主导智驾技术转型",
        "title_en": "XPeng VP Li Liyun Departs After 6 Years",
        "summary": "李力耘在小鹏汽车工作6年零4个月，历任高级总监、自动驾驶中心负责人、副总裁，被定义为智驾技术一号位。2025年10月在朋友圈官宣离职。",
        "source": "腾讯新闻",
        "source_url": "https://news.qq.com/rain/a/20260422A05N6N00",
        "date": "2025-10-01"
    },
    {
        "company": "魔法原子",
        "person_name": "吴长征",
        "action": "离职",
        "old_role": "创始人/CEO",
        "new_role": "-",
        "title": "魔法原子创始人吴长征离职，CTO陈春玉接棒",
        "title_en": "MagicLab Founder Wu Changzheng Steps Down, CTO Chen Chunyu Takes Over",
        "summary": "2026年3月6日，魔法原子正式发布公告，创始人吴长征离职，公司核心管理团队进行调整。CTO陈春玉接棒继续带领公司发展。吴长征已于2026年1-2月陆续卸任旗下多家主体的法定代表人、董事等职务。",
        "source": "界面新闻",
        "source_url": "https://www.jiemian.com/article/14082526.html",
        "date": "2026-03-06"
    },
    {
        "company": "魔法原子",
        "person_name": "陈春玉",
        "action": "晋升",
        "old_role": "CTO",
        "new_role": "代理CEO/CTO",
        "title": "魔法原子CTO陈春玉接棒，负责公司全面运营",
        "title_en": "MagicLab CTO Chen Chunyu Takes Leadership After Founder's Exit",
        "summary": "陈春玉是魔法原子联合创始人，十余年机器人行业经验，曾任职优必选，主导过人形与四足机器人量产交付。在创始人吴长征离职后，继续担任CTO并负责公司全面运营。",
        "source": "界面新闻",
        "source_url": "https://www.jiemian.com/article/14082526.html",
        "date": "2026-03-06"
    },
    {
        "company": "魔法原子",
        "person_name": "张涛",
        "action": "加入",
        "old_role": "-",
        "new_role": "具身模型负责人/算法VP",
        "title": "前阿里、蔚来算法专家张涛加入魔法原子，担任具身模型负责人",
        "title_en": "MagicLab Hires Ex-Alibaba & NIO Algorithm Expert Zhang Tao",
        "summary": "张涛加入魔法原子担任具身模型负责人、算法VP，具备阿里、蔚来算法背景，将负责具身智能大模型研发及技术体系建设。",
        "source": "界面新闻",
        "source_url": "https://www.jiemian.com/article/14082526.html",
        "date": "2026-03-06"
    },
    {
        "company": "魔法原子",
        "person_name": "李翔",
        "action": "加入",
        "old_role": "-",
        "new_role": "首席科学家",
        "title": "清华大学博导李翔加入魔法原子，担任首席科学家",
        "title_en": "Tsinghua Professor Li Xiang Joins MagicLab as Chief Scientist",
        "summary": "清华大学博导李翔加入魔法原子担任首席科学家，将主导灵巧手技术突破。李翔在机器人领域有深厚学术积累。",
        "source": "界面新闻",
        "source_url": "https://www.jiemian.com/article/14082526.html",
        "date": "2026-03-06"
    },
    {
        "company": "Figure AI",
        "person_name": "-",
        "action": "重组",
        "old_role": "-",
        "new_role": "-",
        "title": "Figure AI完成史上最大规模重组，三个团队并入Helix小组",
        "title_en": "Figure AI Completes Largest Reorganization, Three Teams Merge into Helix Group",
        "summary": "Figure创始人兼CEO Brett Adcock在推特宣布，公司已完成史上最大规模重组，将三个独立团队合并进AI小组Helix，以加速AI模型的研发和商业化落地。",
        "source": "Sohu",
        "source_url": "https://www.sohu.com/a/900130477_114877",
        "date": "2025-05-30"
    },
    {
        "company": "智元机器人",
        "person_name": "彭志辉",
        "action": "晋升",
        "old_role": "首席技术官",
        "new_role": "总裁兼CTO",
        "title": "智元机器人联合创始人彭志辉晋升为总裁兼CTO",
        "title_en": "AgiBot Co-founder Peng Zhihui Promoted to President & CTO",
        "summary": "2025年11月，智元机器人联合创始人彭志辉（网名\"稚晖君\"）被任命为总裁兼CTO。彭志辉出生于1993年，曾以\"华为天才少年\"身份进入公众视野，于2023年2月参与创立智元机器人。",
        "source": "WWO",
        "source_url": "https://m.wwo.com.cn/youxi/202511/193760.html",
        "date": "2025-11-01"
    },
    {
        "company": "原力无限",
        "person_name": "待查",
        "action": "加入",
        "old_role": "-",
        "new_role": "-",
        "title": "前英伟达自动驾驶创始人加入原力无限科技",
        "title_en": "Ex-NVIDIA Autonomous Driving Founder Joins Yuanli Unlimited",
        "summary": "2026年2月，原力无限科技控股（浙江）有限公司发生人事变动，前英伟达自动驾驶创始人加入。",
        "source": "企查查",
        "source_url": "https://www.qcc.com/creport/deff662a8964e6310448343ade6a8391.html",
        "date": "2026-02-25"
    },
    # ===== 2026-04-27 新增 =====
    {
        "company": "Boston Dynamics",
        "person_name": "Aaron Saunders",
        "action": "离职",
        "old_role": "CTO",
        "new_role": "-",
        "title": "Boston Dynamics CTO Aaron Saunders离职，任职23年",
        "title_en": "Boston Dynamics CTO Aaron Saunders Departs After 23 Years",
        "summary": "Boston Dynamics CTO Aaron Saunders正式离职。他曾主导开发早期机器狗BigDog，带领团队打造Spot、Stretch和Atlas等人形机器人，推动了AI与物理世界的结合。在公司任职23年。",
        "source": "机电工程师网",
        "source_url": "https://www.jdgcs.org/news/agility-robotics-boston-dynamics-see-leadership-changes-17729/",
        "date": "2025-08-05"
    },
    {
        "company": "Boston Dynamics",
        "person_name": "Milan Kovac",
        "action": "加入",
        "old_role": "特斯拉高级副总裁/Optimus项目负责人",
        "new_role": "-",
        "title": "特斯拉前高级副总裁、Optimus项目负责人Milan Kovac加入Boston Dynamics",
        "title_en": "Former Tesla VP & Optimus Lead Milan Kovac Joins Boston Dynamics",
        "summary": "特斯拉前高级副总裁、人形机器人Optimus项目负责人Milan Kovac加入Boston Dynamics，进一步增强了公司的人形机器人研发实力。",
        "source": "机电工程师网",
        "source_url": "https://www.jdgcs.org/news/agility-robotics-boston-dynamics-see-leadership-changes-17729/",
        "date": "2025-08-05"
    },
    {
        "company": "Boston Dynamics",
        "person_name": "Robert Playter",
        "action": "卸任",
        "old_role": "CEO",
        "new_role": "-",
        "title": "Boston Dynamics CEO Robert Playter卸任",
        "title_en": "Boston Dynamics CEO Robert Playter Steps Down",
        "summary": "Boston Dynamics元老级人物Robert Playter卸任CEO，标志着公司进入新的发展阶段。",
        "source": "机电工程师网",
        "source_url": "https://www.jdgcs.org/news/agility-robotics-boston-dynamics-see-leadership-changes-17729/",
        "date": "2025-08-05"
    },
    {
        "company": "Agility Robotics",
        "person_name": "Melonee Wise",
        "action": "离职",
        "old_role": "CPO（首席产品官）",
        "new_role": "-",
        "title": "Agility Robotics CPO Melonee Wise离职，曾任Fetch Robotics CEO",
        "title_en": "Agility Robotics CPO Melonee Wise Departs",
        "summary": "Melonee Wise于2023年加入Agility Robotics，担任CPO。她曾任Zebra Technologies自动化副总裁及Fetch Robotics CEO，在机器人软硬件开发方面经验丰富，曾参与创建开源机器人系统ROS。她在扩展Digit机器人和Agility Arc平台方面发挥了关键作用。",
        "source": "机电工程师网",
        "source_url": "https://www.jdgcs.org/news/agility-robotics-boston-dynamics-see-leadership-changes-17729/",
        "date": "2025-08-05"
    },
    {
        "company": "智元机器人",
        "person_name": "彭志辉",
        "action": "创业",
        "old_role": "华为天才少年",
        "new_role": "智元机器人创始人兼总裁/CTO",
        "title": "华为天才少年彭志辉创立智元机器人",
        "title_en": "Huawei Genius Youth Peng Zhihui Founds AgiBot",
        "summary": "彭志辉（网名'稚晖君'）顶着'华为天才少年'标签从华为出走创业，2023年2月创立智元机器人，现任总裁兼CTO。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2023-02-01"
    },
    {
        "company": "它石智航",
        "person_name": "丁文超",
        "action": "创业",
        "old_role": "-",
        "new_role": "它石智航创始人",
        "title": "科学家丁文超创立它石智航",
        "title_en": "Scientist Ding Wenchao Founds Tashi Zhihang",
        "summary": "来自高校/科研背景的顶尖科学家丁文超出走创业，创立它石智航，专注于具身智能领域。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2023-01-01"
    },
    {
        "company": "银河通用",
        "person_name": "王鹤",
        "action": "创业",
        "old_role": "-",
        "new_role": "银河通用创始人",
        "title": "科学家王鹤创立银河通用",
        "title_en": "Scientist Wang He Founds Yinhe General",
        "summary": "王鹤作为科学家背景创业者，创立银河通用机器人公司，专注泛化具身机器人研发。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2023-01-01"
    },
    {
        "company": "星动纪元",
        "person_name": "陈建宇",
        "action": "创业",
        "old_role": "清华大学助理教授",
        "new_role": "星动纪元创始人",
        "title": "清华助理教授陈建宇创立星动纪元",
        "title_en": "Tsinghua Assistant Professor Chen Jianyu Founds Star Era",
        "summary": "清华大学交叉信息研究院助理教授陈建宇创立星动纪元，公司是清华大学唯一持股的具身智能企业。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2023-08-01"
    },
    {
        "company": "昆仑行",
        "person_name": "郎咸朋",
        "action": "创业",
        "old_role": "理想汽车智能驾驶总裁",
        "new_role": "昆仑行创始人",
        "title": "前理想汽车智驾总裁郎咸朋创立昆仑行",
        "title_en": "Ex-Li Auto VP Lang Xianpeng Founds Kunlunxing",
        "summary": "前理想汽车智能驾驶总裁郎咸朋出走创业，创办具身智能大模型公司昆仑行。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "至简动力",
        "person_name": "贾鹏/王凯",
        "action": "创业",
        "old_role": "理想汽车高管",
        "new_role": "至简动力创始人",
        "title": "理想汽车高管贾鹏、王凯创立至简动力",
        "title_en": "Ex-Li Auto Execs Jia Peng & Wang Kai Founds Zhijian Power",
        "summary": "前理想自动驾驶技术研发负责人贾鹏、前理想CTO王凯出走创办至简动力，半年内完成5轮融资。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "无界动力",
        "person_name": "夏中谱",
        "action": "加入",
        "old_role": "理想汽车智驾技术负责人",
        "new_role": "联合创始人兼联席CTO",
        "title": "前理想智驾负责人夏中谱加入无界动力任联席CTO",
        "title_en": "Ex-Li Auto Exec Xia Zhongpu Joins Wujie Power as Co-CTO",
        "summary": "前理想前端到端智驾技术负责人夏中谱离开理想，加入无界动力担任联合创始人兼联席CTO。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "无界动力",
        "person_name": "张玉峰",
        "action": "创业",
        "old_role": "地平线副总裁/智能汽车事业部总裁",
        "new_role": "无界动力创始人",
        "title": "前地平线副总裁张玉峰创立无界动力",
        "title_en": "Ex-Horizon VP Zhang Yufeng Founds Wujie Power",
        "summary": "前地平线副总裁、智能汽车事业部总裁张玉峰出走创办无界动力。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "小雨智造",
        "person_name": "乔忠良/王文林",
        "action": "创业",
        "old_role": "小米高管",
        "new_role": "小雨智造创始人",
        "title": "小米初创成员乔忠良、王文林创立小雨智造",
        "title_en": "Ex-Xiaomi Execs Qiao Zhongliang & Wang Wenlin Founds Xiaoyu Zhizao",
        "summary": "小米初创成员乔忠良、前小米软件系统平台部总经理王文林联手创办小雨智造，瞄准工业具身智能。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "阿米奥机器人",
        "person_name": "刘方",
        "action": "创业",
        "old_role": "小米汽车自动驾驶产品技术负责人",
        "new_role": "阿米奥机器人创始人",
        "title": "小米汽车前高管刘方成立阿米奥机器人",
        "title_en": "Ex-Xiaomi Auto Exec Liu Fang Founds Amio Robotics",
        "summary": "前小米汽车自动驾驶产品技术负责人和量产交付负责人刘方出走，成立阿米奥机器人。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "灵足时代",
        "person_name": "王勃",
        "action": "创业",
        "old_role": "小米系",
        "new_role": "灵足时代创始人",
        "title": "小米系创业者王勃创办灵足时代",
        "title_en": "Ex-Xiaomi Founder Wang Bo Founds Lingzu Era",
        "summary": "小米系创业者王勃出走创办灵足时代，主营一体化关节模组。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-01-01"
    },
    {
        "company": "破壳机器人",
        "person_name": "许华哲",
        "action": "创业",
        "old_role": "星海图首席科学家",
        "new_role": "破壳机器人创始人",
        "title": "星海图前首席科学家许华哲创立破壳机器人",
        "title_en": "Ex-StarSea CTO Xu Huazhe Founds Poko Robotics",
        "summary": "星海图前首席科学家许华哲离开，成立新公司破壳机器人，瞄准家庭机器人，已获星海图种子轮投资。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2025-06-01"
    },
    {
        "company": "1X Technologies",
        "person_name": "多位关键人才",
        "action": "加入",
        "old_role": "特斯拉员工",
        "new_role": "-",
        "title": "1X Technologies从特斯拉挖走多个关键人物",
        "title_en": "1X Technologies Hires Multiple Key Personnel from Tesla",
        "summary": "挪威人形机器人公司1X Technologies于2024年从特斯拉挖走了多个关键人物，增强其机器人研发团队。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3769206575510016",
        "date": "2024-01-01"
    },
    {
        "company": "Physical Intelligence",
        "person_name": "Karol Hausman",
        "action": "创业",
        "old_role": "斯坦福大学研究员",
        "new_role": "Physical Intelligence联合创始人/CEO",
        "title": "斯坦福研究员Karol Hausman创立Physical Intelligence",
        "title_en": "Stanford Researcher Karol Hausman Co-founds Physical Intelligence",
        "summary": "斯坦福大学研究员Karol Hausman联合创立Physical Intelligence (PI)，致力于将通用人工智能应用于物理世界。PI团队汇集了学术大牛和产业老兵，包括Chelsea Finn、Sergey Levine等知名学者。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/2687713640148354",
        "date": "2024-03-01"
    },
    {
        "company": "千寻智能",
        "person_name": "韩峰涛",
        "action": "创业",
        "old_role": "珞石机器人联合创始人兼CTO",
        "new_role": "千寻智能创始人兼CEO",
        "title": "珞石机器人前CTO韩峰涛创立千寻智能",
        "title_en": "Ex-Rokae CTO Han Fengtao Founds Spirit AI",
        "summary": "韩峰涛本科毕业于华中科技大学自动化学院，硕士毕业于浙江大学，曾任珞石机器人联合创始人兼CTO。2024年2月创立千寻智能，机器人行业从业十余年。",
        "source": "百度百科",
        "source_url": "https://baike.baidu.com/item/韩峰涛/66237371",
        "date": "2024-02-01"
    },
    # ===== 2026-04-27 新增人事动态 =====
    {
        "company": "宇树科技",
        "person_name": "王兴兴",
        "action": "晋升",
        "old_role": "董事",
        "new_role": "董事长",
        "title": "宇树科技完成更名，王兴兴由董事晋升为董事长",
        "title_en": "Unitree CEO Wang Xingxing Promoted to Chairman",
        "summary": "2025年10月23日，宇树科技完成企业名称变更，由'杭州宇树科技股份有限公司'变更为'宇树科技股份有限公司'。同时，CEO王兴兴由董事晋升为董事长，为上市铺路。",
        "source": "IT之家",
        "source_url": "https://news.qq.com/rain/a/20251023A04TQE00",
        "date": "2025-10-23"
    },
    {
        "company": "特斯拉",
        "person_name": "Ashish Kumar",
        "action": "离职",
        "old_role": "Optimus AI团队负责人",
        "new_role": "-",
        "title": "特斯拉Optimus AI团队负责人Ashish Kumar离职，加入Meta",
        "title_en": "Tesla Optimus AI Lead Ashish Kumar Departs for Meta",
        "summary": "特斯拉Optimus AI团队负责人Ashish Kumar于2023年7月加入特斯拉，2025年9月19日宣布离职并加入Meta担任研究科学家。他领导团队研究可扩展AI方法，用强化学习技术替换传统机器人控制栈。",
        "source": "新浪财经",
        "source_url": "https://finance.sina.com.cn/stock/bxjj/2025-09-19/doc-infqyxsq9853632.shtml",
        "date": "2025-09-19"
    },
    {
        "company": "特斯拉",
        "person_name": "Milan Kovac",
        "action": "离职",
        "old_role": "Optimus项目负责人/高级副总裁",
        "new_role": "-",
        "title": "特斯拉Optimus项目负责人Milan Kovac宣布离职",
        "title_en": "Tesla Optimus Project Lead Milan Kovac Departs",
        "summary": "特斯拉Optimus人形机器人项目负责人Milan Kovac在社交媒体宣布即将离职，他表示这是'一生中最艰难的决定'。Milan Kovac曾负责Optimus项目的整体技术方向。",
        "source": "今日头条",
        "source_url": "https://www.toutiao.com/article/7513050617695175195/",
        "date": "2025-06-07"
    },
    {
        "company": "Sanctuary AI",
        "person_name": "Geordie Rose",
        "action": "离职",
        "old_role": "创始人兼CEO",
        "new_role": "-",
        "title": "Sanctuary AI创始人兼CEO Geordie Rose离职（被董事会罢免）",
        "title_en": "Sanctuary AI Co-founder & CEO Geordie Rose Departs",
        "summary": "2024年11月9日，Sanctuary AI在官网宣布创始人兼CEO Geordie Rose离职。媒体报道显示，Geordie Rose是被董事会罢免的，而非主动辞职。公司当时正面临量产进度不及预期的压力。",
        "source": "腾讯新闻",
        "source_url": "https://news.qq.com/rain/a/20241117A0209E00",
        "date": "2024-11-09"
    },
    {
        "company": "Sanctuary AI",
        "person_name": "Rachael McIntosh",
        "action": "接任",
        "old_role": "-",
        "new_role": "临时CEO",
        "title": "Sanctuary AI首席商务官Rachael McIntosh接任临时CEO",
        "title_en": "Sanctuary AI Appoints Rachael McIntosh as Interim CEO",
        "summary": "在创始人Geordie Rose被罢免后，Sanctuary AI首席商务官Rachael McIntosh接任临时CEO。",
        "source": "The Logic",
        "source_url": "https://info.creditriskmonitor.com/NewsStory.aspx?NewsId=49229588",
        "date": "2024-11-09"
    },
    {
        "company": "星海图",
        "person_name": "许华哲",
        "action": "离职",
        "old_role": "首席科学家",
        "new_role": "-",
        "title": "星海图首席科学家许华哲离职创业，成立破壳机器人",
        "title_en": "StarSea Chief Scientist Xu Huazhe Departs to Found Poko Robotics",
        "summary": "2026年2月，星海图首席科学家许华哲正式离职创业，成立新公司破壳机器人，瞄准家庭机器人市场。破壳机器人已获得星海图种子轮投资。许华哲是清华大学博士，曾任星海图首席科学家。",
        "source": "搜狐",
        "source_url": "https://www.sohu.com/a/986273677_701814",
        "date": "2026-02-11"
    },
    {
        "company": "智元机器人",
        "person_name": "多位高管",
        "action": "离职",
        "old_role": "高管",
        "new_role": "-",
        "title": "智元机器人多位高管密集离职",
        "title_en": "Multiple Executives Depart from AgiBot",
        "summary": "2025年8月，智元机器人被曝多位高管密集离职。此前2024年10月，CEO邓泰华进行了研发部门组织架构改革，由中台部门变为以各产品线为核心的项目制。",
        "source": "腾讯新闻",
        "source_url": "https://news.qq.com/rain/a/20250807A05DTE00",
        "date": "2025-08-07"
    },
    {
        "company": "傅利叶",
        "person_name": "顾捷",
        "action": "创业",
        "old_role": "-",
        "new_role": "傅利叶创始人兼CEO",
        "title": "顾捷创立傅利叶智能",
        "title_en": "Gu Jie Founds Fourier Intelligence",
        "summary": "顾捷毕业于上海交通大学机械系，2003年毕业后曾在美国国家仪器担任高管。2015年在上海浦东张江创立傅利叶智能，2017年研发出国内首款有'触觉'的下肢外骨骼康复机器人Fourier X1。",
        "source": "百度百科",
        "source_url": "https://baike.baidu.com/item/顾捷/22072963",
        "date": "2015-01-01"
    },
    {
        "company": "梅卡曼德",
        "person_name": "邵天兰",
        "action": "创业",
        "old_role": "-",
        "new_role": "梅卡曼德创始人兼CEO",
        "title": "邵天兰创立梅卡曼德机器人",
        "title_en": "Shao Tianlan Founds Mecademic Robotics",
        "summary": "邵天兰本科毕业于清华大学软件学院，后于德国慕尼黑工业大学获得机器人方向硕士学位。创立梅卡曼德机器人，致力于工业3D视觉和机器人'眼脑手'技术研发。",
        "source": "百度百科",
        "source_url": "https://baike.baidu.com/item/邵天兰/24113920",
        "date": "2016-01-01"
    },
    {
        "company": "思灵机器人",
        "person_name": "陈兆芃",
        "action": "创业",
        "old_role": "德国宇航中心机器人实验室副主任",
        "new_role": "思灵机器人创始人兼CEO",
        "title": "德国宇航中心科学家陈兆芃创立思灵机器人",
        "title_en": "Chen Zhaopeng Founds Agile Robots from DLR",
        "summary": "陈兆芃毕业于哈尔滨工业大学、德国航空航天中心(DLR)获博士学位，曾任德国宇航中心机器人实验室副主任。2018年创立思灵机器人，核心团队均来自德国宇航中心机器人研究所。",
        "source": "百度百科",
        "source_url": "https://baike.baidu.com/item/陈兆芃/61992611",
        "date": "2018-07-24"
    },
    {
        "company": "穹彻智能",
        "person_name": "卢策吾",
        "action": "创业",
        "old_role": "上海交通大学教授",
        "new_role": "穹彻智能创始人",
        "title": "上交大教授卢策吾创立穹彻智能",
        "title_en": "Professor Lu Cewo Founds UniX Robotics",
        "summary": "卢策吾是上海交通大学教授，2023年11月创立穹彻智能，专注于'以力为中心'的具身智能大模型研发。公司由非夕科技孵化，已完成数亿元多轮融资。",
        "source": "企查查",
        "source_url": "https://www.qcc.com/firm/8b35ea81d3a95ea6f0df2f1e962fbed2.html",
        "date": "2023-11-01"
    },
    {
        "company": "Apptronik",
        "person_name": "Jeff Cardenas",
        "action": "创业",
        "old_role": "-",
        "new_role": "Apptronik创始人兼CEO",
        "title": "Jeff Cardenas创立Apptronik",
        "title_en": "Jeff Cardenas Founds Apptronik",
        "summary": "Jeff Cardenas是Apptronik创始人兼CEO。公司由德克萨斯大学奥斯汀分校人本机器人实验室团队于2016年创立，该团队曾参与NASA的Valkyrie人形机器人开发。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/3589487362899974",
        "date": "2016-01-01"
    },
    {
        "company": "Apptronik",
        "person_name": "Nicholas Paine",
        "action": "加入",
        "old_role": "NASA-JSC工程师",
        "new_role": "CTO兼联合创始人",
        "title": "NASA工程师Nicholas Paine加入Apptronik任CTO",
        "title_en": "NASA Engineer Nicholas Paine Joins Apptronik as CTO",
        "summary": "Nicholas Paine是NASA约翰逊航天中心工程师出身，后加入Apptronik担任CTO兼联合创始人。他在美国德克萨斯大学奥斯汀分校人本机器人实验室期间曾参与NASA Valkyrie机器人开发。",
        "source": "36氪",
        "source_url": "https://eu.36kr.com/zh/p/3589487362899974",
        "date": "2016-01-01"
    },
    {
        "company": "Skild AI",
        "person_name": "Abhinav Gupta",
        "action": "创业",
        "old_role": "卡内基梅隆大学教授",
        "new_role": "Skild AI联合创始人/总裁",
        "title": "CMU教授Abhinav Gupta创立Skild AI",
        "title_en": "CMU Professor Abhinav Gupta Co-founds Skild AI",
        "summary": "Abhinav Gupta是卡内基梅隆大学前教授，与Deepak Pathak共同创立Skild AI。公司致力于构建能安装到各种机器人设备上的通用'具身大脑'，2025年估值达320亿美元。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/2863460836526979",
        "date": "2023-05-01"
    },
    {
        "company": "Skild AI",
        "person_name": "Deepak Pathak",
        "action": "创业",
        "old_role": "卡内基梅隆大学教授",
        "new_role": "Skild AI联合创始人/CEO",
        "title": "CMU教授Deepak Pathak创立Skild AI",
        "title_en": "CMU Professor Deepak Pathak Co-founds Skild AI",
        "summary": "Deepak Pathak是卡内基梅隆大学前教授，与Abhinav Gupta共同创立Skild AI。两人在机器人和AI领域共拥有25年的研究经验，曾在Meta平台担任研究科学家。",
        "source": "36氪",
        "source_url": "https://www.36kr.com/p/2863460836526979",
        "date": "2023-05-01"
    },
    {
        "company": "Agibot",
        "person_name": "邓泰华",
        "action": "加入",
        "old_role": "华为公司高层",
        "new_role": "智元机器人CEO",
        "title": "华为背景邓泰华加入智元机器人出任CEO",
        "title_en": "Ex-Huawei Executive Deng Taihua Joins AgiBot as CEO",
        "summary": "邓泰华具有华为背景，加入智元机器人后担任CEO。2024年10月，他对研发部门进行组织架构改革。2025年3月，法定代表人由舒远春变更为邓泰华。",
        "source": "上证报",
        "source_url": "https://www.cnstock.com/commonDetail/380145",
        "date": "2024-01-01"
    },
    {
        "company": "灵御智能",
        "person_name": "金戈",
        "action": "创业",
        "old_role": "前硬科技投资人",
        "new_role": "灵御智能联合创始人兼CEO",
        "title": "清华系创业者金戈创立灵御智能",
        "title_en": "Tsinghua Alumni Jin Ge Founds Lingyu Intelligence",
        "summary": "金戈毕业于清华大学自动化系，后获清华大学经济管理学院MBA，曾任远镜创投管理合伙人、奥量光子副总。2025年2月创立灵御智能，专注于具身智能基础设施和遥操作技术。",
        "source": "搜狐",
        "source_url": "https://www.sohu.com/a/996033750_439726",
        "date": "2025-02-01"
    },
    {
        "company": "Generalist",
        "person_name": "Pete Florence",
        "action": "创业",
        "old_role": "DeepMind高级研究科学家",
        "new_role": "Generalist AI创始人兼CEO",
        "title": "DeepMind科学家Pete Florence创立Generalist AI",
        "title_en": "Ex-DeepMind Scientist Pete Florence Founds Generalist AI",
        "summary": "Pete Florence是前DeepMind高级研究科学家，曾参与PaLM-E、RT-2两大具身智能里程碑项目。2025年3月离开Google创立Generalist AI，获NVIDIA投资。",
        "source": "搜狐",
        "source_url": "https://www.sohu.com/a/939945034_121124378",
        "date": "2025-03-01"
    },
    {
        "company": "智在无界",
        "person_name": "卢宗青",
        "action": "创业",
        "old_role": "北京大学计算机学院长聘副教授/智源研究院多模态交互研究中心负责人",
        "new_role": "智在无界创始人兼CEO",
        "title": "前智源团队卢宗青创立智在无界",
        "title_en": "Ex-BAAI Researcher Lu Zongqing Founds BeingBeyond",
        "summary": "卢宗青是北京大学计算机学院长聘副教授，前智源研究院多模态交互研究中心负责人，曾负责首个国家自然科学基金委原创探索计划通用智能体项目。2025年1月创立智在无界(BeingBeyond)，获联想之星领投数千万元天使轮融资。",
        "source": "36氪",
        "source_url": "https://36kr.com/p/3324923112614405",
        "date": "2025-01-01"
    },
    {
        "company": "Tesla Optimus",
        "person_name": "Milan Kovac",
        "action": "离职",
        "old_role": "Optimus项目负责人/VP",
        "new_role": "-",
        "title": "特斯拉Optimus项目负责人Milan Kovac离职",
        "title_en": "Tesla Optimus Project Lead Milan Kovac Departs",
        "summary": "Milan Kovac自2016年加入特斯拉，2022年起负责Optimus项目硬件与软件平台搭建，2024年底晋升为副总裁。2025年6月7日宣布离职，称需要更多时间陪伴家人。特斯拉AI软件副总裁Ashok Elluswamy接任项目负责人。",
        "source": "新浪财经",
        "source_url": "https://finance.sina.com.cn/stock/hkstock/hkstocknews/2025-06-07/doc-inezfuhy1500594.shtml",
        "date": "2025-06-07"
    },
    {
        "company": "Tesla Optimus",
        "person_name": "Ashish Kumar",
        "action": "离职加入Meta",
        "old_role": "AI团队负责人",
        "new_role": "Meta研究科学家",
        "title": "特斯拉Optimus AI团队负责人Ashish Kumar离职加入Meta",
        "title_en": "Tesla Optimus AI Lead Ashish Kumar Leaves for Meta",
        "summary": "Ashish Kumar于2023年7月加入特斯拉担任Optimus AI团队负责人，2025年9月离职加入Meta担任研究科学家。",
        "source": "Reportify",
        "source_url": "https://reportify.cn/news/1166374005352042496",
        "date": "2025-09-19"
    },
    {
        "company": "Agility Robotics",
        "person_name": "Damion Shelton",
        "action": "卸任",
        "old_role": "CEO",
        "new_role": "-",
        "title": "Agility Robotics创始人Damion Shelton卸任CEO",
        "title_en": "Agility Robotics Co-Founder Damion Shelton Steps Down as CEO",
        "summary": "Agility Robotics创始人Damion Shelton于2024年3月4日卸任CEO，由微软前高管Peggy Johnson接任。Shelton曾是卡内基梅隆大学研究员，2015年创立Agility Robotics，领导Digit机器人开发。",
        "source": "机电工程师网",
        "source_url": "https://www.jdgcs.org/news/agility-robotics-boston-dynamics-see-leadership-changes-17729/",
        "date": "2024-03-04"
    },
    {
        "company": "大晓机器人",
        "person_name": "王晓刚",
        "action": "加入",
        "old_role": "-",
        "new_role": "董事长",
        "title": "商汤科技联合创始人王晓刚出任大晓机器人董事长",
        "title_en": "SenseTime Co-Founder Wang Xiaogang Joins Daxiao Robotics as Chairman",
        "summary": "2025年12月，商汤科技联合创始人王晓刚出任大晓机器人董事长。王晓刚是商汤科技创始人之一，在计算机视觉和AI领域有深厚积累，此次加入大晓机器人标志着具身智能领域的强强联合。",
        "source": "公开信息",
        "source_url": "https://www.qcc.com/firm/34337a9c25db2d3dc97d62b242dcefb5.html",
        "date": "2025-12-01"
    },
    {
        "company": "逐际动力",
        "person_name": "张力",
        "action": "离职",
        "old_role": "COO（首席运营官）",
        "new_role": "-",
        "title": "逐际动力联合创始人兼COO张力离职",
        "title_en": "Limx Dynamics Co-Founder and COO Zhang Li Departs",
        "summary": "2026年4月8日确认，逐际动力联合创始人兼COO张力已于年初正式离职，未来将筹备新的创业项目，聚焦具身模型方向。张力是南方科技大学长聘教授，与创始人张巍共同创办逐际动力。",
        "source": "搜狐",
        "source_url": "https://www.sohu.com/a/1008714416_121777994",
        "date": "2026-04-08"
    },
    {
        "company": "Hexagon",
        "person_name": "Anders Svensson",
        "action": "接任",
        "old_role": "-",
        "new_role": "总裁兼CEO",
        "title": "Anders Svensson接任Hexagon总裁兼CEO",
        "title_en": "Anders Svensson Appointed President and CEO of Hexagon",
        "summary": "2025年7月21日，Hexagon宣布Anders Svensson正式出任总裁兼首席执行官，接替临时CEO Norbert Hanke。Hexagon是全球测量技术领军企业，在工业软件和传感器领域有重要地位。",
        "source": "Hexagon官网",
        "source_url": "https://hexagon.com/company/newsroom/press-releases/2025/anders-svensson-appointed-as-new-president-and-ceo-of-hexagon",
        "date": "2025-07-21"
    },
    {
        "company": "Figure AI",
        "person_name": "Jerry Pratt",
        "action": "离职",
        "old_role": "CTO（首席技术官）",
        "new_role": "-",
        "title": "Figure AI首席技术官Jerry Pratt离职创业",
        "title_en": "Figure AI CTO Jerry Pratt Departs to Start New Venture",
        "summary": "Figure AI首席技术官Jerry Pratt于2024年离职，与另一位机器人专家Nic Radford共同创立人形机器人公司Persona AI。Jerry Pratt在Figure AI期间领导了多项核心技术研发。",
        "source": "腾讯新闻",
        "source_url": "https://new.qq.com/rain/a/20240709A08S9K00",
        "date": "2024-06-01"
    },
    {
        "company": "Figure AI",
        "person_name": "Caitlin Kalinowski",
        "action": "加入",
        "old_role": "-",
        "new_role": "机器人程序团队负责人",
        "title": "Meta前AR眼镜项目负责人Caitlin Kalinowski加入Figure AI",
        "title_en": "Former Meta AR Glasses Lead Caitlin Kalinowski Joins Figure AI",
        "summary": "2024年底，Meta前AR眼镜项目负责人Caitlin Kalinowski加入Figure AI，领导机器人程序团队重组。Figure AI于2025年2月宣布终止与OpenAI的合作，转而自主研发AI模型。",
        "source": "搜狐",
        "source_url": "https://www.sohu.com/a/856711833_121902920",
        "date": "2024-12-01"
    },
    {
        "company": "Figure AI",
        "person_name": "-",
        "action": "团队重组",
        "old_role": "-",
        "new_role": "-",
        "title": "Figure AI与OpenAI终止合作，进行团队重组",
        "title_en": "Figure AI Ends OpenAI Partnership, Undergoes Team Restructuring",
        "summary": "2025年2月4日，Figure AI宣布终止与OpenAI的合作关系，转而自主研发AI模型。公司进行团队重组，由Caitlin Kalinowski领导新的机器人程序团队，旨在推动人形机器人技术的自主发展。",
        "source": "搜狐",
        "source_url": "https://www.sohu.com/a/856711833_121902920",
        "date": "2025-02-04"
    },
    {
        "company": "智元机器人",
        "person_name": "邓泰华",
        "action": "加入",
        "old_role": "-",
        "new_role": "创始人、董事长兼CEO",
        "title": "华为前副总裁邓泰华加入智元机器人任董事长兼CEO",
        "title_en": "Former Huawei VP Deng Taihua Joins AgiBot as Chairman and CEO",
        "summary": "2025年3月，华为前副总裁、计算产品线总裁邓泰华加入智元机器人，担任创始人、董事长兼CEO。邓泰华此前在华为任职超过20年，负责计算产品线。智元机器人由此进入新的发展阶段。",
        "source": "新浪财经",
        "source_url": "https://finance.sina.com.cn/jjxw/2025-03-24/doc-inequiik6571403.shtml",
        "date": "2025-03-24"
    },
    {
        "company": "智元机器人",
        "person_name": "魏强",
        "action": "离职",
        "old_role": "灵犀事业部总裁",
        "new_role": "-",
        "title": "智元机器人灵犀事业部总裁魏强离职",
        "title_en": "AgiBot Lingxi Business Unit President Wei Qiang Departs",
        "summary": "2025年8月，智元机器人灵犀事业部总裁魏强离职。魏强此前负责智元机器人灵犀事业部，后由创始人彭志辉轮值接任该事业部总裁。",
        "source": "腾讯新闻",
        "source_url": "https://news.qq.com/rain/a/20250807A05DTE00",
        "date": "2025-08-07"
    },
    {
        "company": "智元机器人",
        "person_name": "闫维新",
        "action": "离职",
        "old_role": "联合创始人",
        "new_role": "-",
        "title": "智元机器人联合创始人闫维新离职",
        "title_en": "AgiBot Co-Founder Yan Weixin Departs",
        "summary": "2025年8月，智元机器人联合创始人闫维新离职。闫维新来自上海交通大学，是智元机器人早期核心团队成员之一。离职后由彭志辉轮值接任灵犀事业部总裁。",
        "source": "腾讯新闻",
        "source_url": "https://news.qq.com/rain/a/20250807A05DTE00",
        "date": "2025-08-07"
    }
]

def main():
    # 加载现有事件
    events = load_events()
    existing_ids = {e.get('id') for e in events}
    
    # 生成新事件
    new_count = 0
    for pe in personnel_events:
        event_id = generate_id(pe['company'], pe['date'])
        idx = 0
        while event_id in existing_ids:
            idx += 1
            event_id = generate_id(pe['company'], pe['date'], idx)
        
        event = {
            "id": event_id,
            "company": pe['company'],
            "type": "personnel",
            "title": pe['title'],
            "title_en": pe.get('title_en', ''),
            "summary": pe.get('summary', ''),
            "source": pe['source'],
            "source_url": pe['source_url'],
            "date": pe['date'],
            "created_at": datetime.now().isoformat(),
            "media_sources": [pe['source']],
            # 人事动态特有字段
            "person_name": pe['person_name'],
            "action": pe['action'],
            "old_role": pe.get('old_role', ''),
            "new_role": pe.get('new_role', '')
        }
        events.append(event)
        new_count += 1
        print(f"+ {pe['company']} - {pe['person_name']} {pe['action']} ({pe['date']})")
    
    # 去重
    print("\n[Dedup] Running deduplication...")
    events = deduplicate_events(events)
    
    # 保存
    save_events(events)
    print(f"[OK] Added {new_count} personnel events")
    print(f"[Total] Current events: {len(events)}")

if __name__ == '__main__':
    main()
