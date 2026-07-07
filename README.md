# Market Risk Analytics Platform

A small Python-based market risk analytics prototype built in Google Colab.

This project demonstrates a simplified market risk workflow, including portfolio pricing, market risk measurement, Historical VaR, VaR backtesting, stress testing, and Black-Scholes Greeks.

The goal is not to build a production-level bank risk system, but to show how financial risk concepts can be translated into reusable Python code.

---

## Repository Structure

```text
market_risk_project/
│
├── Notebook/
│   ├── 00_Builder_Setup.ipynb
│   ├── 01_Pricing_and_Market_Risk.ipynb
│   ├── 02_Historical_VaR.ipynb
│   └── 03_Derivatives_Pricing_Greeks.ipynb
│
├── data/
│   └── generated CSV outputs
│
└── src/
    ├── black_scholes.py
    ├── pricing_engine.py
    ├── risk_engine.py
    └── var_engine.py
```

---

## How to Read This Project

Recommended reading order:

1. `01_Pricing_and_Market_Risk.ipynb`
2. `02_Historical_VaR.ipynb`
3. `03_Derivatives_Pricing_Greeks.ipynb`

`00_Builder_Setup.ipynb` was mainly used during development to build reusable functions and classes. It is included for transparency, but it is not the best starting point for reading the final project.

---

## Project Overview

The project uses ETF market data to build a hypothetical portfolio and then applies common market risk analytics.

Assets used:

- SPY
- QQQ
- GLD
- BND
- VTI

Hypothetical portfolio:

| ETF | Shares |
|---|---:|
| SPY | 100 |
| QQQ | 80 |
| GLD | 50 |
| BND | 120 |
| VTI | 90 |

---

## Main Modules

### 1. Portfolio Pricing and Market Risk

This part builds the portfolio pricing and market risk workflow.

It calculates:

- Position values
- Total portfolio value
- Daily PnL
- Portfolio returns
- Cumulative return
- Portfolio weights
- Asset volatility
- Correlation matrix
- Covariance matrix
- Rolling volatility
- Return distribution statistics

Reusable source files:

```text
src/pricing_engine.py
src/risk_engine.py
```

---

### 2. Historical VaR, Backtesting, and Stress Testing

This part estimates portfolio downside risk using Historical VaR.

Historical VaR is treated as one-tail left-tail risk:

```python
95% VaR = quantile(0.05)
99% VaR = quantile(0.01)
```

It also includes VaR backtesting and stress testing.

VaR backtesting checks whether actual daily losses exceed the VaR threshold too often.

Stress testing scenarios include:

- Equity Market Crash
- Technology Selloff
- Interest Rate Shock
- Flight to Safety
- Broad Market Rally

Reusable source file:

```text
src/var_engine.py
```

---

### 3. Derivatives Pricing and Greeks

This part extends the project from linear ETF portfolio risk to nonlinear derivative risk.

It prices a European call option on SPY using the Black-Scholes model and calculates:

- Option price
- Delta
- Gamma
- Vega
- Theta
- Rho

Reusable source file:

```text
src/black_scholes.py
```

Greeks show how option value changes when market risk factors move, such as underlying price, volatility, time, and interest rates.

---

## Tech Stack

- Python
- pandas
- numpy
- scipy
- yfinance
- matplotlib
- Google Colab

---

## Why This Project Matters

This project shows a simplified end-to-end market risk workflow:

```text
Market Data
→ Portfolio Pricing
→ PnL and Returns
→ Volatility / Correlation / Covariance
→ Historical VaR
→ VaR Backtesting
→ Stress Testing
→ Black-Scholes Greeks
```

It connects financial risk concepts with reusable Python implementation.

The project is relevant to discussions around:

- Market risk analytics
- Portfolio valuation
- PV engine logic
- VaR and backtesting
- Stress testing
- Derivatives pricing
- Risk factor sensitivity

---

## Limitations

This is a simplified prototype, not a production-level bank risk system.

It does not include:

- Real trading system integration
- Database architecture
- Full FRTB implementation
- CCR / CVA engine
- Large-scale distributed computation
- Complex derivatives portfolio

The purpose is to demonstrate structure, learning ability, and financial risk understanding.

---

## Interview Summary

This is a small market risk analytics platform built in Python.

It starts from ETF market data, builds a hypothetical portfolio, calculates portfolio value and risk metrics, estimates Historical VaR, performs backtesting and stress testing, and finally adds Black-Scholes Greeks for derivative risk.

The project is not intended to replicate a full bank-level risk system. Instead, it shows my ability to structure market risk concepts into reusable Python modules.
