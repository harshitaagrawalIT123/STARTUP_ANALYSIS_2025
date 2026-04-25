import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="India Startup Pulse 2025",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="India Startup Pulse 2025",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL STYLES (CLEANED) ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f35 50%, #0a1f15 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}
[data-testid="stToolbar"]    { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* FIX: Force sidebar to stay open and hide collapse arrow */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%);
    border-right: 1px solid rgba(0,220,130,0.15);
    min-width: 320px !important;
}

[data-testid="stSidebar"] * { color: #c8e6d0 !important; }

/* ... keep your .hero-wrap, .kpi-grid, and other styles below ... */
.hero-wrap { 
    /* ... existing hero code ... */
}
</style>
""", unsafe_allow_html=True)


# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = load_data()


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:8px;'>
        <span style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;'>
            ⚡ Startup Pulse
        </span><br>
        <span style='font-size:0.7rem;letter-spacing:2px;color:#5a8fa8;text-transform:uppercase;'>
            India · 2025
        </span>
    </div>
    <hr style='margin:12px 0;'>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sidebar-badge'>
        <span class='sb-num'>{len(df):,}</span>
        <span class='sb-label'>Startups Tracked</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🔍 Quick Filters**")

    sectors = ["All Sectors"] + sorted(df['Sector'].dropna().unique().tolist())
    selected_sector = st.selectbox("Sector", sectors)

    states = ["All States"] + sorted(df['State'].dropna().unique().tolist())
    selected_state = st.selectbox("State", states)

    filtered_df = df.copy()
    if selected_sector != "All Sectors":
        filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
    if selected_state != "All States":
        filtered_df = filtered_df[filtered_df['State'] == selected_state]

    st.markdown(f"<br><small style='color:#5a8fa8;'>Showing **{len(filtered_df):,}** results</small>",
                unsafe_allow_html=True)


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='hero-wrap'>
    <div class='hero-tag'>India Ecosystem Report</div>
    <h1 class='hero-title'>Startup<br><span>Intelligence</span> Hub</h1>
    <p class='hero-sub'>
        Real-time analytics across {df['Sector'].nunique()} sectors, {df['State'].nunique()} states,
        and {len(df):,} ventures shaping India's startup landscape in 2025.
    </p>
    <div class='hero-year'>2025</div>
</div>
""", unsafe_allow_html=True)


# ─── KPI CARDS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='kpi-grid'>
    <div class='kpi-card'>
        <span class='kpi-icon'>🏢</span>
        <div class='kpi-value'>{len(filtered_df):,}</div>
        <div class='kpi-label'>Total Startups</div>
    </div>
    <div class='kpi-card'>
        <span class='kpi-icon'>📍</span>
        <div class='kpi-value'>{filtered_df['State'].nunique()}</div>
        <div class='kpi-label'>States</div>
    </div>
    <div class='kpi-card'>
        <span class='kpi-icon'>🏙️</span>
        <div class='kpi-value'>{filtered_df['Headquarters'].nunique()}</div>
        <div class='kpi-label'>Cities</div>
    </div>
    <div class='kpi-card'>
        <span class='kpi-icon'>💼</span>
        <div class='kpi-value'>{filtered_df['Sector'].nunique()}</div>
        <div class='kpi-label'>Sectors</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── DATASET PREVIEW ──────────────────────────────────────────────────────────
st.markdown("<div class='section-heading'>📋 Dataset Preview</div>", unsafe_allow_html=True)

preview_cols = [c for c in ['Company', 'Sector', 'State', 'Headquarters', 'Team Size'] if c in filtered_df.columns]
st.dataframe(
    filtered_df[preview_cols].head(10),
    use_container_width=True,
    hide_index=True,
)

st.markdown(f"<small style='color:#5a8fa8;'>Displaying top 10 of {len(filtered_df):,} records · Use sidebar filters to refine</small>",
            unsafe_allow_html=True)