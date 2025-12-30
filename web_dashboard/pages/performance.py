"""
Performance Analytics Page - Comprehensive performance analysis and visualizations

Enhanced with Phase 4.3.3 & 4.3.4 features:
- Date range selector with presets
- Rolling returns analysis
- Benchmark comparison
- Calendar heatmap
- Interactive zoomable charts
- Win rate with confidence intervals
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import sys
from pathlib import Path

# Add parent for theme imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from web_dashboard.theme import COLORS  # noqa: E402


def show():
    st.title("Performance Analytics")

    # Date range selector with presets (Phase 4.3.3)
    st.markdown("#### Select Date Range")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        btn_7d = st.button("7D", use_container_width=True, key="range_7d")
    with col2:
        btn_30d = st.button("30D", use_container_width=True, key="range_30d")
    with col3:
        btn_90d = st.button("90D", use_container_width=True, key="range_90d")
    with col4:
        btn_ytd = st.button("YTD", use_container_width=True, key="range_ytd")
    with col5:
        btn_all = st.button("All", use_container_width=True, key="range_all")
    with col6:
        custom_range = st.button("Custom", use_container_width=True, key="range_custom")

    # Determine selected period
    if 'selected_period' not in st.session_state:
        st.session_state.selected_period = '30D'

    if btn_7d:
        st.session_state.selected_period = '7D'
    elif btn_30d:
        st.session_state.selected_period = '30D'
    elif btn_90d:
        st.session_state.selected_period = '90D'
    elif btn_ytd:
        st.session_state.selected_period = 'YTD'
    elif btn_all:
        st.session_state.selected_period = 'All'

    period = st.session_state.selected_period

    # Period to days mapping
    period_days = {
        '7D': 7,
        '30D': 30,
        '90D': 90,
        'YTD': (datetime.now() - datetime(datetime.now().year, 1, 1)).days,
        'All': 365
    }
    days = period_days.get(period, 30)

    # Custom date range
    if custom_range:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        days = (end_date - start_date).days

    st.markdown("---")

    # Generate demo data based on period
    np.random.seed(42)  # Consistent demo data
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    # Equity curve data
    initial_capital = 100000
    daily_returns = np.random.normal(0.002, 0.015, days)  # 0.2% avg, 1.5% std
    equity = initial_capital * (1 + daily_returns).cumprod()

    # Benchmark (Nifty) returns
    nifty_returns = np.random.normal(0.001, 0.012, days)  # Slightly lower
    nifty_equity = initial_capital * (1 + nifty_returns).cumprod()

    equity_df = pd.DataFrame({
        'Date': dates,
        'Equity': equity,
        'Nifty': nifty_equity,
        'Daily_Return': daily_returns * 100,
        'Nifty_Return': nifty_returns * 100
    })

    # Calculate rolling returns (Phase 4.3.3)
    equity_df['Rolling_7D'] = equity_df['Daily_Return'].rolling(7).sum()
    equity_df['Rolling_30D'] = equity_df['Daily_Return'].rolling(30).sum()
    equity_df['Rolling_90D'] = equity_df['Daily_Return'].rolling(min(90, days)).sum()

    # Drawdown calculation
    equity_df['Peak'] = equity_df['Equity'].cummax()
    equity_df['Drawdown'] = (equity_df['Equity'] - equity_df['Peak']) / equity_df['Peak'] * 100

    # Key Metrics with benchmark comparison
    st.subheader("Key Metrics")

    total_return = (equity[-1] / initial_capital - 1) * 100
    nifty_total_return = (nifty_equity[-1] / initial_capital - 1) * 100
    alpha = total_return - nifty_total_return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Return", f"{total_return:.2f}%", delta=f"{total_return:.1f}%")
        wins = len([r for r in daily_returns if r > 0])
        win_rate = (wins / len(daily_returns)) * 100 if len(daily_returns) > 0 else 0
        # Confidence interval (Phase 4.3.3)
        ci = 1.96 * np.sqrt(win_rate * (100 - win_rate) / max(len(daily_returns), 1))
        st.metric("Win Rate", f"{win_rate:.1f}%", help=f"95% CI: [{win_rate-ci:.1f}%, {win_rate+ci:.1f}%]")

    with col2:
        # Sharpe ratio calculation
        sharpe = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252) if np.std(daily_returns) > 0 else 0
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        # Profit factor
        wins_sum = sum([r for r in daily_returns * initial_capital if r > 0])
        losses_sum = abs(sum([r for r in daily_returns * initial_capital if r < 0]))
        profit_factor = wins_sum / losses_sum if losses_sum > 0 else 0
        st.metric("Profit Factor", f"{profit_factor:.2f}")

    with col3:
        max_dd = equity_df['Drawdown'].min()
        st.metric("Max Drawdown", f"{max_dd:.2f}%", delta_color="inverse")
        st.metric("Vs Nifty (Alpha)", f"{alpha:+.2f}%",
                 delta="Outperform" if alpha > 0 else "Underperform")

    with col4:
        # Rolling returns display
        latest_7d = equity_df['Rolling_7D'].iloc[-1] if len(equity_df) > 7 else 0
        latest_30d = equity_df['Rolling_30D'].iloc[-1] if len(equity_df) > 30 else 0
        st.metric("7-Day Rolling", f"{latest_7d:.2f}%")
        st.metric("30-Day Rolling", f"{latest_30d:.2f}%")

    st.markdown("---")

    # Interactive Equity Curve (Phase 4.3.4)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Equity Curve vs Benchmark")

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.75, 0.25],
            subplot_titles=("Equity vs Nifty", "Drawdown %")
        )

        # Portfolio equity
        fig.add_trace(
            go.Scatter(
                x=equity_df['Date'],
                y=equity_df['Equity'],
                mode='lines',
                name='Portfolio',
                line=dict(color=COLORS['profit'], width=2),
                hovertemplate='Date: %{x}<br>Equity: ₹%{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )

        # Nifty benchmark
        fig.add_trace(
            go.Scatter(
                x=equity_df['Date'],
                y=equity_df['Nifty'],
                mode='lines',
                name='Nifty',
                line=dict(color=COLORS['info'], width=2, dash='dash'),
                hovertemplate='Date: %{x}<br>Nifty: ₹%{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )

        # Initial capital line
        fig.add_hline(y=initial_capital, line_dash="dot", line_color=COLORS['text_muted'],
                     annotation_text="Initial Capital", row=1, col=1)

        # Drawdown overlay (Phase 4.3.4)
        fig.add_trace(
            go.Scatter(
                x=equity_df['Date'],
                y=equity_df['Drawdown'],
                mode='lines',
                name='Drawdown',
                line=dict(color=COLORS['loss'], width=1),
                fill='tozeroy',
                fillcolor='rgba(239, 68, 68, 0.2)',
                hovertemplate='Date: %{x}<br>Drawdown: %{y:.2f}%<extra></extra>'
            ),
            row=2, col=1
        )

        # Configure for zoom and pan (Phase 4.3.4)
        fig.update_layout(
            height=500,
            showlegend=True,
            legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)'),
            hovermode='x unified',
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                gridcolor='rgba(51, 65, 85, 0.3)',
                rangeslider=dict(visible=True, thickness=0.05),  # Zoomable
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="7D", step="day", stepmode="backward"),
                        dict(count=30, label="30D", step="day", stepmode="backward"),
                        dict(count=90, label="90D", step="day", stepmode="backward"),
                        dict(step="all", label="All")
                    ]),
                    bgcolor=COLORS['bg_secondary'],
                    activecolor=COLORS['accent_primary'],
                    font=dict(color=COLORS['text_primary'])
                )
            ),
            yaxis=dict(gridcolor='rgba(51, 65, 85, 0.3)'),
            xaxis2=dict(gridcolor='rgba(51, 65, 85, 0.3)'),
            yaxis2=dict(gridcolor='rgba(51, 65, 85, 0.3)')
        )

        # Enable chart config for export (Phase 4.3.4)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'equity_curve',
                    'height': 600,
                    'width': 1200,
                    'scale': 2
                },
                'displayModeBar': True,
                'modeBarButtonsToAdd': ['drawline', 'eraseshape']
            }
        )

    with col2:
        st.subheader("Rolling Returns")

        # Rolling returns chart
        fig_roll = go.Figure()

        fig_roll.add_trace(go.Scatter(
            x=equity_df['Date'],
            y=equity_df['Rolling_7D'],
            mode='lines',
            name='7-Day',
            line=dict(color=COLORS['info'], width=2)
        ))

        fig_roll.add_trace(go.Scatter(
            x=equity_df['Date'],
            y=equity_df['Rolling_30D'],
            mode='lines',
            name='30-Day',
            line=dict(color=COLORS['profit'], width=2)
        ))

        fig_roll.add_hline(y=0, line_dash="dash", line_color=COLORS['text_muted'])

        fig_roll.update_layout(
            height=250,
            showlegend=True,
            legend=dict(orientation='h', y=1.15),
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(51, 65, 85, 0.3)'),
            yaxis=dict(gridcolor='rgba(51, 65, 85, 0.3)', title='Return %')
        )

        st.plotly_chart(fig_roll, use_container_width=True)

        # Win rate confidence interval display
        st.markdown("#### Win Rate Analysis")
        st.markdown(f"""
        <div style="background: {COLORS['bg_secondary']}; padding: 1rem; border-radius: 8px;">
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['text_primary']};">{win_rate:.1f}%</div>
            <div style="font-size: 0.875rem; color: {COLORS['text_muted']};">
                95% CI: [{max(0, win_rate-ci):.1f}%, {min(100, win_rate+ci):.1f}%]
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Calendar Heatmap (Phase 4.3.3)
    st.subheader("Daily P&L Calendar Heatmap")

    # Prepare calendar data
    equity_df['DayOfWeek'] = pd.to_datetime(equity_df['Date']).dt.dayofweek
    equity_df['Week'] = pd.to_datetime(equity_df['Date']).dt.isocalendar().week
    equity_df['Month'] = pd.to_datetime(equity_df['Date']).dt.month
    equity_df['Year'] = pd.to_datetime(equity_df['Date']).dt.year

    # Group by month for heatmap
    monthly_returns = equity_df.groupby(['Year', 'Month'])['Daily_Return'].sum().reset_index()

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = sorted(monthly_returns['Year'].unique())

    # Create heatmap matrix
    heatmap_data = np.zeros((len(years), 12))
    for _, row in monthly_returns.iterrows():
        year_idx = years.index(row['Year'])
        month_idx = int(row['Month']) - 1
        heatmap_data[year_idx][month_idx] = row['Daily_Return']

    fig_cal = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=months,
        y=[str(y) for y in years],
        colorscale=[
            [0, COLORS['loss']],
            [0.5, COLORS['bg_secondary']],
            [1, COLORS['profit']]
        ],
        zmid=0,
        text=[[f"{v:.1f}%" for v in row] for row in heatmap_data],
        texttemplate='%{text}',
        textfont={"size": 11},
        colorbar=dict(title="Return %", ticksuffix='%'),
        hovertemplate='%{y} %{x}<br>Return: %{z:.2f}%<extra></extra>'
    ))

    fig_cal.update_layout(
        height=150 * len(years),
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_cal, use_container_width=True)

    st.markdown("---")

    # Performance by Time Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Performance by Hour of Day")

        hours = list(range(9, 16))
        avg_pnl = [300, 450, 200, -100, 350, 500, 250]
        hour_win_rates = [70, 65, 55, 45, 68, 72, 60]

        fig_hour = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.5, 0.5]
        )

        colors = [COLORS['profit'] if x > 0 else COLORS['loss'] for x in avg_pnl]
        fig_hour.add_trace(
            go.Bar(x=hours, y=avg_pnl, name='Avg P&L', marker_color=colors),
            row=1, col=1
        )

        fig_hour.add_trace(
            go.Scatter(x=hours, y=hour_win_rates, mode='lines+markers',
                      name='Win Rate', line=dict(color=COLORS['info'], width=2)),
            row=2, col=1
        )

        fig_hour.add_hline(y=50, line_dash="dash", line_color=COLORS['text_muted'], row=2, col=1)

        fig_hour.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_hour.update_xaxes(title_text="Hour", row=2, col=1)
        fig_hour.update_yaxes(title_text="Avg P&L (₹)", row=1, col=1, gridcolor='rgba(51, 65, 85, 0.3)')
        fig_hour.update_yaxes(title_text="Win Rate %", row=2, col=1, gridcolor='rgba(51, 65, 85, 0.3)')

        st.plotly_chart(fig_hour, use_container_width=True)

    with col2:
        st.subheader("Strategy Performance")

        strategies = ['Supertrend', 'Breakout', 'Mean Reversion', 'ORB', 'Iron Condor']
        returns = [12.5, 8.3, 15.2, 6.8, 10.1]
        trades = [25, 18, 30, 15, 12]
        strat_win_rates = [68, 61, 72, 55, 70]

        strategy_df = pd.DataFrame({
            'Strategy': strategies,
            'Return %': returns,
            'Trades': trades,
            'Win Rate %': strat_win_rates
        })

        fig_strat = go.Figure()

        fig_strat.add_trace(go.Bar(
            x=strategies,
            y=returns,
            name='Return %',
            marker_color=[COLORS['profit'] if r > 10 else COLORS['info'] for r in returns],
            text=[f'{r:.1f}%' for r in returns],
            textposition='outside'
        ))

        fig_strat.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='rgba(51, 65, 85, 0.3)', title='Return %')
        )

        st.plotly_chart(fig_strat, use_container_width=True)

        st.dataframe(
            strategy_df.style.background_gradient(
                subset=['Return %'],
                cmap='RdYlGn',
                vmin=0,
                vmax=20
            ),
            hide_index=True,
            use_container_width=True
        )

    st.markdown("---")

    # Recent Trades with hover details (Phase 4.3.4)
    st.subheader("Recent Trades")

    trades_data = {
        'Date': [datetime.now() - timedelta(days=i) for i in range(10)],
        'Instrument': ['NIFTY CE', 'BANKNIFTY PE', 'NIFTY CE', 'FINNIFTY CE', 'NIFTY PE',
                       'BANKNIFTY CE', 'NIFTY CE', 'MIDCPNIFTY PE', 'NIFTY CE', 'BANKNIFTY PE'],
        'Direction': ['LONG', 'SHORT', 'LONG', 'LONG', 'SHORT', 'LONG', 'SHORT', 'LONG', 'LONG', 'SHORT'],
        'Entry': [250, 180, 245, 120, 190, 310, 255, 95, 260, 175],
        'Exit': [275, 160, 230, 135, 185, 335, 240, 105, 280, 165],
        'P&L': [1250, 500, -750, 750, 250, 1250, -750, 500, 1000, 250],
        'Return %': [10.0, 11.1, -6.1, 12.5, 2.6, 8.1, -5.9, 10.5, 7.7, 5.7],
        'Strategy': ['Supertrend', 'Iron Condor', 'Breakout', 'ORB', 'Mean Rev',
                    'Supertrend', 'Breakout', 'ORB', 'Supertrend', 'Iron Condor']
    }

    trades_df = pd.DataFrame(trades_data)
    trades_df['Date'] = trades_df['Date'].dt.strftime('%Y-%m-%d')

    def style_pnl(row):
        if row['P&L'] > 0:
            return [f'background-color: rgba(34, 197, 94, 0.2); color: {COLORS["profit"]}'] * len(row)
        elif row['P&L'] < 0:
            return [f'background-color: rgba(239, 68, 68, 0.2); color: {COLORS["loss"]}'] * len(row)
        return [''] * len(row)

    st.dataframe(
        trades_df.style.apply(style_pnl, axis=1),
        hide_index=True,
        use_container_width=True
    )

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("**Avg Hold Time:** 4.5 hours")
    with col2:
        st.info(f"**Best Trade:** ₹{max(trades_data['P&L']):,}")
    with col3:
        st.info(f"**Worst Trade:** ₹{min(trades_data['P&L']):,}")
    with col4:
        st.info("**Consecutive Wins:** 3")

    # Export buttons
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Report", use_container_width=True):
            st.success("Report generated successfully!")

    with col2:
        export_df = equity_df[['Date', 'Equity', 'Nifty', 'Daily_Return', 'Drawdown']].copy()
        st.download_button(
            "Export Data",
            export_df.to_csv(index=False),
            "performance_data.csv",
            "text/csv",
            use_container_width=True
        )
