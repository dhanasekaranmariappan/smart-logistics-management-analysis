# sidebar.py
import streamlit as st

def render_sidebar():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    [data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 280px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: var(--secondary-background-color);
        padding: 1.5rem 1rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.8rem 0.8rem 1.2rem 0.8rem;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        margin-bottom: 1.2rem;
    }

    .sidebar-brand-icon { font-size: 2rem; line-height: 1; }

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
        font-family: 'DM Sans', sans-serif;
    }

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
        transition: background 0.15s ease !important;
        margin-bottom: 0.2rem !important;
    }

    [data-testid="stSidebar"] a:hover {
        background: rgba(0,128,255,0.08) !important;
        color: #0080ff !important;
    }

    [data-testid="stSidebar"] a[aria-current="page"] {
        background: rgba(0,128,255,0.12) !important;
        color: #0080ff !important;
        font-weight: 600 !important;
        border-left: 3px solid #0080ff !important;
    }

    .sidebar-divider {
        height: 1px;
        background: var(--text-color);
        opacity: 0.08;
        margin: 0.5rem 0.8rem 1rem 0.8rem;
    }

    .sidebar-footer {
        font-size: 0.68rem;
        opacity: 0.35;
        color: var(--text-color);
        font-family: 'DM Sans', sans-serif;
        text-align: center;
        padding: 0 0.8rem;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

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
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # Footer at bottom
        st.markdown("<br>" * 3, unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-footer">
            Smart Logistics Platform<br>
            Powered by MySQL + Streamlit
        </div>
        """, unsafe_allow_html=True)