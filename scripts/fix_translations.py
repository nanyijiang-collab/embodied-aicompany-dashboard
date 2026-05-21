#!/usr/bin/env python3
"""
修复 translate_titles.py 错位导致的 title_en 损坏（v4）
策略：
1. 用 43c2580 的干净 title_en 恢复老事件
2. 清除所有新增事件（不在 43c2580 中的）的 title_en（这些全是错位垃圾）
3. 保存后由修复好的 translate_titles.py 重跑翻译
"""
import json
import subprocess
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_git_file(commit, path):
    raw = subprocess.check_output(['git', 'show', f'{commit}:{path}'], encoding='utf-8')
    return json.loads(raw)

def main():
    print("加载干净版本 (43c2580)...")
    clean = load_git_file('43c2580', 'data/events.json')
    print(f"  条数: {len(clean)}")

    print("加载当前版本 (HEAD)...")
    current = load_git_file('HEAD', 'data/events.json')
    print(f"  条数: {len(current)}")

    # Build title -> title_en mapping from clean version
    title_to_en = {}
    for e in clean:
        title = (e.get('title') or '').strip()
        title_en = (e.get('title_en') or '').strip()
        if title and title_en and len(title_en) >= 5:
            title_to_en[title] = title_en

    print(f"干净 title_en 映射: {len(title_to_en)} 条")

    fixed = 0
    cleared = 0
    kept = 0

    for e in current:
        title = (e.get('title') or '').strip()
        current_en = (e.get('title_en') or '').strip()

        if not title:
            continue

        if title in title_to_en:
            expected = title_to_en[title]
            if current_en != expected:
                e['title_en'] = expected
                fixed += 1
            else:
                kept += 1
        else:
            # Event not in clean version - its title_en is garbage from offset bug
            if current_en and len(current_en) >= 5:
                e['title_en'] = ''
                cleared += 1

    print(f"\n恢复正确翻译: {fixed} 条")
    print(f"保持不变: {kept} 条")
    print(f"清除错位垃圾: {cleared} 条")

    remaining_empty = sum(1 for e in current if not (e.get('title_en') or '').strip() or len((e.get('title_en') or '').strip()) < 5)
    print(f"待重新翻译: {remaining_empty} 条")

    # Verify
    print("\n修复后示例:")
    shown = 0
    for e in current:
        en = (e.get('title_en') or '').strip()
        if en and shown < 8:
            print(f"  {e.get('title','')[:45]} -> {en[:55]}")
            shown += 1

    # Save
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(current, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 已保存 data/events.json ({len(current)} 条)")
    print(f"[下一步] 请运行修复后的 translate_titles.py 重翻译 {remaining_empty} 条")

if __name__ == "__main__":
    main()
