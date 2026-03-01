import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from shared_db import run_query
from sidebar import render_sidebar

#  Page Config 
st.set_page_config(page_title="Cost Analytics", page_icon="💰", layout="wide")
render_sidebar()

#  CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f39c12, #e17055);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.95rem;
    opacity: 0.55;
    color: var(--text-color);
    margin-bottom: 1.5rem;
}
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #f39c12;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #f39c1222;
}
.kpi-card {
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    border-left: 4px solid transparent;
    background-color: var(--secondary-background-color);
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-card.orange { border-left-color: #f39c12; }
.kpi-card.red    { border-left-color: #e17055; }
.kpi-card.blue   { border-left-color: #0080ff; }
.kpi-card.purple { border-left-color: #7b61ff; }
.kpi-card.green  { border-left-color: #00b894; }
.kpi-card.teal   { border-left-color: #00cec9; }

.kpi-icon-wrap {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center;
    justify-content: center;
    font-size: 1.2rem; margin-bottom: 0.7rem;
}
.kpi-card.orange .kpi-icon-wrap { background: #f39c1218; }
.kpi-card.red    .kpi-icon-wrap { background: #e1705518; }
.kpi-card.blue   .kpi-icon-wrap { background: #0080ff18; }
.kpi-card.purple .kpi-icon-wrap { background: #7b61ff18; }
.kpi-card.green  .kpi-icon-wrap { background: #00b89418; }
.kpi-card.teal   .kpi-icon-wrap { background: #00cec918; }

.kpi-label {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    opacity: 0.55; color: var(--text-color); margin-bottom: 0.25rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.75rem; font-weight: 800;
    line-height: 1.1; margin-bottom: 0.2rem;
}
.kpi-card.orange .kpi-value { color: #f39c12; }
.kpi-card.red    .kpi-value { color: #e17055; }
.kpi-card.blue   .kpi-value { color: #0080ff; }
.kpi-card.purple .kpi-value { color: #7b61ff; }
.kpi-card.green  .kpi-value { color: #00b894; }
.kpi-card.teal   .kpi-value { color: #00cec9; }
.kpi-sub { font-size: 0.72rem; opacity: 0.45; color: var(--text-color); }

.filter-card {
    background-color: var(--secondary-background-color);
    border-radius: 14px; padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 1.2rem; border-top: 3px solid #f39c12;
}
.chart-wrap {
    background-color: var(--secondary-background-color);
    border-radius: 14px; padding: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}
.soft-divider {
    height: 1px; background: var(--text-color);
    opacity: 0.08; margin: 1.5rem 0;
}
.insight-box {
    background-color: var(--secondary-background-color);
    border-radius: 12px; padding: 1rem 1.2rem;
    border-left: 4px solid #f39c12;
    margin-bottom: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.insight-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem; font-weight: 700;
    color: #f39c12; margin-bottom: 0.3rem;
}
.insight-text {
    font-size: 0.82rem; color: var(--text-color);
    opacity: 0.75; line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

#  Header
st.markdown('<div class="page-title">💰 Cost Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Fuel, labor and operational cost breakdown across routes and couriers</div>', unsafe_allow_html=True)

# Load Data
with st.spinner("Loading cost data..."):

    # Overall KPIs
    kpi = run_query("""
        SELECT
            ROUND(SUM(fuel_cost + labor_cost + misc_cost), 2)       AS total_cost,
            ROUND(AVG(fuel_cost + labor_cost + misc_cost), 2)       AS avg_cost,
            ROUND(SUM(fuel_cost), 2)                                AS total_fuel,
            ROUND(SUM(labor_cost), 2)                               AS total_labor,
            ROUND(SUM(misc_cost), 2)                                AS total_misc,
            ROUND(MAX(fuel_cost + labor_cost + misc_cost), 2)       AS max_cost,
            ROUND(MIN(fuel_cost + labor_cost + misc_cost), 2)       AS min_cost
        FROM costs
    """).iloc[0]

    # Cost by route
    route_cost = run_query("""
        SELECT
            s.origin,
            s.destination,
            CONCAT(s.origin, ' → ', s.destination)                  AS route,
            COUNT(*)                                                 AS shipments,
            ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS avg_total,
            ROUND(AVG(c.fuel_cost), 2)                              AS avg_fuel,
            ROUND(AVG(c.labor_cost), 2)                             AS avg_labor,
            ROUND(AVG(c.misc_cost), 2)                              AS avg_misc,
            ROUND(SUM(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS total_cost
        FROM costs c
        JOIN shipments s ON c.shipment_id = s.shipment_id
        GROUP BY s.origin, s.destination
        ORDER BY avg_total DESC
    """)

    # Cost by courier
    courier_cost = run_query("""
        SELECT
            cs.name,
            cs.vehicle_type,
            COUNT(*)                                                    AS shipments,
            ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2)    AS avg_total,
            ROUND(AVG(c.fuel_cost), 2)                                  AS avg_fuel,
            ROUND(AVG(c.labor_cost), 2)                                 AS avg_labor,
            ROUND(AVG(c.misc_cost), 2)                                  AS avg_misc,
            ROUND(SUM(c.fuel_cost + c.labor_cost + c.misc_cost), 2)    AS total_cost
        FROM costs c
        JOIN shipments s  ON c.shipment_id  = s.shipment_id
        JOIN courier_staff cs ON s.courier_id = cs.courier_id
        GROUP BY cs.name, cs.vehicle_type
        ORDER BY avg_total DESC
    """)

    # Cost by status
    status_cost = run_query("""
        SELECT
            s.status,
            COUNT(*)                                                    AS shipments,
            ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2)    AS avg_cost,
            ROUND(SUM(c.fuel_cost + c.labor_cost + c.misc_cost), 2)    AS total_cost
        FROM costs c
        JOIN shipments s ON c.shipment_id = s.shipment_id
        GROUP BY s.status
        ORDER BY total_cost DESC
    """)

    # Cost by vehicle type
    vehicle_cost = run_query("""
        SELECT
            cs.vehicle_type,
            ROUND(AVG(c.fuel_cost), 2)                                  AS avg_fuel,
            ROUND(AVG(c.labor_cost), 2)                                 AS avg_labor,
            ROUND(AVG(c.misc_cost), 2)                                  AS avg_misc
        FROM costs c
        JOIN shipments s    ON c.shipment_id  = s.shipment_id
        JOIN courier_staff cs ON s.courier_id = cs.courier_id
        GROUP BY cs.vehicle_type
        ORDER BY avg_fuel DESC
    """)

    # High cost shipments
    high_cost = run_query("""
        SELECT
            s.shipment_id,
            s.origin,
            s.destination,
            s.status,
            cs.name                                                     AS courier,
            cs.vehicle_type,
            ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2)        AS total_cost,
            ROUND(c.fuel_cost, 2)                                      AS fuel_cost,
            ROUND(c.labor_cost, 2)                                     AS labor_cost,
            ROUND(c.misc_cost, 2)                                      AS misc_cost
        FROM costs c
        JOIN shipments s    ON c.shipment_id  = s.shipment_id
        JOIN courier_staff cs ON s.courier_id = cs.courier_id
        ORDER BY total_cost DESC
        LIMIT 500
    """)

# KPI Cards
st.markdown('<div class="section-header">💵 Cost Overview</div>', unsafe_allow_html=True)

row1 = [
    ("orange", "💰", "Total Op. Cost",     f"₹{kpi['total_cost']:,.0f}",   "All shipments combined"),
    ("blue",   "📉", "Avg Cost/Shipment",  f"₹{kpi['avg_cost']:,.2f}",     "Per shipment average"),
    ("red",    "🔝", "Highest Shipment",   f"₹{kpi['max_cost']:,.2f}",     "Most expensive single shipment"),
    ("green",  "🔻", "Lowest Shipment",    f"₹{kpi['min_cost']:,.2f}",     "Cheapest single shipment"),
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
    ("orange", "⛽", "Total Fuel Cost",    f"₹{kpi['total_fuel']:,.0f}",   f"{round(kpi['total_fuel']*100/kpi['total_cost'],1)}% of total"),
    ("purple", "👷", "Total Labor Cost",   f"₹{kpi['total_labor']:,.0f}",  f"{round(kpi['total_labor']*100/kpi['total_cost'],1)}% of total"),
    ("teal",   "📦", "Total Misc Cost",    f"₹{kpi['total_misc']:,.0f}",   f"{round(kpi['total_misc']*100/kpi['total_cost'],1)}% of total"),
    ("blue",   "🛣️", "Total Routes",       f"{len(route_cost):,}",          "Origin-destination pairs"),
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

# Cost Breakdown Charts
st.markdown('<div class="section-header">📊 Cost Breakdown</div>', unsafe_allow_html=True)

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    # Fuel vs Labor vs Misc donut
    fig_donut = go.Figure(go.Pie(
        labels=['⛽ Fuel', '👷 Labor', '📦 Misc'],
        values=[kpi['total_fuel'], kpi['total_labor'], kpi['total_misc']],
        hole=0.60,
        marker=dict(
            colors=['#f39c12', '#0080ff', '#7b61ff'],
            line=dict(width=2)
        ),
        textfont=dict(family='DM Sans', size=12),
        hovertemplate='<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>'
    ))
    fig_donut.update_layout(
        title=dict(text='Fuel vs Labor vs Misc', font=dict(family='Syne', size=14)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', size=11),
        legend=dict(orientation='h', y=-0.1, bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=40, b=0), height=300
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    # Cost by shipment status
    fig_status = px.bar(
        status_cost, x='status', y=['avg_cost'],
        color_discrete_map={'avg_cost': '#f39c12'},
        labels={'status': 'Status', 'value': 'Avg Cost (₹)', 'variable': ''},
        title='Average Cost by Shipment Status',
        text_auto=True,
        barmode='group'
    )
    fig_status.update_traces(
        marker_color=['#00b894', '#e17055', '#0080ff', '#f39c12'][:len(status_cost)],
        texttemplate='₹%{y:,.0f}', textposition='outside'
    )
    fig_status.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', size=11),
        title=dict(font=dict(family='Syne', size=14)),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(128,128,128,0.15)', tickprefix='₹'),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=20), height=300
    )
    st.plotly_chart(fig_status, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# Cost by Vehicle Type
st.markdown('<div class="section-header">🚗 Cost by Vehicle Type</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
vehicle_melt = vehicle_cost.melt(
    id_vars='vehicle_type',
    value_vars=['avg_fuel', 'avg_labor', 'avg_misc'],
    var_name='cost_type', value_name='amount'
)
vehicle_melt['cost_type'] = vehicle_melt['cost_type'].map({
    'avg_fuel':  '⛽ Fuel',
    'avg_labor': '👷 Labor',
    'avg_misc':  '📦 Misc'
})
fig_vehicle = px.bar(
    vehicle_melt, x='vehicle_type', y='amount',
    color='cost_type',
    color_discrete_map={'⛽ Fuel': '#f39c12', '👷 Labor': '#0080ff', '📦 Misc': '#7b61ff'},
    barmode='group',
    labels={'vehicle_type': 'Vehicle Type', 'amount': 'Avg Cost (₹)', 'cost_type': 'Cost Type'},
    title='Average Cost Breakdown by Vehicle Type',
    text_auto=True
)
fig_vehicle.update_traces(texttemplate='₹%{y:,.0f}', textposition='outside')
fig_vehicle.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', size=11),
    title=dict(font=dict(family='Syne', size=14)),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor='rgba(128,128,128,0.15)', tickprefix='₹'),
    legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', y=1.12),
    margin=dict(l=0, r=0, t=60, b=0), height=300
)
st.plotly_chart(fig_vehicle, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# Top Expensive Route
st.markdown('<div class="section-header">🛣️ Most Expensive Routes</div>', unsafe_allow_html=True)

col_f1, col_f2 = st.columns([1, 3])
with col_f1:
    top_n = st.slider("Show top N routes", 5, 30, 10, 5)
with col_f2:
    sort_route = st.selectbox("Sort by", ["avg_total", "total_cost", "shipments"],
        format_func=lambda x: {
            "avg_total":   "Avg Cost per Shipment",
            "total_cost":  "Total Cost",
            "shipments":   "Number of Shipments"
        }[x]
    )

top_routes = route_cost.nlargest(top_n, sort_route)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
fig_route = px.bar(
    top_routes, x='avg_total', y='route', orientation='h',
    color='avg_total',
    color_continuous_scale=['#fff3cd', '#f39c12', '#e17055'],
    labels={'avg_total': 'Avg Cost (₹)', 'route': ''},
    title=f'Top {top_n} Most Expensive Routes',
    text='avg_total'
)
fig_route.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
fig_route.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', size=11),
    title=dict(font=dict(family='Syne', size=14)),
    xaxis=dict(showgrid=False, showticklabels=False),
    yaxis=dict(showgrid=False),
    coloraxis_showscale=False,
    margin=dict(l=0, r=80, t=40, b=0), height=max(300, top_n * 32)
)
st.plotly_chart(fig_route, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# Top Expensive Couriers
st.markdown('<div class="section-header">🚴 Courier Cost Comparison</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
top_couriers = courier_cost.nlargest(15, 'avg_total')
courier_melt = top_couriers.melt(
    id_vars=['name', 'vehicle_type'],
    value_vars=['avg_fuel', 'avg_labor', 'avg_misc'],
    var_name='cost_type', value_name='amount'
)
courier_melt['cost_type'] = courier_melt['cost_type'].map({
    'avg_fuel':  '⛽ Fuel',
    'avg_labor': '👷 Labor',
    'avg_misc':  '📦 Misc'
})
fig_courier = px.bar(
    courier_melt, x='amount', y='name', orientation='h',
    color='cost_type',
    color_discrete_map={'⛽ Fuel':'#f39c12','👷 Labor':'#0080ff','📦 Misc':'#7b61ff'},
    barmode='stack',
    labels={'amount':'Cost (₹)','name':'','cost_type':''},
    title='Top 15 Couriers by Avg Shipment Cost (Stacked)'
)
fig_courier.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', size=11),
    title=dict(font=dict(family='Syne', size=14)),
    xaxis=dict(gridcolor='rgba(128,128,128,0.15)', tickprefix='₹'),
    yaxis=dict(showgrid=False),
    legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1),
    margin=dict(l=0, r=0, t=60, b=0), height=420
)
st.plotly_chart(fig_courier, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# High Cost Shipments Table

st.markdown('<div class="section-header">🔍 High Cost Shipments</div>', unsafe_allow_html=True)

col_h1, col_h2 = st.columns(2)
with col_h1:
    min_cost_filter = st.slider(
        "Min Total Cost (₹)",
        min_value=int(high_cost['total_cost'].min()),
        max_value=int(high_cost['total_cost'].max()),
        value=int(high_cost['total_cost'].quantile(0.75))
    )
with col_h2:
    status_options = ["All"] + high_cost['status'].unique().tolist()
    status_filter  = st.selectbox("Filter by Status", status_options)

filtered_high = high_cost[high_cost['total_cost'] >= min_cost_filter]
if status_filter != "All":
    filtered_high = filtered_high[filtered_high['status'] == status_filter]

st.caption(f"Showing {len(filtered_high):,} high-cost shipments")

def style_cost(val):
    if isinstance(val, float):
        if val >= high_cost['total_cost'].quantile(0.90):
            return 'color: #e17055; font-weight: 700;'
        elif val >= high_cost['total_cost'].quantile(0.75):
            return 'color: #f39c12; font-weight: 600;'
    return ''

styled = filtered_high.style.map(style_cost, subset=['total_cost'])

st.dataframe(
    styled,
    use_container_width=True,
    height=400,
    column_config={
        "shipment_id":  st.column_config.TextColumn("Shipment ID",  width="small"),
        "origin":       st.column_config.TextColumn("Origin"),
        "destination":  st.column_config.TextColumn("Destination"),
        "status":       st.column_config.TextColumn("Status",       width="small"),
        "courier":      st.column_config.TextColumn("Courier"),
        "vehicle_type": st.column_config.TextColumn("Vehicle"),
        "total_cost":   st.column_config.NumberColumn("Total Cost", format="₹%.2f"),
        "fuel_cost":    st.column_config.NumberColumn("Fuel",       format="₹%.2f"),
        "labor_cost":   st.column_config.NumberColumn("Labor",      format="₹%.2f"),
        "misc_cost":    st.column_config.NumberColumn("Misc",       format="₹%.2f"),
    }
)

st.markdown("<br>", unsafe_allow_html=True)
col_dl, col_info = st.columns([1, 3])
with col_dl:
    csv = filtered_high.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="high_cost_shipments.csv",
        mime="text/csv",
        use_container_width=True
    )
with col_info:
    st.caption("Color coding: 🔴 Top 10% cost  🟡 Top 25% cost")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Smart Logistics Platform • Cost Analytics • Powered by MySQL + Streamlit")