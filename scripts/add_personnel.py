#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加人事动态事件到 events.json
"""

import json
import os
from datetime import datetime

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
    
    # 保存
    save_events(events)
    print(f"[OK] Added {new_count} personnel events")
    print(f"[Total] Current events: {len(events)}")

if __name__ == '__main__':
    main()
