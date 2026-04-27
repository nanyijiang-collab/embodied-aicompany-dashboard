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
