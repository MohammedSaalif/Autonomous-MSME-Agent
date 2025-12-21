import streamlit as st
import pandas as pd
import time
import plotly.express as px
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
    # Dynamic Inventory Metrics
    total_skus = len(agent.inventory.df_inv)
    
    # Calculate overstocked items
    overstocked_items = []
    low_stock_items = []
    
    for pid in agent.inventory.df_inv['product_id']:
        res = agent.inventory.analyze_product(pid)
        if "OVERSTOCK" in res['status']:
            overstocked_items.append(f"{res['product']} ({res['stock']} units)")
        elif "LOW STOCK" in res['status']:
            # Store tuple (display_string, product_id) so we can look up email later
            low_stock_items.append((f"{res['product']} ({res['stock']} units)", pid))
            
    st.metric(label="Total SKUs", value=str(total_skus), delta=f"{len(overstocked_items)} Overstocked", delta_color="inverse")
    
    if overstocked_items:
        with st.expander("🔴 Clearance Needed (Overstock)", expanded=False):
            st.caption("Dead Stock causing loss. Recommended: Setup Promo.")
            for item in overstocked_items:
                st.write(f"• {item}")
                
    if low_stock_items:
        with st.expander("🟡 Reorder Needed (Low Stock)", expanded=False):
            st.caption("Selling fast! Reorder immediately.")
            
            # Create columns for layout
            for item_str, pid in low_stock_items:
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.write(f"• **{item_str}**")
                with c2:
                    # Unique key is needed for buttons in loop
                    if st.button(f"📧 Reorder", key=f"btn_{pid}"):
                        # Find vendor email
                        row = agent.inventory.df_inv[agent.inventory.df_inv['product_id'] == pid].iloc[0]
                        v_email = row['vendor_email']
                        
                        with st.spinner(f"Sending PO to {v_email}..."):
                            time.sleep(1.5) # Simulate network
                        st.toast(f"Order sent to {v_email}!", icon="📤")

with col3:
    st.markdown("### 🕵️ Market Status")
    # Dynamic Market Metrics
    # Calculate avg price difference %
    diffs = []
    losing_items = []
    winning_items = []
    
    for pid in agent.inventory.df_inv['product_id']:
        comp_data = agent.competitor.compare_price(pid)
        my = comp_data['my_price']
        comp = comp_data['competitor_price']
        
        if comp > 0:
            diff_pct = ((my - comp) / comp) * 100
            diffs.append(diff_pct)
            
            # Categorize significant differences
            pname = agent.inventory.df_inv[agent.inventory.df_inv['product_id'] == pid]['product_name'].values[0]
            if diff_pct > 5: # We are > 5% more expensive
                losing_items.append(f"{pname} (+{diff_pct:.1f}%)")
            elif diff_pct < -5: # We are > 5% cheaper
                winning_items.append(f"{pname} ({diff_pct:.1f}%)")
    
    avg_diff = sum(diffs) / len(diffs) if diffs else 0
    
    pressure = "Medium"
    if avg_diff > 10: pressure = "High (Overpriced)"
    elif avg_diff < -10: pressure = "Low (Underpriced)"
    
    delta_val = f"{avg_diff:+.1f}% Price Gap"
    st.metric(label="Competitor Pressure", value=pressure, delta=delta_val, delta_color="inverse")
    
    # Detailed Expanders
    if losing_items:
        with st.expander("🚨 Losing Price War (Overpriced)", expanded=False):
            st.caption("We are significantly more expensive than market.")
            for item in losing_items[:5]: # Show top 5
                st.write(f"• {item}")
                
    if winning_items:
        with st.expander("✅ Winning (Underpriced)", expanded=False):
            st.caption("We are beating the market price.")
            for item in winning_items[:5]: # Show top 5
                st.write(f"• {item}")

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
    
    # Calculate Velocity
    velocity = round(inv_data['7d_sales'] / 7, 2)

    # Product Status Card
    st.markdown(f"""
    <div style="padding:15px; background-color:#262730; border-radius:10px;">
        <b>📦 Stock:</b> {inv_data['stock']} units<br>
        <b>📉 7-Day Sales:</b> {inv_data['7d_sales']} units<br>
        <b>⚡ Velocity:</b> {velocity} units/day<br>
        <b>⚠️ Status:</b> {inv_data['status']}
    </div>
    """, unsafe_allow_html=True)
    
    # Contextual Actions
    if "OVERSTOCK" in inv_data['status']:
        st.warning("📦 Excess Stock!")
        if st.button("🔥 Generate Clearance Sale", key=f"clearance_{product_id}"):
            st.info(f"🔥 CLEARANCE! Get {selected_product_name} for only ${inv_data['stock'] // 2}! #Sale")
            
    elif "LOW STOCK" in inv_data['status']:
        st.error("⚠️ Shortage Risk!")
        if st.button("📧 One Click Order", key=f"reorder_{product_id}"):
            # Look up email
            row = df_inv[df_inv['product_id'] == product_id].iloc[0]
            vendor_email = row.get('vendor_email', "support@vendor.com")
            
            st.success(f"Email Drafted to {vendor_email}")
            st.code(f"""Subject: Stock Reorder for {selected_product_name}\n\nDear Vendor,\n\nOur system indicates low stock for {selected_product_name} ({inv_data['stock']} units). Please process a reorder of 50 units.\n\nBest Regards,\nMSME Agent Bot""", language="text")
    
    # LOAD & FILTER SALES DATA
    df_sales = pd.read_csv("sales_history.csv")

    # We need to reshape the data for the chart
    sales_col = f"{product_id}_sales"

    # Create a clean dataframe for plotting
    chart_data = pd.DataFrame({
        "Date": df_sales["date"],
        "Sales": df_sales[sales_col]
    })

    # Create the Line Chart
    fig = px.line(chart_data, x="Date", y="Sales", title=f"7-Day Sales Trend: {selected_product_name}", markers=True)
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))

    # Display it
    st.plotly_chart(fig, use_container_width=True)

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

            st.markdown("---")
            st.markdown("### ⚡ Automate Execution")

            # Define the action button based on the decision
            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                if st.button("🚀 Launch Campaign (Meta Ads)"):
                    with st.status("Connecting to Ad Manager...", expanded=True) as status:
                        st.write("Checking Budget...")
                        time.sleep(1)
                        if crisis_mode:
                            status.update(label="❌ ACTION BLOCKED", state="error", expanded=False)
                            st.error("Transaction Declined: Finance Agent block due to Low Cash.")
                        else:
                            st.write("Drafting Ad Copy...")
                            time.sleep(1)
                            st.write("Setting Bid Cap...")
                            time.sleep(1)
                            status.update(label="✅ Campaign Active!", state="complete", expanded=False)
                            st.toast("Campaign ID #9823 Live on Facebook!", icon="🚀")

            with col_btn2:
                if st.button("📧 Send Email Blast"):
                    with st.spinner("Sending to 5,000 subscribers..."):
                        time.sleep(2)
                    st.toast("Email Dispatched!", icon="📨")

    with st.expander("🛠️ System Architecture"):
        st.image("architecture.png")

# --- 3. RAW DATA (For Credibility) ---
with st.expander("📊 View Live Data Feeds"):
    st.dataframe(pd.read_csv("inventory.csv"))

# --- 4. AUDIT TRAIL (Compliance) ---
st.divider()
st.subheader("📜 Audit & Compliance Log")
st.markdown("Every AI decision is hashed and logged for traceability.")

logs = agent.audit.get_recent_logs()
if not logs.empty:
    st.dataframe(logs, use_container_width=True)
else:
    st.info("No audit logs available yet. Generate a strategy to create records.")