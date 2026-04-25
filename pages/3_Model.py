import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib

st.set_page_config(
    page_title="India Startup Pulse 2025",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── BASE ────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #e8f4f0 !important;
}

/* ── BACKGROUND ──────────────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f35 50%, #0a1f15 100%);
    background-attachment: fixed;
}

/* ── HIDE CHROME ─────────────────────────────────────────────── */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── HEADINGS ────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

/* ── MARKDOWN TEXT ───────────────────────────────────────────── */
[data-testid="stMarkdownContainer"] p  { color: #c8e6d0 !important; }
[data-testid="stMarkdownContainer"] li { color: #c8e6d0 !important; }
[data-testid="stMarkdownContainer"] strong { color: #ffffff !important; }
[data-testid="stMarkdownContainer"] em    { color: #a0c4b8 !important; }

/* ── BUTTON ──────────────────────────────────────────────────── */
[data-testid="stButton"] button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* ── METRIC ──────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: rgba(11,31,53,0.85);
    border: 1px solid rgba(0,220,130,0.2);
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    color: #5a8fa8 !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.8rem !important;
}

/* ── SUCCESS / INFO / WARNING ALERTS ────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(11,31,53,0.9) !important;
    border: 1px solid rgba(0,220,130,0.25) !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"] p { color: #c8e6d0 !important; }

/* ── SPINNER ─────────────────────────────────────────────────── */
[data-testid="stSpinner"] p { color: #c8e6d0 !important; }

/* ── EXPANDER ────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(11,31,53,0.6) !important;
    border: 1px solid rgba(0,220,130,0.15) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #ffffff !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] summary:hover {
    color: #00dc82 !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li { color: #c8e6d0 !important; }

/* ── CAPTION ─────────────────────────────────────────────────── */
[data-testid="stCaptionContainer"] p { color: #5a8fa8 !important; }

/* ── DATAFRAME ───────────────────────────────────────────────── */
[data-testid="stDataFrame"] th {
    background: rgba(0,220,130,0.1) !important;
    color: #00dc82 !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
[data-testid="stDataFrame"] td { color: #e0f0e8 !important; }

/* ── SELECTBOX / SLIDER LABELS ───────────────────────────────── */
[data-testid="stWidgetLabel"] p { color: #a0c4b8 !important; font-weight: 500 !important; }
.stSlider [data-testid="stWidgetLabel"] p { color: #a0c4b8 !important; }

/* ── HR ──────────────────────────────────────────────────────── */
hr { border-color: rgba(0,220,130,0.15) !important; }

/* ── SIDEBAR ─────────────────────────────────────────────────── */
[data-testid="stSidebarCollapseButton"] { display: none !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #071525 0%, #0b2040 100%);
    border-right: 1px solid rgba(0,220,130,0.15);
    min-width: 320px !important;
    max-width: 320px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] strong { color: #00dc82 !important; }
[data-testid="stSidebar"] small  { color: #c8e6d0 !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #a0c4b8 !important; }

/* ── HIGHLIGHT UTIL ──────────────────────────────────────────── */
.highlight { color: #ffcc00 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ─── PAGE CONTENT ──────────────────────────────────────────────────────────────
st.title("🚀 Startup Team Size Predictor")
st.markdown("**Enhanced Poisson Regression** — Optimal hiring for your startup")

@st.cache_resource
def load_model_components():
    model    = joblib.load('team_size_poisson_final.pkl')
    encoders = joblib.load('encoders_final.pkl')
    scaler   = joblib.load('scaler_final.pkl')
    features = joblib.load('features_final.pkl')
    return model, encoders, scaler, features

model, encoders, scaler, features = load_model_components()
st.success("✅ Production model loaded! (787 startups trained)")

@st.cache_data
def get_data():
    return pd.read_excel("Finalcompanies.xlsx")

df = get_data()
st.sidebar.success(f"📊 {len(df)} startups | MAE: ~3 employees")

# ─── SIDEBAR INPUTS ────────────────────────────────────────────────────────────
st.sidebar.header("📝 Your Startup")

sector_options   = list(encoders['Sector'].classes_)
state_options    = list(encoders['State'].classes_)
tier_options     = list(encoders['Locality_Tier'].classes_)
type_options     = list(encoders['Company Type'].classes_)

sector        = st.sidebar.selectbox("Sector",    sector_options)
state         = st.sidebar.selectbox("State",     state_options)
locality_tier = st.sidebar.selectbox("City Tier", tier_options)
company_type  = st.sidebar.selectbox("Funding",   type_options)

funding_cr  = st.sidebar.slider("Funding (₹ Cr)",  0.0,  25.0, 2.5,  0.5)
gdp_rank    = st.sidebar.slider("GDP Rank",          1,    25,   10)
city_pop_mn = st.sidebar.slider("City Pop (Mn)",    1.0,  70.0, 20.0, 5.0)
founders    = st.sidebar.slider("Founders",          1,    8,    2)

# ─── PREDICTION ────────────────────────────────────────────────────────────────
def safe_predict(sector, state, locality_tier, company_type,
                 funding_cr, gdp_rank, city_pop, founders):
    input_data = pd.DataFrame({
        'Sector': [sector], 'State': [state],
        'Locality_Tier': [locality_tier], 'Company Type': [company_type],
        'Funding_Cr': [funding_cr], 'GDP_Rank': [gdp_rank],
        'City_Population_Million': [city_pop], 'Founder Count': [founders]
    })
    categorical_features = ['Sector', 'State', 'Locality_Tier', 'Company Type']
    numeric_features     = ['Funding_Cr', 'GDP_Rank', 'City_Population_Million', 'Founder Count']
    for col in categorical_features:
        try:
            input_data[col] = encoders[col].transform(input_data[col].astype(str))
        except:
            input_data[col] = 0
    input_data[numeric_features] = scaler.transform(input_data[numeric_features])
    pred = model.predict(input_data)[0]
    return int(np.clip(pred.round(), 1, 500))

if st.button("🔮 Predict Optimal Team Size", type="primary", use_container_width=True):
    with st.spinner("⚙️ Calculating..."):
        predicted_size = safe_predict(sector, state, locality_tier, company_type,
                                      funding_cr, gdp_rank, city_pop_mn, founders)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Team Size",   f"{predicted_size}")
        col2.metric("💰 Funding",     f"₹{funding_cr:,.1f} Cr")
        col3.metric("🏛️ City Tier",   locality_tier)
        col4.metric("👨‍👩‍👧‍👦 Founders", founders)

        st.balloons()

        st.markdown(f"""
## 🎯 Hiring Recommendation

**Your {sector} startup** in **{state}** should hire **{predicted_size} employees**.

**Growth Factors:**
- ✅ {company_type} status
- ✅ {locality_tier} city
- ✅ GDP Rank #{gdp_rank}
        """)

# ─── EXPANDERS ─────────────────────────────────────────────────────────────────
with st.expander("📊 Model Performance & Features"):
    try:
        impact_df = pd.read_excel('feature_importance_final.xlsx')
        st.dataframe(impact_df.head(10), use_container_width=True)
        st.caption("Top features driving team size predictions")
    except:
        st.info("📈 Feature importance: Funding_Cr, Locality_Tier, GDP_Rank lead")

with st.expander("🔍 Dataset Explorer"):
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[['Company', 'Sector', 'State', 'Team Size']].head(10))
    with col2:
        st.metric("Total Startups",  len(df))
        st.metric("Avg Team Size",   f"{df['Team Size'].mean():.0f}")

st.markdown("---")
st.markdown("**🎓 Harshita Agrawal | PoissonRegressor v2**")