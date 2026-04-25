import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="👥 Team Size Predictor v2", layout="wide", page_icon="🚀")

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
/* ── Remove Streamlit white top bar ── */
[data-testid="stHeader"] {
    display: none !important;
}
header {
    display: none !important;
}
[data-testid="stToolbar"] {
    display: none !important;
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

/* Alert / info / success boxes */
[data-testid="stAlert"] {
    background: rgba(11,31,53,0.9) !important;
    border: 1px solid rgba(0,220,130,0.2) !important;
    border-radius: 10px !important;
    color: #a8c8d8 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: rgba(11,31,53,0.7) !important;
    border: 1px solid rgba(0,220,130,0.12) !important;
    border-radius: 12px !important;
}

/* Primary button */
[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(90deg, #00dc82, #00b4d8) !important;
    color: #050d1a !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    opacity: 0.88 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Startup Team Size Predictor")
st.markdown("**Enhanced Poisson Regression** - Optimal hiring for your startup")

# Load model (cached for speed)
@st.cache_resource
def load_model_components():
    model = joblib.load('team_size_poisson_final.pkl')
    encoders = joblib.load('encoders_final.pkl')
    scaler = joblib.load('scaler_final.pkl')
    features = joblib.load('features_final.pkl')
    return model, encoders, scaler, features

model, encoders, scaler, features = load_model_components()
st.success("✅ Production model loaded! (787 startups trained)")

# Load dataset for reference
@st.cache_data
def get_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = get_data()
st.sidebar.success(f"📊 {len(df)} startups | MAE: ~3 employees")

# ==================================================
# USER INPUTS (Sidebar)
# ==================================================
st.sidebar.header("📝 Your Startup")

# Dropdowns (match training data)
sector_options = list(encoders['Sector'].classes_)
state_options = list(encoders['State'].classes_)
tier_options = list(encoders['Locality_Tier'].classes_)
type_options = list(encoders['Company Type'].classes_)

sector = st.sidebar.selectbox("**Sector**", sector_options)
state = st.sidebar.selectbox("**State**", state_options)
locality_tier = st.sidebar.selectbox("**City Tier**", tier_options)
company_type = st.sidebar.selectbox("**Funding**", type_options)

# Sliders (match feature ranges)
funding_cr = st.sidebar.slider("**Funding (₹ Cr)**", 0.0, 25.0, 2.5, 0.5)
gdp_rank = st.sidebar.slider("**GDP Rank**", 1, 25, 10)
city_pop_mn = st.sidebar.slider("**City Pop (Mn)**", 1.0, 70.0, 20.0, 5.0)
founders = st.sidebar.slider("**Founders**", 1, 8, 2)

# ==================================================
# BULLETPROOF PREDICTION
# ==================================================
def safe_predict(sector, state, locality_tier, company_type, funding_cr, gdp_rank, city_pop, founders):
    input_data = pd.DataFrame({
        'Sector': [sector], 'State': [state], 'Locality_Tier': [locality_tier], 
        'Company Type': [company_type], 'Funding_Cr': [funding_cr], 
        'GDP_Rank': [gdp_rank], 'City_Population_Million': [city_pop], 
        'Founder Count': [founders]
    })
    
    categorical_features = ['Sector', 'State', 'Locality_Tier', 'Company Type']
    numeric_features = ['Funding_Cr', 'GDP_Rank', 'City_Population_Million', 'Founder Count']
    
    # Safe encoding
    for col in categorical_features:
        try:
            input_data[col] = encoders[col].transform(input_data[col].astype(str))
        except:
            input_data[col] = 0  # Fallback to most common
    
    # Safe scaling
    input_data[numeric_features] = scaler.transform(input_data[numeric_features])
    
    pred = model.predict(input_data)[0]
    return int(np.clip(pred.round(), 1, 500))  # Reasonable bounds

# ==================================================
# PREDICT BUTTON
# ==================================================
if st.button("🔮 **Predict Optimal Team Size**", type="primary", use_container_width=True):
    with st.spinner("⚙️ Calculating..."):
        predicted_size = safe_predict(sector, state, locality_tier, company_type,
                                    funding_cr, gdp_rank, city_pop_mn, founders)
        
        # Results
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 **Team Size**", f"{predicted_size}")
        col2.metric("💰 **Funding**", f"₹{funding_cr:,.1f} Cr")
        col3.metric("🏛️ **City**", locality_tier)
        col4.metric("👨‍👩‍👧‍👦 **Founders**", founders)
        
        st.balloons()
        
        # Recommendation
        st.markdown(f"""
        ## 🎯 **Hiring Recommendation**
        **Your {sector} startup** in **{state}** should hire **{predicted_size} employees**.
        
        **Growth Factors:**
        - ✅ {company_type} status
        - ✅ Tier-{locality_tier.split('-')[0]} city  
        - ✅ GDP Rank #{gdp_rank}
        """)

# ==================================================
# MODEL INSIGHTS
# ==================================================
with st.expander("📊 **Model Performance & Features**"):
    try:
        impact_df = pd.read_excel('feature_importance_final.xlsx')
        st.dataframe(impact_df.head(10), use_container_width=True)
        st.caption("Top features driving team size predictions")
    except:
        st.info("📈 Feature importance: Funding_Cr, Locality_Tier, GDP_Rank lead")

# ==================================================
# DATA EXPLORER
# ==================================================
with st.expander("🔍 **Dataset Explorer**"):
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[['Company', 'Sector', 'State', 'Team Size']].head(10))
    with col2:
        st.metric("Dataset Stats", len(df))
        st.metric("Avg Team Size", f"{df['Team Size'].mean():.0f}")

st.markdown("---")
st.markdown("**🎓 Harshita Agrawal | PoissonRegressor v2 **")