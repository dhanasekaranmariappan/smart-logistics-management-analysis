import streamlit as st

st.set_page_config(
    page_title="Smart Logistics Platform",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Sidebar Width ── */
[data-testid="stSidebar"] {
    min-width: 280px !important;
    max-width: 280px !important;
}

/* ── Sidebar Background ── */
[data-testid="stSidebar"] > div:first-child {
    background-color: var(--secondary-background-color);
    padding: 1.5rem 1rem;
}

/* ── Logo / Brand Area ── */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.8rem 0.8rem 1.2rem 0.8rem;
    border-bottom: 1px solid rgba(128,128,128,0.15);
    margin-bottom: 1.2rem;
}

.sidebar-brand-icon {
    font-size: 2rem;
    line-height: 1;
}

.sidebar-brand-text {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-color);
    line-height: 1.2;
}

.sidebar-brand-sub {
    font-size: 0.7rem;
    opacity: 0.45;
    color: var(--text-color);
    font-weight: 400;
    font-family: 'DM Sans', sans-serif;
}

/* ── Nav Section Label ── */
.sidebar-nav-label {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #0080ff;
    padding: 0 0.8rem;
    margin-bottom: 0.4rem;
    font-family: 'DM Sans', sans-serif;
}

/* ── Navigation Links ── */
[data-testid="stSidebar"] a {
    display: flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    padding: 0.65rem 0.8rem !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    color: var(--text-color) !important;
    text-decoration: none !important;
    transition: background 0.15s ease, color 0.15s ease !important;
    margin-bottom: 0.2rem !important;
}

[data-testid="stSidebar"] a:hover {
    background: rgba(0, 128, 255, 0.08) !important;
    color: #0080ff !important;
}

[data-testid="stSidebar"] a[aria-current="page"] {
    background: rgba(0, 128, 255, 0.12) !important;
    color: #0080ff !important;
    font-weight: 600 !important;
    border-left: 3px solid #0080ff !important;
}

/* ── Page Icons in Nav ── */
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span {
    font-size: 1.1rem !important;
}

/* ── Sidebar Footer ── */
.sidebar-footer {
    position: absolute;
    bottom: 1.5rem;
    left: 0; right: 0;
    padding: 0 1rem;
    text-align: center;
}

.sidebar-footer-text {
    font-size: 0.68rem;
    opacity: 0.35;
    color: var(--text-color);
    font-family: 'DM Sans', sans-serif;
    line-height: 1.5;
}

.sidebar-divider {
    height: 1px;
    background: var(--text-color);
    opacity: 0.08;
    margin: 1rem 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Content ────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🚚</div>
        <div>
            <div class="sidebar-brand-text">Smart Logistics</div>
            <div class="sidebar-brand-sub">Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nav label
    st.markdown('<div class="sidebar-nav-label">Navigation</div>', unsafe_allow_html=True)

    # Divider
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="sidebar-footer">
        <div class="sidebar-footer-text">
            Smart Logistics Platform<br>
            Built with Streamlit + MySQL
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Home Page Content ──────────────────────────────────────────
st.markdown("""
<style>
.home-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0080ff, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.home-sub {
    font-size: 1rem;
    opacity: 0.55;
    color: var(--text-color);
    margin-bottom: 2rem;
}
.home-card {
    background-color: var(--secondary-background-color);
    border-radius: 14px;
    padding: 1.4rem;
    border-left: 4px solid transparent;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    transition: transform 0.2s ease;
    height: 100%;
}
.home-card:hover { transform: translateY(-3px); }
.home-card.blue   { border-left-color: #0080ff; }
.home-card.green  { border-left-color: #00b894; }
.home-card.purple { border-left-color: #7b61ff; }
.home-card.orange { border-left-color: #f39c12; }
.home-card-icon  { font-size: 2rem; margin-bottom: 0.6rem; }
.home-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 0.3rem;
}
.home-card-desc {
    font-size: 0.82rem;
    opacity: 0.55;
    color: var(--text-color);
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="home-title">🚚 Smart Logistics Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="home-sub">Centralized analytics for modern logistics operations</div>', unsafe_allow_html=True)

# Feature cards
c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "blue",   "📊", "KPI Overview",          "Track shipment totals, delivery rates, costs and monthly trends at a glance."),
    (c2, "green",  "🔍", "Shipment Search",        "Filter and search shipments by status, date range, origin, destination and courier."),
    (c3, "purple", "🚴", "Courier Performance",    "Rank couriers by on-time delivery, shipment volume and average ratings."),
    (c4, "orange", "💰", "Cost Analytics",         "Break down fuel, labor and misc costs per route, courier and shipment."),
]
for col, color, icon, title, desc in cards:
    with col:
        st.markdown(f"""
        <div class="home-card {color}">
            <div class="home-card-icon">{icon}</div>
            <div class="home-card-title">{title}</div>
            <div class="home-card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Select a page from the sidebar to get started!")
st.caption("Smart Logistics Platform • Powered by MySQL + Streamlit")
