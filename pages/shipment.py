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
st.set_page_config(page_title="Shipment Search", page_icon="🔍", layout="wide")
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
    background: linear-gradient(90deg, #00b894, #0080ff);
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
    color: #00b894;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #00b89422;
}
.filter-card {
    background-color: var(--secondary-background-color);
    border-radius: 14px;
    padding: 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 1.2rem;
    border-top: 3px solid #00b894;
}
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    margin-right: 0.4rem;
}
.pill-blue   { background: #0080ff18; color: #0080ff; }
.pill-green  { background: #00b89418; color: #00b894; }
.pill-red    { background: #e1705518; color: #e17055; }
.pill-orange { background: #f39c1218; color: #f39c12; }
.soft-divider {
    height: 1px;
    background: var(--text-color);
    opacity: 0.08;
    margin: 1.5rem 0;
}
.chart-wrap {
    background-color: var(--secondary-background-color);
    border-radius: 14px;
    padding: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="page-title">🔍 Shipment Search</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Filter, search and explore shipment records in real-time</div>', unsafe_allow_html=True)

# Load Filter Options
origins      = run_query("SELECT DISTINCT origin FROM shipments ORDER BY origin")['origin'].tolist()
destinations = run_query("SELECT DISTINCT destination FROM shipments ORDER BY destination")['destination'].tolist()
couriers     = run_query("SELECT courier_id, name FROM courier_staff ORDER BY name")

# Filters Panel
st.markdown('<div class="section-header">🎛️ Filters</div>', unsafe_allow_html=True)
st.markdown('<div class="filter-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    search_id = st.text_input("🔎 Search by Shipment ID", placeholder="e.g. dc84cc15")
    status_filter = st.multiselect(
        "📦 Status",
        options=["Delivered", "In Transit", "Cancelled", "Pending"],
        default=["Delivered", "In Transit", "Cancelled", "Pending"]
    )

with col2:
    origin_filter = st.multiselect("📍 Origin", options=origins, placeholder="All origins")
    dest_filter   = st.multiselect("🏁 Destination", options=destinations, placeholder="All destinations")

with col3:
    date_range     = st.date_input("📅 Order Date Range", value=[], help="Select start and end date")
    courier_options = ["All"] + couriers['name'].tolist()
    courier_filter  = st.selectbox("🚴 Courier", options=courier_options)

st.markdown('</div>', unsafe_allow_html=True)

# Build Dynamic Query
where = ["1=1"]

if search_id:
    where.append(f"s.shipment_id LIKE '%{search_id}%'")

if status_filter:
    status_str = ", ".join([f"'{x}'" for x in status_filter])
    where.append(f"s.status IN ({status_str})")

if origin_filter:
    origin_str = ", ".join([f"'{x}'" for x in origin_filter])
    where.append(f"s.origin IN ({origin_str})")

if dest_filter:
    dest_str = ", ".join([f"'{x}'" for x in dest_filter])
    where.append(f"s.destination IN ({dest_str})")

if len(date_range) == 2:
    where.append(f"s.order_date BETWEEN '{date_range[0]}' AND '{date_range[1]}'")

if courier_filter != "All":
    safe_courier = courier_filter.replace("'", "''")
    where.append(f"cs.name = '{safe_courier}'")

where_clause = " AND ".join(where)

query = f"""
    SELECT
        s.shipment_id,
        s.order_date,
        s.origin,
        s.destination,
        s.weight,
        cs.name          AS courier,
        cs.vehicle_type,
        s.status,
        s.delivery_date,
        DATEDIFF(s.delivery_date, s.order_date)            AS delivery_days,
        ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2) AS total_cost
    FROM shipments s
    LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
    LEFT JOIN costs c ON s.shipment_id = c.shipment_id
    WHERE {where_clause}
    ORDER BY s.order_date DESC
    LIMIT 1000
"""

with st.spinner("Fetching shipments..."):
    df = run_query(query)

# Summary Pills
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📊 Results Summary</div>', unsafe_allow_html=True)

total      = len(df)
delivered  = len(df[df['status'] == 'Delivered'])
cancelled  = len(df[df['status'] == 'Cancelled'])
in_transit = len(df[df['status'] == 'In Transit'])

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<span class="stat-pill pill-blue">📦 Total: {total:,}</span>',        unsafe_allow_html=True)
c2.markdown(f'<span class="stat-pill pill-green">✅ Delivered: {delivered:,}</span>', unsafe_allow_html=True)
c3.markdown(f'<span class="stat-pill pill-red">❌ Cancelled: {cancelled:,}</span>',   unsafe_allow_html=True)
c4.markdown(f'<span class="stat-pill pill-orange">🚛 In Transit: {in_transit:,}</span>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts
if not df.empty:
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        fig_status = px.pie(
            status_counts, names='status', values='count',
            hole=0.55,
            color='status',
            color_discrete_map={
                'Delivered':  '#00b894',
                'Cancelled':  '#e17055',
                'In Transit': '#0080ff',
                'Pending':    '#f39c12'
            },
            title='Status Breakdown'
        )
        fig_status.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', size=11),
            title=dict(font=dict(family='Syne', size=14)),
            legend=dict(orientation='h', y=-0.15, bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0), height=260
        )
        st.plotly_chart(fig_status, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        top_routes = df.groupby(['origin','destination']).size().reset_index(name='count')
        top_routes['route'] = top_routes['origin'] + " → " + top_routes['destination']
        top_routes = top_routes.nlargest(8, 'count')
        fig_routes = px.bar(
            top_routes, x='count', y='route', orientation='h',
            color='count',
            color_continuous_scale=[[0,'rgba(225,112,85,0.12)'],[0.5,'#f39c12'],[1,'#00b894']],
            labels={'count':'Shipments','route':''},
            title='Top Routes in Results',
            text='count'
        )
        fig_routes.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_routes.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', size=11),
            title=dict(font=dict(family='Syne', size=14)),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False,
            margin=dict(l=0, r=50, t=40, b=0), height=260
        )
        st.plotly_chart(fig_routes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Data Table
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📋 Shipment Records</div>', unsafe_allow_html=True)

if df.empty:
    st.info("No shipments found matching your filters. Try adjusting the criteria.")
else:
    def style_status(val):
        colors = {
            'Delivered':  'background-color: #00b89420; color: #00b894;',
            'Cancelled':  'background-color: #e1705520; color: #e17055;',
            'In Transit': 'background-color: #0080ff20; color: #0080ff;',
            'Pending':    'background-color: #f39c1220; color: #f39c12;',
        }
        return colors.get(val, '')

    styled_df = df.style.map(style_status, subset=['status'])

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=420,
        column_config={
            "shipment_id":   st.column_config.TextColumn("Shipment ID",   width="small"),
            "order_date":    st.column_config.DateColumn("Order Date",    width="small"),
            "origin":        st.column_config.TextColumn("Origin"),
            "destination":   st.column_config.TextColumn("Destination"),
            "weight":        st.column_config.NumberColumn("Weight (kg)", format="%.2f kg"),
            "courier":       st.column_config.TextColumn("Courier"),
            "vehicle_type":  st.column_config.TextColumn("Vehicle"),
            "status":        st.column_config.TextColumn("Status",        width="small"),
            "delivery_date": st.column_config.DateColumn("Delivery Date"),
            "delivery_days": st.column_config.NumberColumn("Days Taken",  format="%d days"),
            "total_cost":    st.column_config.NumberColumn("Total Cost",  format="₹%.2f"),
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_dl, col_info = st.columns([1, 3])
    with col_dl:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name="shipments_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_info:
        st.caption(f"Showing {len(df):,} records (max 1,000). Apply filters to narrow results.")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Smart Logistics Platform • Shipment Search • Powered by MySQL + Streamlit")