# 📈 Black-Scholes Option Pricing Dashboard

Interactive Streamlit app to price **European call & put options** using:
- **Black-Scholes closed-form**
- **Monte Carlo simulation** (10k paths)

It lets you explore how **spot (S)**, **volatility (σ)**, **time to maturity (T)**, **strike (K)**, and **risk-free rate (r)** affect prices and **P&L** through heatmaps and payoff charts.

## Live Demo
https://blackscholesappapp-d2dyuzgvzpu3acdsqmk9xi.streamlit.app

## What’s inside the app:
- **Theoretical prices** (Call & Put) via Black-Scholes  
- **Monte Carlo** prices for comparison  
- **Option Price Heatmaps** (price vs Spot & Vol)  
- **P&L Heatmaps** (model price − purchase price)  
- **P&L line charts at expiry** with strike & breakeven markers  
- Sidebar controls for all inputs and heatmap ranges

## How it works in short:
- **Black-Scholes** computes today’s fair value with a closed formula.
- **Monte Carlo** simulates many possible end prices using Geometric Brownian Motion, takes the average discounted payoff.
- **P&L** = (model price) − (your purchase price). Heatmaps/lines show where you’d profit (green) or lose (red).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
