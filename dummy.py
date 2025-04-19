import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Simulated invoice database
@st.cache_data
def load_data():
    return pd.read_csv("invoices_mock.csv")  # columns: client, date, amount, status, region

invoices = load_data()

# --- UI ---
st.set_page_config(page_title="Fruteez AI Assistant", layout="wide")
st.title("🧠 Fruteez AI Assistant")
st.markdown("Talk to your invoicing system like never before. Type a command below:")

# Chat input
query = st.text_input("💬 Type your request (in French or English)", placeholder="e.g. Show me unpaid invoices for Monoprix")

# --- Simple Query Parser ---
def parse_query(q):
    q = q.lower()
    if "unpaid" in q or "non payé" in q:
        if "monoprix" in q:
            return invoices[(invoices["client"] == "Monoprix") & (invoices["status"] == "unpaid")]
        elif "carrefour" in q:
            return invoices[(invoices["client"] == "Carrefour") & (invoices["status"] == "unpaid")]
        else:
            return invoices[invoices["status"] == "unpaid"]
    elif "generate invoice" in q or "générer facture" in q:
        # simulate invoice preview
        return "generate_invoice"
    elif "report" in q or "rapport" in q:
        return "generate_report"
    return None

# --- Response Handler ---
result = parse_query(query)

if isinstance(result, pd.DataFrame) and not result.empty:
    st.success(f"Found {len(result)} invoice(s).")
    st.dataframe(result)
elif result == "generate_invoice":
    st.info("📄 Simulated invoice for Carrefour - April 3")
    st.code("""
    Invoice #INV-20250403
    Client: Carrefour
    Date: 03-April-2025
    Amount: €1,200.00
    Status: Unpaid
    """)
elif result == "generate_report":
    st.subheader("📊 Unpaid Invoices by Region")
    chart = invoices[invoices["status"] == "unpaid"].groupby("region")["amount"].sum().reset_index()
    fig = px.bar(chart, x="region", y="amount", title="Unpaid Invoices by Region (€)")
    st.plotly_chart(fig)
elif query:
    st.warning("🤔 Sorry, I couldn't understand that. Try again with a clearer request.")

# --- Footer ---
st.markdown("---")
st.caption("Fruteez Assistant Prototype – Powered by Streamlit")
