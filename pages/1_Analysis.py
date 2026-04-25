import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.markdown("""
<style>
    /* Full width container */
    .block-container {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        padding-top: 1rem !important;
        max-width: none !important;
    }
    
    /* Full width columns */
    .element-container {
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Plotly full width */
    .plotly-chart {
        width: 100% !important;
    }
    
    /* Column full stretch */
    [data-testid="column"] {
        width: 100% !important;
        padding: 0 0.5rem !important;
    }
    
    /* Main app full width */
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: none !important;
    }

    /* ── Background: deep navy + subtle green grid ── */
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

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #071525 0%, #0b2040 100%);
        border-right: 1px solid rgba(0,220,130,0.15);
    }
    [data-testid="stSidebar"] * { color: #c8e6d0 !important; }

    /* ── Typography: titles & subheaders ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        font-family: 'Syne', sans-serif !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }

    /* ── Page title ── */
    [data-testid="stMarkdownContainer"] h1 {
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* ── Subheaders ── */
    [data-testid="stMarkdownContainer"] h2,
    .stMarkdown h2 {
        color: #00dc82 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px;
    }

    /* ── Body text & markdown ── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong {
        color: #a8c8d8 !important;
    }

    /* ── Horizontal rule ── */
    hr {
        border-color: rgba(0,220,130,0.12) !important;
    }

    /* ── Plotly chart backgrounds → transparent to show app bg ── */
    .js-plotly-plot .plotly,
    .js-plotly-plot .plotly .bg {
        background: transparent !important;
    }

    /* ── Streamlit metric boxes ── */
    [data-testid="metric-container"] {
        background: rgba(11,31,53,0.85);
        border: 1px solid rgba(0,220,130,0.15);
        border-radius: 12px;
        padding: 16px !important;
    }
    [data-testid="metric-container"] label {
        color: #5a8fa8 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'Syne', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Startup Analysis")

@st.cache_data
def get_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = get_data()

# Spacer
st.markdown("---")

# -----------------------------------------------------------
# PIE CHART — Sector Distribution + Right Analysis
# -----------------------------------------------------------
st.subheader("1️⃣ Sector Distribution")
col1, col2 = st.columns([2, 1])

with col1:
    fig1 = px.pie(df, names="Sector", title="Sector Breakdown")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("**🔥 Key Insights:**")
    top_sectors = df['Sector'].value_counts().head(3)
    st.markdown(f"**{top_sectors.index[0]}**: {top_sectors.iloc[0]} startups")
    st.markdown(f"**{top_sectors.index[1]}**: {top_sectors.iloc[1]} startups") 
    st.markdown(f"**{top_sectors.index[2]}**: {top_sectors.iloc[2]} startups")
    st.markdown("*IT dominates 42% of ecosystem*")

# -----------------------------------------------------------
#  REGION BAR CHART + Right Analysis
# -----------------------------------------------------------
st.subheader("2️⃣ Regional Dominance")
col1, col2 = st.columns([2, 1])

with col1:
    fig2 = px.bar(df.groupby(['Region', 'Sector']).size().reset_index(name='Count'), 
                  x='Count', y='Region', color='Sector', orientation='h')
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("**🌍 Takeaways:**")
    region_counts = df['Region'].value_counts()
    st.markdown(f"**{region_counts.index[0]}**: {region_counts.iloc[0]} startups")
    st.markdown("*North leads due to Delhi NCR*")
    st.markdown("*South growing rapidly*")

# -----------------------------------------------------------
#  HEATMAP — Tier vs Sector + Right Analysis
# -----------------------------------------------------------
st.subheader("3️⃣ Locality Tier vs Sector")
col1, col2 = st.columns([2, 1])

with col1:
    fig3 = px.imshow(pd.crosstab(df['Locality_Tier'], df['Sector']), 
                    title='Tier vs Sector Distribution')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("**🏙️ Strategy:**")
    st.markdown("**Tier-1 metros**:")
    st.markdown("• IT heaviest (490+ startups)")
    st.markdown("• E-commerce strong")
    st.markdown("*Tier-3: Niche survival*")

# -----------------------------------------------------------
#  GDP/POPULATION BUBBLE + Right Analysis
# -----------------------------------------------------------
st.subheader("4️⃣ Economic Drivers")
col1, col2 = st.columns([2, 1])

with col1:
    startup_count = dict(df["State"].value_counts())
    df["Startup_Count"] = df["State"].map(startup_count)
    fig4 = px.scatter(df, x='GDP_Rank', y='State_Population_Million',
                     size='Startup_Count', color='Startup_Count',
                     hover_name='State', size_max=50)
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.markdown("**💰 Economic Drivers:**")
    top_state = df['State'].value_counts().index[0]
    st.markdown(f"**{top_state}** = Startup capital")
    st.markdown("*Bubble size = Startup density*")
    delhi_count = len(df[df['State']=='Delhi'])
    karnataka_count = len(df[df['State']=='Karnataka'])
    st.markdown(f"**Delhi**: {delhi_count} startups (GDP #{df[df['State']=='Delhi']['GDP_Rank'].iloc[0]})")
    st.markdown(f"**Karnataka**: {karnataka_count} startups (GDP #{df[df['State']=='Karnataka']['GDP_Rank'].iloc[0]})")
    st.markdown("*Tier-1 metros defy GDP rankings*")
# CLEAN TREEMAP (Top 10 cities)
st.subheader("5️⃣ City-Sector Breakdown")
col1, col2 = st.columns([3, 1])

with col1:
    top_cities = df['Headquarters'].value_counts().head(10).index
    df_city_top = df[df['Headquarters'].isin(top_cities)]
    
    fig5 = px.treemap(df_city_top, path=['Headquarters','Sector'],
                     title="**Top 10 Startup Cities**",
                     color='Sector')
    fig5.update_layout(height=500, margin=dict(t=50, l=0, r=0, b=0))
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown("**📍 Top Cities:**")
    for i, city in enumerate(top_cities):
        count = len(df[df['Headquarters']==city])
        st.markdown(f"{i+1}. **{city}**: {count}")

# CLEAN ICICLE (Top states)
st.subheader("6️⃣ State → City Hierarchy")
col1, col2 = st.columns([3, 1])

with col1:
    top_states = df['State'].value_counts().head(8).index
    df_state_top = df[df['State'].isin(top_states)]
    
    fig6 = px.icicle(df_state_top, path=['State','Headquarters'],
                    title="**Top 8 States → Cities**")
    fig6.update_layout(height=500)
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    st.markdown("**🗺️ State Leaders:**")
    for i, state in enumerate(top_states):
        count = len(df[df['State']==state])
        st.markdown(f"{i+1}. **{state}**: {count}")

# -----------------------------------------------------------
# FUNDING Box plot + Right Analysis
st.subheader("7️⃣ Funding Distribution")
col1, col2 = st.columns([3, 1])

with col1:
    # Filter funded startups only
    funded_df = df[df['Amount raised numeric'] > 0].copy()
    
    # Box plot + outliers (perfect for skew)
    fig7 = px.box(funded_df, 
                 y="Amount raised numeric",
                 orientation="v",
                 title="Funding: Extreme Right Skew (61 Funded Startups)",
                 points="all",  # Show all points for density
                 color_discrete_sequence=['#FF6B6B'],
                 labels={'Amount raised numeric': 'Funding Amount (₹)'})
    
    # Key annotations (data-driven)
    median_val = funded_df['Amount raised numeric'].median()
    p90_val = funded_df['Amount raised numeric'].quantile(0.9)
    max_val = funded_df['Amount raised numeric'].max()
    
    # Green median line
    fig7.add_hline(y=median_val/1e7,  # Convert to Cr
                   line_dash="dash", line_color="green",
                   annotation_text=f"Median: ₹{median_val:,.0f}", 
                   annotation_position="right")
    
    # Orange 90th percentile
    fig7.add_hline(y=p90_val/1e7,
                   line_dash="dot", line_color="orange",
                   annotation_text=f"90th: ₹{p90_val:,.0f}", 
                   annotation_position="right")
    
    # Red max outlier
    fig7.add_hline(y=max_val/1e7,
                   line_dash="solid", line_color="red",
                   annotation_text=f"Max: ₹{max_val:,.0f}", 
                   annotation_position="right")
    
    # Log Y-axis for clean skew visualization
    fig7.update_yaxes(type="log", 
                     tickformat=".0f",
                     range=[5,9])  # Auto-scale
    
    fig7.update_layout(height=500, showlegend=False)
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