import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="India Startup Pulse 2025",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
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

/* ── Hide header bar but KEEP it in the DOM so toggle button works ── */
[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}
[data-testid="stToolbar"] {
    display: none !important;
}
[data-testid="stDecoration"] {
    display: none !important;
}

/* ── Style the sidebar toggle button ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(0, 220, 130, 0.15) !important;
    border: 1px solid rgba(0, 220, 130, 0.3) !important;
    border-radius: 8px !important;
}
[data-testid="collapsedControl"] svg {
    fill: #00dc82 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%);
    border-right: 1px solid rgba(0,220,130,0.15);
}
[data-testid="stSidebar"] * { color: #c8e6d0 !important; }

/* ── Hero banner ── */
.hero-wrap {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    padding: 56px 48px 48px;
    margin-bottom: 36px;
    background: linear-gradient(125deg, #071e35 0%, #0d3350 55%, #082b1e 100%);
    border: 1px solid rgba(0,220,130,0.2);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 80% 20%, rgba(0,220,130,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 10% 90%, rgba(0,120,255,0.08) 0%, transparent 55%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    background: rgba(0,220,130,0.15);
    border: 1px solid rgba(0,220,130,0.4);
    color: #00dc82;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 18px;
    font-weight: 500;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    color: #ffffff;
    margin: 0 0 14px;
    letter-spacing: -1px;
}
.hero-title span {
    background: linear-gradient(90deg, #00dc82, #00b4d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: #7fafc4;
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 520px;
    line-height: 1.7;
    margin: 0;
}
.hero-year {
    position: absolute;
    right: 48px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Syne', sans-serif;
    font-size: clamp(5rem, 9vw, 9rem);
    font-weight: 800;
    color: rgba(0,220,130,0.06);
    letter-spacing: -4px;
    pointer-events: none;
    user-select: none;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 36px;
}
.kpi-card {
    background: linear-gradient(140deg, #0b1f35 0%, #0d2840 100%);
    border: 1px solid rgba(0,220,130,0.12);
    border-radius: 16px;
    padding: 24px 22px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color .25s, transform .25s;
}
.kpi-card:hover {
    border-color: rgba(0,220,130,0.35);
    transform: translateY(-3px);
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00dc82, #00b4d8);
    border-radius: 2px;
    opacity: 0.7;
}
.kpi-icon { font-size: 1.5rem; margin-bottom: 10px; display: block; }
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-label {
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #5a8fa8;
    font-weight: 500;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.3px;
    margin: 0 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(0,220,130,0.12);
}

[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid rgba(0,220,130,0.1) !important;
}

hr { border-color: rgba(0,220,130,0.08) !important; }

.sidebar-badge {
    background: rgba(0,220,130,0.1);
    border: 1px solid rgba(0,220,130,0.25);
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    margin-top: 16px;
}
.sidebar-badge .sb-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #00dc82;
    display: block;
}
.sidebar-badge .sb-label {
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #5a8fa8;
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

    st.markdown(f"<br><small style='color:#5a8fa8;'>Showing **{len(filtered_df):,}** results</small>", unsafe_allow_html=True)


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

st.markdown(f"<small style='color:#5a8fa8;'>Displaying top 10 of {len(filtered_df):,} records · Use sidebar filters to refine</small>", unsafe_allow_html=True)