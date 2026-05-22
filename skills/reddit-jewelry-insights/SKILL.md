---
name: reddit-jewelry-insights
description: Use this skill for broad Reddit research, weekly monitoring, seed-user discovery, and community engagement strategy around jewelry user pain points, including tarnish, fading, allergy, sensitive ears, comfort, styling, storage, price, quality, workwear, travel, capsule wardrobe, and separately modular or convertible jewelry opportunities.
---

# Reddit Jewelry Insights

Use this skill when the user wants to research Reddit for jewelry pain points, seed users, product positioning, community engagement, or weekly Reddit insight reports.

The default scope is broad jewelry pain discovery:

- Material and durability issues: tarnish, fading, oxidation, plating wear, green skin, broken clasps, loose stones.
- Body and comfort issues: sensitive ears, nickel allergy, irritation, heaviness, earring backs, difficult changing.
- Styling and occasion issues: office jewelry, formal events, daily wear, outfit matching, too much or too little.
- Ownership issues: storage, travel packing, capsule wardrobe, too many pieces, hard to organize.
- Buying issues: price, quality, dupes, reviews, recommendations, trust, return policies.

Treat modular or convertible jewelry as a separate opportunity lens, not the default filter. If relevant signals appear, create a separate section or separate report for modular/convertible opportunities.

## Workflow

1. Confirm the research objective.
   - If the user already gave a clear product and market, do not over-question.
   - Default market: English-speaking Reddit users in the US/UK/Canada/Australia.
   - Default cadence: weekly monitoring.

2. Build or refine the subreddit set.
   - Start with the subreddit tiers in `references/subreddits.md`.
   - Prefer 8-15 communities per scrape.
   - Mix direct jewelry communities, fashion/workwear communities, capsule/travel communities, and pain-point communities.
   - If the user asks for a current list, verify with web search because subreddit size, rules, and activity change.

3. Build the keyword map.
   - Start with broad pain terms: tarnish, fading, gold plated, green skin, oxidation, nickel allergy, sensitive ears, irritation, heavy earrings, broken clasp, loose stone.
   - Include scenario terms: office jewelry, work appropriate earrings, business casual jewelry, wedding guest jewelry, travel jewelry, capsule jewelry.
   - Include buying-intent terms: recommendations, alternatives, worth it, everyday earrings, high quality jewelry.
   - Keep modular terms in a separate optional keyword group: modular jewelry, convertible jewelry, detachable earrings, earrings to ring, day to night jewelry.

4. Collect posts.
   - Prefer an existing Reddit scraper if available. In this user's environment, check:
     `/Users/a166/.claude/skills/brand-launch-ops/scripts/reddit_scraper.py`
   - If available, use it instead of rewriting a scraper.
   - Use respectful crawl settings and avoid spammy automation.
   - If live scraping needs browser login or network access, explain the requirement and request approval when needed.

5. Analyze the data.
   - Separate raw popularity from product relevance. A viral outfit post is not automatically a strong product signal.
   - Score each post for:
     - Pain intensity
     - Product relevance
     - Interaction opportunity
     - Seed-user potential
     - Community risk, such as strict no-promotion rules
   - Preserve useful user wording. Quote only short excerpts and link the source.

6. Produce the report.
   - Use the structure in `references/report_schema.md`.
   - Always include concrete next actions, not just observations.
   - Include suggested soft-engagement replies that ask for feedback rather than sell.

## Output Modes

### Subreddit Map

Use when the user asks where to research. Output:

- Tiered subreddit list
- Why each community matters
- What to search there
- How to enter without looking promotional
- Priority score

### Weekly Insight Report

Use when Reddit data has been collected. Output:

- Executive summary
- Top pain points
- Product opportunities
- Subreddit activity summary
- High-value posts
- Seed-user candidates
- Suggested replies
- Next week's search plan

### Modular Opportunity Report

Use only when the user asks for modular or convertible jewelry analysis, or when the broad pain report surfaces enough signals to justify it. Output:

- Which broad pain points modular jewelry could address
- Which pain points it does not solve
- Best-fit use cases
- Likely objections
- Concept-test questions
- Suggested communities for soft validation

### Seed User Pipeline

Use when the user wants users to contact or nurture. Output:

- Reddit username
- Source subreddit and post
- Pain signal
- Suggested first reply
- Follow-up path
- Risk notes

## Community Engagement Rules

- Do not recommend direct product promotion as the first interaction.
- Prefer curiosity-led replies: ask about use cases, friction, desired materials, preferred styles, and willingness to test.
- Treat Reddit as a community, not a lead list.
- Check each subreddit rules page before posting.
- Avoid fake testimonials, astroturfing, mass DMing, or pretending to be a customer.
- When asking for feedback, be transparent if speaking as a founder, designer, or researcher.

## Useful Soft Prompts

Use these as patterns, adapting to the thread:

```text
I am exploring a jewelry design idea and would love honest feedback: would a piece that switches quickly between office-appropriate earrings and a ring/statement piece after work feel useful, or would that be too much friction?
```

```text
For people who keep a capsule wardrobe, do you also keep a capsule jewelry setup? What makes one piece versatile enough to earn a permanent spot?
```

```text
For anyone with sensitive ears: is material the main issue, or is comfort/weight/ease of changing earrings just as important?
```

## Optional Automation

For a recurring workflow, set up:

1. Weekly scrape of selected subreddits and keywords.
2. JSON archive by date.
3. AI analysis into report schema.
4. Seed-user candidate table.
5. A short team summary in Markdown or HTML.

If the user asks for implementation, create a small project with config files for subreddits and keywords rather than hard-coding everything in the scraper.
