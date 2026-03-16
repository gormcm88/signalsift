# Cloudflare Pages Deploy

## Recommended project settings
- Framework preset: **None**
- Build command: **(leave blank)**
- Build output directory: **projects/autonomous-business**

## Why Cloudflare Pages
- free tier is enough for MVP traffic
- static site deploys are dead simple
- custom domain support is straightforward
- fast global CDN by default

## Steps
1. Push this workspace/repo to GitHub (or connect local repo if preferred).
2. In Cloudflare Pages, create a new project from Git.
3. Set the output directory to `projects/autonomous-business`.
4. Deploy.
5. Add custom domain once purchased.

## Notes
- The current MVP is static.
- Lead capture is browser-local only right now; next step is wiring a backend, Cloudflare Worker, Formspree, or email workflow.
- `_headers` and `_redirects` are included for Pages-compatible static hosting behavior.
