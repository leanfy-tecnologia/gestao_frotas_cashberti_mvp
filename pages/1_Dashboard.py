"""
Página Dashboard - Métricas e Gráficos Principais
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_resumo_hoje, get_resumo_mes, get_consumo_diario, get_consumo_mensal, get_tanques
from utils.helpers import formatar_reais, formatar_litros, delta_formatado, CORES_COMBUSTIVEL
from utils.charts import (
    grafico_consumo_diario, grafico_consumo_mensal,
    grafico_faturamento_diario, grafico_veiculos_por_dia,
    gauge_tanque, grafico_distribuicao_combustivel
)
from utils.navigation import header_menu

st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")
header_menu()

st.title("Dashboard")
st.caption("Visão geral das métricas de consumo e faturamento")


# ============================================================
# KPIs - Mês
# ============================================================
st.markdown("---")
st.markdown("### Métricas do Mês")

resumo_mes = get_resumo_mes()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Litros no Mês",
        formatar_litros(resumo_mes["litros_mes"]),
        delta=delta_formatado(resumo_mes["litros_mes"], resumo_mes["litros_mes_ant"]),
        help="Comparação com mês anterior"
    )

with col2:
    st.metric(
        "Faturamento Mensal",
        formatar_reais(resumo_mes["faturamento_mes"]),
        delta=delta_formatado(resumo_mes["faturamento_mes"], resumo_mes["faturamento_mes_ant"]),
        help="Comparação com mês anterior"
    )

with col3:
    st.metric(
        "Abastecimentos no Mês",
        resumo_mes["abastecimentos_mes"],
        delta=delta_formatado(resumo_mes["abastecimentos_mes"], resumo_mes["abastecimentos_mes_ant"]),
        help="Comparação com mês anterior"
    )

with col4:
    st.metric(
        "Veículos no Mês",
        resumo_mes["veiculos_mes"],
        delta=delta_formatado(resumo_mes["veiculos_mes"], resumo_mes["veiculos_mes_ant"]),
        help="Veículos únicos. Comparação com mês anterior"
    )

# ============================================================
# Gráficos
# ============================================================
st.markdown("---")
st.markdown("### Análise de Consumo")

tab_diario, tab_mensal = st.tabs(["Diário (30 dias)", "Mensal"])

consumo_diario = get_consumo_diario(30)
consumo_mensal_data = get_consumo_mensal(6)

with tab_diario:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grafico_consumo_diario(consumo_diario), use_container_width=True)
    with col2:
        st.plotly_chart(grafico_faturamento_diario(consumo_diario), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(grafico_veiculos_por_dia(consumo_diario), use_container_width=True)
    with col4:
        st.plotly_chart(grafico_distribuicao_combustivel(consumo_diario), use_container_width=True)

with tab_mensal:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grafico_consumo_mensal(consumo_mensal_data), use_container_width=True)
    with col2:
        st.plotly_chart(grafico_distribuicao_combustivel(consumo_mensal_data), use_container_width=True)

# ============================================================
# Nível dos Tanques
# ============================================================
st.markdown("---")
st.markdown("### Nível dos Tanques")

tanques = get_tanques()

if not tanques.empty:
    cols = st.columns(len(tanques))
    for i, (_, tanque) in enumerate(tanques.iterrows()):
        cor = CORES_COMBUSTIVEL.get(tanque["tipo_combustivel"], "#FF6B35")
        with cols[i]:
            fig = gauge_tanque(
                tanque["nome"],
                tanque["nivel_atual_litros"],
                tanque["capacidade_litros"],
                cor
            )
            st.plotly_chart(fig, use_container_width=True)

            percentual = (tanque["nivel_atual_litros"] / tanque["capacidade_litros"] * 100)
            if percentual < 20:
                st.warning(f"Atenção: Nível baixo! {percentual:.0f}%")
            elif percentual < 40:
                st.info(f"Informação: Nível moderado: {percentual:.0f}%")
else:
    st.info("Nenhum tanque cadastrado. Execute o seed para popular dados.")
