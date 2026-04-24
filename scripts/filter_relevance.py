#!/usr/bin/env python3
"""
新闻相关性过滤脚本 - 使用豆包大模型判断新闻是否与具身智能相关
"""
import json
import requests
import time
from tqdm import tqdm

# 豆包 API 配置
API_BASE = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
MODEL = "doubao-pro-32k"

# 具身智能相关性判断系统提示
SYSTEM_PROMPT = """请判断以下新闻是否与"具身智能"（Embodied AI）领域相关。

具身智能相关领域包括：
- 人形机器人（Figure 01/02/03, Tesla Optimus, 宇树H1, 智元机器人, 银河通用等）
- 机器人操作系统、VLA（视觉-语言-动作）模型
- 工业机器人、服务机器人、四足机器人
- 机器人感知、控制、规划、导航技术
- 机器人与AI大模型的结合应用
- 具身智能相关的投融资、并购、战略合作
- 机器人相关学术研究、技术突破、开源

不相关领域包括：
- 纯AI/LLM大模型新闻（不涉及具身）
- GPU/CPU芯片发布、显卡评测（不涉及机器人应用）
- 自动驾驶/ Robotaxi（除非明确提到人形机器人）
- 互联网、科技公司财报分析
- 地缘政治、芯片出口管制新闻

请只回答"相关"或"不相关"，不要解释。
"""

def call_doubao_api(title, api_key):
    """调用豆包大模型API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"新闻标题：{title}"}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(API_BASE, headers=headers, json=data, timeout=30)
        result = response.json()

        if 'choices' in result:
            answer = result['choices'][0]['message']['content'].strip()
            return "相关" in answer
        else:
            print(f"API Error: {result}")
            return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None


def filter_news(api_key):
    """过滤新闻"""
    with open('data/events.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"总新闻数: {len(data)}")
    print("开始大模型过滤...\n")

    # 逐条判断
    relevant_count = 0
    irrelevant_count = 0
    error_count = 0

    for i, event in enumerate(tqdm(data, desc="过滤中")):
        title = event.get('title', '')

        # 跳过已有判断的
        if event.get('is_relevant') is not None:
            if event.get('is_relevant'):
                relevant_count += 1
            else:
                irrelevant_count += 1
            continue

        result = call_doubao_api(title, api_key)

        if result is None:
            error_count += 1
        elif result:
            relevant_count += 1
        else:
            irrelevant_count += 1
            event['is_relevant'] = False
        # 相关 = is_relevant=True 或 None（默认）

        # 控制请求频率
        time.sleep(0.3)

        # 每100条保存一次
        if (i + 1) % 100 == 0:
            with open('data/events.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    # 最终保存
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n=== 过滤结果 ===")
    print(f"相关: {relevant_count}")
    print(f"不相关: {irrelevant_count}")
    print(f"错误: {error_count}")

    # 列出不相关的新闻
    print("\n=== 不相关新闻示例 ===")
    count = 0
    for e in data:
        if e.get('is_relevant') == False and count < 20:
            print(f"  [{e.get('company')}] {e.get('title')[:50]}")
            count += 1


def main():
    import sys

    if len(sys.argv) < 2:
        print("=" * 50)
        print("豆包大模型新闻过滤脚本")
        print("=" * 50)
        print("\n使用方法:")
        print("  python filter_relevance.py <你的豆包API-Key>")
        print("\n获取API Key:")
        print("  1. 访问 https://console.volcengine.com/ark")
        print("  2. 注册/登录火山引擎账号")
        print("  3. 进入 ARK → API Key 管理")
        print("  4. 创建密钥并复制")
        print("\n免费额度:")
        print("  新用户有免费Tokens额度")
        print("  价格便宜：约 0.3元/百万Tokens")
        return

    api_key = sys.argv[1]
    filter_news(api_key)


if __name__ == "__main__":
    main()
