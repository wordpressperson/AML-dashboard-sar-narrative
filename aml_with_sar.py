import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# ==================== CUSTOM CSS - Professional dark theme like your example images ====================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: #f1f5f9;}
    .stMetric {background: linear-gradient(135deg, #1e2937, #334155); border-radius: 16px; padding: 15px 20px; box-shadow: 0 10px 30px rgba(245, 166, 35, 0.25);}
    .stMetric label {color: #f5a623 !important; font-size: 1.1rem;}
    .stMetric div[data-testid="stMetricValue"] {font-size: 2.4rem; font-weight: 700;}
    h1, h2, h3 {color: #f5a623 !important;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .css-1d391kg {background-color: #1e2937; border-radius: 12px; padding: 1rem;}
    .alert-card {background: #1e2937; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #f5a623;}
    .dataframe {background-color: #1e2937 !important;}
</style>
""", unsafe_allow_html=True)

# ==================== SECRETS (exactly as before) ====================
try:
    BASE_URL = st.secrets["api"]["base_url"]
    BEARER_TOKEN = st.secrets["api"]["bearer_token"]
    OPENAI_API_KEY = st.secrets["openai"]["api_key"]
except Exception:
    st.error("Missing secrets. Please add [api] and [openai] sections in Streamlit Secrets.")
    st.stop()

headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "accept": "application/json"}

st.set_page_config(page_title="FinGuard AML", layout="wide", page_icon="🛡️")

# ==================== SIDEBAR ====================
st.sidebar.image("https://via.placeholder.com/220x60/1e2937/f5a623?text=FinGuard+AML", width=220)
page = st.sidebar.radio("Navigation", ["Dashboard", "Customers", "Transactions", "Alerts", "Screening", "Reports"])

# ==================== DATA LOADING ====================
@st.cache_data(ttl=60)
def load_data():
    try:
        alerts_resp = requests.get(f"{BASE_URL}/v1/alerts", headers=headers, params={"limit": 100}, timeout=10)
        alerts_resp.raise_for_status()
        alerts_data = alerts_resp.json()
        alerts_df = pd.DataFrame(alerts_data.get("alerts", alerts_data) if isinstance(alerts_data, dict) else alerts_data)
    except:
        alerts_df = pd.DataFrame()

    try:
        customers_df = pd.read_json("fixtures/customers.json")
        accounts_df = pd.read_json("fixtures/accounts.json")
        transactions_df = pd.read_json("fixtures/transactions.json")
    except:
        st.warning("Using demo data (fixtures not found)")
        customers_df = pd.DataFrame([{"customer_id": "C001", "full_name": "Client Johnson", "risk_category": "high"}])
        accounts_df = pd.DataFrame()
        transactions_df = pd.DataFrame([{"txn_id": "T001", "timestamp": "2026-04-23 08:15", "amount": 550000}])

    return customers_df, accounts_df, transactions_df, alerts_df

customers_df, accounts_df, transactions_df, alerts_df = load_data()

# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.title("🛡️ AML & Fraud Monitoring Dashboard")
    st.caption("Real-time Anti-Money Laundering & Fraud Detection | Powered by AzurizedAMLSolution")

    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", f"{len(transactions_df):,}" if not transactions_df.empty else "36,421", "↑ 12%")
    with col2:
        st.metric("Unusual Transactions", "250", "🔥", delta_color="inverse")
    with col3:
        st.metric("AML Entities", f"{len(customers_df):,}" if not customers_df.empty else "10,108")
    with col4:
        st.metric("Amount Transacted", "GH₵36.19B", "↑ 8%")

    # Main layout mirroring your images
    left_col, center_col, right_col = st.columns([1.2, 2.5, 1.2])

    with left_col:
        st.subheader("Recent Activity")
        st.metric("Total Today", "2,847", "↑ 18%")
        st.metric("Unusual Today", "41", "🔥")

    with center_col:
        st.subheader("Transactions by Time of Day")
        # Demo data that matches your first image
        hourly = pd.DataFrame({
            'hour': list(range(8,16)),
            'Valid': [17, 12, 14, 15, 5, 4, 20, 16],
            'Fraud': [3, 5, 6, 9, 3, 2, 8, 10],
            'Unassigned': [8, 4, 5, 10, 2, 1, 14, 11]
        })
        fig_bar = px.bar(
            hourly, x='hour', y=['Valid', 'Fraud', 'Unassigned'],
            color_discrete_sequence=['#f5a623', '#ef553b', '#a3bffa'],
            barmode='stack', title="Valid vs Fraud vs Unassigned"
        )
        fig_bar.update_layout(template="plotly_dark", plot_bgcolor="#1e2937", paper_bgcolor="#1e2937", height=380)
        st.plotly_chart(fig_bar, use_container_width=True)

    with right_col:
        st.subheader("Today – Verification")
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Verified as valid", "Confirmed as fraudulent", "Unassigned"],
            values=[130, 80, 40],
            hole=0.65,
            marker_colors=["#f5a623", "#ef553b", "#64748b"]
        )])
        fig_pie.update_layout(template="plotly_dark", margin=dict(t=0,b=0,l=0,r=0), height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Lower sections
    tab1, tab2, tab3 = st.tabs(["Unusual Transaction Alerts", "Ongoing Investigations", "Risk Monitoring"])

    with tab1:
        st.subheader("Unusual Transaction Alerts")
        alert_examples = [
            {"icon": "⚠️", "text": "Client Johnson did more than 10 transactions at same time a day totaling GH₵550,000"},
            {"icon": "⚠️", "text": "Client Martha did more than 25 transactions in same month totaling GH₵2,550,000"}
        ]
        for alert in alert_examples:
            st.markdown(f"""
            <div class="alert-card">
                <strong>{alert['icon']} {alert['text']}</strong>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Ongoing Investigation")
        investigation_data = pd.DataFrame({
            "Bank": ["Federal bank USA", "Add text here", "Add text here", "Add text here"],
            "Client": ["Johnson", "Martha", "Add text here", "Add text here"],
            "Assigned to": ["Agent Smith", "Agent Smith", "Agent Smith", "Agent Smith"],
            "Progress": ["Investigation opened", "In peer review", "Complete", "Confirmed as unusual"]
        })
        st.dataframe(investigation_data, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Synthetic Identities – Risk Alerts")
        risk_data = pd.DataFrame({
            "Risk Category": ["Low risk", "Medium risk", "High risk"],
            "Transactions": [98, 8, 4]
        })
        fig_risk = px.bar(risk_data, x="Transactions", y="Risk Category", orientation='h',
                          color="Risk Category", color_discrete_sequence=["#ec4899", "#f43f5e", "#be123c"])
        fig_risk.update_layout(template="plotly_dark", height=280)
        st.plotly_chart(fig_risk, use_container_width=True)

        st.subheader("Transaction Summary (by Country)")
        dates = pd.date_range(start="2026-04-15", periods=7, freq='D')
        area_data = pd.DataFrame({
            "Date": dates,
            "US": [320, 180, 250, 380, 450, 390, 480],
            "Sweden": [150, 90, 220, 180, 300, 420, 490],
            "France": [280, 120, 90, 210, 340, 280, 310],
            "India": [90, 70, 110, 250, 400, 370, 460]
        })
        fig_area = px.area(area_data, x="Date", y=["US","Sweden","France","India"],
                           color_discrete_sequence=px.colors.sequential.Plasma_r)
        fig_area.update_layout(template="plotly_dark", height=340)
        st.plotly_chart(fig_area, use_container_width=True)

# ==================== OTHER PAGES (kept functional) ====================
elif page == "Customers":
    st.subheader("Customer Directory")
    st.dataframe(customers_df, use_container_width=True, height=700)

elif page == "Transactions":
    st.subheader("All Transactions")
    st.dataframe(transactions_df, use_container_width=True, height=700)

elif page == "Alerts":
    st.subheader("Alert Queue")
    st.caption("Manage and investigate all AML/CFT alerts.")
    if alerts_df.empty:
        st.info("No alerts from API – showing demo alerts")
        display_alerts = transactions_df.head(8).copy() if not transactions_df.empty else pd.DataFrame()
    else:
        display_alerts = alerts_df.copy()

    if not display_alerts.empty:
        st.dataframe(display_alerts, use_container_width=True, height=500)

    st.subheader("SAR Narratives (AI Generated)")
    model_choice = st.selectbox("OpenAI Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
    if st.button("Generate New SAR Narrative", type="primary"):
        with st.spinner("Generating professional SAR narrative with OpenAI..."):
            try:
                import openai
                openai.api_key = OPENAI_API_KEY
                prompt = f"""You are a senior AML compliance officer. Generate a formal Suspicious Activity Report (SAR) narrative.
Customer: {display_alerts.iloc[0].get('full_name', 'Unknown') if not display_alerts.empty else 'Unknown'}
Risk Score: 0.92
Alert Type: Multiple rapid high-value transfers"""
                response = openai.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                st.success("SAR Generated!")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"OpenAI error: {e}")

elif page == "Screening":
    st.subheader("Screening Results")
    st.dataframe(customers_df, use_container_width=True)

elif page == "Reports":
    st.subheader("Generated Reports")
    reports = pd.DataFrame([
        {"Report Name": "SAR-2026-04-001", "Type": "SAR", "Generated Date": "2026-04-23", "Status": "Draft"},
        {"Report Name": "CTR-Q2-2026", "Type": "CTR", "Generated Date": "2026-04-20", "Status": "Submitted"},
    ])
    st.dataframe(reports, use_container_width=True)

# Footer
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Connected to {BASE_URL} | Demo Ready 🚀")
if st.button("🔄 Refresh All Data"):
    st.cache_data.clear()
    st.rerun()
