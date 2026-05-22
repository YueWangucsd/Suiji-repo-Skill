# Post Intelligence Workbook Schema

Create a date-stamped weekly snapshot workbook for every production weekly Reddit run. Create Daily Rising as a separate daily-mode workbook, not as a required sheet in the weekly workbook. When a cumulative master database exists, append unique weekly posts to it after generating the weekly snapshot.

## Workbook Layers

Use two layers:

1. Weekly snapshot workbook.
   - One file per week.
   - Tied to that week's report, raw data, scoring rules, and coverage.
   - Best for weekly review and traceability.

2. Cumulative master post database.
   - One long-running table across weeks.
   - Append unique posts from weekly snapshots.
   - Deduplicate by Reddit post ID first, then permalink.
   - Best for trend analysis, seed-user tracking, and later Feishu Bitable migration.

Do not overwrite historical rows in the cumulative master unless the user explicitly asks for a re-score or cleanup.

## Sheets

- `Overview`: first sheet. Explain what this workbook is, the recommended reading order, which sheet each team should use, and the biggest limitations of the run.
- `Action Queue`: short operational table for what to review or reply to first. This is the main sheet for the founder/operations workflow.
- `Posts`: every crawled post, sorted by `Importance Score` descending. Enable filters and freeze the header row.
- `High Priority`: focused A-tier table. Keep it readable; do not simply clone every full `Posts` column unless needed for traceability.
- `Product Design`: focused product-team table. Include only product-design-routed rows and product-relevant fields.
- `Daily Rising`: daily-mode sheet for a separate daily workbook, with rising/new posts, post age, score velocity, comment velocity, and whether to handle today.
- `Subreddit Rules`: covered subreddit, rules URL, rule summary, rule count, and manual-review status.
- `Tag Dictionary`: definitions for every pain cluster, intent tag, product fit tag, reply risk, and recommended action.
- `Column Guide`: Chinese field dictionary. For each important column, explain what it means, why it matters, who should use it, and how to filter/read it.
- `Scoring Guide`: Chinese explanation of workbook usage, score meanings, score bands, and ranking logic.
- `Coverage`: run metadata, subreddit list, query list, endpoint types, limitations, raw input file path.

## Weekly Workbook Layout Rules

The weekly workbook must be readable as a team artifact, not just a raw database export.

- Keep `Overview`, `Action Queue`, `High Priority`, and focused review sheets before `Posts`.
- Use compact data rows by default. Do not enable automatic text wrapping for every data cell in `Posts`, `Action Queue`, `High Priority`, or `Product Design`; it makes Excel and Feishu expand rows into unreadable blocks.
- Freeze headers and useful left-side columns. Suggested freezes: `Action Queue` and `High Priority` at `F2`, `Product Design` at `E2`, and `Posts` at `J2`.
- Use fixed row heights: about 18px for `Posts`, 22px for action/review sheets, and 24px for guide/reference sheets.
- Keep filters enabled on every table sheet.
- Preserve low-frequency metadata in `Posts`, but hide secondary metadata columns by default when they are not needed for first-pass review.

## Human Reading Order

Use this order in the `Overview` sheet and in final run summaries:

1. `Overview`: understand what was collected, what changed, and known limitations.
2. `Action Queue`: decide what to review, reply to, send to product design, or ignore.
3. `Product Design`: product team reviews weight, allergy/sensitivity, and wearing comfort posts.
4. `High Priority`: founder/researcher scans A-tier evidence for weekly insights and seed-user opportunities.
5. `Posts`: full traceable database for filtering and deeper checks.
6. `Column Guide` and `Scoring Guide`: explain fields and scoring when the team is confused.

## Reply Priority Rules

Do not make users guess whether to reply to `rising` or `new`.

- `rising` comes first when the post is jewelry-related, A/B-tier, low or medium risk, and has a clear question, complaint, or purchase-research signal.
- `new` comes second. Treat it as early monitoring unless it is highly relevant, low-risk, and clearly asks for help.
- Product-design-routed posts come before public replies when they mention weight, allergy/sensitivity, or wearing comfort. Product design provides facts and questions; operations/founder writes the public reply.
- High-risk posts, medical-adjacent posts, rule-unclear posts, and piercing aftercare posts should be marked for manual review or observation rather than immediate public reply.
- High Reddit Score alone is not enough. Reply priority depends on jewelry relevance, intent, pain clarity, risk, and whether the thread is currently gaining traction.

For the every-2-days reply assignment workbook, do not split by product group or operations group. It is an execution sheet for assigning exact replies.

Recommended action labels:

- `P0 今天优先回复`: low/medium risk, A-tier, reply opportunity clear, usually `rising`.
- `P1 产品组先看`: product-design pain around weight, allergy/sensitivity, or wearing comfort.
- `P2 本周准备回复`: useful A/B-tier posts that are not urgent.
- `P3 收藏观察`: useful for insight but not ready for reply.
- `P4 暂不公开回复`: high-risk, weak relevance, rule-unclear, or not worth engagement.

## Every-2-Days Reply Assignment Workbook

Use this mode when the user asks for the every-2-days reply table or automation.

This workbook must be intentionally small. It should contain only:

- `待回复`
- `已处理`
- `字段说明`

`待回复` must have exactly these 12 default columns:

- `优先级`
- `问题类型`
- `Subreddit`
- `帖子标题`
- `原帖链接`
- `建议回复位置`
- `建议动作`
- `负责人名`
- `是否回复`
- `实际回复类型`
- `回复内容`
- `备注`

Allowed values:

- `建议回复位置`: `帖子回复`, `评论回复`, `both`, `暂不回复`
- `实际回复类型`: `未回复`, `帖子回复`, `评论回复`, `both`, `不回复`
- `是否回复`: `否`, `是`, `不适合回复`, `待复核`

Selection:

- Include high-relevance Rising posts first when they are A/B-tier, have clear pain or advice intent, and are low/medium risk.
- Include high-value high-risk posts only as `待复核` and set `建议回复位置 = 暂不回复`.
- Exclude pure showcase posts, weakly related fashion posts, and high-score posts with no real reply opening.

`已处理` should be populated from the cumulative master database when available, using `是否回复`, `实际回复类型`, `回复内容`, `回复日期`, and `跟进状态` to avoid duplicate replies.

After a human fills `负责人名`, `是否回复`, `实际回复类型`, `回复内容`, or `备注`, sync those fields back into the cumulative master database. Match rows by Reddit post ID when available, otherwise by `原帖链接`.

## Required Posts Columns

Use Chinese headers in the `Posts` and `High Priority` sheets for the China team. Keep `Importance Score`, `Score Band`, and `Reddit Score` concepts, but display them with Chinese-friendly names.

- 排名
- 重要性分数
- 分数区间
- 优先级
- 处理优先级
- 回复顺序建议
- 优先理由
- Subreddit
- Subreddit 分类
- API订阅人数
- Sidebar订阅人数
- 社区成员数
- 社区成员数显示
- 页面周活跃用户数
- 页面周活跃用户数显示
- 页面周贡献数
- 页面周贡献数显示
- 社区当前活跃人数
- 社区当前活跃人数显示
- 社区活跃比例
- 社区规模档位
- 社区活跃度档位
- 页面成员标签
- 页面活跃标签
- 社区数据来源
- 社区数据状态
- 帖子标题
- 帖子链接
- 作者
- 收集日期
- 帖子发布日期
- Reddit 原帖分数
- 评论数
- 帖子年龄（小时）
- 每小时得分
- 每小时评论数
- 首饰相关性
- 来源类型
- 搜索关键词
- 是否首饰类
- 首饰类型
- 痛点标签
- 用户意图标签
- 产品相关标签
- 产品组痛点类型
- 是否产品组处理
- 负责人
- 产品组备注
- 回复归属建议
- 机会类型
- 情绪强度
- 回复机会
- 回复风险
- 种子用户匹配度
- 建议动作
- SUIJI 启发
- Subreddit 规则摘要
- 参考规则和帖子内容的回复建议
- 帖子摘要

## Scoring Guidance

Prioritize posts with clear user pain, complaint/advice/purchase intent, relevance to SUIJI's Grade 5 titanium or Core-Lock structure, strong engagement, and a safe public reply opportunity.

De-rank generic showcase posts, broad non-jewelry posts, and posts where the only relevance is weak keyword overlap.

Use `Reddit Score` / `Reddit 原帖分数` for Reddit-native popularity only. Use `Importance Score` / `重要性分数` for SUIJI research value. `Score Band` / `分数区间` is derived from `Importance Score`: A = 70+, B = 50-69, C = 30-49, D < 30.

All tag values in the workbook should be Chinese for the China team. The `Scoring Guide` sheet must include explicit scoring rules, including every additive rule, cap/downranking rule, and score-band threshold.

## Subreddit Metadata Guidance

Preserve multiple subreddit metadata sources because Reddit exposes different numbers in different places:

- `API订阅人数`: `about.json` `subscribers`.
- `Sidebar订阅人数`: subreddit page `Subscriber Info`, for example `994,828 piercing enthusiasts subscribed`.
- `页面周活跃用户数`: subreddit page header `weekly-active-users`, corresponding to the large visible community activity number such as `681K`.
- `页面周贡献数`: subreddit page header `weekly-contributions`, corresponding to the visible contributing number such as `11K`.
- `页面成员标签`: page header `subscribers-text`, such as `Piercing enthusiasts`.
- `页面活跃标签`: page header `currently-viewing-text`, such as `Enthusiasts contributing`.

If the page returns `Reddit - Please wait for verification`, the collector may complete the lightweight JavaScript challenge and retry. If page metadata still fails because of proxy, SSL, timeout, or blocking, keep the `about.json` values and mark page-derived fields as `未知/待人工补充`. Do not silently substitute one source for another without keeping source/status columns.

## Product Design Routing

Do not use product-vs-operations split in the every-2-days reply assignment workbook.

The `Product Design` sheet must include only posts where `是否产品组处理 = 是`.

Every product-design row must include only the fields the product team needs first:

- `处理优先级`
- `Subreddit`
- `社区规模档位`
- `社区活跃度档位`
- `帖子标题`
- `帖子链接`
- `帖子发布日期`
- `是否首饰类`
- `首饰类型`
- `产品组痛点类型`
- `痛点标签`
- `用户意图标签`
- `负责人`
- `产品组备注`
- `回复归属建议`
- `SUIJI 启发`
- `帖子摘要`
- `参考规则和帖子内容的回复建议`

Use `首饰类型` to distinguish earrings, rings, necklaces, bracelets, piercing jewelry, material/allergy, clasp/structure, wearing comfort, storage/travel, and styling/workwear. Jewelry-related posts can still be routed to operations/founder for public replies; product design primarily provides product facts, design hypotheses, and research questions.

## Daily Rising Workbook

Daily mode should collect `rising` and `new` by default. Add recent keyword-search posts only when the daily run is healthy and deeper daily coverage is needed.

Include:

- focused action columns first, not all `Posts` columns
- `帖子年龄（小时）`
- `每小时得分`
- `每小时评论数`
- `是否建议今天处理`

Use daily rising to identify posts worth quick review or same-day public reply. Do not replace weekly strategic reports with daily rising data.

## Column Guide Requirements

The `Column Guide` sheet is mandatory because the workbook contains many columns.

It must include:

- sheet or context where the column appears
- column name
- plain-Chinese definition
- importance level: `核心`, `高`, `中`, `辅助`
- primary owner: `运营/创始人`, `产品组`, `研究/分析`, or `所有人`
- how to use it: recommended filter, sort, or interpretation

At minimum, explain:

- `处理优先级`
- `回复顺序建议`
- `重要性分数`
- `分数区间`
- `Reddit 原帖分数`
- `Subreddit`
- `社区规模档位`
- `社区活跃度档位`
- `来源类型`
- `首饰相关性`
- `是否首饰类`
- `首饰类型`
- `痛点标签`
- `用户意图标签`
- `产品组痛点类型`
- `是否产品组处理`
- `负责人`
- `回复机会`
- `回复风险`
- `建议动作`
- `参考规则和帖子内容的回复建议`
- `帖子摘要`

## Cumulative Master Database

The cumulative master should preserve all `Posts` columns from the weekly workbook and add operational metadata:

- 首次收集日期
- 最近一次出现日期
- 来源周报
- 来源原始数据
- 跟进负责人
- 跟进状态
- 最后动作日期
- 人工备注

Recommended follow-up statuses:

- 未处理
- 已收藏
- 待人工复核
- 可回复
- 已回复
- 不适合回复
- 已归档

When imported to Feishu, keep the weekly snapshot as a normal Feishu Sheet. Consider migrating only the cumulative master database to Feishu Bitable after the team has 3-4 weeks of data and needs CRM-like tracking.

## Rule Handling

Fetch subreddit rules using `scripts/fetch_reddit_subreddit_rules.py` when possible. For important posts, never invent rules. If rules are missing, set `Subreddit Rules Summary` to `needs manual verification` and make the suggested reply conservative.

## Reply Guidance

Suggested replies should be soft, helpful, and research-oriented. Avoid hard promotion, fake customer framing, medical advice, and absolute material claims such as `100% no allergy`.
