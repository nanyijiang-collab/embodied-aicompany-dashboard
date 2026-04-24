#!/usr/bin/env python3
"""
批量翻译新闻标题为英文
使用 Google Translate 免费接口
"""
import json
import time
import re
import sys
import os

# 尝试导入翻译库
try:
    from deep_translator import GoogleTranslator
    USE_DEEP_TRANSLATOR = True
except ImportError:
    USE_DEEP_TRANSLATOR = False
    print("deep_translator not installed, trying googletrans...")

try:
    from googletrans import Translator
    USE_GOOGLETRANS = True
except ImportError:
    USE_GOOGLETRANS = False

# 加载事件数据
def load_events():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存事件数据
def save_events(events):
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

# 使用 deep-translator 翻译
def translate_deep(text, max_retries=3):
    if not text or not text.strip():
        return text
    
    for attempt in range(max_retries):
        try:
            result = GoogleTranslator(source='zh-CN', target='en').translate(text)
            return result
        except Exception as e:
            print(f"  翻译失败 (尝试 {attempt+1}/{max_retries}): {e}")
            time.sleep(2)
    return None

# 使用 googletrans 翻译
def translate_googletrans(text, max_retries=3):
    if not text or not text.strip():
        return text
    
    translator = Translator()
    for attempt in range(max_retries):
        try:
            result = translator.translate(text, src='zh-CN', dest='en')
            return result.text
        except Exception as e:
            print(f"  翻译失败 (尝试 {attempt+1}/{max_retries}): {e}")
            time.sleep(2)
    return None

# 主翻译函数
def translate(text):
    if not text or not text.strip():
        return text
    
    if USE_DEEP_TRANSLATOR:
        return translate_deep(text)
    elif USE_GOOGLETRANS:
        return translate_googletrans(text)
    else:
        print("No translator library available!")
        return None

# 翻译进度
def translate_all(progress_callback=None):
    events = load_events()
    total = len(events)
    
    # 统计
    needs_translation = 0
    already_has_en = 0
    
    for event in events:
        if not event.get('title_en'):
            needs_translation += 1
        else:
            already_has_en += 1
    
    print(f"总事件数: {total}")
    print(f"已有英文标题: {already_has_en}")
    print(f"需要翻译: {needs_translation}")
    print()
    
    if needs_translation == 0:
        print("没有需要翻译的事件！")
        return
    
    # 确认
    response = input(f"是否开始翻译 {needs_translation} 条标题? (y/n): ")
    if response.lower() != 'y':
        print("取消翻译")
        return
    
    # 开始翻译
    translated = 0
    failed = 0
    
    for i, event in enumerate(events):
        if event.get('title_en'):
            continue
        
        title = event.get('title', '')
        if title:
            # 显示进度
            print(f"[{i+1}/{total}] 翻译: {title[:50]}...")
            
            title_en = translate(title)
            if title_en:
                event['title_en'] = title_en
                translated += 1
            else:
                failed += 1
                print(f"  翻译失败!")
            
            # 保存进度（每100条保存一次）
            if (i + 1) % 100 == 0:
                save_events(events)
                print(f"\n>>> 已保存进度 ({i+1}/{total}) <<<\n")
        
        # 礼貌延迟，避免请求过快
        time.sleep(0.3)
    
    # 最终保存
    save_events(events)
    
    print()
    print(f"翻译完成!")
    print(f"成功翻译: {translated}")
    print(f"翻译失败: {failed}")
    print(f"已有英文: {already_has_en}")

if __name__ == '__main__':
    print("=" * 50)
    print("具身智能媒体监测 - 标题翻译工具")
    print("=" * 50)
    print()
    
    # 检查库
    if not USE_DEEP_TRANSLATOR and not USE_GOOGLETRANS:
        print("正在安装翻译库...")
        os.system(f"{sys.executable} -m pip install deep-translator -q")
        try:
            from deep_translator import GoogleTranslator
            USE_DEEP_TRANSLATOR = True
        except:
            pass
    
    translate_all()
