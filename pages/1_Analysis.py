import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Startup Ecosystem Insights", 
    layout="wide", 
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* GLOBAL FONT + BASE TEXT COLOR */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #e8f4f0 !important;
}

/* REMOVE DEFAULT HEADER GAP */
header[data-testid="stHeader"] {
    display: none !important;
}

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f35 50%, #0a1f15 100%);
    background-attachment: fixed;
}

/* ── FIX: st.title / st.subheader / st.header ────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* ── FIX: st.markdown plain text ───────────────────────────────── */
p, li, span, div {
    color: #e8f4f0;
}

/* ── FIX: st.markdown bold (**text**) ─────────────────────────── */
strong {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── FIX: st.markdown italic (*text*) ─────────────────────────── */
em {
    color: #a0c4b8 !important;
}

/* ── FIX: horizontal rule ──────────────────────────────────────── */
hr {
    border-color: rgba(0,220,130,0.2) !important;
}

/* SIDEBAR COLLAPSE HIDE */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%) !important;
    border-right: 1px solid rgba(0,220,130,0.15);
    min-width: 320px !important;
    max-width: 320px !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stTextElement {
    color: #ffffff !important;
}

[data-testid="stSidebar"] strong {
    color: #00dc82 !important;
}

/* Metric Container */
[data-testid="metric-container"] {
    background: rgba(11,31,53,0.85);
    border: 1px solid rgba(0,220,130,0.15);
    border-radius: 12px;
    padding: 16px !important;
}

[data-testid="metric-container"] label {
    color: #a0c4b8 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ── SUBHEADER ACCENT LINE ─────────────────────────────────────── */
h2[data-testid="stHeading"],
.stSubheader {
    padding-bottom: 8px !important;
    border-bottom: 1px solid rgba(0,220,130,0.2) !important;
}

/* ── DATAFRAME ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"] th {
    background: rgba(0,220,130,0.1) !important;
    color: #00dc82 !important;
    font-size: 0.78rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

[data-testid="stDataFrame"] td {
    color: #e0f0e8 !important;
}

/* OPTIONAL: custom highlight class */
.highlight {
    color: #ffeb3b !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY DARK THEME HELPER ───────────────────────────────────────────────────
# Apply this to every fig so chart text is always bright on dark background
def dark_theme(fig, height=500):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11,31,53,0.6)",
        font=dict(color="#e8f4f0", family="DM Sans"),
        title_font=dict(color="#ffffff", size=16),
        legend=dict(
            bgcolor="rgba(11,31,53,0.8)",
            bordercolor="rgba(0,220,130,0.2)",
            font=dict(color="#e8f4f0"),
        ),
        xaxis=dict(
            color="#a0c4b8",
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(0,220,130,0.2)",
        ),
        yaxis=dict(
            color="#a0c4b8",
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(0,220,130,0.2)",
        ),
    )
    return fig


# ─── PAGE CONTENT ──────────────────────────────────────────────────────────────
st.title("📊 Startup Analysis")

@st.cache_data
def get_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = get_data()

st.markdown("---")

# 1️⃣ Sector Distribution
st.subheader("1️⃣ Sector Distribution")
col1, col2 = st.columns([2, 1])
with col1:
    fig1 = px.pie(df, names="Sector", title="Sector Breakdown")
    fig1 = dark_theme(fig1)
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.markdown("**🔥 Key Insights:**")
    top_sectors = df['Sector'].value_counts().head(3)
    st.markdown(f"**{top_sectors.index[0]}**: {top_sectors.iloc[0]} startups")
    st.markdown(f"**{top_sectors.index[1]}**: {top_sectors.iloc[1]} startups")
    st.markdown(f"**{top_sectors.index[2]}**: {top_sectors.iloc[2]} startups")
    st.markdown("*IT dominates 42% of ecosystem*")

# 2️⃣ Regional Dominance
st.subheader("2️⃣ Regional Dominance")
col1, col2 = st.columns([2, 1])
with col1:
    fig2 = px.bar(df.groupby(['Region', 'Sector']).size().reset_index(name='Count'),
                  x='Count', y='Region', color='Sector', orientation='h')
    fig2 = dark_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.markdown("**🌍 Takeaways:**")
    region_counts = df['Region'].value_counts()
    st.markdown(f"**{region_counts.index[0]}**: {region_counts.iloc[0]} startups")
    st.markdown("*North leads due to Delhi NCR*")
    st.markdown("*South growing rapidly*")

# 3️⃣ Locality Tier vs Sector
st.subheader("3️⃣ Locality Tier vs Sector")
col1, col2 = st.columns([2, 1])
with col1:
    fig3 = px.imshow(pd.crosstab(df['Locality_Tier'], df['Sector']),
                     title='Tier vs Sector Distribution')
    fig3 = dark_theme(fig3)
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.markdown("**🏙️ Strategy:**")
    st.markdown("**Tier-1 metros**:")
    st.markdown("• IT heaviest (490+ startups)")
    st.markdown("• E-commerce strong")
    st.markdown("*Tier-3: Niche survival*")

# 4️⃣ Economic Drivers
st.subheader("4️⃣ Economic Drivers")
col1, col2 = st.columns([2, 1])
with col1:
    startup_count = dict(df["State"].value_counts())
    df["Startup_Count"] = df["State"].map(startup_count)
    fig4 = px.scatter(df, x='GDP_Rank', y='State_Population_Million',
                      size='Startup_Count', color='Startup_Count',
                      hover_name='State', size_max=50)
    fig4 = dark_theme(fig4)
    st.plotly_chart(fig4, use_container_width=True)
with col2:
    st.markdown("**💰 Economic Drivers:**")
    top_state = df['State'].value_counts().index[0]
    st.markdown(f"**{top_state}** = Startup capital")
    st.markdown("*Bubble size = Startup density*")
    delhi_count = len(df[df['State'] == 'Delhi'])
    karnataka_count = len(df[df['State'] == 'Karnataka'])
    st.markdown(f"**Delhi**: {delhi_count} startups (GDP #{df[df['State']=='Delhi']['GDP_Rank'].iloc[0]})")
    st.markdown(f"**Karnataka**: {karnataka_count} startups (GDP #{df[df['State']=='Karnataka']['GDP_Rank'].iloc[0]})")
    st.markdown("*Tier-1 metros defy GDP rankings*")

# 5️⃣ City-Sector Breakdown
st.subheader("5️⃣ City-Sector Breakdown")
col1, col2 = st.columns([3, 1])
with col1:
    top_cities = df['Headquarters'].value_counts().head(10).index
    df_city_top = df[df['Headquarters'].isin(top_cities)]
    fig5 = px.treemap(df_city_top, path=['Headquarters', 'Sector'],
                      title="Top 10 Startup Cities", color='Sector')
    fig5 = dark_theme(fig5)
    fig5.update_layout(margin=dict(t=50, l=0, r=0, b=0))
    st.plotly_chart(fig5, use_container_width=True)
with col2:
    st.markdown("**📍 Top Cities:**")
    for i, city in enumerate(top_cities):
        count = len(df[df['Headquarters'] == city])
        st.markdown(f"{i+1}. **{city}**: {count}")

# 6️⃣ State → City Hierarchy
st.subheader("6️⃣ State → City Hierarchy")
col1, col2 = st.columns([3, 1])
with col1:
    top_states = df['State'].value_counts().head(8).index
    df_state_top = df[df['State'].isin(top_states)]
    fig6 = px.icicle(df_state_top, path=['State', 'Headquarters'],
                     title="Top 8 States → Cities")
    fig6 = dark_theme(fig6)
    st.plotly_chart(fig6, use_container_width=True)
with col2:
    st.markdown("**🗺️ State Leaders:**")
    for i, state in enumerate(top_states):
        count = len(df[df['State'] == state])
        st.markdown(f"{i+1}. **{state}**: {count}")

# 7️⃣ Funding Distribution
st.subheader("7️⃣ Funding Distribution")
col1, col2 = st.columns([3, 1])
with col1:
    funded_df = df[df['Amount raised numeric'] > 0].copy()
    fig7 = px.box(funded_df,
                  y="Amount raised numeric",
                  orientation="v",
                  title="Funding: Extreme Right Skew (61 Funded Startups)",
                  points="all",
                  color_discrete_sequence=['#FF6B6B'],
                  labels={'Amount raised numeric': 'Funding Amount (₹)'})
    median_val = funded_df['Amount raised numeric'].median()
    p90_val    = funded_df['Amount raised numeric'].quantile(0.9)
    max_val    = funded_df['Amount raised numeric'].max()
    fig7.add_hline(y=median_val, line_dash="dash",  line_color="#00dc82",
                   annotation_text=f"Median: ₹{median_val:,.0f}", annotation_position="right")
    fig7.add_hline(y=p90_val,    line_dash="dot",   line_color="orange",
                   annotation_text=f"90th: ₹{p90_val:,.0f}",    annotation_position="right")
    fig7.add_hline(y=max_val,    line_dash="solid", line_color="red",
                   annotation_text=f"Max: ₹{max_val:,.0f}",     annotation_position="right")
    fig7.update_yaxes(type="log", tickformat=".0f", range=[5, 9])
    fig7 = dark_theme(fig7)
    fig7.update_layout(showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)
with col2:
    funded_pct = (len(funded_df) / len(df)) * 100
    st.markdown("**💸 Bootstrap Reality:**")
    st.markdown(f"**{funded_pct:.0f}% funded** (61 startups)")
    st.markdown("**Key Stats:**")
    st.markdown("*PB Healthcare (HealthTech): ₹21.8Cr*")
    st.markdown("*Emergent (IT): ₹10 Cr*")
    st.markdown(f"• Median: **₹27L**")
    st.markdown(f"• 90th %ile: **₹1.5Cr**")
    st.markdown(f"• Max: **₹21.8Cr**")
    st.markdown("*96.5% bootstrapped*")