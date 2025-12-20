import streamlit as st
import pandas as pd
import time
from marketing_agent import MarketingAgent

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Marketing Agent", page_icon="🤖", layout="wide")

# --- CSS FOR SCI-FI LOOK ---
st.markdown("""
<style>
    .metric-card {background-color: #0e1117; border: 1px solid #303030; padding: 20px; border-radius: 10px;}
    .stButton>button {width: 100%; border-radius: 5px;}
    .crisis-mode {border: 2px solid red; padding: 10px; border-radius: 5px; background-color: #330000;}
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE AGENT ---
@st.cache_resource
def load_agent():
    return MarketingAgent()

agent = load_agent()

# --- SIDEBAR: CONTROLS ---
st.sidebar.title("🎛️ Control Panel")

# 🚨 THE PANIC BUTTON
st.sidebar.markdown("### 🧪 Simulation")
crisis_mode = st.sidebar.toggle("🚨 SIMULATE MARKET CRASH", value=False)

if crisis_mode:
    st.sidebar.error("⚠️ SIMULATION ACTIVE: Cash Reserves Depleted.")

st.sidebar.markdown("---")
st.sidebar.info("System Status: ONLINE")

# --- MAIN DASHBOARD ---
st.title("🚀 Autonomous Marketing Agent")
if crisis_mode:
    st.markdown('<div class="crisis-mode"><h3>🚨 EMERGENCY PROTOCOL ACTIVE</h3><p>Cash Critical. Survival Mode Engaged.</p></div>', unsafe_allow_html=True)
else:
    st.markdown("### *Intelligence-Driven Decisions, Not Just Ads.*")

# --- 1. LIVE METRICS ROW ---
fin_status = agent.finance.get_status()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💰 Cash Runway")
    # If crisis mode, fake the numbers for visuals
    display_cash = "$500" if crisis_mode else f"${fin_status['cash']}"
    display_runway = "0.2 Months" if crisis_mode else f"{fin_status['runway_months']} Months"
    color = "inverse" if crisis_mode else "normal"
    st.metric(label="Available Cash", value=display_cash, delta=display_runway, delta_color=color)

with col2:
    st.markdown("### 📦 Inventory Health")
    st.metric(label="Total SKUs", value="4", delta="1 Overstocked", delta_color="inverse")

with col3:
    st.markdown("### 🕵️ Market Status")
    st.metric(label="Competitor Pressure", value="High", delta="-12% Price Gap", delta_color="inverse")

st.divider()

# --- 2. ACTION CENTER ---
col_left, col_right = st.columns([1, 2])

# Load Products
df_inv = pd.read_csv("inventory.csv")
product_list = df_inv['product_name'].tolist()

with col_left:
    st.subheader("1️⃣ Select Target")
    selected_product_name = st.selectbox("Choose Product to Analyze", product_list)
    
    # Get ID & Data
    product_id = df_inv[df_inv['product_name'] == selected_product_name]['product_id'].values[0]
    inv_data = agent.inventory.analyze_product(product_id)
    
    # Product Status Card
    st.markdown(f"""
    <div style="padding:15px; background-color:#262730; border-radius:10px;">
        <b>📦 Stock:</b> {inv_data['stock']} units<br>
        <b>📉 7-Day Sales:</b> {inv_data['7d_sales']} units<br>
        <b>⚠️ Status:</b> {inv_data['status']}
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.subheader("2️⃣ Agent Decision")
    if st.button("🧠 GENERATE STRATEGY", type="primary"):
        with st.spinner("🤖 Consulting Finance, Inventory & Competitor Agents..."):
            # Artificial delay for effect
            time.sleep(1.5) 
            
            # Call Agent
            strategy = agent.generate_strategy(product_id, crisis_mode=crisis_mode)
            
            # Show Result
            st.success("Analysis Complete")
            st.markdown(f"### 🎯 Strategy: {selected_product_name}")
            st.markdown(strategy)

# --- 3. RAW DATA (For Credibility) ---
with st.expander("📊 View Live Data Feeds"):
    st.dataframe(pd.read_csv("inventory.csv"))