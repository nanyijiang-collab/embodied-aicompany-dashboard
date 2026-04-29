# -*- coding: utf-8 -*-
import re

# Read both files
with open('companies.html', 'r', encoding='utf-8') as f:
    html_companies = f.read()

with open('company.html', 'r', encoding='utf-8') as f:
    html_company = f.read()

# 1. companies.html company names
names_html = re.findall(r'name\s*:\s*"([^"]+)"', html_companies)
print(f'companies.html: {len(names_html)} 家公司')

# 2. rankingData
ranking_match = re.search(r'const rankingData = \[(.*?)\];', html_company, re.DOTALL)
ranking_companies = re.findall(r"company: '([^']+)'", ranking_match.group(1))
print(f'rankingData: {len(ranking_companies)} 家公司')

# 3. getCompanyInfo companies object
companies_match = re.search(r"const companies = \{(.*?)\n\t\t\};", html_company, re.DOTALL)
companies_keys = re.findall(r"'\s*([^']+)\s*':", companies_match.group(1)) if companies_match else []
print(f'getCompanyInfo companies: {len(companies_keys)} 家公司')

# 4. companyTagsMap
tags_match = re.search(r'const companyTagsMap = \{(.*?)\n        \};', html_company, re.DOTALL)
tags_keys = re.findall(r"'\s*([^']+)\s*':", tags_match.group(1)) if tags_match else []
print(f'companyTagsMap: {len(tags_keys)} 家公司')

print()
print('=== companies.html 公司 → 匹配结果 ===')
problems = []
for name in names_html:
    cn = re.split(r'\s*[\(（]', name)[0].strip()

    matched_ranking = None
    for rc in ranking_companies:
        if rc == cn or rc == name:
            matched_ranking = ('rankingData精确', rc); break
        elif cn in rc or rc in cn:
            matched_ranking = ('rankingData包含', rc); break

    matched_companies = None
    for ck in companies_keys:
        if ck == cn or ck == name:
            matched_companies = ('companies精确', ck); break
        elif cn in ck or ck in cn:
            matched_companies = ('companies包含', ck); break

    matched_tags = None
    for tk in tags_keys:
        if tk == cn or tk == name:
            matched_tags = ('tagsMap精确', tk); break
        elif cn in tk or tk in cn:
            matched_tags = ('tagsMap包含', tk); break

    has_basic = matched_ranking or matched_companies
    status = 'OK' if has_basic else 'MISS'
    detail = []
    if matched_ranking: detail.append(f'rankingData="{matched_ranking[1]}"')
    if matched_companies: detail.append(f'companies="{matched_companies[1]}"')
    if matched_tags and not has_basic: detail.append(f'仅tags="{matched_tags[1]}"')

    if not has_basic:
        problems.append((name, detail))

    print(f'  [{status}] {name}')
    if detail:
        print(f'      -> {", ".join(detail)}')

print(f'\nWARNING: {len(problems)} 家没有 rankingData 或详细数据：')
for name, detail in problems:
    print(f'  - {name}')
    for d in detail:
        print(f'    {d}')
