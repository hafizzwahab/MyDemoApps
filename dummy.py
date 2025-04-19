import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Fruteez AI Assistant", layout="wide")
genai.configure(api_key="AIzaSyAckighcNr9MJPTNh2YSyCD5aalWskYEYE")  # Your Gemini API key

# --- Load dummy data ---
@st.cache_data
def load_data():
    return pd.read_csv("invoices_mock.csv")  # Make sure it's in the same directory

invoices = load_data()

# --- Gemini Model Setup ---
model = genai.GenerativeModel("gemini-pro")

def query_gemini(user_input):
    prompt = f"""You are Fruteez AI Assistant, helping a billing team manage invoices in an ERP called Dolibarr. 
You can answer questions, generate invoices, and provide business reports using the following data:
{invoices.head(10).to_string(index=False)}

Respond clearly in French (or Tunisian tone if internal).

Now answer the following user request:
{user_input}
"""
    response = model.generate_content(prompt)
    return response.text

# --- UI ---
st.title("🧠 Fruteez AI Assistant – Dolibarr Smart ERP Chat")
st.markdown("Parlez à votre ERP comme à un collègue. Posez une question ci-dessous 👇")

user_input = st.text_input("💬 Votre demande", placeholder="e.g. Montre-moi les factures impayées pour Monoprix")

if user_input:
    with st.spinner("Analyse en cours avec Gemini..."):
        response = query_gemini(user_input)

    st.markdown("### 🤖 Réponse de Fruteez AI")
    st.write(response)

    # Optional visual response for reporting
    if "rapport" in user_input.lower() or "report" in user_input.lower():
        st.markdown("### 📊 Vue graphique : Factures impayées par région")
        chart = invoices[invoices["status"] == "unpaid"].groupby("region")["amount"].sum().reset_index()
        fig = px.bar(chart, x="region", y="amount", title="Factures impayées (€) par région")
        st.plotly_chart(fig)

# --- Footer ---
st.markdown("---")
st.caption("Fruteez – Assistant ERP intelligent, propulsé par Gemini & Streamlit")
