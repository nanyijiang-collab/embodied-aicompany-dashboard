# 具身智能媒体监测系统 - 公司管理手册

> 本文档定义添加新公司和更新公司信息的标准化工作流程。

---

## 一、添加新公司到监测列表

当发现一家新的具身智能公司需要添加时，需要执行以下步骤：

### 步骤 1：确认公司信息

收集以下信息：
- [ ] 公司中文名
- [ ] 公司英文名（如有）
- [ ] 总部所在地（国内/海外）
- [ ] 成立时间
- [ ] 创始人/核心团队背景
- [ ] 主营业务/产品
- [ ] 最新融资情况
- [ ] 公司官网（如有）

### 步骤 2：添加到 potential_companies.json

将公司信息添加到 `data/potential_companies.json`：

```json
{
  "name": "公司名",
  "discovered_from": "发现来源（如36Kr文章）",
  "article_title": "相关文章标题",
  "article_url": "相关文章链接",
  "discovered_date": "YYYY-MM-DD",
  "status": "approved",
  "category": "domestic_vla|overseas_humanoid|domestic_control|etc",
  "note": "备注信息（创始人背景、融资情况等）"
}
```

### 步骤 3：创建公司介绍页

在项目根目录创建 `company-{公司名}.html` 或直接在 `company.html` 中添加公司信息。

公司介绍页应包含：
- [ ] 公司基本信息（成立时间、总部、创始人）
- [ ] 核心技术/产品
- [ ] 融资历程
- [ ] 团队关键成员介绍
- [ ] 公司动态/里程碑

### 步骤 4：添加人事动态（可选但推荐）

如果能找到创始人或核心团队的人事背景，在 `scripts/add_personnel.py` 中添加：

```python
{
    "company": "公司名",
    "person_name": "人名",
    "action": "创业|加入|离职|晋升",
    "old_role": "原职位",
    "new_role": "新职位",
    "title": "新闻标题",
    "title_en": "English Title",
    "summary": "事件摘要",
    "source": "来源",
    "source_url": "链接",
    "date": "YYYY-MM-DD"
}
```

然后运行：
```bash
python scripts/add_personnel.py
```

### 步骤 5：更新工作记忆

在 `MEMORY.md` 和当日日记中记录：
- 新增公司名称
- 添加日期
- 信息来源

---

## 二、搜索人事动态的方法

### 数据来源优先级

1. **官方公告**：公司官网、公众号、微博
2. **权威媒体**：36氪、机器人大讲堂、晚点、量子位
3. **企查查/天眼查**：工商变更信息
4. **社交媒体**：创始人Twitter/X、LinkedIn

### 搜索关键词模板

```
# 国内公司
{公司名} 创始人 高管 人事 变动 离职 加入 晋升

# 海外公司
{公司名} CEO CTO founder executive depart join hire
```

### 重点关注的人事变动类型

| 类型 | 说明 |
|------|------|
| 创始人创业 | 从大厂/学术界出来创业 |
| 高管加入 | 从知名公司跳槽加入 |
| 高管离职 | 核心人员离开 |
| 职位晋升 | CTO→CEO等 |
| 团队重组 | 大规模调整 |

---

## 三、公司别名管理

为避免数据分散，需要统一公司名称：

| 别名 | 统一名 |
|------|--------|
| AgiBot, 智元 | 智元机器人 |
| Boston Dynamics, 波士顿动力 | Boston Dynamics |
| Figure, Figure AI | Figure AI |
| PI, Physical Intelligence | Physical Intelligence |
| Galbot, 银河通用 | 银河通用 |

---

## 四、检查清单

### 添加新公司
- [ ] 确认公司名不与其他公司重复
- [ ] 添加到 potential_companies.json
- [ ] 创建/更新公司介绍页
- [ ] 添加创始人/核心团队人事动态
- [ ] 运行 add_personnel.py（如有新增）
- [ ] 更新 index.html 导航（如需要）
- [ ] 更新工作记忆

### 定期维护
- [ ] 每季度检查一次公司信息是否过时
- [ ] 关注公司官网最新公告
- [ ] 更新融资/估值信息
- [ ] 补充新的人事动态

---

## 五、常见问题

### Q: 公司改名了怎么办？
A: 在 index.html 和 company.html 中同时保留新旧名称的链接指向，备注"原XXX公司"。

### Q: 某公司突然有很多新闻但没有详细信息？
A: 先添加到 potential_companies.json 的 pending 列表，后续跟进。

### Q: 如何处理海外公司的中文名？
A: 优先使用公司官方中文名（如有），没有则使用英文名或音译。

---

*最后更新: 2026-04-27*
