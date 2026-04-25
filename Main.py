import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="🚀 Startup Analytics Platform", 
    page_icon="🚀",
    layout="wide"
)
# Global data
@st.cache_data
def load_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = load_data()

# 4 METRICS
st.markdown("### 📊 Dashboard Overview")
col1, col2, col3, col4 = st.columns(4)

col1.metric("🏢 **Total Startups**", f"{len(df):,}")
col2.metric("📍 **States**", df['State'].nunique())
col3.metric("🏙️ **Cities**", df['Headquarters'].nunique())
col4.metric("💼 **Sectors**", df['Sector'].nunique())

# DATA SAMPLE
st.markdown("### 📋 Dataset Preview")
st.dataframe(df[['Company', 'Sector', 'State', 'Headquarters', 'Team Size']].head(10), 
             use_container_width=True)


st.sidebar.success(f"📊 Dataset: {len(df):,} startups")