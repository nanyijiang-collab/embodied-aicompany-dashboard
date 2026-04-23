# -*- coding: utf-8 -*-
import json

d = json.load(open('data/events.json', encoding='utf-8'))

# 检查Bing新闻（非搜狗、非微信）
bing_links = [e for e in d if 'weixin.sogou.com' not in e.get('source_url', '') and 'mp.weixin.qq.com' not in e.get('source_url', '')]

print(f'非搜狗/微信直链数量: {len(bing_links)}')

# 按来源统计
from collections import Counter
sources = Counter([e.get('source', '') for e in bing_links])
print('\n=== 来源分布 ===')
for source, count in sources.most_common(15):
    print(f"  {source}: {count}")

# 看几条示例
print('\n=== 示例 ===')
for e in bing_links[:10]:
    url = e.get('source_url', '')
    domain = url.split('/')[2] if '://' in url else url[:40]
    print(f"  [{e.get('company', '')[:12]}] {e.get('type', ''):15} {domain}")
