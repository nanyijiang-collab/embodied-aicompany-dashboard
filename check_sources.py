# -*- coding: utf-8 -*-
import json

d = json.load(open('data/events.json', encoding='utf-8'))
wechat = [e for e in d if '微信' in e.get('source','')]
direct = [e for e in d if not '微信' in e.get('source','') and e.get('source_url','')]

print(f'微信来源事件: {len(wechat)}')
print(f'直链来源事件: {len(direct)}')

# 检查微信链接格式
wechat_sogou = [e for e in wechat if 'weixin.sogou.com' in e.get('source_url','')]
wechat_mp = [e for e in wechat if 'mp.weixin.qq.com' in e.get('source_url','')]
print(f'  - 搜狗跳转: {len(wechat_sogou)}')
print(f'  - 微信直链: {len(wechat_mp)}')

print('\n直链来源示例:')
for e in direct[:5]:
    print(f'  [{e.get("source","")}] {e.get("title","")[:40]}')
    print(f'    URL: {e.get("source_url","")[:60]}...')
