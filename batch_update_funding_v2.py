#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新 company.html 中的融资表格"""

import re

# 从 generated_funding.py 读取融资数据
exec(open('generated_funding.py', encoding='utf-8').read().replace('generated_funding = ', ''))

def update_company_html():
    with open('company.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_count = 0
    not_found = []
    
    for company_name, funding_info in generated_funding.items():
        # 查找简单映射模式: '公司名': { name: '公司名', nameEn: 'xxx' }
        # 需要替换为包含 fundingTable 的完整定义
        
        # 模式1: '星海图': { name: '星海图', nameEn: 'StellarSea' }
        pattern1 = rf"('{company_name}':\s*\{{\s*name:\s*'{company_name}'"
        
        match = re.search(pattern1, content)
        if match:
            # 找到简单映射，尝试匹配到对应的 }
            start = match.start()
            
            # 找到这行的结束位置
            line_end = content.find('\n', start)
            if line_end == -1:
                line_end = len(content)
            
            # 提取整行内容
            old_line = content[start:line_end]
            
            # 检查是否已有 fundingTable（避免重复添加）
            if 'fundingTable' not in old_line:
                # 构建新行 - 保留 name 和 nameEn，添加融资信息
                name_match = re.search(r"nameEn:\s*'([^']+)'", old_line)
                name_en = name_match.group(1) if name_match else company_name
                
                new_line = f"'{company_name}': {{ name: '{company_name}', nameEn: '{name_en}', {funding_info}"
                
                content = content[:start] + new_line + content[line_end:]
                updated_count += 1
                print(f"✓ 已更新: {company_name}")
            else:
                print(f"- 已有融资表格: {company_name}")
        else:
            # 检查是否是完整定义但没有 fundingTable
            if company_name in content:
                if 'fundingTable' in generated_funding.get(company_name, ''):
                    print(f"? 需要手动检查: {company_name} (可能已有定义)")
                else:
                    not_found.append(company_name)
            else:
                not_found.append(company_name)
    
    # 保存更新后的内容
    with open('company.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n=== 更新完成 ===")
    print(f"成功更新: {updated_count} 家公司")
    if not_found:
        print(f"未找到: {len(not_found)} 家")
        for name in not_found[:10]:
            print(f"  - {name}")
        if len(not_found) > 10:
            print(f"  ... 还有 {len(not_found) - 10} 家")

if __name__ == '__main__':
    update_company_html()
