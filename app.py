import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import os

# 1. PAGE CONFIGURATION 
st.set_page_config(
    page_title="Romina PLC | EUDR Compliance Console",
    page_icon="☕",
    layout="wide",
)

# Custom Dark Mode "Control Room" CSS
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; }
    div[data-testid="stMetric"] {
        background-color: #1A1F26;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 15px;
    }
    .main-title { color: #00FFCC; font-weight: 800; font-size: 2.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOAD WITH TYPE FORCING 
@st.cache_data
def load_data():
    file_path = 'romina_compliance_final.csv'
    if not os.path.exists(file_path): return None

    data = pd.read_csv(file_path)
    data.columns = [c.lower().strip() for c in data.columns]

    # Ensure numeric types for map/plots
    for col in ['latitude', 'longitude', 'eudr_readiness_score', 'plot_size_ha', 'altitude_masl']:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

    return data.dropna(subset=['latitude', 'longitude'])

df = load_data()
if df is None: st.stop()

# 3. ADVANCED SIDEBAR FILTERS 
st.sidebar.header("EUDR Compliance Filters")

# A. Geography
with st.sidebar.expander("🌍 Geographic Scope", expanded=True):
    regions = sorted(df['region'].unique())
    reg_sel = st.multiselect("Region", regions, default=regions)
    woredas = sorted(df[df['region'].isin(reg_sel)]['woreda'].unique())
    wor_sel = st.multiselect("Woreda", woredas)

# B. Risk Parameters
with st.sidebar.expander("Risk Thresholds", expanded=True):
    min_score = st.slider("Min. Readiness Score %", 0, 100, 0)
    risk_only = st.checkbox("Show Only 'High Risk' Plots", value=False)
    # Filter for plots larger than 4 hectares (EUDR higher scrutiny)
    large_plots = st.toggle("Focus on Large Plots (>4ha)")

# C. Apply Logic
mask = (df['region'].isin(reg_sel)) & (df['eudr_readiness_score'] >= min_score)
if wor_sel: mask = mask & (df['woreda'].isin(wor_sel))
if risk_only: mask = mask & (df['is_non_compliant'] == True)
if large_plots: mask = mask & (df['plot_size_ha'] > 4.0)

filtered_df = df[mask].copy()

# 4. EXECUTIVE SUMMARY (KPIs) 
st.markdown('<p class="main-title">☕ Romina PLC | EUDR Compliance Console</p>', unsafe_allow_html=True)
st.markdown(f"**Data Status:** LIVE | **Filtered Plots:** {len(filtered_df):,} | **Current Date:** 2026-04-02")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Supply Base", f"{len(filtered_df):,}")
k2.metric("Compliance Avg", f"{filtered_df['eudr_readiness_score'].mean():.1f}%")
k3.metric("Mapped Area", f"{filtered_df['plot_size_ha'].sum():,.1f} ha")

# Dynamic Risk Delta
non_compliant_count = len(filtered_df[filtered_df['is_non_compliant'] == True])
k4.metric("Non-Compliant", non_compliant_count, delta=f"{non_compliant_count} Risks", delta_color="inverse")

st.divider()

# 5. GEOSPATIAL INTELLIGENCE
st.subheader("Risk Distribution Map")

if not filtered_df.empty:
    try:
        # 1. Prepare clean data for the map engine
        map_df = filtered_df.dropna(subset=['latitude', 'longitude']).copy()

        # 2. Add a friendly Status string for the tooltip
        map_df['status_text'] = map_df['is_non_compliant'].map({
            True: "🔴 NON-COMPLIANT (Risk Detected)", 
            False: "🟢 COMPLIANT (Safe)"
        })

        # 3. Define the Color Logic (Red for Risk, Cyan for Success)
        map_df['color'] = map_df['is_non_compliant'].apply(
            lambda x: [255, 40, 40, 200] if x else [0, 255, 180, 160]
        )

        # 4. Convert to a list of dictionaries to prevent 'vars()' errors
        chart_data = map_df.to_dict(orient='records')

        # 5. Render the Deck with Advanced Tooltips
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10',
            initial_view_state=pdk.ViewState(
                latitude=map_df['latitude'].mean(), 
                longitude=map_df['longitude'].mean(), 
                zoom=7.5, 
                pitch=45
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer", 
                    data=chart_data,
                    get_position='[longitude, latitude]', 
                    get_fill_color='color', 
                    get_radius=700, 
                    pickable=True
                )
            ],
            # UPDATED TOOLTIP LOGIC
            tooltip={
                "html": """
                    <div style="font-family: sans-serif; padding: 10px; background-color: #1A1F26; border: 1px solid #30363D; border-radius: 5px;">
                        <b style="color: #00FFCC;">Farmer ID:</b> {farmer_id}<br/>
                        <b>Woreda:</b> {woreda}<br/>
                        <b>Compliance Score:</b> {eudr_readiness_score}%<br/>
                        <hr style="margin: 5px 0; border-color: #30363D;">
                        <span style="font-weight: bold;">{status_text}</span>
                    </div>
                """,
                "style": {"color": "white"}
            }
        ))
    except Exception as e:
        st.error(f"Map Rendering Error: {e}")
else:
    st.warning("No data found for the current selection.")

# 6. EUDR AUDIT LOG 
st.subheader("📋 Traceability Audit Log")
# Add a status column with emojis for the table
filtered_df['status'] = filtered_df['is_non_compliant'].map({True: "FAILED", False: " PASSED"})

st.dataframe(
    filtered_df[['farmer_id', 'woreda', 'altitude_masl', 'plot_size_ha', 'eudr_readiness_score', 'status']],
    use_container_width=True,
    hide_index=True
)

# Export Functionality
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Export Audit Report (CSV)", data=csv, file_name="romina_eudr_audit.csv", mime="text/csv")
