# Weekly Reddit Report Schema

Use this structure for production weekly jewelry Reddit reports. The report must align with the post intelligence workbook and should not treat Reddit popularity as research value by itself.

## Core Principles

- Reports must be evidence-led and traceable to the Excel workbook.
- Use Chinese section titles and Chinese analysis for the China team.
- Prioritize posts with `首饰相关性 >= 4`, `重要性分数 >= 70` or at least B-tier, and clear complaint/advice/purchase intent.
- Do not cite generic high-upvote posts unless they are explicitly jewelry, accessory, capsule-jewelry, travel-jewelry, or workwear-accessory related.
- Separate user pain from SUIJI opportunity. Do not imply SUIJI can solve every pain.
- For any reply recommendation, include subreddit rule awareness and reply risk.
- If comments were not fetched, state that the report is based on post-level data only.

## 1. 本周结论

Include:

- Collection window
- Whether the canary, core batch, and extended batch were completed
- Total posts collected
- Total A-tier posts in workbook
- Strongest verified pain cluster
- Strongest SUIJI opportunity
- One recommended team action

Keep this section short and decisive.

## 2. 数据覆盖与限制

Include:

- Subreddit list and count
- Endpoint types: `new`, `top/week`, keyword search, comments if included
- Date range
- Total posts collected
- Whether subreddit rules were fetched
- Whether subreddit metadata included `about.json`, Sidebar Subscriber Info, page weekly active users, and page weekly contributions
- Workbook path
- Raw JSON path
- Collection failures, if any
- Data quality rating

Limitations must explicitly mention:

- Whether comments were fetched
- Whether all 18 communities were covered, or only the core batch was covered because of 403/429 collection risk
- Whether rules were fetched or only summarized
- Whether page-level subreddit metadata failed because of verification, SSL, proxy, timeout, or blocking
- That automated labels/scores are for first-pass triage and require human spot-checking

Do not generate a full product insight report if the collection did not meet the minimum useful threshold.

## 3. 关键痛点 Top 5

Choose pain clusters from the workbook, not from intuition. For each cluster include:

- Pain cluster name in Chinese
- Why it matters
- User language or short paraphrase
- Representative posts
- Current workaround
- SUIJI 可切入点
- SUIJI 不能解决/不能承诺的部分
- Follow-up validation question

Representative posts must include:

- Post title
- Subreddit
- Link
- 重要性分数
- 分数区间
- 首饰相关性
- 回复风险
- 建议动作

Common pain clusters to watch:

- 掉色/氧化/镀层磨损
- 皮肤变绿
- 敏感耳/刺激/发炎
- 重量/佩戴不适
- 拆装困难/部件掉落/锁扣信任
- 断裂/维修/松石/松扣
- 材质认知混乱：gold plated, gold filled, vermeil, sterling silver, titanium, stainless steel
- 职场/婚礼/约会/日常场景造型不确定
- 旅行收纳/缠绕/丢失
- 价格/质量/品牌信任
- 少而精但不能无聊的 capsule/accessory 需求

## 4. 产品机会评分

Score each opportunity from 1-5:

- 用户痛点强度
- 与 SUIJI Grade 5 titanium / Core-Lock / 模块化结构的匹配度
- 潜在付费意愿
- 差异化程度
- 解释难度
- 怀疑风险

For each opportunity, include:

- Opportunity name
- Best supporting posts from workbook
- Why it fits SUIJI
- Key skepticism/risk
- Suggested validation method

## 5. 模块化机会单独分析

Keep separate from the broad pain analysis.

Assess:

- 哪些痛点模块化可能解决
- 哪些痛点模块化不能解决
- Best use cases: office-to-evening, travel, capsule wardrobe, gifting, identity switching
- Likely objections: durability, lost parts, gimmick risk, hygiene, weight, comfort, price, mechanism trust
- Concept-test questions
- Best subreddits for validation

Do not overstate modular demand. If modular/convertible terms are low frequency, say so plainly and position modularity as a solution lens rather than an already-proven user category.

## 6. 高价值帖子清单

Use the workbook's `High Priority` sheet. Include 8-15 posts max.

For each post:

- Title
- Subreddit
- Link
- 重要性分数
- 分数区间
- 首饰相关性
- Reddit 原帖分数 / 评论数
- Pain signal
- Why it matters
- Suggested action
- Reply risk
- Rule-aware note

Do not include generic showcase posts unless they reveal a clear buying, styling, quality, material, or scenario insight.

## 7. 种子用户/可互动对象

For each candidate:

- Username
- Subreddit
- Link
- Pain signal
- Why they are a fit
- Reply risk
- First public interaction suggestion
- Follow-up path
- Risk notes

Prefer public helpful replies before any private outreach. Do not recommend mass DM.

## 8. 产品组痛点分诊

Include this as a separate product-design-facing section or as a separate short report when the output mode requires Product Design Triage.

Only include posts where the workbook field `是否产品组处理` is `是`.

For each cluster or post include:

- 是否首饰类
- 首饰类型
- 产品组痛点类型: 重量、过敏/敏感、佩戴舒适度
- Representative post link
- Subreddit
- 社区规模/活跃上下文: API订阅人数, Sidebar订阅人数, 页面周活跃用户数, 页面周贡献数 when available
- User pain signal
- Why product design should review it
- What product design should judge
- Suggested research question or reply input for operations/founder
- Reply risk and rule caveat

Do not assume product design should directly answer Reddit. Product design gives factual product judgment and questions; operations/founder decides the public community-safe reply.

## 9. 规则感知回复策略

Include:

- Low-risk comments
- Medium/high-risk comments requiring manual review
- Feedback-seeking questions
- Product-discovery questions
- Phrases to avoid
- Disclosure recommendation

For suggested replies:

- Mention the relevant subreddit rule summary where available
- Include reply risk: 高/中/低
- Avoid direct selling
- Avoid fake customer framing
- Avoid medical advice
- Use careful material language

Careful material language:

- Good: "我们在研究 Grade 5 titanium，因为很多敏感佩戴者会在意更亲肤、低敏倾向的材质选择。"
- Avoid: "100% 不过敏" or "永不过敏"

## 10. 下周抓取和验证计划

Give 3-7 concrete actions, such as:

- 抓取 high-value posts 的评论
- 回复 3-5 个低风险帖子
- 发一个 soft feedback post
- 增加/删除关键词
- 对某个 subreddit 做规则复核
- 做一个 Core-Lock 信任问题概念测试
- 做一个旅行/capsule jewelry 轻量化概念测试

## Daily Rising Summary

When producing a daily report, use the `Daily Rising` sheet instead of the weekly report structure.

Include:

- Date and collection window
- Subreddits covered
- Total rising/new posts reviewed
- Top posts by `是否建议今天处理 = 是`
- Posts with high score velocity or comment velocity
- Reply risk and suggested same-day action
- Any subreddit rules requiring manual review
- Any product-design-flagged rising posts, with `是否首饰类` and `首饰类型`

Daily rising output is operational and should not be treated as a full strategic insight report.

## 11. 附录

Include:

- Excel workbook path
- Raw data path
- Rules data path
- Date generated
- Exact subreddit count and list
- Any caveats about local proxy, API method, or missing comments
