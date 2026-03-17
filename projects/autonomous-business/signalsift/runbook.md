# SignalSift runbook

## Local demo run
```bash
python3 projects/autonomous-business/signalsift/monitor.py
python3 -m http.server 4180
```

## Files that matter
- `watchlist.json` — file-based targets used by monitor
- `snapshots.json` — latest extracted page data
- `alerts.json` — recent generated alerts
- `watchlist.html` — browser-side watchlist builder (localStorage)
- `dashboard.html` — UI for alerts and snapshots

## Suggested next build priorities
1. import localStorage watchlist into file-based runner flow
2. better diffing around headings/offers/links
3. classify signals by severity
4. export leads / alerts CSV
5. email digest generation
6. hosted scheduler

## Manual customer validation flow
1. pick a niche (agencies first)
2. create 5-10 sample targets in that niche
3. run monitor
4. inspect alerts
5. improve alert language until it feels immediately useful
6. only then do outreach
