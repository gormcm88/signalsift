# SKILL_DEFAULTS.md

Default skill-routing rules for Judith.

## Core principle
When a curated skill clearly matches the task, use it before improvising.

## Engineering / code

### Debugging
Default to:
- `skills/curated/superpowers/systematic-debugging`

Use when:
- tests fail
- code behaves unexpectedly
- integration breaks
- performance or build issues appear

Rule:
- do root-cause investigation before proposing fixes
- do not stack speculative fixes

### Larger implementation work
Default sequence:
1. `skills/curated/superpowers/writing-plans`
2. `skills/curated/superpowers/test-driven-development` when tests make sense
3. `skills/curated/superpowers/verification-before-completion`

Use when:
- building new features
- restructuring code
- handling multi-step implementation

## Marketing / growth
Default to:
- `skills/curated/marketingskills/`

First-check shortlist:
- `copywriting`
- `content-strategy`
- `email-sequence`
- `launch-strategy`
- `pricing-strategy`
- `marketing-ideas`
- `social-content`

Use when:
- writing offers, pages, campaigns, emails
- brainstorming customer acquisition
- improving messaging or conversion

## SEO
Default to:
- `skills/curated/claude-seo/`

First-check shortlist:
- `seo-audit`
- `seo-page`
- `seo-plan`
- `seo-schema`
- `seo-local`
- `seo-technical`

Use when:
- auditing or improving rankings
- fixing metadata/schema/sitemap issues
- doing local SEO for service businesses or real estate

## Obsidian / notes
Default to:
- `skills/curated/obsidian-skills/`

First-check shortlist:
- `obsidian-cli`
- `obsidian-markdown`
- `obsidian-bases`

Use when:
- interacting with an Obsidian vault
- cleaning notes or metadata
- automating note workflows

## Memory / recall
Default sequence:
1. `memory_search`
2. `memory_get` or direct file read of authoritative source
3. answer with verified facts only

Use when:
- asked about prior work
- recalling project state, decisions, preferences, dates, people, or todos

## Project facts
For active projects, prefer:
- `STATUS.md` for live state / links / latest commit
- `FACTS.md` for authoritative values
- `DECISIONS.md` if strategy branches become important

## Safety / anti-hallucination
- Never guess factual table values for published deliverables.
- If a fact is unverified, say so or use `TBD`.
- Retrieval beats fluent improvisation.
- Verification before completion is mandatory for high-stakes edits.
