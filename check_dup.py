# -*- coding: utf-8 -*-
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

d = json.load(open('data/events.json', encoding='utf-8'))

# 按标题+source_url去重，统计剩余
seen_titles = {}
dupes = []
for e in d:
    key = (e.get('title', ''), e.get('source', ''), e.get('source_url', ''))
    if key in seen_titles:
        dupes.append(e['id'])
    else:
        seen_titles[key] = e

print('Total events:', len(d))
print('Duplicate entries:', len(dupes))
print('After dedup:', len(seen_titles))

# 找同一标题不同来源的（转载）
title_sources = {}
for e in d:
    t = e.get('title', '')
    s = e.get('source', '')
    if t not in title_sources:
        title_sources[t] = []
    if s not in title_sources[t]:
        title_sources[t].append(s)

multi_source = [(t, srcs) for t, srcs in title_sources.items() if len(srcs) > 1]
print()
print('Same title from multiple sources:', len(multi_source))
for t, srcs in multi_source[:5]:
    print('  Title:', t[:60])
    print('  Sources:', srcs)
    print()
