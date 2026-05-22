# SUIJI Codex Skills

This repository stores the SUIJI Reddit-related Codex skills and version archives.

## Current Skills

- `skills/reddit-jewelry-research`
  - Main active skill for SUIJI Reddit research and operations.
  - Covers weekly/daily Reddit research, Daily Rising, seed-user operations, team check-ins, KPI workflows, reply queues, Feishu delivery, and workbook generation.

- `skills/reddit-jewelry-insights`
  - Older broad Reddit jewelry insight skill.
  - Kept as historical reference for research framing.

## Archives

- `archives/2026-05-22_18-02-27`
  - Snapshot taken before the 2026-05-22 update to `reddit-jewelry-research`.
  - Includes both `reddit-jewelry-research` and `reddit-jewelry-insights`.
  - See `ARCHIVE_MANIFEST.md` for SHA256 checksums and source paths.

## 2026-05-22 Update Summary

`reddit-jewelry-research` was expanded from a research/reporting skill into the main SUIJI Reddit research and operations skill.

Added output modes:

- `seed_ops_daily`
- `weekly_ops_review`
- `team_checkin`

Clarified operating goal:

- 30% customer pain understanding
- 70% seed-user incubation

Compliance boundary:

- The skill can research, score, summarize, draft, and create Feishu/local workbooks.
- The skill must not automate Reddit posting, commenting, voting, messaging, or account creation.
- Humans must manually perform Reddit user actions from their own accounts.
