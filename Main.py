import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="India Startup Pulse 2025",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── BASE ───────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #e8f4f0 !important;
}

/* ── BACKGROUND ─────────────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f35 50%, #0a1f15 100%);
    background-attachment: fixed;
}

/* ── HIDE CHROME ────────────────────────────────────────────── */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* ── HEADINGS ───────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

/* ── MARKDOWN TEXT ──────────────────────────────────────────── */
[data-testid="stMarkdownContainer"] p      { color: #c8e6d0 !important; }
[data-testid="stMarkdownContainer"] li     { color: #c8e6d0 !important; }
[data-testid="stMarkdownContainer"] strong { color: #ffffff !important; }
[data-testid="stMarkdownContainer"] em     { color: #a0c4b8 !important; }
[data-testid="stMarkdownContainer"] small  { color: #5a8fa8 !important; }

hr { border-color: rgba(0,220,130,0.15) !important; }

/* ── SIDEBAR ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%) !important;
    border-right: 1px solid rgba(0,220,130,0.15);
    min-width: 320px !important;
    max-width: 320px !important;
}

/* ✅ THE SIDEBAR TEXT FIX — target every possible text element */
[data-testid="stSidebar"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #c8e6d0 !important;
}

/* Bold & strong inside sidebar → green accent */
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #00dc82 !important;
    font-weight: 700 !important;
}

/* Sidebar selectbox text */
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #ffffff !important;
    background-color: rgba(11,31,53,0.9) !important;
}

/* ── SIDEBAR BADGE ──────────────────────────────────────────── */
.sidebar-badge {
    background: rgba(0,220,130,0.08);
    border: 1px solid rgba(0,220,130,0.25);
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
    margin-bottom: 8px;
}
.sb-num {
    display: block;
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #00dc82 !important;
}
.sb-label {
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #5a8fa8 !important;
}

/* Sidebar stat row */
.sb-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(0,220,130,0.08);
}
.sb-stat-label { font-size: 0.8rem; color: #7aafc4 !important; }
.sb-stat-value { font-size: 0.9rem; font-weight: 700; color: #ffffff !important; }

/* ── HERO ───────────────────────────────────────────────────── */
.hero-wrap {
    padding: 48px 0 32px 0;
    position: relative;
}
.hero-tag {
    display: inline-block;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00dc82 !important;
    border: 1px solid rgba(0,220,130,0.4);
    border-radius: 20px;
    padding: 4px 14px;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.6rem;
    font-weight: 800;
    line-height: 1.1;
    color: #ffffff !important;
    margin: 0 0 16px 0;
}
.hero-title span { color: #00dc82 !important; }
.hero-sub {
    font-size: 1.05rem;
    color: #a0c4b8 !important;
    max-width: 620px;
    line-height: 1.7;
}
.hero-year {
    position: absolute;
    right: 0; top: 40px;
    font-family: 'Syne', sans-serif;
    font-size: 7rem;
    font-weight: 800;
    color: rgba(0,220,130,0.06);
    pointer-events: none;
    user-select: none;
}

/* ── KPI CARDS ──────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 28px 0 36px 0;
}
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,220,130,0.15);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: rgba(0,220,130,0.45); }
.kpi-icon { font-size: 1.6rem; display: block; margin-bottom: 8px; }
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #5a8fa8 !important;
    margin-top: 6px;
}

/* ── SECTION HEADING ────────────────────────────────────────── */
.section-heading {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.45rem;
    font-weight: 700;
    color: #ffffff !important;
    margin: 36px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(0,220,130,0.2);
}
.section-tag {
    font-size: 0.68rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00dc82;
    margin-bottom: 4px;
}

/* ── INSIGHT CARDS ──────────────────────────────────────────── */
.insight-card {
    background: rgba(11,31,53,0.7);
    border: 1px solid rgba(0,220,130,0.15);
    border-radius: 14px;
    padding: 20px;
    height: 100%;
}
.insight-card h4 {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    color: #00dc82 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 0 0 12px 0;
}
.insight-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.88rem;
}
.insight-row:last-child { border-bottom: none; }
.ir-name  { color: #c8e6d0 !important; }
.ir-value { color: #ffffff !important; font-weight: 700; font-family: 'Syne', sans-serif; }

/* ── DATAFRAME ──────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(0,220,130,0.15);
}
[data-testid="stDataFrame"] th {
    background: rgba(0,220,130,0.1) !important;
    color: #00dc82 !important;
    font-size: 0.78rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}
[data-testid="stDataFrame"] td { color: #e0f0e8 !important; }

/* ── HIGHLIGHT UTILITY ──────────────────────────────────────── */
.highlight-text { color: #ffffff !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ── DARK THEME FOR PLOTLY ─────────────────────────────────────────────────────
def dt(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11,31,53,0.5)",
        font=dict(color="#e8f4f0", family="DM Sans", size=12),
        title_font=dict(color="#ffffff", size=14, family="Syne"),
        legend=dict(bgcolor="rgba(11,31,53,0.8)", bordercolor="rgba(0,220,130,0.2)",
                    font=dict(color="#e8f4f0")),
        xaxis=dict(color="#a0c4b8", gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(0,220,130,0.2)", tickfont=dict(color="#a8c8d8")),
        yaxis=dict(color="#a0c4b8", gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(0,220,130,0.2)", tickfont=dict(color="#a8c8d8")),
    )
    return fig


# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = load_data()


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
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
    <hr style='margin:12px 0;border-color:rgba(0,220,130,0.15);'>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sidebar-badge'>
        <span class='sb-num'>{len(df):,}</span>
        <span class='sb-label'>Startups Tracked</span>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats in sidebar
    top_sector = df['Sector'].value_counts().index[0]
    top_state  = df['State'].value_counts().index[0]
    top_city   = df['Headquarters'].value_counts().index[0]

    st.markdown(f"""
    <div style='margin: 16px 0 8px 0;'>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>🏆 Top Sector</span>
            <span class='sb-stat-value'>{top_sector}</span>
        </div>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>📍 Top State</span>
            <span class='sb-stat-value'>{top_state}</span>
        </div>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>🏙️ Top City</span>
            <span class='sb-stat-value'>{top_city}</span>
        </div>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>📊 Total Sectors</span>
            <span class='sb-stat-value'>{df['Sector'].nunique()}</span>
        </div>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>🗺️ States Covered</span>
            <span class='sb-stat-value'>{df['State'].nunique()}</span>
        </div>
    </div>
    <hr style='border-color:rgba(0,220,130,0.1);margin:14px 0;'>
    """, unsafe_allow_html=True)

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

    st.markdown(f"<br><small>Showing **{len(filtered_df):,}** results</small>",
                unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='hero-wrap'>
    <div class='hero-tag'>India Ecosystem Report · 2025</div>
    <h1 class='hero-title'>Startup<br><span>Intelligence</span> Hub</h1>
    <p class='hero-sub'>
        Tracking {len(df):,} ventures across {df['Sector'].nunique()} sectors and
        {df['State'].nunique()} states — a living map of India's startup landscape in 2025.
    </p>
    <div class='hero-year'>2025</div>
</div>
""", unsafe_allow_html=True)


# ── KPI CARDS ─────────────────────────────────────────────────────────────────
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


# ── SECTION 1: SECTOR BREAKDOWN ───────────────────────────────────────────────
st.markdown("<div class='section-tag'>Where are they building?</div>", unsafe_allow_html=True)
st.markdown("<div class='section-heading'>🏭 Sector Breakdown</div>", unsafe_allow_html=True)

col_chart, col_insight = st.columns([3, 2])

with col_chart:
    sector_counts = filtered_df['Sector'].value_counts().reset_index()
    sector_counts.columns = ['Sector', 'Count']
    fig_sector = px.bar(sector_counts.head(12), x='Count', y='Sector', orientation='h',
                        color='Count', color_continuous_scale='Viridis',
                        title="Top Sectors by Number of Startups")
    fig_sector = dt(fig_sector, height=400)
    fig_sector.update_layout(yaxis=dict(categoryorder='total ascending'), showlegend=False)
    st.plotly_chart(fig_sector,width="stretch")

with col_insight:
    top5_sectors = filtered_df['Sector'].value_counts().head(5)
    total = len(filtered_df)
    rows = "".join([
        f"<div class='insight-row'>"
        f"<span class='ir-name'>{s}</span>"
        f"<span class='ir-value'>{c:,} <span style='color:#5a8fa8;font-size:0.75rem;font-weight:400;'>({c/total*100:.1f}%)</span></span>"
        f"</div>"
        for s, c in top5_sectors.items()
    ])
    st.markdown(f"""
    <div class='insight-card' style='margin-top:40px;'>
        <h4>Top 5 Sectors</h4>
        {rows}
        <div style='margin-top:14px;font-size:0.82rem;color:#7aafc4;'>
            💡 Top 3 sectors account for
            <strong style='color:#00dc82;'>{top5_sectors.iloc[:3].sum()/total*100:.0f}%</strong>
            of all startups
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── SECTION 2: STATE & CITY ────────────────────────────────────────────────────
st.markdown("<div class='section-tag'>Where are they located?</div>", unsafe_allow_html=True)
st.markdown("<div class='section-heading'>🗺️ State & City Distribution</div>", unsafe_allow_html=True)

col_state, col_city = st.columns(2)

with col_state:
    state_counts = filtered_df['State'].value_counts().head(10).reset_index()
    state_counts.columns = ['State', 'Count']
    fig_state = px.bar(state_counts, x='Count', y='State', orientation='h',
                       color='Count', color_continuous_scale='Blues',
                       title="Top 10 States")
    fig_state = dt(fig_state, height=380)
    fig_state.update_layout(yaxis=dict(categoryorder='total ascending'), showlegend=False)
    st.plotly_chart(fig_state, width="stretch")

with col_city:
    city_counts = filtered_df['Headquarters'].value_counts().head(10).reset_index()
    city_counts.columns = ['City', 'Count']
    fig_city = px.bar(city_counts, x='Count', y='City', orientation='h',
                      color='Count', color_continuous_scale='Teal',
                      title="Top 10 Cities (HQ)")
    fig_city = dt(fig_city, height=380)
    fig_city.update_layout(yaxis=dict(categoryorder='total ascending'), showlegend=False)
    st.plotly_chart(fig_city, width="stretch")


# ── SECTION 3: SECTOR × STATE HEATMAP ────────────────────────────────────────
st.markdown("<div class='section-tag'>How do sectors spread across states?</div>", unsafe_allow_html=True)
st.markdown("<div class='section-heading'>🔥 Sector × State Heatmap</div>", unsafe_allow_html=True)

top_states_list  = filtered_df['State'].value_counts().head(10).index
top_sectors_list = filtered_df['Sector'].value_counts().head(8).index
heat_df = filtered_df[
    filtered_df['State'].isin(top_states_list) &
    filtered_df['Sector'].isin(top_sectors_list)
]
pivot = pd.crosstab(heat_df['State'], heat_df['Sector'])
fig_heat = px.imshow(pivot, color_continuous_scale='Viridis', aspect='auto',
                     title="Startup Count: Top States × Top Sectors")
fig_heat = dt(fig_heat, height=420)
fig_heat.update_layout(
    xaxis=dict(tickangle=-30, tickfont=dict(size=10, color="#a8c8d8")),
    coloraxis_colorbar=dict(tickfont=dict(color="#a8c8d8"),
                            title=dict(text="Count", font=dict(color="#a8c8d8")))
)
st.plotly_chart(fig_heat, width="stretch")


# ── SECTION 4: DATASET PREVIEW ───────────────────────────────────────────────
st.markdown("<div class='section-heading'>📋 Dataset Preview</div>", unsafe_allow_html=True)

preview_cols = [c for c in ['Company', 'Sector', 'State', 'Headquarters', 'Team Size']
                if c in filtered_df.columns]
st.dataframe(filtered_df[preview_cols].head(10), width="stretch", hide_index=True)

st.markdown(
    f"<small style='color:#5a8fa8;'>Displaying top 10 of {len(filtered_df):,} records · "
    f"Use sidebar filters to refine</small>",
    unsafe_allow_html=True
)