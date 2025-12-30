# 🚀 Launching TradeFlow v2 Web Dashboard

## Quick Start

```bash
python launch_dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## What You'll See

### 📊 Main Dashboard
- Real-time account overview
- Active positions tracking
- Live trading signals feed
- Economic calendar events
- Trading rules status
- Interactive equity curve

### 📈 Trading Signals Page
- Multi-instrument monitoring (NIFTY, BANKNIFTY, FINNIFTY, etc.)
- Timeframe selection (1min to 1day)
- Signal strength filtering
- Interactive candlestick charts with indicators
- Signal history tracking

### 🎯 Strategy Builder Page
Choose from three strategy types:

1. **Options Strategies** (7 pre-built):
   - Iron Condor
   - Bull/Bear Call Spreads
   - Bull/Bear Put Spreads
   - Long/Short Straddle
   - Long/Short Strangle

2. **Directional Strategies** (5 types):
   - Supertrend Following
   - Breakout Trading
   - Mean Reversion
   - Opening Range Breakout (ORB)
   - Support/Resistance Trading

3. **Custom Spread Builder**:
   - Multi-leg options combinations
   - Interactive payoff diagrams
   - Real-time P&L calculations
   - Risk:Reward analysis

### 📊 Performance Analytics
- Comprehensive metrics (Win Rate, Sharpe Ratio, Profit Factor)
- Interactive charts:
  - Equity curve with drawdown overlay
  - Monthly returns heatmap
  - P&L distribution histogram
  - Hourly performance analysis
  - Strategy comparison
- Recent trades table with filters
- Summary statistics

## Controls

- **Keyboard**: Press `Ctrl+C` in terminal to stop the server
- **Browser**: Refresh to see code changes
- **Auto-reload**: Dashboard automatically reloads on file changes

## Troubleshooting

### Dashboard won't start
```bash
# Make sure streamlit is installed
python -m pip install streamlit

# Try running directly
python -m streamlit run web_dashboard/app.py
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port already in use
```bash
# Use a different port
python -m streamlit run web_dashboard/app.py --server.port=8502
```

## Features

✅ Real-time data visualization
✅ Interactive strategy building
✅ Comprehensive analytics
✅ Economic calendar integration
✅ Position tracking
✅ Performance monitoring
✅ Risk management tools

## Next Steps

1. Configure your API credentials in `.env`
2. Customize strategies in the Strategy Builder
3. Monitor positions in real-time
4. Review performance analytics
5. Export data for further analysis

---

**TradeFlow v2** - Professional F&O Trading Platform
