#!/usr/bin/env python3
import argparse
import html
import http.cookiejar
import json
import random
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen
from urllib.request import HTTPCookieProcessor, HTTPSHandler, build_opener


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def is_blocked_error(exc):
    if isinstance(exc, HTTPError):
        return exc.code in {403, 429}
    text = repr(exc).lower()
    return "blocked" in text or "too many requests" in text


def now_utc():
    return datetime.now(timezone.utc)


def fetch_json(url, timeout, insecure_ssl=False):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    context = ssl._create_unverified_context() if insecure_ssl else None
    with urlopen(req, timeout=timeout, context=context) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_text_with_reddit_challenge(url, timeout, insecure_ssl=False):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }
    context = ssl._create_unverified_context() if insecure_ssl else None
    jar = http.cookiejar.CookieJar()
    opener = build_opener(HTTPSHandler(context=context), HTTPCookieProcessor(jar))

    req = Request(url, headers=headers)
    with opener.open(req, timeout=timeout) as resp:
        text = resp.read().decode("utf-8", "ignore")

    if "Reddit - Please wait for verification" not in text:
        return text

    seed_match = re_search(r'await\(async e=>e\+e\)\("([^"]+)"\)', text)
    token_match = re_search(r'name="token" value="([^"]+)"', text)
    action_match = re_search(r'<form hidden method="GET" action="([^"]+)"', text)
    if not (seed_match and token_match and action_match):
        return text

    from urllib.parse import urljoin

    challenge_params = {
        "solution": seed_match.group(1) * 2,
        "js_challenge": "1",
        "token": token_match.group(1),
        "jsc_orig_r": "",
    }
    challenge_url = urljoin("https://www.reddit.com", action_match.group(1))
    challenge_url = f"{challenge_url}?{urlencode(challenge_params)}"
    challenge_req = Request(challenge_url, headers={**headers, "Referer": url})
    with opener.open(challenge_req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "ignore")


def re_search(pattern, text, flags=0):
    import re

    return re.search(pattern, text, flags)


def parse_int(value):
    if value in (None, ""):
        return None
    try:
        return int(str(value).replace(",", ""))
    except ValueError:
        return None


def collect_subreddit_page_metadata(sub, timeout, insecure_ssl=False):
    import re

    url = f"https://www.reddit.com/r/{quote_plus(sub)}/"
    page = fetch_text_with_reddit_challenge(url, timeout, insecure_ssl)
    if "Reddit - Please wait for verification" in page:
        return {
            "page_url": url,
            "page_status": "verification not completed",
        }

    def attr(name):
        match = re.search(rf'\b{name}="([^"]*)"', page)
        return html.unescape(match.group(1)).strip() if match else ""

    sidebar_subscribers = None
    sidebar_label = ""
    sidebar_match = re.search(r'<strong>([0-9,]+)</strong>\s*([^<]*?subscribed)', page)
    if sidebar_match:
        sidebar_subscribers = parse_int(sidebar_match.group(1))
        sidebar_label = html.unescape(sidebar_match.group(2)).strip()

    weekly_active_users = parse_int(attr("weekly-active-users"))
    weekly_contributions = parse_int(attr("weekly-contributions"))
    page_status = "ok" if weekly_active_users is not None or sidebar_subscribers is not None else "needs manual verification"
    return {
        "page_url": url,
        "page_status": page_status,
        "page_source": "subreddit page header/sidebar",
        "sidebar_subscribers": sidebar_subscribers,
        "sidebar_subscribers_label": sidebar_label,
        "weekly_active_users": weekly_active_users,
        "weekly_contributions": weekly_contributions,
        "page_subscribers_text": attr("subscribers-text"),
        "page_currently_viewing_text": attr("currently-viewing-text"),
    }


def post_from_child(child, source_url, source_kind, query=None):
    data = child.get("data", {})
    permalink = data.get("permalink") or ""
    return {
        "id": data.get("id"),
        "subreddit": data.get("subreddit"),
        "title": data.get("title"),
        "selftext": data.get("selftext") or "",
        "author": data.get("author"),
        "created_utc": data.get("created_utc"),
        "score": data.get("score"),
        "num_comments": data.get("num_comments"),
        "upvote_ratio": data.get("upvote_ratio"),
        "url": data.get("url"),
        "permalink": f"https://www.reddit.com{permalink}" if permalink.startswith("/") else permalink,
        "source_url": source_url,
        "source_kind": source_kind,
        "query": query,
        "link_flair_text": data.get("link_flair_text"),
        "over_18": data.get("over_18"),
    }


def collect_endpoint(url, source_kind, query, cutoff_utc, timeout, insecure_ssl=False):
    payload = fetch_json(url, timeout, insecure_ssl)
    children = payload.get("data", {}).get("children", [])
    posts = []
    for child in children:
        post = post_from_child(child, url, source_kind, query)
        created = post.get("created_utc") or 0
        if created >= cutoff_utc and post.get("id"):
            posts.append(post)
    return posts


def collect_subreddit_metadata(subs, timeout, delay_min, delay_max, insecure_ssl=False):
    metadata = {}
    errors = []
    for sub in subs:
        url = f"https://www.reddit.com/r/{quote_plus(sub)}/about.json?raw_json=1"
        try:
            payload = fetch_json(url, timeout, insecure_ssl)
            data = payload.get("data", {})
            active = data.get("accounts_active")
            if active is None:
                active = data.get("active_user_count")
            try:
                page_metadata = collect_subreddit_page_metadata(sub, timeout, insecure_ssl)
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as page_exc:
                page_metadata = {
                    "page_url": f"https://www.reddit.com/r/{sub}/",
                    "page_status": "needs manual verification",
                    "page_error": repr(page_exc),
                }
            metadata[sub] = {
                "subreddit": sub,
                "display_name": data.get("display_name") or sub,
                "title": data.get("title") or "",
                "subscribers": data.get("subscribers"),
                "api_subscribers": data.get("subscribers"),
                "active_user_count": active,
                "created_utc": data.get("created_utc"),
                "public_description": data.get("public_description") or "",
                "url": f"https://www.reddit.com/r/{sub}/",
                "source": "about.json + subreddit page",
                "status": "ok",
            }
            metadata[sub].update(page_metadata)
            if page_metadata.get("page_status") not in {"ok", None}:
                metadata[sub]["status"] = "partial; page metadata needs manual verification"
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            page_metadata = {}
            try:
                page_metadata = collect_subreddit_page_metadata(sub, timeout, insecure_ssl)
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as page_exc:
                page_metadata = {"page_status": "needs manual verification", "page_error": repr(page_exc)}
            metadata[sub] = {
                "subreddit": sub,
                "url": f"https://www.reddit.com/r/{sub}/",
                "source": "about.json + subreddit page",
                "status": "needs manual verification",
                "error": repr(exc),
            }
            metadata[sub].update(page_metadata)
            errors.append({"subreddit": sub, "url": url, "error": repr(exc)})
        time.sleep(random.uniform(delay_min, delay_max))
    return metadata, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subs", nargs="+", required=True)
    parser.add_argument("--queries", nargs="*", default=[])
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--search-limit", type=int, default=15)
    parser.add_argument(
        "--endpoints",
        nargs="+",
        choices=["new", "rising", "top_week", "search"],
        default=["new", "rising", "top_week", "search"],
        help="Endpoint groups to collect. Use fewer endpoint groups for daily or canary runs.",
    )
    parser.add_argument("--delay-min", type=float, default=2.8)
    parser.add_argument("--delay-max", type=float, default=5.5)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument(
        "--stop-after-blocked",
        type=int,
        default=8,
        help="Stop the run after this many consecutive 403/429-style errors.",
    )
    parser.add_argument("--insecure-ssl", action="store_true")
    parser.add_argument(
        "--collect-community-metadata",
        action="store_true",
        help="Also attempt to collect subreddit size/activity metadata from about.json. Failures are recorded but do not stop post collection.",
    )
    parser.add_argument("--output", default="reddit-data/live")
    args = parser.parse_args()

    started_at = now_utc()
    cutoff_utc = started_at.timestamp() - args.days * 24 * 3600
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_posts = {}
    community_metadata = {}
    errors = []
    requests_made = []
    consecutive_blocked = 0
    stopped_early = False

    for sub in args.subs:
        endpoints = []
        if "new" in args.endpoints:
            endpoints.append((
                    "new",
                    f"https://www.reddit.com/r/{quote_plus(sub)}/new.json?{urlencode({'limit': args.limit, 'raw_json': 1})}",
                    None,
            ))
        if "rising" in args.endpoints:
            endpoints.append((
                    "rising",
                    f"https://www.reddit.com/r/{quote_plus(sub)}/rising.json?{urlencode({'limit': args.limit, 'raw_json': 1})}",
                    None,
            ))
        if "top_week" in args.endpoints:
            endpoints.append((
                    "top_week",
                    f"https://www.reddit.com/r/{quote_plus(sub)}/top.json?{urlencode({'limit': args.limit, 't': 'week', 'raw_json': 1})}",
                    None,
            ))
        if "search" in args.endpoints:
            for query in args.queries:
                params = {
                    "q": query,
                    "restrict_sr": 1,
                    "sort": "new",
                    "t": "week",
                    "limit": args.search_limit,
                    "raw_json": 1,
                }
                endpoints.append(("search_new_week", f"https://www.reddit.com/r/{quote_plus(sub)}/search.json?{urlencode(params)}", query))

        for source_kind, url, query in endpoints:
            try:
                posts = collect_endpoint(url, source_kind, query, cutoff_utc, args.timeout, args.insecure_ssl)
                for post in posts:
                    all_posts[post["id"]] = post
                requests_made.append({"subreddit": sub, "kind": source_kind, "query": query, "url": url, "posts": len(posts)})
                consecutive_blocked = 0
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
                errors.append({"subreddit": sub, "kind": source_kind, "query": query, "url": url, "error": repr(exc)})
                if is_blocked_error(exc):
                    consecutive_blocked += 1
                else:
                    consecutive_blocked = 0
                if args.stop_after_blocked and consecutive_blocked >= args.stop_after_blocked:
                    stopped_early = True
                    errors.append({
                        "subreddit": sub,
                        "kind": "run_control",
                        "query": None,
                        "url": "",
                        "error": f"Stopped early after {consecutive_blocked} consecutive blocked/rate-limited responses.",
                    })
                    break
            time.sleep(random.uniform(args.delay_min, args.delay_max))
        if stopped_early:
            break

    if args.collect_community_metadata:
        community_metadata, metadata_errors = collect_subreddit_metadata(
            args.subs,
            args.timeout,
            args.delay_min,
            args.delay_max,
            args.insecure_ssl,
        )
        for err in metadata_errors:
            errors.append({
                "subreddit": err.get("subreddit"),
                "kind": "community_metadata",
                "query": None,
                "url": err.get("url", ""),
                "error": err.get("error"),
            })

    posts = sorted(all_posts.values(), key=lambda p: (p.get("created_utc") or 0), reverse=True)
    finished_at = now_utc()
    result = {
        "meta": {
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "days": args.days,
            "cutoff_utc": cutoff_utc,
            "subreddits": args.subs,
            "queries": args.queries,
            "endpoints": args.endpoints,
            "community_metadata_collected": bool(args.collect_community_metadata),
            "total_unique_posts": len(posts),
            "request_count": len(requests_made),
            "stopped_early": stopped_early,
            "errors": errors,
        },
        "requests": requests_made,
        "community_metadata": community_metadata,
        "posts": posts,
    }
    stamp = finished_at.strftime("%Y%m%d_%H%M%S")
    out = output_dir / f"reddit_public_json_{stamp}.json"
    latest = output_dir / "latest.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    latest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(out), "latest": str(latest), "posts": len(posts), "errors": len(errors)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
