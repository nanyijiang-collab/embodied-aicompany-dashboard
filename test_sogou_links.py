# -*- coding: utf-8 -*-
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# 从数据中取几个搜狗链接测试
import json
d = json.load(open('data/events.json', encoding='utf-8'))
sogou_links = list(set([e.get('source_url', '') for e in d if 'weixin.sogou.com/link' in e.get('source_url', '')]))[:3]

print(f'测试 {len(sogou_links)} 个搜狗链接...\n')

for i, url in enumerate(sogou_links):
    try:
        resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        final_url = resp.url
        is_wechat = 'mp.weixin.qq.com' in final_url
        is_sogou = 'weixin.sogou.com' in final_url
        domain = final_url.split('/')[2] if '://' in final_url else final_url
        
        print(f'链接{i+1}:')
        print(f'  原始: {url[:60]}...')
        print(f'  最终: {final_url[:70]}...')
        print(f'  状态: {resp.status_code}')
        print(f'  域名: {domain}')
        print(f'  最终是微信: {is_wechat}')
        print(f'  最终是搜狗: {is_sogou}')
        print()
    except Exception as e:
        print(f'错误: {e}\n')
    time.sleep(1)
