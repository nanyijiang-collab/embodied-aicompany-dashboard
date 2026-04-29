# -*- coding: utf-8 -*-
import re, json

# Extract allCompanies names from companies.html
with open('companies.html', 'r', encoding='utf-8') as f:
    html = f.read()

names = re.findall(r'name:"([^"]+)"', html)
print(f'companies.html 共有 {len(names)} 家公司\n')

# Extract rankingData company names from company.html
with open('company.html', 'r', encoding='utf-8') as f:
    company_html = f.read()

ranking_match = re.search(r'const rankingData = \[(.*?)\];', company_html, re.DOTALL)
ranking_companies = re.findall(r"company: '([^']+)'", ranking_match.group(1))
print(f'company.html rankingData 共有 {len(ranking_companies)} 家公司\n')

# Find missing
missing = []
for n in names:
    # Extract the Chinese name (before any parenthesis or English)
    cn_name = re.split(r'\s*[\(（]', n)[0].strip()
    found = False
    for rc in ranking_companies:
        if cn_name == rc or rc in n or n in rc:
            found = True
            break
    if not found:
        missing.append((n, cn_name))

print(f'=== 在 rankingData 中找不到对应条目的公司 ({len(missing)}家) ===')
for name, cn in missing:
    print(f'  companies.html: "{name}"')
    print(f'  尝试匹配: "{cn}"')
    print()
