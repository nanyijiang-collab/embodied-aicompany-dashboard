# -*- coding: utf-8 -*-
"""快速测试 Google News RSS"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'

from scripts.crawler import EmbodiedAICrawler
c = EmbodiedAICrawler()

print('=== Test: 智元机器人 ===')
results = c.crawl_google_news('智元机器人')
print('Total:', len(results), 'results')
for r in results[:5]:
    print('  - [' + r['date'] + '] ' + r['title'][:50])
    print('    source:', r['source'])
    print('    url:', r['source_url'][:80])

print()
print('=== Test: Figure AI ===')
results2 = c.crawl_google_news('Figure AI humanoid robot')
print('Total:', len(results2), 'results')
for r in results2[:3]:
    print('  - [' + r['date'] + '] ' + r['title'][:60])
    print('    source:', r['source'])
