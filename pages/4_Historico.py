"""
Página Histórico de Abastecimentos
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_abastecimentos
from utils.helpers import formatar_reais, formatar_litros
from utils.navigation import header_menu

st.set_page_config(page_title="Histórico", layout="wide", initial_sidebar_state="collapsed")
header_menu()

st.title("Histórico de Abastecimentos")
st.caption("Consulte todos os registros de abastecimento com filtros avançados")

# ============================================================
# Filtros
# ============================================================
st.markdown("### Filtros")

col1, col2, col3, col4 = st.columns(4)

with col1:
    data_inicio = st.date_input(
        "Data Início",
        value=datetime.now() - timedelta(days=30),
        format="DD/MM/YYYY"
    )

with col2:
    data_fim = st.date_input(
        "Data Fim",
        value=datetime.now(),
        format="DD/MM/YYYY"
    )

with col3:
    placa_filtro = st.text_input(
        "Placa",
        placeholder="Filtrar por placa...",
        max_chars=7
    )

with col4:
    tipo_filtro = st.selectbox(
        "Tipo de Combustível",
        options=["Todos", "Gasolina Comum", "Gasolina Aditivada", "Diesel S10"]
    )

# Buscar dados
df = get_abastecimentos(
    data_inicio=data_inicio.strftime("%Y-%m-%d"),
    data_fim=data_fim.strftime("%Y-%m-%d"),
    placa=placa_filtro if placa_filtro else None,
    tipo=tipo_filtro if tipo_filtro != "Todos" else None
)

# ============================================================
# Resumo do Período
# ============================================================
st.markdown("---")

if not df.empty:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de Registros", len(df))

    with col2:
        st.metric("Total de Litros", formatar_litros(df["litros"].sum()))

    with col3:
        st.metric("Faturamento Total", formatar_reais(df["valor_total"].sum()))

    with col4:
        st.metric("Veículos Únicos", df["placa_veiculo"].nunique())

    st.markdown("---")

    # ============================================================
    # Tabela de Dados
    # ============================================================
    st.markdown("### Registros")

    # Formatar para exibição
    df_display = df[[
        "data_hora", "placa_veiculo", "tipo_combustivel",
        "litros", "valor_litro", "valor_total"
    ]].copy()

    df_display.columns = [
        "Data/Hora", "Placa", "Combustível",
        "Litros", "R$/Litro", "Valor Total"
    ]

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={
            "Litros": st.column_config.NumberColumn(format="%.1f L"),
            "R$/Litro": st.column_config.NumberColumn(format="R$ %.2f"),
            "Valor Total": st.column_config.NumberColumn(format="R$ %.2f"),
            "Data/Hora": st.column_config.TextColumn(width="medium"),
            "Placa": st.column_config.TextColumn(width="small"),
            "Combustível": st.column_config.TextColumn(width="medium"),
        }
    )

    # ============================================================
    # Exportar
    # ============================================================
    st.markdown("---")

    col_exp1, col_exp2, _ = st.columns([1, 1, 2])

    with col_exp1:
        csv = df_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Exportar CSV",
            csv,
            "abastecimentos.csv",
            "text/csv",
            use_container_width=True
        )

    with col_exp2:
        st.caption(f"Período: {data_inicio.strftime('%d/%m/%Y')} — {data_fim.strftime('%d/%m/%Y')}")

else:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
    st.markdown("""
    **Sugestões:**
    - Amplie o período de datas
    - Remova o filtro de placa
    - Selecione "Todos" no tipo de combustível
    """)
