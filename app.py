"""
Dashboard Gestão de Bomba de Gasolina
Aplicação principal - Página Home
"""

import streamlit as st
from database import init_db, get_tanques, get_resumo_hoje
from utils.helpers import formatar_reais, formatar_litros, CORES

from utils.navigation import header_menu

# Configuração da página
st.set_page_config(
    page_title="Gestão de Bomba de Gasolina",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Header menu
header_menu()

# CSS customizado agora é carregado via header_menu()

# Página Home
st.markdown("""
<div class="hero-banner">
    <h2>Gestão de Bomba de Gasolina</h2>
    <p>Painel completo para controle de abastecimentos, consumo e estoque de combustível</p>
</div>
""", unsafe_allow_html=True)

# Resumo rápido
try:
    resumo = get_resumo_hoje()
    tanques = get_tanques()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="quick-stat">
            <div class="icon">~</div>
            <div class="value">{}</div>
            <div class="label">Litros Hoje</div>
        </div>
        """.format(formatar_litros(resumo["litros_hoje"])), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="quick-stat">
            <div class="icon">$</div>
            <div class="value">{}</div>
            <div class="label">Faturamento Hoje</div>
        </div>
        """.format(formatar_reais(resumo["faturamento_hoje"])), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="quick-stat">
            <div class="icon">#</div>
            <div class="value">{}</div>
            <div class="label">Veículos Hoje</div>
        </div>
        """.format(resumo["veiculos_hoje"]), unsafe_allow_html=True)

    with col4:
        total_estoque = tanques["nivel_atual_litros"].sum() if not tanques.empty else 0
        st.markdown("""
        <div class="quick-stat">
            <div class="icon">%</div>
            <div class="value">{}</div>
            <div class="label">Estoque Total</div>
        </div>
        """.format(formatar_litros(total_estoque)), unsafe_allow_html=True)

except Exception:
    st.info("🔄 Execute o seed para popular o banco: `python seed_data.py`")

st.markdown("---")

# # Features
# st.subheader("🎯 Funcionalidades")

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("""
#     **Dashboard Completo**
    
#     Acompanhe métricas de consumo diário e mensal, 
#     faturamento, e quantidade de veículos abastecidos
#     com gráficos interativos.
#     """)

# with col2:
#     st.markdown("""
#     **Gestão de Tanques**
    
#     Monitore o nível atual de cada tanque em 
#     tempo real com indicadores visuais gauge.
#     """)

#     st.markdown("""
#     **Histórico Completo**
    
#     Consulte todos os abastecimentos com filtros 
#     por data, placa e tipo de combustível.
#     """)