# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
import time

from scripts.crawler import EmbodiedAICrawler

c = EmbodiedAICrawler()
companies = ['智元机器人', '宇树科技', 'Figure AI']

total_new = 0
for name in companies:
    t0 = time.time()
    results = c.crawl_google_news(name)
    t1 = time.time()
    print(f'{name}: {len(results)} articles in {t1-t0:.1f}s')
    total_new += len(results)

print(f'\nTotal: {total_new} articles from 3 companies in {t1-t0:.1f}s')
print('Estimated for all 60+ companies: ~{:.0f} minutes'.format(
    (time.time() - t0) / 3 * 60 / 60 if t0 else 0
))
