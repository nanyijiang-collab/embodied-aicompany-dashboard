# -*- coding: utf-8 -*-
import json

d = json.load(open('data/events.json', encoding='utf-8'))

sogou_links = [e for e in d if 'weixin.sogou.com' in e.get('source_url', '')]
mp_links = [e for e in d if 'mp.weixin.qq.com' in e.get('source_url', '')]
direct_links = [e for e in d if e.get('source_url', '') and not any(x in e.get('source_url', '') for x in ['weixin.sogou.com', 'mp.weixin.qq.com'])]
empty_links = [e for e in d if not e.get('source_url', '')]

print(f'搜狗跳转链接: {len(sogou_links)}')
print(f'微信直链: {len(mp_links)}')
print(f'其他直链: {len(direct_links)}')
print(f'空链接: {len(empty_links)}')
print(f'总计: {len(d)}')

print('\n=== 搜狗跳转链接示例 ===')
for e in sogou_links[:5]:
    print(f"  [{e.get('company', '')[:15]}] {e.get('title', '')[:40]}...")
    print(f"    URL: {e.get('source_url', '')[:80]}")

print('\n=== 微信直链示例 ===')
for e in mp_links[:5]:
    print(f"  [{e.get('company', '')[:15]}] {e.get('title', '')[:40]}...")
    print(f"    URL: {e.get('source_url', '')[:80]}")

print('\n=== 其他直链示例 ===')
for e in direct_links[:10]:
    url = e.get('source_url', '')
    domain = url.split('/')[2] if '/' in url else url
    print(f"  [{e.get('company', '')[:15]}] {domain}")
