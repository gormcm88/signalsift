# SignalSift deploy notes

## Current deployment recommendation
Use **Cloudflare Pages** for the static UI/demo layer first.

### Publish this directory
`projects/autonomous-business/signalsift`

### Framework preset
None

### Build command
Leave blank

### Output directory
`projects/autonomous-business/signalsift`

## What will be live immediately
- landing page
- prototype
- watchlist editor
- dashboard (reads static JSON files)
- niche landing pages

## What will NOT be live-dynamic yet
The Python monitor does not run on Cloudflare Pages by itself. For live monitoring, we will eventually need one of:
1. scheduled local runner on Chris's Mac mini
2. Cloudflare Worker / serverless job
3. small VPS or hosted cron runner

## Fastest staged launch
Phase 1:
- deploy static site and use it for demos / early customer conversations

Phase 2:
- run monitor locally on schedule and update JSON outputs

Phase 3:
- move monitoring to hosted automation

## Advantage of this staged approach
We can validate positioning and demand before spending money on backend complexity.
