# SignalSift

SignalSift is an autonomous buying-signal monitor for agencies, recruiters, consultants, and B2B sellers.

## Core promise
Track the companies you care about and get alerted when something changes that creates an opening:
- hiring activity
- website offer changes
- new location pages
- review spikes or drops
- visible positioning shifts

## Why this can win
- clearer ROI than generic AI content
- larger horizontal TAM
- highly automatable
- easier to start narrow and grow

## MVP scope
- user enters list of target company URLs
- system snapshots selected pages
- detects changes in title/meta/body snippets
- generates short sales angle summaries
- stores watchlist + recent changes locally

## Initial audience
- agencies prospecting SMBs
- recruiters targeting active hirers
- consultants looking for outreach triggers

## Current status
Working local prototype with:
- watchlist input
- snapshot store
- richer change detection (title, meta, headings, interesting links)
- alert generation
- local dashboard
- browser-side editable watchlist
- redesigned homepage focused on agencies as the first ICP
- niche landing pages for early GTM

## Run locally
```bash
python3 projects/autonomous-business/signalsift/monitor.py
python3 projects/autonomous-business/signalsift/export_alerts.py
python3 projects/autonomous-business/signalsift/email_digest.py
python3 -m http.server 4175
```
Then open:
- `/projects/autonomous-business/signalsift/index.html`
- `/projects/autonomous-business/signalsift/prototype.html`
- `/projects/autonomous-business/signalsift/dashboard.html`

Generated artifacts:
- `alerts.csv`
- `daily-digest.md`
- normalized `alerts.json`
