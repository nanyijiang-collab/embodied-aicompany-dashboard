# 具身智能媒体监测系统

## 项目目标
为具身智能创业公司CMO搭建自动化媒体监测看板，跟踪：
1. 投融资动态
2. PR发布（官方渠道 + 媒体报道）
3. 产品/技术进展

## 公司库

### 海外 - 通用具身大模型（VLA/世界模型）
| 公司 | 核心产品 | 官网 |
|------|----------|------|
| NVIDIA | GR00T + Isaac平台 | nvidia.com |
| Physical Intelligence (PI) | π模型 | physicalintelligence.ai |
| Skild AI | Skild Brain | skildai.com |
| Figure AI | Figure 03 | figure.ai |
| Agility Robotics | Digit | agilityrobotics.com |
| Apptronik | Apollo | apptronik.com |
| Field AI | 风险感知大模型 | fieldai.com |
| Sanctuary AI | Phoenix | sanctuary.ai |

### 海外 - 其他
| 公司 | 核心产品 | 官网 |
|------|----------|------|
| 1X Technologies (挪威) | EVE模型 | 1x.tech |
| Boston Dynamics (美国) | Atlas工业版 | bostondynamics.com |
| Mimic Robotics (瑞士) | 模仿学习算法 | mimicrobotics.com |
| Anybotics (瑞士) | 四足工业巡检 | anybotics.com |
| Hexagon (瑞典) | 工业感知+控制 | hexagon.com |
| Skydio (美国) | 自主导航AI | skydio.com |

### 国内 - 通用具身大模型（VLA/世界模型）
千寻智能、银河通用、自变量机器人、智元机器人、魔法原子、星海图、智平方、它石智航、跨维智能、穹彻智能

### 国内 - 控制大脑
星动纪元、思灵机器人、逐际动力、灵初智能、大晓机器人、梅卡曼德、傅利叶智能、七腾机器人、珞石机器人、镜识科技、优理奇智能、加速进化、帕西尼感知、地瓜机器人、觅蜂科技

## 数据源
- 微信公众号（官方PR）
- 公司官网（中英文）
- 英文主流科技媒体
- 国内科技媒体

## 展示形态
网页看板

## 需求确认

### 数据抓取方案
- 微信PR：公众号名称搜索
- 官网PR：网页抓取
- 英文媒体：TechCrunch、Wired、The Verge等
- 融资数据：详细信息（金额、投资方、估值）

### PR分类
- 产品发布
- 技术突破/开源
- 项目落地/合作
- 活动/展会
- 采访/观点
- 其他

### 更新频率
- 每周一自动更新
- 手动刷新按钮（随时可点）

## 状态
✅ 看板原型已完成
✅ 低成本爬虫方案（零Token消耗）
✅ 英文标题翻译显示
✅ 新公司探测器功能
✅ 估值排行货币换算
✅ 真实新闻链接

## 新功能

### 英文标题翻译
- 事件标题如果是英文的，会用小字斜体显示原文
- 字段：`title_en`

### 新公司探测器
- 自动发现疑似具身智能新公司
- 展示面板：`data/potential_companies.json`
- 一键添加：点击"添加到监测"即可，无需分类

### 估值排行
- 自动将美元换算为人民币（汇率7.2）
- 统一按亿人民币排序
- 显示货币符号区分：💵美元 / 💴人民币

## 文件结构
- `index.html` - 网页看板主页面（含新公司探测器UI）
- `scripts/crawler.py` - 爬虫脚本（含新公司探测器类）
- `data/events.json` - 事件数据
- `data/potential_companies.json` - 潜在新公司数据
- `data/crawl_state.json` - 爬虫状态（增量更新用）

## 下一步
1. GitHub + Vercel 部署（已完成Git初始化）
2. 设置每周自动化任务
3. 接入真实数据源（36Kr/机器之心API）

## 待完成：GitHub部署

## 已完成：链接验证模块
- `scripts/crawler.py` 已集成 LinkValidator 类
- 验证规则：
  1. 首页链接检测（如 nvidia.com 而非具体文章）
  2. 已知假域名过滤（starmotion.ai、fulani.cn等）
  3. 可信来源自动通过（36kr、TechCrunch等）
  4. HTTP状态码验证
- 命令：`python scripts/crawler.py --validate`（仅验证）
- 爬虫保存时自动验证：`python scripts/crawler.py`
- GitHub账号：nanyijiang-collab
- 待创建仓库：embodied-ai-dashboard
- 待执行推送命令：
  ```
  git remote add origin https://github.com/nanyijiang-collab/embodied-ai-dashboard.git
  git push -u origin main
  ```
- 然后在 Vercel 导入仓库部署
