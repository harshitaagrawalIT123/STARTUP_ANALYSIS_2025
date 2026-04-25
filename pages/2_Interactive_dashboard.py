import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib

st.set_page_config(page_title="2025 Startups Dashboard", layout="wide")

# ── Background & theme styling ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Deep navy + subtle green grid */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f35 50%, #0a1f15 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    display: none !important;
}
header {
    display: none !important;
}
[data-testid="stToolbar"] {
    display: none !important;
}
# Replace the header-hiding block with this more targeted version:
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}
[data-testid="stToolbar"] {
    display: none !important;
}
/* Keep the sidebar toggle button visible */
[data-testid="collapsedControl"] {
    display: flex !important;
    background: rgba(0, 220, 130, 0.15) !important;
    border: 1px solid rgba(0, 220, 130, 0.3) !important;
    border-radius: 8px !important;
    color: #00dc82 !important;
}
[data-testid="collapsedControl"] svg {
    fill: #00dc82 !important;
}       
/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%);
    border-right: 1px solid rgba(0,220,130,0.15);
}
[data-testid="stSidebar"] * { color: #c8e6d0 !important; }

/* Titles & subheaders */
h1, h2, h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

/* Body text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong {
    color: #a8c8d8 !important;
}

/* HR divider */
hr { border-color: rgba(0,220,130,0.12) !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: rgba(11,31,53,0.85);
    border: 1px solid rgba(0,220,130,0.15);
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="metric-container"] label { color: #5a8fa8 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
}

/* Info/warning boxes */
[data-testid="stAlert"] {
    background: rgba(11,31,53,0.9) !important;
    border: 1px solid rgba(0,220,130,0.2) !important;
    border-radius: 10px !important;
    color: #a8c8d8 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("Finalcompanies.xlsx")
    df['Team_Size_Num'] = pd.to_numeric(df['Team Size'], errors='coerce')
    return df

df = load_data()
st.title("🚀 2025 Startups Dashboard")

# Apply filters
st.sidebar.header("🔍 Filters")

# 1. STATE
state_list = ["All"] + sorted(df["State"].dropna().unique().tolist())
state = st.sidebar.selectbox("State", state_list)

# 2. CITY 
if state == "All":
    hq_list = ["All"] + sorted(df["Headquarters"].dropna().unique().tolist())
else:
    state_df = df[df["State"] == state]
    hq_list = ["All"] + sorted(state_df["Headquarters"].dropna().unique().tolist())
hq = st.sidebar.selectbox("City", hq_list)

# 3. Other filters 
sector_list = ["All"] + sorted(df["Sector"].dropna().unique().tolist())
sector = st.sidebar.selectbox("Sector", sector_list)

ctype_list = ["All"] + sorted(df["Company Type"].dropna().unique().tolist())
ctype = st.sidebar.selectbox("Company Type", ctype_list)

filtered_df = df.copy()

# State first
if state != "All":
    filtered_df = filtered_df[filtered_df["State"] == state]

# City (only if state selected OR All)
if hq != "All":
    filtered_df = filtered_df[filtered_df["Headquarters"] == hq]

# Other filters
if sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == sector]

if ctype != "All":
    filtered_df = filtered_df[filtered_df["Company Type"] == ctype]

# ==================================================
# 📊 FILTER STATUS
# ==================================================
st.sidebar.markdown("---")
st.sidebar.info(f"""
**Active Filters:**
• State: {state}
• City: {hq} 
• Sector: {sector}
• Type: {ctype}

**Results: {len(filtered_df)} startups**
""")

if len(filtered_df) == 0:
    st.warning("❌ No data. Reset filters.")
    st.stop()

# === KPIs ===
col1, col2, col3, col4 = st.columns(4)
col1.metric("Startups", len(filtered_df))
col2.metric("Sectors", filtered_df["Sector"].nunique())
col3.metric("Cities", filtered_df["Headquarters"].nunique())
col4.metric("Avg Team", f"{filtered_df['Team_Size_Num'].mean():.0f}")

col1, col2 = st.columns(2)

#  CHART 1: TREEMAP
sector_agg = filtered_df.groupby(["Sector", "Sub Sector Main"]).size().reset_index(name='count')
fig1 = px.treemap(sector_agg, path=["Sector", "Sub Sector Main"], 
                 values="count",
                 title="📊 Sector → Sub-Sectors",
                 color="count",
                 color_continuous_scale='Viridis')
st.plotly_chart(fig1, use_container_width=True)

#  CHART 2: ICICLE
city_counts = filtered_df['Headquarters'].value_counts().head(15).reset_index()
city_counts.columns = ['City', 'Startups']
fig2 = px.bar(city_counts, x='Startups', y='City', orientation='h',
             title="🏙️ Top 15 Startup Cities",
             color='Startups', 
             color_continuous_scale='Blues',
             text='Startups')
fig2.update_traces(textposition='outside')
fig2.update_layout(height=500, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

#  CHART 3: Top States (Sector-aware)
if sector != "All":
    state_counts = filtered_df['State'].value_counts().head(10)
else:
    state_counts = df['State'].value_counts().head(10)
fig3 = px.bar(state_counts.reset_index(), x='count', y='State', 
             orientation='h', title="🏆 Top States",
             color='count', color_continuous_scale='Viridis')
st.plotly_chart(fig3, use_container_width=True)

#  CHART 4: Top Sectors (State-aware)
if state != "All":
    sector_counts = filtered_df['Sector'].value_counts().head(10)
else:
    sector_counts = df['Sector'].value_counts().head(10)
fig4 = px.bar(sector_counts.reset_index(), x='count', y='Sector', 
             orientation='h', title="📈 Top Sectors",
             color='count', color_continuous_scale='Plasma')
st.plotly_chart(fig4, use_container_width=True)

# === ROW 3: Sunburst + Box ===
col1, col2 = st.columns(2)

# CHART 5: SUNBURST
top_states_f = filtered_df['State'].value_counts().head(8).index
sun_df = filtered_df[filtered_df['State'].isin(top_states_f)]
sun_agg = sun_df.groupby(["Sector", "State", "Headquarters"]).size().reset_index(name='count')
fig5 = px.sunburst(sun_agg, path=["Sector", "State", "Headquarters"],
                  values="count",
                  title="🌟 Hierarchy: Sector→State→HQ")
st.plotly_chart(fig5, use_container_width=True)

#  CHART 6: TEAM BOX
fig6 = px.box(filtered_df, x='Sector', y='Team_Size_Num',
             title="👥 Team Size Distribution",
             color='Sector')
fig6.update_layout(height=400)
st.plotly_chart(fig6, use_container_width=True)

# === ROW 4: FUNDING HEATMAP ===
st.subheader("💰 Funding: State vs Sector")
pivot = pd.crosstab(filtered_df["State"], filtered_df["Sector"], 
                   values=filtered_df["Amount raised numeric"], aggfunc='mean').fillna(0)
fig7 = px.imshow(pivot, title="Avg Funding Heatmap", 
                color_continuous_scale='Viridis', aspect="auto")
st.plotly_chart(fig7, use_container_width=True)

st.sidebar.info(f"**Filtered: {len(filtered_df)} startups**")