import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取rankingData中的公司
matches = re.findall(r"company: '([^']+)'", content)
print(f'rankingData中的公司数量: {len(matches)}')
print('\n公司列表:')
for i, c in enumerate(matches, 1):
    print(f'{i:2d}. {c}')
