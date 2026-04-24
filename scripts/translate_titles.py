#!/usr/bin/env python3
"""
Google Translate 并行翻译 - 多线程加速版
"""
import json
import time
import sys
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

THREADS = 10  # 10个线程并行
BATCH_SIZE = 500  # 每次处理500条

def translate_single(text):
    """翻译单条"""
    try:
        translator = GoogleTranslator(source='zh-CN', target='en')
        return translator.translate(text[:500]).strip()
    except:
        return ''

def main():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"总新闻数: {len(data)}")
    
    # 找出需要翻译的
    needs_translate = []
    indices = []
    for i, event in enumerate(data):
        title_en = event.get('title_en', '')
        if not title_en or len(title_en.strip()) < 5:
            needs_translate.append(event.get('title', ''))
            indices.append(i)
    
    total_need = len(needs_translate)
    print(f"需要翻译: {total_need}")
    
    if not needs_translate:
        print("全部已完成！")
        return
    
    # 只处理前 BATCH_SIZE 条
    batch = needs_translate[:BATCH_SIZE]
    batch_indices = indices[:BATCH_SIZE]
    
    print(f"\n并行翻译 {len(batch)} 条 ({THREADS} 线程)...\n")
    start = time.time()
    
    # 多线程并行翻译
    translations = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(translate_single, t): i for i, t in enumerate(batch)}
        
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            translations.append(result)
            completed += 1
            if completed % 100 == 0:
                print(f"  进度: {completed}/{len(batch)}")
    
    elapsed = time.time() - start
    print(f"\n完成! 耗时: {elapsed:.1f}秒 ({len(batch)/elapsed:.1f} 条/秒)")
    
    # 更新数据
    for idx, translation in zip(batch_indices, translations):
        data[idx]['title_en'] = translation
    
    # 统计
    translated = sum(1 for e in data if e.get('title_en') and len(e.get('title_en', '')) > 5)
    remaining = total_need - len(batch)
    
    print(f"\n{'='*50}")
    print(f"本批完成: {len(batch)}")
    print(f"剩余待翻: {remaining}")
    print(f"总计英文标题: {translated}/{len(data)}")
    
    # 保存
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 翻译示例
    print(f"\n{'='*50}")
    print("翻译示例:")
    shown = 0
    for e in data[:20]:
        if e.get('title_en') and shown < 5:
            print(f"  {e.get('title')[:40]} → {e.get('title_en')[:50]}")
            shown += 1

if __name__ == "__main__":
    main()
