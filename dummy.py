import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAckighcNr9MJPTNh2YSyCD5aalWskYEYE")
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.set_page_config(page_title="Invoice Chatbot", layout="centered")
st.title("📋 Invoice Management Chatbot")
st.write("Posez vos questions sur les factures ou la gestion des paiements 👇")

# Suggestive Questions
suggestions = [
    "Montre-moi les factures impayées.",
    "Quelle est la dernière facture de Monoprix ?",
    "Génère une facture pour Carrefour aujourd'hui.",
    "Donne-moi un rapport des paiements par région.",
    "Est-ce que Géant a réglé ses factures ?"
]

st.markdown("### 💡 Suggestions")
for s in suggestions:
    if st.button(s):
        st.session_state.user_input = s

# Chat Input
user_input = st.text_input("💬 Votre question", value=st.session_state.get("user_input", ""), key="chat_input")

# Gemini Prompt Logic
if user_input:
    with st.spinner("Analyse en cours..."):
        prompt = f"""
Tu es un assistant intelligent pour un système de gestion de factures. 
Toutes les questions de l'utilisateur concernent la facturation, les paiements, les clients, ou les rapports financiers.

Réponds de manière claire, professionnelle, et orientée vers la gestion des factures.

Question : {user_input}
"""
        response = model.generate_content(prompt)
        st.markdown("### 🤖 Réponse")
        st.write(response.text)
