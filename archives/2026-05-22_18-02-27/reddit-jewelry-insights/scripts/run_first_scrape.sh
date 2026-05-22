#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-Modular Jewelry Reddit Insights}"
OUTPUT_DIR="${2:-./reddit-data}"
DAYS="${3:-7}"

SCRAPER="/Users/a166/.claude/skills/brand-launch-ops/scripts/reddit_scraper.py"

if [ ! -f "$SCRAPER" ]; then
  echo "Missing scraper at: $SCRAPER" >&2
  echo "Copy or create a Reddit scraper before running this script." >&2
  exit 1
fi

python3 "$SCRAPER" \
  --subs jewelry Earrings jewelrymaking femalefashionadvice BusinessFashion fashionwomens35 capsulewardrobe HerOneBag piercing BuyItForLife \
  --days "$DAYS" \
  --fetch-comments \
  --output "$OUTPUT_DIR" \
  --project-name "$PROJECT_NAME"
