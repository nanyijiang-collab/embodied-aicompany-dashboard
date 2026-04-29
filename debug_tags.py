with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

tags_pos = [m.start() for m in re.finditer('companyTagsMap', c)]
print('找到companyTagsMap次数:', len(tags_pos))
tp = tags_pos[1]
print('第2个位置前后:', repr(c[tp-10:tp+60]))
depth=0; i=tp
while i < len(c):
    if c[i] == '{': depth += 1
    elif c[i] == '}':
        depth -= 1
        if depth == 0: break
    i += 1
tags_body = c[tp:i]
print('TagsMap总长:', len(tags_body))
print('前500字符:')
print(tags_body[:500])
print('后100字符:')
print(tags_body[-100:])
# 用不同引号规则匹配
keys_sq = re.findall(r"'([^']+)':", tags_body)
keys_dq = re.findall(r'"([^"]+)":', tags_body)
print('单引号key数:', len(keys_sq), '样例:', keys_sq[:3])
print('双引号key数:', len(keys_dq), '样例:', keys_dq[:3])
