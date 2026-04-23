# -*- coding: utf-8 -*-
"""
Link Validator - 链接质量验证模块
功能：
1. 验证链接可访问性
2. 检测假链接/首页链接
3. 检测重复链接
4. 提供修复建议
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
import time
import json
import os

# 已知的高质量新闻源（可信来源，可以直接信任）
TRUSTED_SOURCES = {
    # 国际
    'techcrunch.com', 'theverge.com', 'wired.com', 'arstechnica.com',
    'engadget.com', 'reuters.com', 'bloomberg.com', 'ft.com',
    'nytimes.com', 'wsj.com', 'economist.com',
    # 国内
    '36kr.com', 'jiqizhixin.com', 'qbitai.com', 'ifeng.com',
    'sina.com.cn', 'sohu.com', 'qq.com', '163.com',
    'eastmoney.com', 'cls.cn', 'jiemian.com', 'thepaper.cn',
    '澎湃新闻': 'thepaper.cn', 'pengpai.cn',
    # 官方
    'github.com', 'arxiv.org',
}

# 已知无效/假链接模式
INVALID_PATTERNS = [
    # 空链接或占位符
    r'^#', r'^javascript:', r'^$',
    # 域名根路径（很可能是首页）
    r'://[^/]+/?$',  # 如 https://example.com 或 https://example.com/
    # 常见假链接域名
    'example.com', 'test.com', 'fake.com',
    'placeholder.com', 'sample.com',
]

# 首页链接检测（不包含实际内容路径的URL）
KNOWN_HOME_PAGES = {
    'https://nvidia.com': True,
    'https://www.nvidia.com': True,
    'https://physicalintelligence.ai': True,
    'https://www.physicalintelligence.ai': True,
    'https://skildai.com': True,
    'https://www.skildai.com': True,
    'https://figure.ai': True,
    'https://www.figure.ai': True,
    'https://agilityrobotics.com': True,
    'https://www.agilityrobotics.com': True,
    'https://apptronik.com': True,
    'https://www.apptronik.com': True,
    'https://fieldai.com': True,
    'https://www.fieldai.com': True,
    'https://sanctuary.ai': True,
    'https://www.sanctuary.ai': True,
    'https://1x.tech': True,
    'https://www.1x.tech': True,
    'https://bostondynamics.com': True,
    'https://www.bostondynamics.com': True,
    'https://mimicrobotics.com': True,
    'https://www.mimicrobotics.com': True,
    'https://anybotics.com': True,
    'https://www.anybotics.com': True,
    'https://hexagon.com': True,
    'https://www.hexagon.com': True,
    'https://skydio.com': True,
    'https://www.skydio.com': True,
}


class LinkValidator:
    """链接质量验证器"""

    def __init__(self, timeout: int = 8):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self.timeout = timeout
        self.cache = {}  # URL缓存，避免重复验证

    def is_homepage_url(self, url: str) -> bool:
        """检测是否是首页链接（没有具体内容路径）"""
        # 直接检查已知首页
        if url in KNOWN_HOME_PAGES:
            return True

        parsed = urlparse(url)
        path = parsed.path.strip('/')

        # 如果路径为空或只有单个单词（可能是公司缩写），认为是首页
        if not path:
            return True

        # 常见首页路径
        homepage_patterns = ['', 'index', 'index.html', 'index.htm', 'home', 'default', 'main']
        if path.lower() in homepage_patterns:
            return True

        return False

    def is_trusted_source(self, url: str) -> bool:
        """检查是否是可信来源"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # 移除www前缀后比较
        if domain.startswith('www.'):
            domain = domain[4:]

        return domain in TRUSTED_SOURCES

    def validate_single(self, url: str, company_name: str = '') -> Dict:
        """验证单个链接"""
        if not url:
            return {
                'valid': False,
                'url': url,
                'reason': '空链接',
                'fix_suggestion': '需要提供真实新闻链接'
            }

        # 检查缓存
        if url in self.cache:
            return self.cache[url]

        result = {
            'url': url,
            'valid': True,
            'reason': '',
            'fix_suggestion': '',
            'status_code': None,
            'is_trusted': self.is_trusted_source(url),
            'is_homepage': False
        }

        # 1. 检查是否是首页链接
        if self.is_homepage_url(url):
            result['valid'] = False
            result['reason'] = '链接指向首页，无具体内容'
            result['is_homepage'] = True
            result['fix_suggestion'] = '需要找到该公司的具体新闻文章链接'
            self.cache[url] = result
            return result

        # 2. 检查是否是不存在的已知假域名
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        fake_domains = ['starmotion.ai', 'fulani.cn', 'zibii.com', 'yolo.ai', 'mifeng.com']
        if any(fake in domain for fake in fake_domains):
            result['valid'] = False
            result['reason'] = '域名不存在或为假链接'
            result['fix_suggestion'] = f'请搜索"{company_name}"的真实新闻链接'
            self.cache[url] = result
            return result

        # 3. 如果是可信来源，跳过HTTP验证（节省时间）
        if result['is_trusted']:
            result['reason'] = '可信来源，直接通过'
            self.cache[url] = result
            return result

        # 4. HTTP验证（非可信来源）
        try:
            resp = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            result['status_code'] = resp.status_code

            if resp.status_code >= 400:
                result['valid'] = False
                result['reason'] = f'HTTP错误: {resp.status_code}'
                result['fix_suggestion'] = f'链接已失效，请搜索"{company_name}"的新闻链接'

            time.sleep(0.3)  # 避免请求过快

        except requests.exceptions.Timeout:
            result['valid'] = False
            result['reason'] = '请求超时'
            result['fix_suggestion'] = '链接可能已失效，请验证'
        except requests.exceptions.ConnectionError:
            result['valid'] = False
            result['reason'] = '连接失败（域名可能不存在）'
            result['fix_suggestion'] = f'请搜索"{company_name}"的真实新闻链接'
        except Exception as e:
            result['reason'] = f'验证异常: {str(e)[:50]}'

        self.cache[url] = result
        return result

    def validate_batch(self, events: List[Dict], dry_run: bool = True) -> Tuple[List[Dict], Dict]:
        """
        批量验证事件中的链接

        Args:
            events: 事件列表
            dry_run: True=只报告不修改，False=直接修复

        Returns:
            (验证后的列表, 验证报告)
        """
        report = {
            'total': len(events),
            'valid': 0,
            'invalid': 0,
            'duplicates': 0,
            'fixed': 0,
            'invalid_events': []
        }

        seen_urls = {}  # 检测重复链接
        validated_events = []

        for event in events:
            url = event.get('source_url', '')
            company = event.get('company', '')

            # 检查重复链接
            if url in seen_urls:
                dup_info = {
                    'event': event,
                    'original_event': seen_urls[url],
                    'issue': '重复链接'
                }
                report['duplicates'] += 1

                if not dry_run:
                    # 跳过重复
                    continue

            # 验证链接
            validation = self.validate_single(url, company)

            if validation['valid']:
                report['valid'] += 1
                validated_events.append(event)
            else:
                report['invalid'] += 1
                event_copy = event.copy()
                event_copy['link_validation'] = validation
                event_copy['link_valid'] = False
                report['invalid_events'].append(event_copy)

                if not dry_run:
                    # 标记为无效但保留
                    event['link_valid'] = False

            seen_urls[url] = event

        return validated_events, report

    def find_real_news_link(self, company_name: str, event_title: str = '') -> Optional[str]:
        """搜索公司真实新闻链接（用于修复）"""
        try:
            from urllib.parse import quote

            # 搜索查询
            query = f"{company_name} 具身智能 OR 人形机器人 OR 融资 OR 新闻"
            if event_title:
                # 从标题提取关键信息
                keywords = re.findall(r'[\u4e00-\u9fa5]{2,10}?(?:完成|获得|融资|发布)', event_title)
                if keywords:
                    query = f"{company_name} {' '.join(keywords)}"

            search_url = f"https://www.bing.com/news/search?q={quote(query)}"
            resp = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 查找第一个新闻链接
            for item in soup.select('div.news-card a.title')[:5]:
                link = item.get('href', '')
                if link and link.startswith('http') and not self.is_homepage_url(link):
                    # 验证链接
                    validation = self.validate_single(link)
                    if validation['valid']:
                        return link

            time.sleep(1)

        except Exception as e:
            print(f"[WARN] Failed to search news for {company_name}: {e}")

        return None


def validate_and_fix_events(events_file: str, dry_run: bool = True) -> Dict:
    """
    验证并修复事件文件中的链接

    Args:
        events_file: events.json 文件路径
        dry_run: True=只报告不修改

    Returns:
        验证报告
    """
    # 加载数据
    with open(events_file, 'r', encoding='utf-8') as f:
        events = json.load(f)

    print(f"📋 Loaded {len(events)} events")

    validator = LinkValidator()

    # 验证所有链接
    validated_events = []
    report = {
        'total': len(events),
        'valid': 0,
        'invalid': 0,
        'duplicates': 0,
        'needs_fix': []
    }

    seen_urls = {}

    for event in events:
        url = event.get('source_url', '')
        company = event.get('company', '')

        # 1. 检查空链接
        if not url:
            report['invalid'] += 1
            report['needs_fix'].append({
                'event': event,
                'issue': '空链接',
                'suggestion': f'搜索{company}新闻'
            })
            continue

        # 2. 检查重复
        if url in seen_urls:
            report['duplicates'] += 1
            continue
        seen_urls[url] = event

        # 3. 验证链接
        validation = validator.validate_single(url, company)

        if validation['valid']:
            report['valid'] += 1
            validated_events.append(event)
        else:
            report['invalid'] += 1
            report['needs_fix'].append({
                'event': event,
                'issue': validation['reason'],
                'suggestion': validation['fix_suggestion']
            })

    # 打印报告
    print("\n" + "=" * 60)
    print("📊 Link Validation Report")
    print("=" * 60)
    print(f"Total events: {report['total']}")
    print(f"Valid links:  {report['valid']} ✅")
    print(f"Invalid links: {report['invalid']} ❌")
    print(f"Duplicates:   {report['duplicates']}")

    if report['needs_fix']:
        print("\n⚠️  Events with invalid links:")
        for i, item in enumerate(report['needs_fix'][:10], 1):
            print(f"\n{i}. [{item['event'].get('company', 'Unknown')}]")
            print(f"   Title: {item['event'].get('title', '')[:50]}...")
            print(f"   URL: {item['event'].get('source_url', 'N/A')}")
            print(f"   Issue: {item['issue']}")
            print(f"   Fix: {item['suggestion']}")

    # 保存报告
    report_file = os.path.join(os.path.dirname(events_file), 'link_validation_report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 Report saved: {report_file}")

    if not dry_run:
        # 备份原文件
        backup_file = events_file + '.backup'
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        print(f"📦 Backup saved: {backup_file}")

        # 保存修复后的数据
        with open(events_file, 'w', encoding='utf-8') as f:
            json.dump(validated_events, f, ensure_ascii=False, indent=2)
        print(f"✅ Fixed data saved: {events_file}")

    return report


if __name__ == '__main__':
    import sys

    # 获取事件文件路径
    if len(sys.argv) > 1:
        events_file = sys.argv[1]
    else:
        events_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')

    # 验证模式
    dry_run = '--fix' not in sys.argv

    print(f"🔍 Validating: {events_file}")
    print(f"Mode: {'DRY RUN (report only)' if dry_run else 'FIX MODE (will modify file)'}")
    print()

    report = validate_and_fix_events(events_file, dry_run=dry_run)
