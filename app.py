import streamlit as st
import pandas as pd
import os

# --- Layout com imagens ---
col1, col2 = st.columns(2)
with col1:
    st.image("imagem/logoCreator.png", use_container_width=True)

st.title("Resumo do Saldo 💰")

# --- Upload do novo CSV ---
st.header("📤 Atualize a base de dados")
uploaded_file = st.file_uploader("Faça upload do novo arquivo CSV", type="csv", help="Apenas arquivos .csv com até 200MB")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=",", encoding="utf-8")
    df.to_csv("dados/arquivo_mais_recente.csv", index=False)
    st.success("Arquivo carregado com sucesso!")

# --- Carregar e exibir os dados ---
if os.path.exists("dados/arquivo_mais_recente.csv"):
    df = pd.read_csv("dados/arquivo_mais_recente.csv")

    # Traduzir nomes das colunas
    df.columns = ['categoria', 'descrição', 'valor líquido', 'moeda']

    # Dicionário para traduzir descrições (opcional)
    traducao_descricoes = {
        'Starting balance': 'Saldo inicial',
        'Account activity before fees': 'Atividade da conta (antes das taxas)',
        'Less fees': 'Taxas descontadas',
        'Activity': 'Atividade',
        'Payouts to bank': 'Transferências para o banco',
        'Payout fees': 'Taxas de saque',
        'Total payouts': 'Total de transferências',
        'Ending balance': 'Saldo final'
    }

    # Aplicar tradução nas descrições (linha por linha)
    for key, val in traducao_descricoes.items():
        df['descrição'] = df['descrição'].str.replace(key, val, regex=False)

    st.header("📊 Dados atuais")
    st.dataframe(df, use_container_width=True)

    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), file_name='base_atual.csv', mime='text/csv')
else:
    st.warning("Nenhum arquivo foi carregado ainda.")
