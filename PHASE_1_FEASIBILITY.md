# Phase 1: Feasibility Study — Multi-Venue Latency Arbitrage Bot

**Project:** Polymarket + Kalshi + Coinbase Predictions Latency Arbitrage  
**Date:** March 30, 2026  
**Status:** DRAFT — For Review

---

## Executive Summary

**Recommendation: PROCEED with caution — single-venue focus on Polymarket only, with extensive paper trading**

The original latency arbitrage edge described in the @adiix_official thread has **significantly compressed** due to:
1. Platform fee implementations (up to 1.56% on Polymarket)
2. Increased bot competition
3. Market microstructure inefficiencies narrowing

Recent live trading data (March 2026) shows win rates of 25-27% — well below the ~53% breakeven threshold required to overcome fees. However, a properly designed system with robust risk management may still find limited opportunities, particularly in cross-venue mispricings.

**Multi-venue strategy is NOT recommended at this stage.** Start with Polymarket only.

---

## 1. Current State Analysis by Venue

### 1.1 Polymarket

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Contracts** | 5-min BTC/ETH Up/Down | Resolves every 5 min |
| **Daily Volume** | ~$60M (5-min crypto) | Dominates prediction flows |
| **Taker Fee** | ~1.56% (at $0.50 price) | Formula: `price × 0.25 × (price × (1-price))²` |
| **Maker Rebate** | 20% of fees | Paid to LPs |
| **Spread** | 2–4 cents per side | Combined asks typically ≥$1.00 |
| **Min Deposit** | $3 (USDC on Polygon) | No KYC required |
| **API** | REST + WebSocket | Gamma API for market discovery |
| **Resolution** | BTC/USD spot at window close | Uses `outcomePrices` field |

**Live Trading Results (March 2026):**
- Win rate: 25–27% (vs. 53% breakeven)
- ROI: -49.5% (Session 1), -13% (Session 2 with improved filters)
- Key failure: Directional bias (80% of trades wrong direction in downtrend)
- Slippage: 2–4 cents/token live vs. 0 in paper

**Competitive Landscape:**
- Arbitrage traders extracted ~$40M from Polymarket (Apr 2024–Apr 2025)
- Multiple bot operators active; edge has compressed
- Polymarket generating $800K–$1M daily in fees (March 2026)

### 1.2 Kalshi

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Regulation** | CFTC-regulated DCM | Designated Contract Market |
| **Contracts** | 15-min BTC/ETH Up/Down, price-at-time | Limited short-duration crypto |
| **Fee Structure** | Taker fees apply | CFTC oversight |
| **Legal Status** | Under litigation | Washington AG sued; Nevada preliminary injunction (March 26, 2026) |
| **API** | REST + WebSocket | Official API available |
| **Access from TX** | Available | CFTC-regulated = legal gray area but operational |

**Key Considerations:**
- More regulatory clarity than Polymarket
- Slightly longer duration (15 min vs. 5 min) reduces signal noise
- Coinbase Predictions routes through Kalshi (see below)
- Texas: Operates but state AG may pursue enforcement

### 1.3 Coinbase Predictions

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Integration** | Powered by Kalshi | Routes through Kalshi order book |
| **Markup** | Additional spread | "Every trade routes through Kalshi with a markup" |
| **Min Bet** | $1 | Integrated into Coinbase app |
| **Legal Issues** | Nevada preliminary injunction | March 26, 2026 — may restrict access |

**Assessment:** Not recommended as primary venue due to:
- Additional markup layer
- Legal uncertainty (ongoing litigation)
- Indirect access via Kalshi anyway

---

## 2. Economic Viability Analysis

### 2.1 Break-Even Win Rate

With 1.56% taker fee on a $0.50 contract:
- Cost per trade: $0.0156 × 2 (entry + exit assumption) = ~3.12%
- Breakeven win rate: ~53% (accounting for 50% probability + fees)

**Reality Check:**
- Observed win rates: 25–27%
- **Gap: 26–28 percentage points below breakeven**

### 2.2 Fee Impact Summary

| Venue | Typical Fee | Breakeven Win Rate |
|-------|-------------|-------------------|
| Polymarket | ~1.56% | ~53% |
| Kalshi | ~0.5–1% (est.) | ~51% |
| Coinbase Pred. | Markup + fees | Higher |

### 2.3 Required Edge

To achieve profitability:
- Need >3% edge per trade (after fees)
- Must correctly predict direction >53% of time
- Requires either:
  - Superior signal generation (momentum + trend filtering)
  - Cross-venue mispricing (Polymarket vs. Kalshi delta)

---

## 3. Infrastructure Requirements

### 3.1 Latency Targets

| Component | Target | Notes |
|-----------|--------|-------|
| CEX Price Feed | <50 ms | Binance/Coinbase WebSocket |
| Signal Processing | <100 ms | Elixir processing pipeline |
| Order Execution | <200 ms | Polymarket/Kalshi API |
| **Total Round-Trip** | <350 ms | End-to-end |

### 3.2 VPS / Colocation

| Option | Latency | Monthly Cost | Suitability |
|--------|---------|--------------|-------------|
| **VPS (Tokyo/Frankfurt)** | 2–4 ms to Binance | $80–150 | Adequate for start |
| **Colocation** | <1 ms | $1,200–$2,000 | Only if scaling |
| **Austin → CEXs** | ~30–50 ms | N/A | Not competitive |

**Recommendation:** Start with VPS in Tokyo or Frankfurt (for Binance access). Consider US East (Virginia) for Coinbase.

### 3.3 Estimated Monthly Costs

| Item | Cost |
|------|------|
| VPS (Tokyo) | $100 |
| Monitoring (Prometheus/Grafana) | $20 |
| Domain + SSL | $10 |
| Data (WebSocket feeds) | $0 |
| **Total** | ~$130/month |

---

## 4. Legal & Regulatory (Austin, Texas)

### 4.1 Venue Legality

| Venue | Regulatory Status | Texas Risk |
|-------|------------------|------------|
| **Polymarket** | Operates outside US | Medium — not explicitly legal |
| **Kalshi** | CFTC-regulated DCM | Low-Medium — CFTC oversight |
| **Coinbase Pred.** | Kalshi-powered | Medium — injunction risk |

### 4.2 Key Legal Developments

- **Kalshi:** Sued by Washington AG (gambling allegations); Nevada preliminary injunction (March 26, 2026)
- **CFTC:** New task force (March 2026) to regulate crypto/AI/prediction markets
- **Texas:** Has not legalized sports gambling; allows CFTC-regulated platforms

### 4.3 Risk Assessment

**Low-risk approach:** Use only CFTC-regulated venues (Kalshi). Avoid Polymarket if regulatory clarity is paramount.

**Realistic approach:** Polymarket offers better liquidity and shorter durations; acceptable risk for a hobby/project if no capital beyond what you can lose.

**⚠️ DISCLAIMER:** This is not legal advice. Consult a licensed attorney in Texas before trading.

---

## 5. Cross-Venue Arbitrage Potential

### 5.1 Opportunity Types

1. **CEX → PM Gap:** Binance/Coinbase price moves → Polymarket/Kalshi lags (original strategy)
2. **Polymarket ↔ Kalshi Delta:** Different pricing on same underlying (rare, quickly arbitraged)
3. **Temporal Arbitrage:** 5-min (Polymarket) vs. 15-min (Kalshi) contracts on same asset

### 5.2 Feasibility

- Cross-venue opportunities exist but are **quickly competed away**
- Requires simultaneous access to both order books
- Transaction costs compound across venues
- **Recommendation:** Focus on single-venue first; add cross-venue only after proving single-venue profitability

---

## 6. Go / No-Go Recommendation

### ✅ GO — With Conditions

| Condition | Rationale |
|-----------|-----------|
| **Paper trading first** | Live results show -13% to -50% ROI without extensive testing |
| **Start small** | $100–$500 max |
| **Single venue** | Polymarket only initially |
| **Conservative risk limits** | Kelly fraction ≤8%, daily loss -20%, max drawdown -40% |
| **6-month evaluation** | Reassess after 200+ paper trades |

### ❌ NO-GO Triggers

- Live win rate <40% after 200 paper trades
- Regulatory enforcement against Polymarket in US
- Fee increases beyond 2%

### Alternative Strategy (If No-Go)

If latency arbitrage proves unviable, consider:
1. **Directional momentum trading** (not pure arbitrage) with longer timeframes
2. **Liquidity providing** (maker rebates) on Polymarket
3. **Meta-strategy:** Sell signals to other traders (no capital at risk)

---

## 7. Recommended Next Steps

1. **Confirm this feasibility report** — Approve to proceed or pivot
2. **If approved → Phase 2:** Build Elixir/OTP system for Polymarket only
3. **Minimum paper trading period:** 7 days or 200 trades
4. **Target metrics for live:**
   - Win rate ≥55%
   - Positive expectancy after fees
   - Max drawdown <20%

---

## 8. Appendix: Sources

- Polymarket fee structure: crypto.news, phemex.com (March 2026)
- Live trading results: Liu, "AI-Augmented Arbitrage in Short-Duration Prediction Markets" (Medium, March 2026)
- Volume data: cryptorank.io, crypto.news
- Kalshi regulation: European Business Magazine, Better Markets
- Coinbase Predictions: defirate.com, cryptotimes.io
- Legal: Stateline.org, ESPN, StockTwits
- Infrastructure: AlphaEx Capital, AIFinanceBites, MamboServer

---

*This report is for informational purposes only. Not financial or legal advice. Past performance does not guarantee future results. You may lose all capital deployed.*