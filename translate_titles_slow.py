#!/usr/bin/env python3
"""限速版翻译脚本：单线程 + 请求间隔，应对引擎限流积压"""
import json
import time
import sys
from deep_translator import MyMemoryTranslator, GoogleTranslator

INPUT_FILE = 'data/events.json'
DELAY = 1.2          # 每次请求间隔（秒）
RATE_WAIT = 60       # 被限流时等待（秒）

def has_chinese(text):
    return any('\u4e00' <= c <= '\u9fff' for c in (text or ''))

def translate_text(text, max_rounds=5):
    text = text.strip()[:450]
    for round_ in range(max_rounds):
        # MyMemory
        try:
            r = MyMemoryTranslator(source='zh-CN', target='en-US').translate(text)
            if r and r != text:
                return r, 'mymemory'
        except Exception:
            pass
        # Google
        try:
            r = GoogleTranslator(source='zh-CN', target='en').translate(text)
            if r:
                return r, 'google'
        except Exception:
            pass
        time.sleep(RATE_WAIT)
    return None, None

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    todo = [d for d in data if not d.get('title_en') and d.get('title')]
    print(f"total={len(data)} todo={len(todo)}", flush=True)
    if not todo:
        print("NOTHING_TO_DO")
        return

    stats = {'cn_ok': 0, 'en': 0, 'failed': 0, 'mymemory': 0, 'google': 0}
    results = []
    start = time.time()

    for i, item in enumerate(todo):
        title = item['title']
        if not has_chinese(title):
            results.append({'id': item['id'], 'title_en': title})
            stats['en'] += 1
        else:
            en, engine = translate_text(title)
            if en:
                results.append({'id': item['id'], 'title_en': en})
                stats['cn_ok'] += 1
                stats[engine] += 1
            else:
                stats['failed'] += 1
            time.sleep(DELAY)
        if (i + 1) % 100 == 0:
            print(f"progress {i+1}/{len(todo)} ok={stats['cn_ok']} en={stats['en']} fail={stats['failed']} elapsed={time.time()-start:.0f}s", flush=True)

    id_map = {r['id']: r['title_en'] for r in results}
    for item in data:
        if item['id'] in id_map:
            item['title_en'] = id_map[item['id']]

    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("=" * 40, flush=True)
    print(f"updated={len(results)} chinese={stats['cn_ok']} english_marked={stats['en']} failed={stats['failed']}")
    print(f"engines: mymemory={stats['mymemory']} google={stats['google']}")
    print(f"elapsed={time.time()-start:.0f}s")

if __name__ == '__main__':
    main()
