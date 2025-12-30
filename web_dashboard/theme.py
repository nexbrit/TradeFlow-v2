"""
TradeFlow Theme Configuration

Professional color scheme and styling for the F&O trading dashboard.
Based on Phase 4.1 requirements from DEVELOPMENT_ROADMAP.md.
"""

# Color Palette
COLORS = {
    # Background colors
    'bg_primary': '#0f172a',      # Dark Navy
    'bg_secondary': '#1e293b',    # Slate
    'bg_accent': '#334155',       # Lighter Slate
    'bg_card': '#1e293b',         # Card background

    # Text colors
    'text_primary': '#f1f5f9',    # Light
    'text_secondary': '#94a3b8',  # Muted
    'text_muted': '#64748b',      # More muted

    # Status colors
    'profit': '#22c55e',          # Green
    'loss': '#ef4444',            # Red
    'warning': '#f59e0b',         # Amber
    'info': '#3b82f6',            # Blue
    'neutral': '#6b7280',         # Gray

    # Accent colors
    'accent_primary': '#3b82f6',  # Blue
    'accent_secondary': '#8b5cf6', # Purple

    # Border colors
    'border_light': '#334155',
    'border_dark': '#1e293b',
}

# Typography
TYPOGRAPHY = {
    'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    'font_mono': "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",

    # Font sizes
    'h1': '2.5rem',
    'h2': '2rem',
    'h3': '1.5rem',
    'h4': '1.25rem',
    'body': '1rem',
    'small': '0.875rem',
    'tiny': '0.75rem',
}

# Component styles
COMPONENTS = {
    'border_radius': '8px',
    'border_radius_lg': '12px',
    'shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'shadow_lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
}


def get_custom_css() -> str:
    """
    Generate custom CSS for Streamlit dashboard.

    Returns:
        CSS string to inject into Streamlit
    """
    return f"""
    <style>
    /* Global styles */
    .stApp {{
        background-color: {COLORS['bg_primary']};
    }}

    /* Main content area */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}

    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']} !important;
        font-family: {TYPOGRAPHY['font_family']};
    }}

    h1 {{
        font-size: {TYPOGRAPHY['h1']} !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }}

    h2 {{
        font-size: {TYPOGRAPHY['h2']} !important;
        font-weight: 600 !important;
    }}

    h3 {{
        font-size: {TYPOGRAPHY['h3']} !important;
        font-weight: 600 !important;
    }}

    /* Body text */
    p, span, div {{
        color: {COLORS['text_secondary']};
    }}

    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-family: {TYPOGRAPHY['font_mono']};
        font-size: 1.75rem !important;
        color: {COLORS['text_primary']} !important;
    }}

    [data-testid="stMetricDelta"] {{
        font-family: {TYPOGRAPHY['font_mono']};
    }}

    [data-testid="stMetricLabel"] {{
        color: {COLORS['text_secondary']} !important;
        font-size: {TYPOGRAPHY['small']} !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Cards and containers */
    .metric-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border_light']};
        padding: 1.25rem;
        border-radius: {COMPONENTS['border_radius']};
        margin-bottom: 1rem;
    }}

    /* Profit/Loss styling */
    .profit {{
        color: {COLORS['profit']} !important;
    }}

    .loss {{
        color: {COLORS['loss']} !important;
    }}

    .warning {{
        color: {COLORS['warning']} !important;
    }}

    /* Connection status indicators */
    .connection-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }}

    .connected {{
        background-color: {COLORS['profit']};
        box-shadow: 0 0 8px {COLORS['profit']};
    }}

    .disconnected {{
        background-color: {COLORS['loss']};
        box-shadow: 0 0 8px {COLORS['loss']};
    }}

    .reconnecting {{
        background-color: {COLORS['warning']};
        box-shadow: 0 0 8px {COLORS['warning']};
        animation: pulse 1s infinite;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}

    /* Token warning banners */
    .token-warning {{
        background: linear-gradient(135deg, {COLORS['warning']} 0%, #d97706 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: {COMPONENTS['border_radius']};
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .token-expired {{
        background: linear-gradient(135deg, {COLORS['loss']} 0%, #dc2626 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: {COMPONENTS['border_radius']};
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* Market overview strip */
    .market-strip {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border_light']};
        border-radius: {COMPONENTS['border_radius']};
        padding: 0.75rem 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }}

    .market-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .market-label {{
        font-size: {TYPOGRAPHY['tiny']};
        color: {COLORS['text_muted']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .market-value {{
        font-size: 1.125rem;
        font-weight: 600;
        font-family: {TYPOGRAPHY['font_mono']};
        color: {COLORS['text_primary']};
    }}

    .market-change {{
        font-size: {TYPOGRAPHY['small']};
        font-family: {TYPOGRAPHY['font_mono']};
    }}

    .market-change.positive {{
        color: {COLORS['profit']};
    }}

    .market-change.negative {{
        color: {COLORS['loss']};
    }}

    /* Account summary card */
    .account-card {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_accent']} 100%);
        border: 1px solid {COLORS['border_light']};
        border-radius: {COMPONENTS['border_radius_lg']};
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}

    .account-capital {{
        font-size: 2.5rem;
        font-weight: 700;
        font-family: {TYPOGRAPHY['font_mono']};
        color: {COLORS['text_primary']};
    }}

    .account-label {{
        font-size: {TYPOGRAPHY['small']};
        color: {COLORS['text_muted']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Portfolio heat gauge */
    .heat-gauge {{
        height: 8px;
        background: {COLORS['bg_accent']};
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.5rem;
    }}

    .heat-fill {{
        height: 100%;
        transition: width 0.3s ease, background-color 0.3s ease;
    }}

    .heat-safe {{ background: {COLORS['profit']}; }}
    .heat-caution {{ background: {COLORS['warning']}; }}
    .heat-danger {{ background: {COLORS['loss']}; }}

    /* Positions table enhancements */
    .positions-table {{
        width: 100%;
        border-collapse: collapse;
    }}

    .positions-table th {{
        background: {COLORS['bg_accent']};
        color: {COLORS['text_secondary']};
        font-size: {TYPOGRAPHY['small']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid {COLORS['border_light']};
    }}

    .positions-table td {{
        padding: 0.75rem;
        border-bottom: 1px solid {COLORS['border_dark']};
        font-family: {TYPOGRAPHY['font_mono']};
        font-size: {TYPOGRAPHY['small']};
    }}

    .positions-table tr:hover {{
        background: {COLORS['bg_accent']};
    }}

    /* Badge styles */
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: {TYPOGRAPHY['tiny']};
        font-weight: 500;
        text-transform: uppercase;
    }}

    .badge-ce {{
        background: rgba(59, 130, 246, 0.2);
        color: {COLORS['info']};
    }}

    .badge-pe {{
        background: rgba(239, 68, 68, 0.2);
        color: {COLORS['loss']};
    }}

    .badge-fut {{
        background: rgba(139, 92, 246, 0.2);
        color: {COLORS['accent_secondary']};
    }}

    /* Circuit breaker indicator */
    .circuit-breaker {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border_light']};
        border-radius: {COMPONENTS['border_radius']};
        padding: 1rem;
        margin-bottom: 1rem;
    }}

    .circuit-breaker.triggered {{
        border-color: {COLORS['loss']};
        background: rgba(239, 68, 68, 0.1);
    }}

    .circuit-breaker.warning {{
        border-color: {COLORS['warning']};
        background: rgba(245, 158, 11, 0.1);
    }}

    /* Last updated timestamp */
    .last-updated {{
        font-size: {TYPOGRAPHY['tiny']};
        color: {COLORS['text_muted']};
        text-align: right;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['bg_secondary']};
    }}

    [data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
    }}

    /* Dataframe styling */
    .stDataFrame {{
        border: 1px solid {COLORS['border_light']};
        border-radius: {COMPONENTS['border_radius']};
    }}

    /* Button styling */
    .stButton > button {{
        background-color: {COLORS['accent_primary']};
        color: white;
        border: none;
        border-radius: {COMPONENTS['border_radius']};
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }}

    .stButton > button:hover {{
        background-color: #2563eb;
    }}

    /* Emergency button */
    .emergency-btn {{
        background: linear-gradient(135deg, {COLORS['loss']} 0%, #dc2626 100%) !important;
    }}

    .emergency-btn:hover {{
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
    }}

    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: {COLORS['bg_secondary']};
        border-radius: {COMPONENTS['border_radius']};
    }}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: {COLORS['bg_secondary']};
        border-radius: {COMPONENTS['border_radius']};
        color: {COLORS['text_secondary']};
        padding: 0.5rem 1rem;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['accent_primary']};
        color: white;
    }}
    </style>
    """


def format_currency(value: float, prefix: str = "₹") -> str:
    """Format value as Indian currency with proper formatting."""
    if abs(value) >= 10000000:  # 1 crore
        return f"{prefix}{value/10000000:.2f} Cr"
    elif abs(value) >= 100000:  # 1 lakh
        return f"{prefix}{value/100000:.2f} L"
    elif abs(value) >= 1000:
        return f"{prefix}{value:,.0f}"
    else:
        return f"{prefix}{value:.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage."""
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def get_pnl_color(value: float) -> str:
    """Get appropriate color for P&L value."""
    if value > 0:
        return COLORS['profit']
    elif value < 0:
        return COLORS['loss']
    return COLORS['neutral']


def get_heat_level(heat_pct: float) -> str:
    """Get heat level CSS class based on portfolio heat percentage."""
    if heat_pct <= 3:
        return 'heat-safe'
    elif heat_pct <= 5:
        return 'heat-caution'
    return 'heat-danger'


def render_market_strip(nifty: dict, banknifty: dict, vix: dict, market_status: str) -> str:
    """
    Render market overview strip HTML.

    Args:
        nifty: Dict with 'value' and 'change' keys
        banknifty: Dict with 'value' and 'change' keys
        vix: Dict with 'value' and 'change' keys
        market_status: Market status string (Pre-open/Open/Closed)

    Returns:
        HTML string for market strip
    """
    def change_class(change: float) -> str:
        return 'positive' if change >= 0 else 'negative'

    return f"""
    <div class="market-strip">
        <div class="market-item">
            <span class="market-label">Nifty 50</span>
            <span class="market-value">{nifty.get('value', 0):,.2f}</span>
            <span class="market-change {change_class(nifty.get('change', 0))}">
                {format_percentage(nifty.get('change', 0))}
            </span>
        </div>
        <div class="market-item">
            <span class="market-label">Bank Nifty</span>
            <span class="market-value">{banknifty.get('value', 0):,.2f}</span>
            <span class="market-change {change_class(banknifty.get('change', 0))}">
                {format_percentage(banknifty.get('change', 0))}
            </span>
        </div>
        <div class="market-item">
            <span class="market-label">India VIX</span>
            <span class="market-value">{vix.get('value', 0):.2f}</span>
            <span class="market-change {change_class(vix.get('change', 0))}">
                {format_percentage(vix.get('change', 0))}
            </span>
        </div>
        <div class="market-item">
            <span class="market-label">Market</span>
            <span class="market-value" style="font-size: 0.875rem;">{market_status}</span>
        </div>
    </div>
    """


def render_account_summary(
    capital: float,
    daily_pnl: float,
    daily_pnl_pct: float,
    positions_count: int,
    margin_used: float,
    margin_available: float,
    portfolio_heat: float
) -> str:
    """
    Render account summary card HTML.

    Returns:
        HTML string for account summary
    """
    pnl_color = get_pnl_color(daily_pnl)
    pnl_sign = "+" if daily_pnl > 0 else ""
    heat_class = get_heat_level(portfolio_heat)

    return f"""
    <div class="account-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div>
                <span class="account-label">Total Capital</span>
                <div class="account-capital">{format_currency(capital)}</div>
            </div>
            <div style="text-align: right;">
                <span class="account-label">Day's P&L</span>
                <div style="font-size: 1.5rem; font-weight: 600; color: {pnl_color};">
                    {pnl_sign}{format_currency(daily_pnl)} ({format_percentage(daily_pnl_pct)})
                </div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
            <div>
                <span class="account-label">Open Positions</span>
                <div style="font-size: 1.25rem; font-weight: 600; color: #f1f5f9;">{positions_count}</div>
            </div>
            <div>
                <span class="account-label">Margin Used</span>
                <div style="font-size: 1.25rem; font-weight: 600; color: #f1f5f9;">{format_currency(margin_used)}</div>
            </div>
            <div>
                <span class="account-label">Available</span>
                <div style="font-size: 1.25rem; font-weight: 600; color: #f1f5f9;">{format_currency(margin_available)}</div>
            </div>
            <div>
                <span class="account-label">Portfolio Heat</span>
                <div style="font-size: 1.25rem; font-weight: 600; color: #f1f5f9;">{portfolio_heat:.1f}%</div>
                <div class="heat-gauge">
                    <div class="heat-fill {heat_class}" style="width: {min(portfolio_heat / 6 * 100, 100)}%;"></div>
                </div>
            </div>
        </div>
    </div>
    """
