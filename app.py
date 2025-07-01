import streamlit as st
import stripe
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Saldo Creator")

# Autentica com chave segura
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# --- Layout com imagens ---
col1, col2 = st.columns(2)
with col1:
    st.image("imagem/logoCreator.png", use_container_width=True)

st.title("💳 Resumo Automático do Stripe")

# --- Obter saldo atual ---
st.subheader("💰 Saldo disponível")
balance = stripe.Balance.retrieve()
for item in balance["available"]:
    valor = item["amount"] / 100
    st.markdown(f"- **{valor:.2f} {item['currency'].upper()}**")

# --- Obter últimas transações ---
st.subheader("📊 Últimas transações")
transactions = stripe.BalanceTransaction.list(limit=100)

# Transformar em DataFrame
dados = []
for t in transactions['data']:
    dados.append({
        'ID': t['id'],
        'Tipo': t['type'],
        'Descrição': t.get('description', ''),
        'Valor líquido': t['net'] / 100,
        'Taxas': t['fee'] / 100,
        'Moeda': t['currency'].upper(),
        'Data': pd.to_datetime(t['created'], unit='s'),
    })

df = pd.DataFrame(dados)
st.dataframe(df, use_container_width=True)

# Botão de download
st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), file_name='transacoes_stripe.csv', mime='text/csv')
