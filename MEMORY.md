# MEMORY.md

## Key Info

- **User:** Chris (first contact March 22, 2026)
- **Model:** openrouter/minimax/minimax-m2.5
- **Workspace:** /root/.openclaw/.openclaw/workspace

## Current Projects

- **ai-pred-mart**: Rails prediction market app
  - Running on localhost:3000
  - Has models: User, Market, Order, Trade, Position, Account, Player, PredictionMarket, Holding, MarketOutcome, PredictionTrade, MarketJudgment, MarketChallenge, MarketNotification
  - API: v1 endpoints for markets, orders, positions, accounts, auth
  - Auth: bcrypt passwords, session-based + API tokens
  - Authorization: Pundit installed

## Memory System

- NOW.md: active workbench (current tasks)
- memory/INDEX.md: navigation hub
- memory/YYYY-MM-DD.md: daily logs (append-only)
- memory/reflections/: nightly self-reflections
- memory/lessons/, decisions/, people/: categorized context

## Today's Highlights (2026-03-26)

- Pushed 97-file commit to GitHub with prediction market models and API
- Installed Pundit (authorization)
- Fixed Rails 8.1 → 7.2 downgrade for Ruby 3.1 compatibility
- Removed stale Tailwind task from NOW.md
- Wrote first nightly reflection