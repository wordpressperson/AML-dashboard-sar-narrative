```markdown
# 🛡️ FinGuard AML Dashboard

**A comprehensive multi-page Streamlit dashboard for the AI-Based Anti-Money Laundering (AML) System**

This is the **full-featured frontend** of the FinGuard AML platform. It provides real-time visibility into customers, transactions, alerts, screening results, and AI-generated SAR narratives.

- **Backend Repository**: [mominalix/AI-Based-Anti-Money-Laundering-AML-System](https://github.com/mominalix/AI-Based-Anti-Money-Laundering-AML-System)

## ✨ Live Demo

[Open FinGuard AML →](https://your-finguard-app-name.streamlit.app)  
*(Replace with your actual Streamlit Cloud URL after deployment)*

## Features

- **6-page navigation**: Dashboard, Customers, Transactions, Alerts, Screening, Reports
- Real-time metrics and transaction volume charts
- Interactive customer directory and transaction table
- Styled alert queue with priority coloring
- AI-powered SAR narrative generation using OpenAI (gpt-4o, gpt-4-turbo, etc.)
- PEP & Sanctions screening view
- Sample reports table
- Secure JWT authentication and OpenAI key via Streamlit Secrets
- Auto-refresh support with fallback to local fixtures

## Tech Stack

- **Framework**: Streamlit
- **Data**: Pandas
- **Visualizations**: Plotly Express
- **API**: Requests (JWT-protected)
- **AI**: OpenAI (for SAR generation)
- **Deployment**: Streamlit Cloud (free tier)
- **Backend**: Same Docker Compose microservices used by the AML Alert Dashboard

## Quick Start (Local Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/finguard-aml-dashboard.git
   cd finguard-aml-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create local secrets for development:
   ```bash
   mkdir -p .streamlit
   nano .streamlit/secrets.toml
   ```
   Paste:
   ```toml
   [api]
   base_url = "http://localhost:8000"
   bearer_token = "your-jwt-token-here"

   [openai]
   api_key = "sk-proj-..."
   ```

4. Run the app:
   ```bash
   streamlit run dashboard.py
   ```

## Deployment to Streamlit Cloud (Free Tier)

1. Push the code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Connect your repo and select `dashboard.py`.
4. After the first deploy, go to **Settings → Secrets** and add:

   ```toml
   [api]
   base_url = "http://YOUR-AZURE-PUBLIC-IP:8000"
   bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

   [openai]
   api_key = "sk-proj-..."
   ```

5. Redeploy. The dashboard will load with a clean sidebar (no exposed keys).

## Project Structure

```
├── dashboard.py                 # Main multi-page Streamlit app
├── requirements.txt             # Python dependencies (includes openai)
├── fixtures/                    # Optional local fallback JSON files
│   ├── customers.json
│   ├── accounts.json
│   └── transactions.json
├── .streamlit/
│   └── secrets.toml             # Local secrets only (gitignored)
└── README.md
```

## Backend Requirement

This dashboard connects to the **same backend** as the AML Alert Dashboard.  
Make sure the backend is running on Azure (or any server) with the test pipeline executed:

```bash
python complete_pipeline_demo.py
```

## Troubleshooting

- **"Missing secrets" error** → Check Streamlit Cloud → Settings → Secrets.
- **No alerts / empty data** → Run the backend pipeline or ensure fixtures exist.
- **OpenAI errors** → Verify the `openai.api_key` in secrets.
- **Connection refused** → Confirm Azure NSG allows port 8000 (or 80 if using Caddy).

## Credits

- Backend & microservices by [mominalix](https://github.com/mominalix)
- FinGuard AML Dashboard built as an enhanced frontend for demonstration and production use

---

**Made with Streamlit** | Powered by Azure + Streamlit Cloud
```
