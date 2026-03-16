# Autonomous Business Build

## Chosen business
**LocalSignal AI** — an automated subscription service that generates hyperlocal real estate market reports, social posts, email newsletters, and listing/seller content for real estate agents, teams, lenders, and brokerages.

## Why this business
- 100% online product and delivery
- Can run with zero employees once set up
- Clear recurring pain point: agents need marketing content and local expertise signals
- Strong fit with Chris's existing domain knowledge
- Reach $10k MRR with realistic pricing:
  - 100 customers at $99/mo
  - 50 customers at $199/mo
  - 20 customers at $499/mo

## Offer ladder
1. **Starter — $99/mo**
   - 4 neighborhood/city market updates per month
   - 8 social captions
   - 1 newsletter draft
2. **Pro — $199/mo**
   - 4 market updates
   - 12 social captions
   - 4 newsletter drafts
   - 4 listing description packs
3. **Brokerage — $499/mo**
   - Multi-market support
   - Team content calendar
   - branded reports and email kits

## Autonomous system design
1. Pull housing/market data from public or low-cost APIs / CSVs
2. Generate structured local insights
3. Use LLM to turn insights into agent-ready content
4. Publish into a dashboard / send via email automatically
5. Acquire users through:
   - SEO pages for cities/neighborhoods
   - free sample reports
   - automated cold email / DM once approved
   - affiliate/referral loop

## Budget target
Under $500 to MVP:
- Domain: ~$15
- Static hosting: free / low cost
- Email sending: free tier initially
- LLM/API: capped low usage while validating
- Data sources: use free/public sources first

## Near-term build plan
- [x] Pick business model
- [x] Define pricing and autonomous workflow
- [x] Build landing page
- [x] Build sample report generator
- [x] Build content generation prompts/templates
- [x] Build lead capture
- [ ] Add automated email delivery
- [ ] Define acquisition experiments

## Reality check
This has a plausible path to $10k MRR, but not a guarantee. The hard part is distribution, not generation. The product can be made autonomous; customer acquisition will still need systems, channels, and iteration.

## Status
LocalSignal AI is now the secondary/fallback concept. The primary active concept is SignalSift (see `projects/autonomous-business/signalsift/` and `pivot-analysis.md`).
