#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-canary}"
OUTPUT_ROOT="${2:-./reddit-data}"
DAYS="${3:-7}"

SCRAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/reddit_public_json_collect.py"

COMMON_ARGS=(
  --days "$DAYS"
  --insecure-ssl
)

PAIN_QUERIES=(
  tarnish
  "green skin"
  "sensitive ears"
  "titanium earrings"
  "office jewelry"
  "travel jewelry"
  "modular jewelry"
  "convertible jewelry"
  "versatile jewelry"
)

case "$MODE" in
  canary)
    python3 "$SCRAPER" \
      --subs jewelry \
      "${COMMON_ARGS[@]}" \
      --limit 5 \
      --endpoints new \
      --delay-min 4 \
      --delay-max 8 \
      --stop-after-blocked 2 \
      --output "$OUTPUT_ROOT/canary"
    ;;
  core)
    python3 "$SCRAPER" \
      --subs jewelry Earrings jewelrymaking femalefashionadvice BusinessFashion fashionwomens35 piercing HerOneBag \
      --queries "${PAIN_QUERIES[@]}" \
      "${COMMON_ARGS[@]}" \
      --limit 25 \
      --search-limit 8 \
      --endpoints new rising top_week search \
      --delay-min 5 \
      --delay-max 10 \
      --stop-after-blocked 6 \
      --output "$OUTPUT_ROOT/weekly-core"
    ;;
  extended)
    python3 "$SCRAPER" \
      --subs capsulewardrobe BuyItForLife OUTFITS PetiteFashionAdvice Weddingattireapproval minimalism onebag PiercingAdvice jewelers JewelryDesign \
      --queries "${PAIN_QUERIES[@]}" \
      "${COMMON_ARGS[@]}" \
      --limit 20 \
      --search-limit 6 \
      --endpoints new rising top_week search \
      --delay-min 6 \
      --delay-max 12 \
      --stop-after-blocked 6 \
      --output "$OUTPUT_ROOT/weekly-extended"
    ;;
  daily)
    python3 "$SCRAPER" \
      --subs jewelry Earrings jewelrymaking femalefashionadvice BusinessFashion fashionwomens35 piercing HerOneBag \
      --days 1 \
      --insecure-ssl \
      --limit 25 \
      --endpoints rising new \
      --delay-min 5 \
      --delay-max 10 \
      --stop-after-blocked 4 \
      --output "$OUTPUT_ROOT/daily-rising"
    ;;
  *)
    echo "Usage: $0 {canary|core|extended|daily} [output_root] [days]" >&2
    exit 2
    ;;
esac
