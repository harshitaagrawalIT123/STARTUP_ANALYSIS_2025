import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib

st.set_page_config(page_title="2025 Startups Dashboard", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8f4f0 !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f35 50%, #0a1f15 100%);
    background-attachment: fixed;
}

[data-testid="stSidebarCollapseButton"] { display: none !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%);
    border-right: 1px solid rgba(0,220,130,0.15);
    min-width: 320px !important;
    max-width: 320px !important;
}
[data-testid="stSidebar"] * { color: #c8e6d0 !important; }

[data-testid="stHeader"]     { background: transparent !important; border-bottom: none !important; }
[data-testid="stToolbar"]    { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

h1, h2, h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: #a8c8d8 !important; }
[data-testid="stMarkdownContainer"] strong { color: #ffffff !important; }

hr { border-color: rgba(0,220,130,0.12) !important; }

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

[data-testid="stAlert"] {
    background: rgba(11,31,53,0.9) !important;
    border: 1px solid rgba(0,220,130,0.2) !important;
    border-radius: 10px !important;
    color: #a8c8d8 !important;
}

/* Section divider */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00dc82;
    margin: 32px 0 4px 0;
}
</style>
""", unsafe_allow_html=True)


# ─── DARK THEME HELPER ────────────────────────────────────────────────────────
def dt(fig, height=420):
    """Apply consistent dark theme to any Plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11,31,53,0.5)",
        font=dict(color="#e8f4f0", family="DM Sans", size=12),
        title_font=dict(color="#ffffff", size=14, family="Syne"),
        coloraxis_colorbar=dict(tickfont=dict(color="#a8c8d8")),
        legend=dict(
            bgcolor="rgba(11,31,53,0.8)",
            bordercolor="rgba(0,220,130,0.2)",
            font=dict(color="#e8f4f0"),
        ),
        xaxis=dict(color="#a0c4b8", gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(0,220,130,0.2)", tickfont=dict(color="#a8c8d8")),
        yaxis=dict(color="#a0c4b8", gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(0,220,130,0.2)", tickfont=dict(color="#a8c8d8")),
    )
    return fig


# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("Finalcompanies.xlsx")
    df['Team_Size_Num'] = pd.to_numeric(df['Team Size'], errors='coerce')
    return df

df = load_data()
st.title("🚀 2025 Startups Dashboard")

# ─── SIDEBAR FILTERS ──────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

state_list = ["All"] + sorted(df["State"].dropna().unique().tolist())
state = st.sidebar.selectbox("State", state_list)

if state == "All":
    hq_list = ["All"] + sorted(df["Headquarters"].dropna().unique().tolist())
else:
    hq_list = ["All"] + sorted(df[df["State"] == state]["Headquarters"].dropna().unique().tolist())
hq = st.sidebar.selectbox("City", hq_list)

sector_list = ["All"] + sorted(df["Sector"].dropna().unique().tolist())
sector = st.sidebar.selectbox("Sector", sector_list)

ctype_list = ["All"] + sorted(df["Company Type"].dropna().unique().tolist())
ctype = st.sidebar.selectbox("Company Type", ctype_list)

filtered_df = df.copy()
if state  != "All": filtered_df = filtered_df[filtered_df["State"]        == state]
if hq     != "All": filtered_df = filtered_df[filtered_df["Headquarters"] == hq]
if sector != "All": filtered_df = filtered_df[filtered_df["Sector"]       == sector]
if ctype  != "All": filtered_df = filtered_df[filtered_df["Company Type"] == ctype]

st.sidebar.markdown("---")
st.sidebar.info(f"""
**Active Filters:**
- State: {state}
- City: {hq}
- Sector: {sector}
- Type: {ctype}

**Results: {len(filtered_df)} startups**
""")

if len(filtered_df) == 0:
    st.warning("❌ No data. Reset filters.")
    st.stop()


# ─── KPIs ─────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Startups",  len(filtered_df))
col2.metric("Sectors",   filtered_df["Sector"].nunique())
col3.metric("Cities",    filtered_df["Headquarters"].nunique())
col4.metric("Avg Team",  f"{filtered_df['Team_Size_Num'].mean():.0f}")

st.markdown("---")


# ─── ROW 1: Sector Treemap (wide) + Top Sectors Bar ──────────────────────────
st.markdown("<div class='section-label'>Distribution</div>", unsafe_allow_html=True)
col_left, col_right = st.columns([3, 2])

with col_left:
    sector_agg = filtered_df.groupby(["Sector", "Sub Sector Main"]).size().reset_index(name='count')
    fig1 = px.treemap(sector_agg, path=["Sector", "Sub Sector Main"], values="count",
                      title="📊 Sector → Sub-Sectors", color="count",
                      color_continuous_scale='Viridis')
    fig1 = dt(fig1, height=420)
    fig1.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    st.plotly_chart(fig1, width="stretch")

with col_right:
    src4 = filtered_df if state != "All" else df
    sector_counts = src4['Sector'].value_counts().head(10)
    fig4 = px.bar(sector_counts.reset_index(), x='count', y='Sector', orientation='h',
                  title="📈 Top Sectors", color='count',
                  color_continuous_scale='Plasma')
    fig4 = dt(fig4, height=420)
    fig4.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig4,width="stretch")


# ─── ROW 2: Top Cities (wide) + Top States ────────────────────────────────────
st.markdown("<div class='section-label'>Geography</div>", unsafe_allow_html=True)
col_left, col_right = st.columns([3, 2])

with col_left:
    city_counts = filtered_df['Headquarters'].value_counts().head(15).reset_index()
    city_counts.columns = ['City', 'Startups']
    fig2 = px.bar(city_counts, x='Startups', y='City', orientation='h',
                  title="🏙️ Top 15 Startup Cities", color='Startups',
                  color_continuous_scale='Blues', text='Startups')
    fig2 = dt(fig2, height=460)
    fig2.update_traces(textposition='outside', textfont=dict(color='#e8f4f0'))
    fig2.update_layout(showlegend=False,
                       yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig2, width="stretch")

with col_right:
    src3 = filtered_df if sector != "All" else df
    state_counts = src3['State'].value_counts().head(10)
    fig3 = px.bar(state_counts.reset_index(), x='count', y='State', orientation='h',
                  title="🏆 Top States", color='count',
                  color_continuous_scale='Viridis')
    fig3 = dt(fig3, height=460)
    fig3.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig3, width="stretch")


# ─── ROW 3: Sunburst + Box Plot ───────────────────────────────────────────────
st.markdown("<div class='section-label'>Hierarchy & Team</div>", unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1])

with col_left:
    top_states_f = filtered_df['State'].value_counts().head(8).index
    sun_df  = filtered_df[filtered_df['State'].isin(top_states_f)]
    sun_agg = sun_df.groupby(["Sector", "State", "Headquarters"]).size().reset_index(name='count')
    fig5 = px.sunburst(sun_agg, path=["Sector", "State", "Headquarters"],
                       values="count", title="🌟 Sector → State → City")
    fig5 = dt(fig5, height=460)
    st.plotly_chart(fig5, width="stretch")

with col_right:
    fig6 = px.box(filtered_df, x='Sector', y='Team_Size_Num',
                  title="👥 Team Size by Sector", color='Sector')
    fig6 = dt(fig6, height=460)
    fig6.update_layout(
        showlegend=False,
        xaxis=dict(tickangle=-30, tickfont=dict(size=10, color="#a8c8d8"))
    )
    st.plotly_chart(fig6,width="stretch")


# ─── ROW 4: Funding Heatmap (full width) ─────────────────────────────────────
st.markdown("<div class='section-label'>Funding</div>", unsafe_allow_html=True)
st.subheader("💰 Avg Funding: State × Sector")

pivot = pd.crosstab(filtered_df["State"], filtered_df["Sector"],
                    values=filtered_df["Amount raised numeric"], aggfunc='mean').fillna(0)
fig7 = px.imshow(pivot, title="Average Funding Heatmap (₹)",
                 color_continuous_scale='Viridis', aspect="auto",
                 labels=dict(color="Avg Funding (₹)"))
fig7 = dt(fig7, height=500)
fig7.update_layout(
    xaxis=dict(tickangle=-35, tickfont=dict(size=10, color="#a8c8d8")),
    coloraxis_colorbar=dict(
        title=dict(text="₹ Avg", font=dict(color="#a8c8d8")),
        tickfont=dict(color="#a8c8d8"),
    )
)
st.plotly_chart(fig7, width="stretch")

st.sidebar.info(f"**Filtered: {len(filtered_df)} startups**")