#!/usr/bin/env python3
"""
多线程批量翻译脚本 - 翻译 events.json 中中文标题的 title_en
只翻译真正的中文内容，英文新闻直接标记跳过
"""

import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator

# 配置
MAX_WORKERS = 10  # 并发线程数
INPUT_FILE = 'data/events.json'
OUTPUT_FILE = 'data/events.json'
LOCK = threading.Lock()

# 统计
stats = {'total': 0, 'chinese': 0, 'english': 0, 'success': 0, 'failed': 0, 'skipped': 0}

def has_chinese(text):
    """判断是否包含中文"""
    if not text:
        return False
    return any('\u4e00' <= c <= '\u9fff' for c in text)

def translate_text(text, max_retries=3):
    """翻译单条文本"""
    if not text or not text.strip():
        return None

    for attempt in range(max_retries):
        try:
            result = GoogleTranslator(source='zh-CN', target='en').translate(text.strip())
            if result:
                return result
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.3 * (attempt + 1))
    return None

def process_item(item):
    """处理单条新闻"""
    global stats

    # 已有的不处理
    if item.get('title_en'):
        with LOCK:
            stats['skipped'] += 1
        return None

    title = item.get('title', '')
    if not title:
        with LOCK:
            stats['skipped'] += 1
        return None

    # 判断是否是中文
    if not has_chinese(title):
        # 英文内容，标记为 title_en = title（原文）
        with LOCK:
            stats['english'] += 1
        return {
            'id': item['id'],
            'title_en': title  # 英文原文
        }

    # 翻译中文标题
    with LOCK:
        stats['chinese'] += 1

    title_en = translate_text(title)
    if not title_en:
        with LOCK:
            stats['failed'] += 1
        return None

    with LOCK:
        stats['success'] += 1

    return {
        'id': item['id'],
        'title_en': title_en
    }

def main():
    global stats

    # 读取数据
    print("📖 读取数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 找出需要处理的（title_en为空）
    to_process = [item for item in data if not item.get('title_en') and item.get('title')]
    stats['total'] = len(to_process)

    print(f"📊 总计 {len(data)} 条新闻")
    print(f"📝 需要处理: {stats['total']} 条")
    print(f"⚡ 并发线程: {MAX_WORKERS}")
    print("-" * 40)

    if not to_process:
        print("✅ 没有需要处理的新闻")
        return

    # 多线程处理
    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_item, item): item for item in to_process}

        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            if result:
                results.append(result)

            # 进度显示
            if completed % 100 == 0 or completed == len(futures):
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                print(f"📈 进度: {completed}/{len(futures)} ({rate:.1f}/s) - 中: {stats['chinese']} | 英: {stats['english']} | 成功: {stats['success']} | 失败: {stats['failed']}")

    # 更新数据
    print("\n💾 更新数据...")
    id_to_result = {r['id']: r['title_en'] for r in results}

    updated = 0
    for item in data:
        if item['id'] in id_to_result:
            item['title_en'] = id_to_result[item['id']]
            updated += 1

    # 保存
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 统计
    elapsed = time.time() - start_time
    print("\n" + "=" * 40)
    print(f"✅ 翻译完成!")
    print(f"   更新: {updated} 条")
    print(f"   中文翻译: {stats['chinese']} 条")
    print(f"   英文标记: {stats['english']} 条")
    print(f"   翻译成功: {stats['success']} 条")
    print(f"   翻译失败: {stats['failed']} 条")
    print(f"   耗时: {elapsed:.1f} 秒")

if __name__ == '__main__':
    main()
