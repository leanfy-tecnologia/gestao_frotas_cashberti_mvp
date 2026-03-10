"""
Página Gestão de Tanques
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_tanques, registrar_reabastecimento_tanque, get_historico_reabastecimentos
from utils.helpers import formatar_litros, formatar_reais, CORES_COMBUSTIVEL
from utils.charts import gauge_tanque
from utils.navigation import header_menu

st.set_page_config(page_title="Gestão de Tanques", layout="wide", initial_sidebar_state="collapsed")
header_menu()

st.title("Gestão de Tanques")
st.caption("Monitore e gerencie o estoque de combustível nos tanques")

# ============================================================
# Nível dos Tanques
# ============================================================
st.markdown("### Nível Atual dos Tanques")

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

            # Info card
            percentual = (tanque["nivel_atual_litros"] / tanque["capacidade_litros"] * 100)
            espaco = tanque["capacidade_litros"] - tanque["nivel_atual_litros"]

            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1A1F2E, #1E2538);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px;
                padding: 14px;
                text-align: center;
                font-size: 0.85rem;
            ">
                <div>
                    <span style="color: rgba(255,255,255,0.5);">Capacidade:</span>
                    <strong>{formatar_litros(tanque['capacidade_litros'])}</strong>
                </div>
                <div style="margin-top: 4px;">
                    <span style="color: rgba(255,255,255,0.5);">Disponível:</span>
                    <strong style="color: {'#E71D36' if percentual < 20 else '#FFBA08' if percentual < 40 else '#20BF55'};">
                        {formatar_litros(tanque['nivel_atual_litros'])}
                    </strong>
                </div>
                <div style="margin-top: 4px;">
                    <span style="color: rgba(255,255,255,0.5);">Espaço livre:</span>
                    <strong>{formatar_litros(espaco)}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Alerta para tanques com nível baixo
    tanques_baixos = tanques[
        tanques.apply(
            lambda t: (t["nivel_atual_litros"] / t["capacidade_litros"] * 100) < 25,
            axis=1
        )
    ]
    if not tanques_baixos.empty:
        st.markdown("---")
        st.warning("**Atenção!** Os seguintes tanques estão com nível abaixo de 25%:")
        for _, t in tanques_baixos.iterrows():
            pct = t["nivel_atual_litros"] / t["capacidade_litros"] * 100
            st.markdown(f"- **{t['nome']}**: {pct:.0f}% ({formatar_litros(t['nivel_atual_litros'])})")

else:
    st.info("Nenhum tanque cadastrado.")



# ============================================================
# Histórico de Reabastecimentos
# ============================================================
st.markdown("---")
st.markdown("### Histórico de Reabastecimentos")

historico = get_historico_reabastecimentos()

if not historico.empty:
    # Filtro por tanque
    filtro_tanque = st.selectbox(
        "Filtrar por tanque",
        options=["Todos"] + list(historico["tanque_nome"].unique()),
        key="filtro_hist_tanque"
    )

    if filtro_tanque != "Todos":
        historico = historico[historico["tanque_nome"] == filtro_tanque]

    # Formatar para exibição
    df_display = historico[["data_hora", "tanque_nome", "tipo_combustivel", "litros_adicionados", "fornecedor"]].copy()
    df_display.columns = ["Data/Hora", "Tanque", "Combustível", "Litros", "Fornecedor"]

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Litros": st.column_config.NumberColumn(format="%.0f L"),
            "Data/Hora": st.column_config.TextColumn(width="medium"),
        }
    )

    st.caption(f"Total de registros: {len(df_display)}")
else:
    st.info("Nenhum reabastecimento registrado.")
