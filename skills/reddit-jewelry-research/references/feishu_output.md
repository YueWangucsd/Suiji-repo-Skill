# Feishu Output and Long-Term Workbook Policy

Use this reference when delivering SUIJI Reddit research outputs to Feishu or setting up automations.

## Default Feishu Destination

When `lark-cli` is configured and authorized, final deliverables should be created in Feishu rather than only left as local files. Local files are temporary staging artifacts until the Feishu version has been verified.

For this Codex workspace, use the Codex-specific wrapper instead of a bare `lark-cli` command:

```bash
scripts/lark-codex ...
```

The wrapper pins `--profile cli_a977576895389bd4`, which is the Feishu CLI app/user pair for `飞书用户9565TR`. Do not use a Claude Code Feishu app/profile for Codex delivery.

Use Feishu bot identity first for automated delivery. In sandboxed or cron contexts, `lark-cli auth status` may fail with `keychain Get failed` / `keychain not initialized`, and user tokens may expire while bot tenant access still works. Treat auth status as a diagnostic, not a hard blocker. Continue when `scripts/lark-codex ... --as bot` import/upload/update operations succeed. Stop only when the bot operation itself fails with a real permission/configuration error.

For diagnostics, run:

```bash
scripts/lark-codex auth status
```

Expected app/user context when diagnostics are readable:

- `appId`: `cli_a977576895389bd4`
- `userName`: `飞书用户9565TR`

Default structure:

- Main folder: `Suiji`
- Working folder: `Suiji/Reddit`
- Backup folder: `Suiji/Reddit/原始文件备份`

Known folder tokens from the initial setup:

- `Suiji`: `Tly1fbLnbl2ID1dkHO7cu1Wfn4b`
- `Suiji/Reddit`: `GOpSfQSrRlbWa5duAfEcDeM7nYc`
- `Suiji/Reddit/原始文件备份`: `T7qtfooxSl05lLdhZS0cgqT8nMX`

Do not store App Secret values in this skill or in reports.

## Feishu Delivery Rules

For each successful weekly run:

1. Import the weekly snapshot Excel workbook as a Feishu Sheet.
2. Import the Chinese weekly report DOCX as a Feishu Docx document.
3. Import the modular opportunity report DOCX as a Feishu Docx document.
4. Upload the original `.xlsx`, `.docx`, `.md`, and raw JSON files to `原始文件备份` when useful.
5. Update or create a Feishu index document in `Suiji/Reddit` containing links to editable files and original backups.

For each successful daily run:

1. Import the Daily Rising workbook as a Feishu Sheet.
2. Update or create the Feishu index document with the newest Daily Rising link.
3. Upload the original `.xlsx` backup when useful.

For each successful every-2-days reply assignment run:

1. Import `SUIJI Reddit 回复分配表 YYYY-MM-DD.xlsx` as a Feishu Sheet.
2. The editable Feishu Sheet must contain only `待回复`, `已处理`, and `字段说明`.
3. Update or create the Feishu index document with the newest reply assignment link.
4. Upload the original `.xlsx` backup when useful.
5. After humans fill the assignment fields, sync `负责人名`, `是否回复`, `实际回复类型`, `回复内容`, and `备注` back into the cumulative master database.

After import/upload, run the consistency gate before cleanup. If Feishu import/upload or verification fails, preserve local outputs and report the failure reason clearly.

## Consistency Gate Before Cleanup

The workflow may generate reports and workbooks locally first, but Feishu is the long-term source of truth after delivery. To avoid local/Feishu mismatch, do not clean local files until all required checks pass.

For every successful weekly or daily run, create a small run manifest in local staging before cleanup. The manifest should include:

- run date and time
- mode: `weekly`, `daily_rising`, or `reply_assignment_2day`
- local source file paths
- source file sizes and, when practical, SHA-256 hashes
- expected sheet names
- expected row counts and column counts for each workbook sheet
- expected report title/headings
- Feishu editable URLs/tokens
- backup file URLs/tokens
- verification status for each output

Minimum verification checks:

1. Feishu import/upload command returned `ok: true`.
2. Feishu URL/token exists for every required deliverable.
3. Imported Feishu file title matches the intended date/title.
4. Feishu file type matches the source: workbook to Sheet, report to Docx, original to file backup.
5. For Feishu Sheets, verify sheet names and dimensions with `lark-cli sheets +info`.
6. For Feishu Sheets, read the header row and 3-5 sample rows with `lark-cli sheets +read`; compare them with the local workbook headers and sampled rows.
7. For Feishu Docx, verify the online document opens/updates successfully and contains the expected title plus the main section headings. If a direct read command is unavailable, treat a successful `docs +update` or `drive +import` plus backup upload as the minimum check, and keep the local DOCX until manual verification.
8. Verify the Feishu index document includes the newest URLs.

If any check fails, mark the run as `verification_failed`, keep all local files for debugging, and do not claim the Feishu version is final.

## Local Retention and Cleanup Policy

Default retention principle: Feishu keeps the long-term archive; local disk is only for staging, troubleshooting, and the latest run manifest.

After all consistency checks pass:

- Delete temporary render folders such as `tmp/docx-render-*`.
- Delete scratch or merged intermediate JSON that is already represented in a verified workbook or uploaded backup.
- Delete duplicate local `.md`, `.xlsx`, and `.docx` working files when they have both an editable Feishu version and an original backup, unless the user asked to keep local copies.
- Keep the latest run manifest and a lightweight collection-status log.
- Keep failed-run artifacts until the next successful run or manual cleanup.

If the user asks for a local archive, retain date-stamped local outputs; otherwise prefer cleanup after Feishu verification.

## Editable vs Backup Outputs

Use two versions of important outputs:

- Editable Feishu version: best for daily team use, filtering, comments, and collaboration.
- Original backup file: best for archive, download, and format-preserving recovery.

Recommended mapping:

| Local output | Feishu editable target | Backup target |
|---|---|---|
| Weekly post intelligence `.xlsx` | Feishu Sheet | `.xlsx` file upload |
| Daily Rising `.xlsx` | Feishu Sheet | `.xlsx` file upload |
| Reply assignment `.xlsx` | Feishu Sheet | `.xlsx` file upload |
| Weekly report `.docx` | Feishu Docx | `.docx` file upload |
| Modular opportunity report `.docx` | Feishu Docx | `.docx` file upload |
| Skill intro `.docx` | Feishu Docx | `.docx` file upload |
| Raw JSON | Usually backup only | `.json` file upload when needed |

## Two-Layer Excel Strategy

Do not choose only "new file every week" or only "one file forever." Use both.

### Layer 1: Weekly Snapshot Workbook

Create one date-stamped workbook per weekly report.

Purpose:

- Keep each report traceable to the exact data used that week.
- Avoid changing historical analysis when scoring rules, keywords, or subreddit coverage change.
- Make weekly review simple for the team.

Example names:

- `SUIJI Reddit 周报帖子库 2026-05-03`
- `SUIJI Reddit 周报帖子库 2026-05-10`
- `SUIJI Reddit 周报帖子库 2026-05-17`

Use this file in the weekly report and Feishu index.

### Layer 2: Cumulative Master Post Database

Maintain one long-running master table, for example:

- `SUIJI Reddit 用户痛点总库`

Update policy:

- Append newly collected posts from each weekly run.
- Deduplicate by Reddit post ID first, then permalink if ID is missing.
- Preserve historical rows; do not overwrite historical tags unless a deliberate re-score is requested.
- Add run metadata columns such as first collected date, latest seen date, source weekly snapshot, and report week.
- Keep the same Chinese tag fields as the weekly workbook so filters are consistent.

Purpose:

- Track long-term pain trends.
- Build a seed-user and reply-candidate pool.
- Compare recurring complaints across weeks.
- Prepare for later migration to Feishu Bitable.

## When To Use Feishu Bitable

Do not start with Bitable by default. Feishu Sheets are lighter and easier for weekly reports.

Consider migrating the cumulative master database to Feishu Bitable after 3-4 weeks if the team is actively using it as a CRM-like workflow.

Bitable becomes useful when the team needs:

- Owner/status fields for follow-up.
- Reply status and next action.
- Seed-user pipeline.
- Views by pain cluster, reply risk, subreddit, score band, and action.
- De-duplicated long-term records with manual notes.

Suggested Bitable fields:

- Reddit Post ID
- Post URL
- Subreddit
- Report Week
- First Collected Date
- Latest Seen Date
- Importance Score
- Score Band
- Pain Tags
- Intent Tags
- Product Fit Tags
- Reply Risk
- Suggested Action
- Owner
- Follow-up Status
- Last Action Date
- Notes

## Feishu CLI Commands

Import an Excel file as Feishu Sheet:

```bash
scripts/lark-codex drive +import --as bot \
  --folder-token GOpSfQSrRlbWa5duAfEcDeM7nYc \
  --type sheet \
  --file path/to/workbook.xlsx \
  --name "SUIJI Reddit 周报帖子库 YYYY-MM-DD"
```

Import a Word report as Feishu Docx:

```bash
scripts/lark-codex drive +import --as bot \
  --folder-token GOpSfQSrRlbWa5duAfEcDeM7nYc \
  --type docx \
  --file path/to/report.docx \
  --name "SUIJI Reddit 首饰用户痛点周报 YYYY-MM-DD"
```

Upload original backup file:

```bash
scripts/lark-codex drive +upload --as bot \
  --folder-token T7qtfooxSl05lLdhZS0cgqT8nMX \
  --file path/to/file.xlsx \
  --name file.xlsx
```

Update an index document:

```bash
scripts/lark-codex docs +update --api-version v2 --as bot \
  --doc "<docx url or token>" \
  --command overwrite \
  --doc-format markdown \
  --content @path/to/index.md
```

Check imported spreadsheet metadata:

```bash
scripts/lark-codex sheets +info --as bot \
  --spreadsheet-token "<sheet token>"
```

Read a spreadsheet sample for verification:

```bash
scripts/lark-codex sheets +read --as bot \
  --spreadsheet-token "<sheet token>" \
  --range "Posts!A1:AE6"
```

If no index exists, create one in `Suiji/Reddit`.
