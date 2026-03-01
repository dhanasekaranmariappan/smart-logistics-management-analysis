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

# Page Config
st.set_page_config(page_title="Courier Performance", page_icon="🚴", layout="wide")
render_sidebar()

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7b61ff, #e84393);
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
    color: #7b61ff;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #7b61ff22;
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
.kpi-card.purple { border-left-color: #7b61ff; }
.kpi-card.pink   { border-left-color: #e84393; }
.kpi-card.blue   { border-left-color: #0080ff; }
.kpi-card.orange { border-left-color: #f39c12; }
.kpi-card.green  { border-left-color: #00b894; }

.kpi-icon-wrap {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; margin-bottom: 0.7rem;
}
.kpi-card.purple .kpi-icon-wrap { background: #7b61ff18; }
.kpi-card.pink   .kpi-icon-wrap { background: #e8439318; }
.kpi-card.blue   .kpi-icon-wrap { background: #0080ff18; }
.kpi-card.orange .kpi-icon-wrap { background: #f39c1218; }
.kpi-card.green  .kpi-icon-wrap { background: #00b89418; }

.kpi-label {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    opacity: 0.55; color: var(--text-color); margin-bottom: 0.25rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem; font-weight: 800; line-height: 1.1; margin-bottom: 0.2rem;
}
.kpi-card.purple .kpi-value { color: #7b61ff; }
.kpi-card.pink   .kpi-value { color: #e84393; }
.kpi-card.blue   .kpi-value { color: #0080ff; }
.kpi-card.orange .kpi-value { color: #f39c12; }
.kpi-card.green  .kpi-value { color: #00b894; }
.kpi-sub { font-size: 0.72rem; opacity: 0.45; color: var(--text-color); }

.filter-card {
    background-color: var(--secondary-background-color);
    border-radius: 14px; padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 1.2rem; border-top: 3px solid #7b61ff;
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

/* Star rating colors */
.star-high   { color: #00b894; font-weight: 700; }
.star-medium { color: #f39c12; font-weight: 700; }
.star-low    { color: #e17055; font-weight: 700; }

/* Leaderboard podium */
.podium-card {
    background-color: var(--secondary-background-color);
    border-radius: 14px; padding: 1.2rem;
    text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.podium-card:hover { transform: translateY(-4px); }
.podium-rank { font-size: 2rem; margin-bottom: 0.3rem; }
.podium-name {
    font-family: 'Syne', sans-serif; font-size: 0.95rem;
    font-weight: 700; color: var(--text-color); margin-bottom: 0.2rem;
}
.podium-stat { font-size: 0.78rem; opacity: 0.55; color: var(--text-color); }
.podium-value {
    font-family: 'Syne', sans-serif; font-size: 1.5rem;
    font-weight: 800; margin: 0.3rem 0;
}
.gold   { border-top: 4px solid #f1c40f; }
.silver { border-top: 4px solid #95a5a6; }
.bronze { border-top: 4px solid #e17055; }
.gold   .podium-value { color: #f1c40f; }
.silver .podium-value { color: #95a5a6; }
.bronze .podium-value { color: #e17055; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="page-title">🚴 Courier Performance</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Rankings, delivery efficiency and courier analytics</div>', unsafe_allow_html=True)

# Load Data
with st.spinner("Loading courier data..."):

    # Overall KPIs
    kpi = run_query("""
        SELECT
            COUNT(DISTINCT courier_id)                          AS total_couriers,
            ROUND(AVG(rating), 2)                               AS avg_rating,
            MAX(rating)                                         AS top_rating,
            COUNT(DISTINCT vehicle_type)                        AS vehicle_types
        FROM courier_staff
    """).iloc[0]

    # Full courier performance table
    perf_df = run_query("""
        SELECT
            cs.courier_id,
            cs.name,
            cs.rating,
            cs.vehicle_type,
            COUNT(s.shipment_id)                                            AS total_shipments,
            ROUND(SUM(s.status='Delivered')*100.0/COUNT(*), 1)             AS delivered_pct,
            ROUND(SUM(s.status='Cancelled')*100.0/COUNT(*), 1)             AS cancelled_pct,
            ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 1)         AS avg_delivery_days,
            ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2)        AS avg_cost
        FROM courier_staff cs
        JOIN shipments s ON cs.courier_id = s.courier_id
        LEFT JOIN costs c ON s.shipment_id = c.shipment_id
        GROUP BY cs.courier_id, cs.name, cs.rating, cs.vehicle_type
        ORDER BY total_shipments DESC
    """)

    # Vehicle type breakdown
    vehicle_df = run_query("""
        SELECT
            cs.vehicle_type,
            COUNT(DISTINCT cs.courier_id)                           AS couriers,
            COUNT(s.shipment_id)                                    AS shipments,
            ROUND(AVG(cs.rating), 2)                                AS avg_rating,
            ROUND(SUM(s.status='Delivered')*100.0/COUNT(*), 1)     AS delivered_pct
        FROM courier_staff cs
        JOIN shipments s ON cs.courier_id = s.courier_id
        GROUP BY cs.vehicle_type
        ORDER BY shipments DESC
    """)

    # Rating distribution
    rating_dist = run_query("""
        SELECT
            CASE
                WHEN rating >= 4.5 THEN '⭐ 4.5 - 5.0 (Excellent)'
                WHEN rating >= 4.0 THEN '⭐ 4.0 - 4.4 (Good)'
                WHEN rating >= 3.0 THEN '⭐ 3.0 - 3.9 (Average)'
                ELSE                    '⭐ Below 3.0 (Poor)'
            END AS rating_band,
            COUNT(*) AS couriers
        FROM courier_staff
        GROUP BY rating_band
        ORDER BY couriers DESC
    """)

    # Top 3 by delivered pct (leaderboard)
    top3 = run_query("""
        SELECT
            cs.name,
            cs.rating,
            cs.vehicle_type,
            COUNT(s.shipment_id)                                        AS total_shipments,
            ROUND(SUM(s.status='Delivered')*100.0/COUNT(*), 1)         AS delivered_pct
        FROM courier_staff cs
        JOIN shipments s ON cs.courier_id = s.courier_id
        GROUP BY cs.courier_id, cs.name, cs.rating, cs.vehicle_type
        HAVING total_shipments >= 50
        ORDER BY delivered_pct DESC
        LIMIT 3
    """)

# KPI Cards
st.markdown('<div class="section-header">📊 Overview Metrics</div>', unsafe_allow_html=True)

row1 = [
    ("purple", "🚴", "Total Couriers",    f"{kpi['total_couriers']:,}",  "Active in fleet"),
    ("orange", "⭐", "Avg Fleet Rating",  f"{kpi['avg_rating']}",        "Out of 5.0"),
    ("green",  "🏆", "Top Rating",        f"{kpi['top_rating']}",        "Best performer"),
    ("blue",   "🚗", "Vehicle Types",     f"{kpi['vehicle_types']}",     "Bike, Van, Car, Truck"),
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

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

#  Top 3 Leaderboard
st.markdown('<div class="section-header">🏆 Top Performers Leaderboard</div>', unsafe_allow_html=True)

if len(top3) >= 3:
    medals = [
        ("gold",   "🥇", "1st Place"),
        ("silver", "🥈", "2nd Place"),
        ("bronze", "🥉", "3rd Place"),
    ]
    cols = st.columns(3)
    for col, (medal_class, emoji, place), (_, row) in zip(cols, medals, top3.iterrows()):
        with col:
            st.markdown(f"""
            <div class="podium-card {medal_class}">
                <div class="podium-rank">{emoji}</div>
                <div class="podium-name">{row['name']}</div>
                <div class="podium-value">{row['delivered_pct']}%</div>
                <div class="podium-stat">Delivery Rate</div>
                <br>
                <div class="podium-stat">⭐ {row['rating']} &nbsp;|&nbsp; 🚗 {row['vehicle_type']}</div>
                <div class="podium-stat">📦 {row['total_shipments']:,} shipments</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# Filters
st.markdown('<div class="section-header">🎛️ Filter Couriers</div>', unsafe_allow_html=True)
st.markdown('<div class="filter-card">', unsafe_allow_html=True)

col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    vehicle_options = ["All"] + perf_df['vehicle_type'].unique().tolist()
    vehicle_filter  = st.selectbox("🚗 Vehicle Type", vehicle_options)
with col_f2:
    min_rating = st.slider("⭐ Min Rating", 1.0, 5.0, 1.0, 0.1)
with col_f3:
    min_shipments = st.slider("📦 Min Shipments", 0, 200, 0, 10)
with col_f4:
    sort_by = st.selectbox("↕️ Sort By", [
        "total_shipments", "delivered_pct", "rating", "avg_delivery_days", "avg_cost"
    ], format_func=lambda x: {
        "total_shipments":   "Total Shipments",
        "delivered_pct":     "Delivery Rate %",
        "rating":            "Rating",
        "avg_delivery_days": "Avg Delivery Days",
        "avg_cost":          "Avg Cost"
    }[x])

st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered = perf_df.copy()
if vehicle_filter != "All":
    filtered = filtered[filtered['vehicle_type'] == vehicle_filter]
filtered = filtered[filtered['rating'] >= min_rating]
filtered = filtered[filtered['total_shipments'] >= min_shipments]
filtered = filtered.sort_values(sort_by, ascending=False)

st.caption(f"Showing {len(filtered):,} of {len(perf_df):,} couriers")

# Charts Row
st.markdown('<div class="section-header">📈 Performance Analytics</div>', unsafe_allow_html=True)

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if filtered.empty:
        st.info("No data matches current filters.")
    else:
        # Fill NaN delivered_pct with 0 before plotting
        top20 = filtered.nlargest(15, 'total_shipments').copy()
        top20['delivered_pct'] = top20['delivered_pct'].fillna(0)

        fig_bar = px.bar(
            top20, x='total_shipments', y='name', orientation='h',
            color='delivered_pct',
            range_color=[0, 100],
            color_continuous_scale=['#e17055', '#f39c12', '#00b894'],
            labels={'total_shipments':'Shipments','name':'','delivered_pct':'Delivery %'},
            title='Top 15 Couriers by Shipment Volume',
            text='total_shipments'
        )
        fig_bar.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', size=11),
            title=dict(font=dict(family='Syne', size=13)),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            coloraxis_colorbar=dict(title='Delivery %', ticksuffix='%'),
            margin=dict(l=0, r=60, t=40, b=0), height=380
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if filtered.empty:
        st.info("No data matches current filters.")
    else:
        scatter_df = filtered.copy()
        scatter_df['delivered_pct'] = scatter_df['delivered_pct'].fillna(0)
        scatter_df['avg_delivery_days'] = scatter_df['avg_delivery_days'].fillna(0)

        fig_scatter = px.scatter(
            scatter_df,
            x='rating', y='delivered_pct',
            size='total_shipments',
            color='vehicle_type',
            hover_name='name',
            hover_data={'total_shipments': True, 'avg_delivery_days': True},
            color_discrete_map={
                'Bike':'#7b61ff','Van':'#0080ff','Truck':'#f39c12','Car':'#00b894'
            },
            labels={
                'rating':            'Courier Rating',
                'delivered_pct':     'Delivery Rate (%)',
                'total_shipments':   'Shipments',
                'avg_delivery_days': 'Avg Days'
            },
            title='Rating vs Delivery Rate  (bubble size = shipment volume)'
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', size=11),
            title=dict(font=dict(family='Syne', size=13)),
            xaxis=dict(gridcolor='rgba(128,128,128,0.15)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.15)', ticksuffix='%'),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0), height=380
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
# Vehicle Type Analytics
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🚗 Vehicle Type Breakdown</div>', unsafe_allow_html=True)

col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    fig_veh = px.bar(
        vehicle_df, x='vehicle_type', y='shipments',
        color='vehicle_type',
        color_discrete_map={
            'Bike':'#7b61ff','Van':'#0080ff','Truck':'#f39c12','Car':'#00b894'
        },
        text='shipments',
        labels={'vehicle_type':'Vehicle','shipments':'Total Shipments'},
        title='Shipments by Vehicle Type'
    )
    fig_veh.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_veh.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', size=11),
        title=dict(font=dict(family='Syne', size=13)),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(128,128,128,0.15)', showticklabels=False),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0), height=280
    )
    st.plotly_chart(fig_veh, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_v2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    fig_rating = px.bar(
        vehicle_df, x='vehicle_type', y='avg_rating',
        color='vehicle_type',
        color_discrete_map={
            'Bike':'#7b61ff','Van':'#0080ff','Truck':'#f39c12','Car':'#00b894'
        },
        text='avg_rating',
        labels={'vehicle_type':'Vehicle','avg_rating':'Avg Rating'},
        title='Average Rating by Vehicle Type'
    )
    fig_rating.update_traces(texttemplate='%{text:.1f} ⭐', textposition='outside')
    fig_rating.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', size=11),
        title=dict(font=dict(family='Syne', size=13)),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(128,128,128,0.15)', range=[0, 6]),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0), height=280
    )
    st.plotly_chart(fig_rating, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Rating Distribution ────────────────────────────────────────
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">⭐ Rating Distribution</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
fig_dist = px.pie(
    rating_dist, names='rating_band', values='couriers',
    hole=0.5,
    color_discrete_sequence=['#00b894', '#7b61ff', '#f39c12', '#e17055'],
    title='Courier Rating Bands'
)
fig_dist.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', size=11),
    title=dict(font=dict(family='Syne', size=13)),
    legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', y=-0.1),
    margin=dict(l=0, r=0, t=40, b=0), height=280
)
st.plotly_chart(fig_dist, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Full Data Table ─────────────────────────────────────────────
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📋 Courier Records</div>', unsafe_allow_html=True)

def style_rating(val):
    if isinstance(val, float):
        if val >= 4.5:   return 'color: #00b894; font-weight: 700;'
        elif val >= 3.5: return 'color: #f39c12; font-weight: 700;'
        else:            return 'color: #e17055; font-weight: 700;'
    return ''

def style_delivery(val):
    if isinstance(val, float):
        if val >= 70:    return 'color: #00b894; font-weight: 600;'
        elif val >= 50:  return 'color: #f39c12; font-weight: 600;'
        else:            return 'color: #e17055; font-weight: 600;'
    return ''

styled = filtered.style\
    .map(style_rating,   subset=['rating'])\
    .map(style_delivery, subset=['delivered_pct'])

st.dataframe(
    styled,
    use_container_width=True,
    height=420,
    column_config={
        "courier_id":        st.column_config.TextColumn("ID",             width="small"),
        "name":              st.column_config.TextColumn("Courier Name"),
        "rating":            st.column_config.NumberColumn("Rating ⭐",    format="%.1f"),
        "vehicle_type":      st.column_config.TextColumn("Vehicle"),
        "total_shipments":   st.column_config.NumberColumn("Shipments",    format="%d"),
        "delivered_pct":     st.column_config.NumberColumn("Delivered %",  format="%.1f%%"),
        "cancelled_pct":     st.column_config.NumberColumn("Cancelled %",  format="%.1f%%"),
        "avg_delivery_days": st.column_config.NumberColumn("Avg Days",     format="%.1f days"),
        "avg_cost":          st.column_config.NumberColumn("Avg Cost",     format="₹%.2f"),
    }
)

# Download
st.markdown("<br>", unsafe_allow_html=True)
col_dl, col_info = st.columns([1, 3])
with col_dl:
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="courier_performance.csv",
        mime="text/csv",
        use_container_width=True
    )
with col_info:
    st.caption(f"Showing {len(filtered):,} couriers. Color coding: 🟢 ≥4.5 rating / ≥70% delivery  🟡 3.5–4.4 / 50–69%  🔴 below thresholds")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Smart Logistics Platform • Courier Performance • Powered by MySQL + Streamlit")