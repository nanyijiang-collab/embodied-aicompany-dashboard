#!/usr/bin/env python3
"""
简单关键词过滤 v2 - 去除明显不相关的新闻
"""
import json

# 不相关关键词
IRRELEVANT_KEYWORDS = [
    # 显卡/GPU硬件（除非提到机器人）
    'RTX 4090', 'RTX 4080', 'RTX 4070', 'RTX 4060', '显卡评测', '公版PCB', '显存',
    
    # 股票分析
    '股价', '涨跌', '市值', '季报', '年报', '营收',
    '买入', '卖出', '评级', '目标价', '分析师',
    
    # 纯LLM/ChatGPT新闻
    'GPT-5', 'GPT-4o', 'ChatGPT', 'Codex编程', 'Sora',
    'Claude', 'Llama', 'Gemini', 'Copilot',
    
    # 纯加密货币（Pi币等）
    'Pi币', 'PI今日价格', '加密货币', '市值行情',
    
    # 地缘政治
    '出口管制', '实体清单',
    
    # Robotaxi（除非提到人形）
    'Robotaxi出故障',
]

# 必须保留的关键词（即使有排除词也要保留）
MUST_KEEP_KEYWORDS = [
    '具身', '人形', '机器人', '机械臂', '机械手', '四足',
    'Digit', 'Atlas', 'Optimus', 'Figure', '宇树', '智元',
    '银河通用', '星动纪元', '逐际', '思灵', '傅利叶',
    'GR00T', 'Isaac', 'VLA', '世界模型', '灵巧手',
    '季报', '对话', '专访', '融资', '融资',
    '英伟达', '黄仁勋',  # 默认相关
]

def is_relevant(news_item):
    """判断新闻是否相关"""
    title = news_item.get('title', '')
    company = news_item.get('company', '')

    # 先检查是否必须保留
    for kw in MUST_KEEP_KEYWORDS:
        if kw in title or kw in company:
            return True

    # 检查是否在排除列表
    for kw in IRRELEVANT_KEYWORDS:
        if kw in title:
            return False

    return True

def main():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_count = len(data)
    
    filtered = []
    removed = []
    
    for item in data:
        if is_relevant(item):
            filtered.append(item)
        else:
            removed.append(item)

    print(f"原始: {original_count}")
    print(f"过滤后: {len(filtered)}")
    print(f"删除: {len(removed)}")
    
    print("\n=== 删除的新闻 ===")
    for e in removed[:30]:
        print(f"  [{e.get('company')}] {e.get('title')[:50]}")
    if len(removed) > 30:
        print(f"  ... 还有 {len(removed)-30} 条")
    
    # 保存
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    
    with open('data/removed_news.json', 'w', encoding='utf-8') as f:
        json.dump(removed, f, ensure_ascii=False, indent=2)
    
    print(f"\n已更新 data/events.json")

if __name__ == "__main__":
    main()
