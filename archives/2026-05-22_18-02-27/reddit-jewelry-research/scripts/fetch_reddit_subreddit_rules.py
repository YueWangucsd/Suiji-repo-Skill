#!/usr/bin/env python3
import argparse
import json
import random
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


USER_AGENT = "Mozilla/5.0 (compatible; SUIJIJewelryResearch/0.1; subreddit rules research)"


def fetch_json(url, timeout, insecure_ssl=False):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    context = ssl._create_unverified_context() if insecure_ssl else None
    with urlopen(req, timeout=timeout, context=context) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subs", nargs="+", required=True)
    parser.add_argument("--output", default="reddit-data/rules")
    parser.add_argument("--delay-min", type=float, default=1.5)
    parser.add_argument("--delay-max", type=float, default=3.0)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--insecure-ssl", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "meta": {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "subreddits": args.subs,
        },
        "subreddits": {},
        "errors": [],
    }

    for sub in args.subs:
        url = f"https://www.reddit.com/r/{quote_plus(sub)}/about/rules.json?raw_json=1"
        try:
            payload = fetch_json(url, args.timeout, args.insecure_ssl)
            rules = []
            for rule in payload.get("rules", []) or []:
                rules.append({
                    "short_name": rule.get("short_name", ""),
                    "description": rule.get("description", ""),
                    "violation_reason": rule.get("violation_reason", ""),
                    "kind": rule.get("kind", ""),
                    "created_utc": rule.get("created_utc"),
                })
            result["subreddits"][sub] = {
                "rules_url": f"https://www.reddit.com/r/{sub}/about/rules",
                "rules": rules,
            }
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            result["errors"].append({"subreddit": sub, "url": url, "error": repr(exc)})
            result["subreddits"][sub] = {
                "rules_url": f"https://www.reddit.com/r/{sub}/about/rules",
                "rules": [],
                "error": repr(exc),
            }
        time.sleep(random.uniform(args.delay_min, args.delay_max))

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out = out_dir / f"subreddit_rules_{stamp}.json"
    latest = out_dir / "latest.json"
    text = json.dumps(result, ensure_ascii=False, indent=2)
    out.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    print(json.dumps({"output": str(out), "latest": str(latest), "subreddits": len(result["subreddits"]), "errors": len(result["errors"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
