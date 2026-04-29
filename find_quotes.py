# -*- coding: utf-8 -*-
with open('companies.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if '\u201c' in line or '\u201d' in line:  # 中文引号
        print(f'L{i}: {line.rstrip()}')
