import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from shared_db import run_query
from sidebar import render_sidebar

st.set_page_config(page_title="KPI Overview", page_icon="📊", layout="wide")
render_sidebar() 

# ── Adaptive CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0080ff, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.page-subtitle {
    font-size: 0.95rem;
    color: var(--text-color);
    opacity: 0.6;
    margin-bottom: 1.5rem;
}

.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #0080ff;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #0080ff22;
}

.kpi-card {
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-left: 4px solid transparent;
    background-color: var(--secondary-background-color);
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.kpi-card.blue   { border-left-color: #0080ff; }
.kpi-card.green  { border-left-color: #00b894; }
.kpi-card.red    { border-left-color: #e17055; }
.kpi-card.purple { border-left-color: #7b61ff; }
.kpi-card.orange { border-left-color: #f39c12; }
.kpi-card.teal   { border-left-color: #00cec9; }
.kpi-card.pink   { border-left-color: #e84393; }

.kpi-icon-wrap {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
}

.kpi-card.blue   .kpi-icon-wrap { background: #0080ff18; }
.kpi-card.green  .kpi-icon-wrap { background: #00b89418; }
.kpi-card.red    .kpi-icon-wrap { background: #e1705518; }
.kpi-card.purple .kpi-icon-wrap { background: #7b61ff18; }
.kpi-card.orange .kpi-icon-wrap { background: #f39c1218; }
.kpi-card.teal   .kpi-icon-wrap { background: #00cec918; }
.kpi-card.pink   .kpi-icon-wrap { background: #e8439318; }

.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.55;
    margin-bottom: 0.25rem;
    color: var(--text-color);
}

.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.kpi-card.blue   .kpi-value { color: #0080ff; }
.kpi-card.green  .kpi-value { color: #00b894; }
.kpi-card.red    .kpi-value { color: #e17055; }
.kpi-card.purple .kpi-value { color: #7b61ff; }
.kpi-card.orange .kpi-value { color: #f39c12; }
.kpi-card.teal   .kpi-value { color: #00cec9; }
.kpi-card.pink   .kpi-value { color: #e84393; }

.kpi-sub {
    font-size: 0.72rem;
    opacity: 0.45;
    color: var(--text-color);
    font-weight: 300;
}

.chart-wrap {
    background-color: var(--secondary-background-color);
    border-radius: 14px;
    padding: 1rem 1rem 0.5rem 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

.soft-divider {
    height: 1px;
    background: var(--text-color);
    opacity: 0.08;
    margin: 1.5rem 0;
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────
st.markdown('<div class="page-title">📊 Operations Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Real-time logistics performance metrics & insights</div>', unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────
with st.spinner("Loading metrics..."):
    kpi = run_query("""
        SELECT
            COUNT(*)                                                    AS total_shipments,
            ROUND(SUM(status='Delivered')*100.0/COUNT(*),2)            AS delivered_pct,
            ROUND(SUM(status='Cancelled')*100.0/COUNT(*),2)            AS cancelled_pct,
            ROUND(SUM(status='In Transit')*100.0/COUNT(*),2)           AS in_transit_pct,
            ROUND(AVG(DATEDIFF(delivery_date, order_date)),1)          AS avg_delivery_days
        FROM shipments
    """).iloc[0]

    cost = run_query("""
        SELECT
            ROUND(SUM(fuel_cost+labor_cost+misc_cost),2)   AS total_cost,
            ROUND(AVG(fuel_cost+labor_cost+misc_cost),2)   AS avg_cost
        FROM costs
    """).iloc[0]

    status_df   = run_query("SELECT status, COUNT(*) AS total FROM shipments GROUP BY status ORDER BY total DESC")
    trend_df    = run_query("SELECT DATE_FORMAT(order_date,'%Y-%m') AS month, COUNT(*) AS shipments FROM shipments GROUP BY month ORDER BY month")
    origins_df  = run_query("SELECT origin AS city, COUNT(*) AS shipments FROM shipments GROUP BY origin ORDER BY shipments DESC LIMIT 8")
    dest_df     = run_query("SELECT destination AS city, COUNT(*) AS shipments FROM shipments GROUP BY destination ORDER BY shipments DESC LIMIT 8")
    cost_df     = run_query("SELECT ROUND(SUM(fuel_cost),2) AS Fuel, ROUND(SUM(labor_cost),2) AS Labor, ROUND(SUM(misc_cost),2) AS Misc FROM costs").iloc[0]

# ── KPI Row 1 ──────────────────────────────────────────────────
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

row1 = [
    ("blue",   "📦", "Total Shipments",  f"{kpi['total_shipments']:,}",  "All time records"),
    ("green",  "✅", "Delivered",        f"{kpi['delivered_pct']}%",      "Successfully completed"),
    ("red",    "❌", "Cancelled",        f"{kpi['cancelled_pct']}%",      "Orders cancelled"),
    ("purple", "🚛", "In Transit",       f"{kpi['in_transit_pct']}%",     "Currently active"),
]
for col, (color, icon, label, value, sub) in zip(st.columns(4), row1):
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
            <div class="kpi-icon-wrap">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

row2 = [
    ("orange", "⏱️", "Avg Delivery Time",   f"{kpi['avg_delivery_days']} days", "Order to delivery"),
    ("teal",   "💰", "Total Op. Cost",       f"₹{cost['total_cost']:,.0f}",      "Fuel + Labor + Misc"),
    ("pink",   "📉", "Avg Cost / Shipment",  f"₹{cost['avg_cost']:,.2f}",        "Per shipment average"),
    ("blue",   "🏭", "Active Warehouses",    "50",                               "Across all regions"),
]
for col, (color, icon, label, value, sub) in zip(st.columns(4), row2):
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
            <div class="kpi-icon-wrap">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# ── Trend + Donut ──────────────────────────────────────────────
st.markdown('<div class="section-header">Shipment Trends</div>', unsafe_allow_html=True)
col_l, col_r = st.columns([1.7, 1])

with col_l:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_df['month'], y=trend_df['shipments'],
        mode='lines+markers',
        line=dict(color='#0080ff', width=2.5, shape='spline'),
        marker=dict(size=5, color='#0080ff'),
        fill='tozeroy', fillcolor='rgba(0,128,255,0.07)',
        hovertemplate='<b>%{x}</b><br>%{y:,} shipments<extra></extra>'
    ))
    fig_trend.update_layout(
        title=dict(text='Monthly Shipment Volume', font=dict(family='Syne', size=14)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', size=11),
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(gridcolor='rgba(128,128,128,0.15)'),
        margin=dict(l=0, r=0, t=40, b=0), height=280, showlegend=False
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        labels=status_df['status'], values=status_df['total'],
        hole=0.62,
        marker=dict(colors=['#00b894','#e17055','#0080ff','#f39c12'], line=dict(width=2)),
        textfont=dict(family='DM Sans', size=11),
        hovertemplate='<b>%{label}</b><br>%{value:,} shipments<br>%{percent}<extra></extra>'
    ))
    fig_donut.update_layout(
        title=dict(text='Status Distribution', font=dict(family='Syne', size=14)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', size=11),
        legend=dict(font=dict(size=10), bgcolor='rgba(0,0,0,0)', orientation='h', y=-0.15),
        margin=dict(l=0, r=0, t=40, b=0), height=280,
        annotations=[dict(
            text=f"<b>{kpi['total_shipments']:,}</b><br>total",
            x=0.5, y=0.5, font=dict(size=14, family='Syne'), showarrow=False
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# ── Origins & Destinations ─────────────────────────────────────
st.markdown('<div class="section-header">Geographic Distribution</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

for col, df, color_scale, title in [
    (col_a, origins_df, [[0,'#cce5ff'],[1,'#0080ff']], 'Top 8 Origins'),
    (col_b, dest_df,    [[0,'#e8e0ff'],[1,'#7b61ff']], 'Top 8 Destinations'),
]:
    with col:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        fig = px.bar(df, x='shipments', y='city', orientation='h',
            color='shipments', color_continuous_scale=color_scale,
            labels={'shipments':'','city':''}, title=title, text='shipments')
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', size=11),
            title=dict(font=dict(family='Syne', size=14)),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False,
            margin=dict(l=0, r=50, t=40, b=0), height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# ── Cost Breakdown ─────────────────────────────────────────────
st.markdown('<div class="section-header">Cost Breakdown</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
fig_cost = go.Figure(go.Bar(
    x=['⛽ Fuel Cost', '👷 Labor Cost', '📦 Misc Cost'],
    y=[cost_df['Fuel'], cost_df['Labor'], cost_df['Misc']],
    marker=dict(color=['#f39c12','#0080ff','#7b61ff'], line=dict(width=0)),
    text=[f"₹{v:,.0f}" for v in [cost_df['Fuel'], cost_df['Labor'], cost_df['Misc']]],
    textposition='outside',
    textfont=dict(family='Syne', size=13),
    hovertemplate='<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>'
))
fig_cost.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', size=12),
    yaxis=dict(gridcolor='rgba(128,128,128,0.15)', tickprefix='₹'),
    xaxis=dict(showgrid=False),
    margin=dict(l=0, r=0, t=20, b=0), height=260, showlegend=False
)
st.plotly_chart(fig_cost, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Smart Logistics Platform • Data refreshes every 60 seconds • Built with Streamlit + MySQL")