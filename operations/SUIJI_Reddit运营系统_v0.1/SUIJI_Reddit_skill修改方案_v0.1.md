# reddit-jewelry-research skill 修改方案 v0.1

## 修改目标

把 `reddit-jewelry-research` 从“研究报告 + 工作簿生成”升级为：

1. 每周 research 仍然稳定产出。
2. 每日运营队列能直接给团队执行。
3. 团队打卡、专家任务、种子用户 CRM 和知识库回写形成闭环。

## 当前保留

必须保留：

- `weekly`
- `daily_rising`
- `reply_assignment_2day`
- `reply_pack`
- broad jewelry pain points 优先
- modular/convertible jewelry 作为 secondary lens
- staged collection
- Feishu delivery
- subreddit metadata
- workbook + master database strategy

## 当前需要调整

### 1. 增加 `ops_system` 模式

用途：

- 创建或更新 SOP。
- 创建运营工作台模板。
- 输出团队配置和 Feishu 文件结构。

输出：

- SOP 文档
- 每日运营制度
- 周报制度
- 工作台 workbook
- Feishu index

### 2. 重命名 `seed_ops_daily` 的措辞

现在文案中有 `account-warming tasks` 和 `普通养号任务`。建议统一改为：

- `community_participation_daily`
- 中文：`普通社区参与任务`

原因：

- “养号”容易让团队理解成刷 karma 或机制化账号操作。
- Reddit 官方反垃圾政策明确不鼓励为了曝光或 karma 进行重复行为。

### 3. 明确每日输出结构

每日应该输出：

- `今日优先队列`
- `普通社区参与任务`
- `专家任务`
- `团队打卡`
- `风险记录`
- `种子用户CRM`
- `知识库回写`
- `字段说明`

### 4. 明确周报输出结构

每周报告要拆成两个层级：

- 面向决策的中文周报。
- 面向执行的工作簿。

周报必须回答：

- 本周用户痛点是什么？
- 本周社区表现如何？
- 哪些帖子/评论结构值得学习？
- 有哪些种子用户候选？
- 下周团队该优先做什么？
- 哪些内容需要回写知识库？

### 5. 增加 `knowledge_backlog` 规则

每次 weekly、daily 或 reply_pack 输出后，都要给出知识库回写建议：

- 新痛点 -> `首饰知识卡` 或 `Reddit 证据库`
- 新社区 -> `Subreddit 社区库`
- 新高赞结构 -> `高赞内容结构库`
- 专家表达 -> `专家输入区`
- 风险案例 -> `风险记录`
- 种子用户 -> `种子用户CRM`

### 6. 增加团队配置

默认团队：

- 1 位首饰专家
- 5 位普通成员
- 1 位运营负责人/创始人
- Codex/AI

skill 应该在每日表里允许 `建议负责人`，但不硬编码真实姓名。

### 7. 增加合规 reference

新增：

`references/reddit_compliance.md`

内容包括：

- Reddit 反垃圾政策摘要
- Reddit User Actions 摘要
- Reddit Pro organic playbook 摘要
- SUIJI 团队红线
- 评论前检查清单

## 推荐最终模式

`reddit-jewelry-research` 最终建议保留这些模式：

- `ops_system`
- `weekly`
- `daily_ops`
- `reply_assignment_2day`
- `weekly_ops_review`
- `team_checkin`
- `reply_pack`

兼容旧模式：

- `daily_rising` 继续支持，但应映射到 `daily_ops` 的数据采集部分。
- `seed_ops_daily` 继续支持，但文案上改为普通社区参与，不再使用“养号”。

## 每周自动化建议

每周五或周日输出：

- `SUIJI Reddit 周报 YYYY-MM-DD`
- `SUIJI Reddit 周报工作簿 YYYY-MM-DD`
- `知识库回写清单`
- `下周运营优先级`

## 每日自动化建议

每天上午输出：

- `SUIJI Reddit 每日运营打卡 YYYY-MM-DD`
- 今日 P0/P1 队列
- 专家任务
- 风险提醒

## 人工部分

人必须做：

- 看帖。
- 判断是否评论。
- 手动发评论/发帖。
- 填打卡。
- 判断是否继续跟进用户。

AI 可以做：

- 抓取。
- 筛选。
- 评分。
- 起草。
- 汇总。
- 建表。
- 提醒风险。
