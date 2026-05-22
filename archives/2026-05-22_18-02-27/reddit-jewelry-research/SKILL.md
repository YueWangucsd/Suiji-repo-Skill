---
name: reddit-jewelry-research
description: Use this skill for weekly or daily Reddit research around broad jewelry user pain points, subreddit discovery, seed-user discovery, reply strategy, Feishu-ready reports, product-design pain triage, subreddit size/activity context, and Excel/Feishu Sheet post intelligence workbooks. The default brand/product context is SUIJI, a demi-fine modular jewelry brand using Grade 5 titanium alloy and a fast Core-Lock detachable structure. Research should prioritize broad jewelry pain points and treat modular or convertible jewelry as a secondary opportunity lens. Use this skill whenever the user asks for SUIJI Reddit reports, Reddit automation, Daily Rising, Feishu delivery, product design team triage, subreddit member/activity metadata, or long-term Reddit post tracking.
---

# Reddit Jewelry Research

Use this skill when the user wants Reddit research for jewelry, jewelry pain points, subreddit mapping, weekly insight reports, seed-user discovery, reply strategy, or a filterable Excel database of crawled posts.

Do not repeatedly ask what the product is. Load `references/product_context.md` when product positioning, brand language, material claims, or reply tone matters.

## Default Scope

Primary scope: broad jewelry user pain points.

Secondary scope: modular or convertible jewelry opportunities.

The modular concept should not narrow the main research. Treat it as a separate opportunity lens after broad jewelry pain points are collected.

## Time Window

Default report window: last 7 days.

The inherited `brand-launch-ops` scraper has two timing mechanisms:

- Reddit ranking window: `top.json?t=week` asks Reddit for that subreddit's weekly top posts.
- Local date filter: `--days 7` filters posts by `created_utc` so only posts from the last 7 days are kept.

Use both for weekly reports unless the user requests a different period.

## Default Delivery

Default document destination: Feishu.

Local files are still generated as temporary working artifacts because Reddit raw data, workbook creation, DOCX creation, and visual verification are more reliable locally. Final user-facing deliverables should be imported or uploaded to Feishu when `lark-cli` is configured and authorized. Use `references/feishu_output.md` for the Feishu folder structure, import/upload strategy, consistency checks, cleanup behavior, index-document behavior, and long-term workbook policy.

Default Feishu structure:

- `Suiji/Reddit`: editable Feishu reports, Feishu Sheets, and index docs.
- `Suiji/Reddit/原始文件备份`: original `.xlsx`, `.docx`, `.md`, and raw data backups when useful.

Do not delete local working artifacts until the Feishu version has passed the consistency gate in `references/feishu_output.md`. If Feishu import/upload or verification fails, keep all local outputs and report the failure reason instead of silently skipping delivery.

## Non-Negotiable Run Contract

Keep this section in the main skill, not only in references. Every run must satisfy it before the final response.

1. Identify the output mode: `weekly`, `daily_rising`, `reply_assignment_2day`, or `reply_pack`.
2. Use the default SUIJI product context without asking again unless the user changes the product.
3. Run collection in stages: canary, core batch, then extended batch only when healthy.
4. Use Reddit links as references for every insight or reply recommendation.
5. Preserve collection limits and failures. Do not invent insights when data is thin.
6. Generate Feishu-ready outputs and verify Feishu/local consistency when Feishu is available.
7. Weekly outputs must include the broad pain report, modular opportunity report, weekly workbook, and master database update.
8. The every-2-days output is a concise reply assignment table, not a product/operations split. It must include only `待回复`, `已处理`, and `字段说明`.
9. Daily Rising and every-2-days reply assignment outputs must make reply priority explicit: handle qualified `rising` posts before ordinary `new` posts; high-risk or rule-unclear posts go to manual review instead of public reply.
10. Never recommend hard selling, fake-user framing, mass DM, medical advice, or absolute claims such as `100% no allergy`.

## Workbook UX Contract

The workbook is a team workflow artifact, not just a database dump.

Required user-facing sheets must appear before full raw/detail sheets:

- `Overview`: what the workbook is, what to look at first, and which team owns which task.
- `Action Queue`: the short operational queue for what to review/reply to first.
- `Product Design` or `产品判断`: only for full weekly analysis if still needed; the every-2-days assignment output must not split product vs operations.
- `Column Guide`: a plain-Chinese field dictionary explaining every important column, why it matters, who uses it, and how to filter it.
- `Scoring Guide`: explicit scoring rules and score-band thresholds.

`Posts` can keep all columns for traceability, but it is not the first place humans should work from. Reports should cite the workbook rows, but the workbook must tell the user which sheet to open first.

Weekly workbooks should read like a workflow file, not a raw export. Keep detail rows compact: fixed row heights, no automatic text wrapping in full database sheets, frozen headers/priority columns, filters enabled, and low-frequency metadata hidden by default while still preserved in the workbook.

For the every-2-days reply assignment workbook, do not include the weekly analysis sheets. It should be a lean execution workbook:

- `待回复`: only the candidates that need assignment or reply review.
- `已处理`: already replied or explicitly not-to-reply records from the master database.
- `字段说明`: how to fill owner, reply status, reply type, reply content, and notes.

## Data Collection

Default method: reuse the `brand-launch-ops` Reddit scraper:

```bash
python3 /Users/a166/.claude/skills/brand-launch-ops/scripts/reddit_scraper.py \
  --subs jewelry Earrings jewelrymaking femalefashionadvice BusinessFashion fashionwomens35 capsulewardrobe HerOneBag piercing BuyItForLife OUTFITS PetiteFashionAdvice Weddingattireapproval minimalism onebag PiercingAdvice jewelers JewelryDesign \
  --days 7 \
  --max-per-sub 50 \
  --output ./reddit-data \
  --project-name "Jewelry Pain Reddit Insights"
```

This method uses Playwright, an optional browser session, and Reddit public `.json` endpoints. It does not use Reddit official API credentials.

If the inherited scraper hangs in a local proxy environment, use the bundled `scripts/reddit_public_json_collect.py` fallback.
When using a local proxy such as COCODUCK, set `HTTP_PROXY` and `HTTPS_PROXY` in the shell and use `--insecure-ssl` only when the local proxy certificate causes Python certificate verification failures.

Do not start production collection with a full 18-community, all-endpoint request burst. Use staged collection:

1. Canary: one subreddit, one lightweight endpoint, no keyword search.
2. Core weekly batch: 8 highest-priority communities.
3. Extended weekly batch: remaining 10 communities only if the canary and core batch are healthy.
4. Daily Rising: separate lightweight workbook using only `rising` and `new`.

Recommended canary:

```bash
python3 scripts/reddit_public_json_collect.py \
  --subs jewelry \
  --days 7 \
  --limit 5 \
  --endpoints new \
  --delay-min 4 \
  --delay-max 8 \
  --stop-after-blocked 2 \
  --output ./reddit-data/canary
```

Recommended core weekly fallback:

```bash
python3 scripts/reddit_public_json_collect.py \
  --subs jewelry Earrings jewelrymaking femalefashionadvice BusinessFashion fashionwomens35 piercing HerOneBag \
  --queries tarnish "green skin" "sensitive ears" "titanium earrings" "office jewelry" "travel jewelry" "modular jewelry" "convertible jewelry" "versatile jewelry" \
  --days 7 \
  --limit 25 \
  --search-limit 8 \
  --endpoints new rising top_week search \
  --delay-min 5 \
  --delay-max 10 \
  --stop-after-blocked 6 \
  --output ./reddit-data/weekly-core
```

Recommended extended weekly fallback, only after the core batch succeeds:

```bash
python3 scripts/reddit_public_json_collect.py \
  --subs capsulewardrobe BuyItForLife OUTFITS PetiteFashionAdvice Weddingattireapproval minimalism onebag PiercingAdvice jewelers JewelryDesign \
  --queries tarnish "green skin" "sensitive ears" "titanium earrings" "office jewelry" "travel jewelry" "modular jewelry" "convertible jewelry" "versatile jewelry" \
  --days 7 \
  --limit 20 \
  --search-limit 6 \
  --endpoints new rising top_week search \
  --delay-min 6 \
  --delay-max 12 \
  --stop-after-blocked 6 \
  --output ./reddit-data/weekly-extended
```

Recommended Daily Rising fallback:

```bash
python3 scripts/reddit_public_json_collect.py \
  --subs jewelry Earrings jewelrymaking femalefashionadvice BusinessFashion fashionwomens35 piercing HerOneBag \
  --days 1 \
  --limit 25 \
  --endpoints rising new \
  --delay-min 5 \
  --delay-max 10 \
  --stop-after-blocked 4 \
  --output ./reddit-data/daily-rising
```

If collection returns too little data, do not invent insights. Output a collection-status report instead.

Minimum useful thresholds:

- 30+ total posts collected, or
- 10+ posts containing jewelry pain keywords, or
- 5+ posts with clear complaints, questions, or purchase intent.

## Workflow

1. Build subreddit map.
   - Start with `references/subreddits.md`.
   - Treat all 18 default communities from `references/subreddits.md` as the full research universe.
   - For collection stability, run the core 8 communities first and the remaining 10 as an extended batch only after the first batch succeeds.
   - Split into primary jewelry, fashion/workwear, pain-point, capsule/travel, and validation communities.
   - Check subreddit rules before suggesting a post or reply.

2. Build keyword map.
   - Start with broad jewelry pain terms from `references/keywords.md`.
   - Keep modular/convertible terms as a separate optional group.

3. Collect data.
   - Use the last 7 days by default.
   - Start every live run with a canary request. If the canary returns 403/429, stop and report collection status instead of starting the full run.
   - Collect the core 8 subreddits first; collect the extended 10 only if the first batch returns useful data and does not trigger repeated 403/429 errors.
   - For weekly reports, collect `new`, `top/week`, and keyword searches when relevant.
   - For daily monitoring, collect only `rising` and `new` by default. Add keyword searches only when the daily run is healthy and the user asks for deeper coverage.
   - Fetch comments only when the user wants deeper thread analysis or reply strategy.
   - Attempt to collect subreddit member/activity metadata weekly. Use both Reddit `about.json` and the subreddit page when practical:
     - `about.json subscribers` becomes `API订阅人数`.
     - Page `Subscriber Info` becomes `Sidebar订阅人数`.
     - Page header `weekly-active-users` becomes `页面周活跃用户数`.
     - Page header `weekly-contributions` becomes `页面周贡献数`.
     - Page labels such as `Piercing enthusiasts` and `Enthusiasts contributing` become the member/activity label fields.
   - These sources may disagree. Preserve all available values, source, status, and fetch time instead of collapsing them into one unexplained number. If page verification, proxy, or SSL issues block page metadata, keep `about.json` values and mark page fields `未知/待人工补充`.
   - Save raw JSON by date.
   - Fetch or verify subreddit rules for high-priority reply candidates before recommending replies.

4. Analyze broad jewelry pain points.
   - Cluster complaints by pain type.
   - Preserve user language with short excerpts and links.
   - Score pain points by frequency, emotional intensity, jewelry relevance, and SUIJI product fit.
   - Separate real complaints from generic showcase posts.
   - For reports, prioritize posts from the workbook with `首饰相关性 >= 4`, `重要性分数 >= 70` or at least B-tier, and clear complaint/advice/purchase intent.
   - Do not use generic high-upvote posts as report evidence unless they are explicitly jewelry/accessory related.

5. Analyze modular opportunity.
   - Identify which broad pain points SUIJI's modular structure, Grade 5 titanium, and Core-Lock mechanism may address.
   - Identify which pain points it does not solve.
   - List likely objections: durability, gimmick risk, hygiene, lost parts, comfort, price, taste mismatch.
   - Suggest concept-test questions.

6. Build reply strategy.
   - Never start with hard selling.
   - Prefer helpful, curious, transparent replies.
   - If posting as founder, designer, or researcher, disclose that.
   - Suggest replies that ask users about pain, tradeoffs, material preference, and use cases.
   - Do not ask the product design team to reply to every jewelry post. Route only material/structure/wearability posts to product design for factual review and follow-up questions.
   - Product design owns posts with real feedback around weight, allergy/sensitivity, and wearing comfort. Operations/founder owns community-friendly public replies after product design provides the product facts or research questions.

7. Build the post intelligence workbook.
   - Create a date-stamped weekly snapshot `.xlsx` file alongside Markdown reports for every weekly run.
   - Maintain or update a cumulative master post database when one exists; append unique posts by Reddit post ID or permalink rather than overwriting history.
   - Include every crawled post, not only posts mentioned in reports.
   - Use `scripts/build_reddit_post_workbook.py` when available.
   - Put `Overview`, `Action Queue`, and focused team sheets before `Posts`.
   - Sort by importance/value descending and enable Excel filters.
   - Keep `Posts` as the complete database, but do not make it the main human workflow surface.
   - Add multi-dimensional labels: pain cluster, intent, product fit, opportunity type, emotional intensity, reply opportunity, reply risk, seed-user fit, and recommended action.
   - Add subreddit context columns: API subscriber count, Sidebar subscriber count, page weekly active users, page weekly contributions, page member/activity labels, best-available member count, active ratio, size band, activity band, data source, and metadata status.
   - Add product design routing columns: whether the post is jewelry-related, jewelry type, product design pain type, whether product design should handle, owner, product design notes, and reply ownership guidance.
   - Add `Column Guide` explaining what every field means, why it matters, who should use it, and how to filter it.
   - Add `Action Queue` explaining whether to reply now, send to product design first, observe, or avoid public reply.
   - In reply prioritization, qualified `rising` posts come before ordinary `new` posts because they are gaining traction now. `new` posts are watched or answered only when they are highly relevant and low-risk.
   - For important posts, include subreddit rules and a rule-aware suggested reply.
   - If subreddit rules could not be fetched, mark the rule column as `needs manual verification` instead of guessing.
   - In daily mode, include `Daily Rising`: rising/new posts with post age, score per hour, comments per hour, and whether they should be handled today.

8. Deliver to Feishu.
   - Import weekly snapshot Excel files as Feishu Sheets for team filtering and collaboration.
   - Import DOCX reports as Feishu Docx documents for online reading/editing.
   - Upload original files to the backup folder.
   - Update or create a Feishu index document with links to the newest weekly snapshot, Daily Rising, reports, skill docs, and backup files.
   - Prefer two Excel layers: weekly snapshot files for traceable reporting, plus one cumulative master database for long-term trend and seed-user tracking.

9. Verify and clean local staging.
   - Run the Feishu consistency gate before cleanup: confirm imported Feishu titles, file types, links, sheet names, row/column counts, and key sample rows/headings match the local source.
   - Confirm original backups were uploaded when the run calls for backups.
   - Write a small run manifest with local source filenames, Feishu URLs/tokens, counts, and verification status.
   - Only after verification succeeds, remove temporary local intermediates such as render folders, merged scratch JSON, temporary Markdown, and duplicate exported files.
   - Keep failed-run artifacts, the latest manifest, and any source files that did not successfully reach Feishu.

## Stable Output Contracts

Use one of these modes:

- `weekly`: strategic weekly insight package. Outputs broad pain report, modular opportunity report, weekly snapshot post intelligence workbook, cumulative master post database update when available, subreddit size/activity metadata when available, rules data, raw JSON, Feishu links, and Feishu/local consistency verification status.
- `daily_rising`: operational monitoring package. Outputs a separate Daily Rising workbook focused on posts to review or reply to today, product-design-flagged rising posts when present, plus Feishu Sheet delivery and consistency verification status when available.
- `reply_assignment_2day`: every-2-days execution package. Reuses recent collected data when possible. Outputs one concise reply assignment workbook named `SUIJI Reddit 回复分配表 YYYY-MM-DD` with only `待回复`, `已处理`, and `字段说明`. It should not rerun the full weekly collection unless the available data is stale or missing.
- `reply_pack`: targeted reply suggestions for selected posts after rule review.

Keep schemas stable across runs. If a column or report section changes, document the change in the final response.

## Output Modes

### Subreddit Map

Output:

- Subreddit
- Priority
- Why it matters
- Pain points to search
- Keywords to use
- Posting/reply risk
- Suggested first action

### Weekly Jewelry Pain Report

Use `references/report_schema.md`.

Output:

- 本周结论
- 数据覆盖与限制
- 关键痛点 Top 5
- 产品机会评分
- 模块化机会单独分析
- 高价值帖子清单
- 种子用户/可互动对象
- 规则感知回复策略
- 下周抓取和验证计划
- 附录：Excel workbook, raw data, rules data

### Modular Jewelry Opportunity Report

Output separately from the broad report:

- Pain points modular jewelry may solve
- Pain points it does not solve
- Best use cases
- User objections
- Concept-test questions
- Best subreddits for validation
- Suggested soft posts/replies

Use the same evidence rules as the weekly report: cite workbook-backed posts with high jewelry relevance and include `重要性分数`, `分数区间`, `首饰相关性`, and `回复风险` when referencing specific posts.

### Product Design Pain Triage Report

Deprecated for the every-2-days workflow. Do not use product/operations split for reply assignment runs.

If the user explicitly asks for a weekly product insight section, output weekly as a separate short report.

Include only posts where the workbook field `是否产品组处理` is `是`, especially real feedback about:

- 重量：too heavy, pulling, sagging, earlobe discomfort, long-wear fatigue
- 过敏/敏感：sensitive ears, nickel allergy, irritation, green skin, swelling, bumps
- 佩戴舒适度：hurt, uncomfortable, sleeping in jewelry, backings, post length, rubbing, pinching

For each cluster include:

- Representative posts with links
- Whether the post is jewelry-related
- Jewelry type: earrings, rings, necklaces, bracelets, piercing jewelry, material/allergy, clasp/structure, wearing comfort, storage/travel, styling/workwear
- Subreddit size/activity context when available
- User's exact pain signal or short paraphrase
- Product implication for SUIJI
- What product design should judge
- Suggested research question or reply input for operations/founder
- Reply risk and any rule caveat

Do not frame this as "product design should directly answer Reddit." Product design should provide product facts, design hypotheses, and follow-up questions; public replies should usually be written by operations/founder in a transparent, non-promotional voice.


### Post Intelligence Workbook

Output as `.xlsx`. See `references/workbook_schema.md` for column definitions and scoring guidance.

Use a two-layer Excel strategy:

- Weekly snapshot workbook: one file per week, tied to that week's report and raw data.
- Cumulative master database: one long-running table that appends unique posts across weeks for trend analysis, seed-user tracking, and future Feishu Bitable migration.

Required sheets:

- `Overview`: workbook reading order, owner routing, and quick instructions.
- `Action Queue`: focused table for reply/review priority, including whether to handle Rising before New.
- `Posts`: all crawled posts, sorted by importance descending, with filters enabled.
- `High Priority`: A-tier posts worth manual review or potential reply.
- `Product Design`: focused product-team table, not a full 50+ column clone, containing posts routed to product design because they contain real feedback about weight, allergy/sensitivity, or wearing comfort.
- `Daily Rising`: included only in daily-mode workbooks, with rising/new posts, velocity metrics, and "是否建议今天处理".
- `Subreddit Rules`: rule summaries and source URLs for covered subreddits.
- `Tag Dictionary`: definitions for categories, scores, risks, and recommended actions.
- `Column Guide`: column-by-column Chinese explanation, importance, owner, and filtering usage.
- `Scoring Guide`: Chinese explanation of workbook usage and scoring standards.
- `Coverage`: run metadata, covered subreddits, query list, endpoint types, and known limitations.

### Every-2-Days Reply Assignment Workbook

Output as `.xlsx` and import to Feishu Sheet when delivery is available.

Filename/title:

- `SUIJI Reddit 回复分配表 YYYY-MM-DD`

Required sheets only:

- `待回复`: main execution sheet. Include only reply candidates, not all crawled posts.
- `已处理`: already replied or explicitly not-to-reply records pulled from the master database when available.
- `字段说明`: short instructions for how humans fill each field.

`待回复` columns:

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

Human-fill fields:

- `负责人名`: assigned human owner.
- `是否回复`: `否`, `是`, `不适合回复`, or `待复核`.
- `实际回复类型`: `未回复`, `帖子回复`, `评论回复`, `both`, or `不回复`.
- `回复内容`: actual posted reply or draft.
- `备注`: manual context, rule notes, or reason for not replying.

After humans fill the sheet, sync the filled fields back to the cumulative master database using `scripts/sync_reply_assignment_to_master.py`.

Implementation notes:

- Build with `scripts/build_reddit_post_workbook.py --mode reply_assignment`.
- Pass `--master path/to/master.xlsx` when available so the `已处理` sheet can prevent duplicate replies.
- Sync filled fields back with `scripts/sync_reply_assignment_to_master.py --assignment path/to/reply_assignment.xlsx --master path/to/master.xlsx --output path/to/updated_master.xlsx`.

### Reply Pack

Output:

- Target post link
- User pain signal
- Recommended reply
- Tone
- Risk level
- Follow-up suggestion

## Engagement Rules

- Do not recommend direct product promotion as the first interaction.
- Do not mass-DM users.
- Do not pretend to be a customer.
- Do not overclaim "no allergy." Prefer "Grade 5 titanium is commonly used for body-friendly, low-sensitivity applications" or similar careful wording.
- Use "designer/founder/researcher asking for feedback" framing when appropriate.
- Always include references to the Reddit posts used for analysis.
