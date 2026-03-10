import streamlit as st
import pandas as pd
import json
import pydeck as pdk
from datetime import datetime
import locale
from utils.navigation import header_menu

# Configuração da página - DEVE SER A PRIMEIRA CHAMADA STREAMLIT
st.set_page_config(
    page_title="Mapa de Abastecimentos",
    page_icon="📍",
    layout="wide"
)

header_menu()

# Tentativa de configurar locale pt_BR para datas e moedas
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252') # Windows fallback
    except locale.Error:
        pass

# Função para carregar os dados
@st.cache_data
def load_data():
    try:
        with open('data/abastecimentos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Verifique se data/abastecimentos.json existe.")
        return pd.DataFrame()

# Título da página
st.title("📍 Mapa de Calor: Abastecimentos")
st.markdown("Visualização geográfica da densidade de abastecimentos na região.")
st.divider()

# Carregar os dados
df = load_data()

if not df.empty and 'latitude' in df.columns and 'longitude' in df.columns:
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        tipos_combustivel = ["Todos"] + list(df['tipo_combustivel'].unique())
        filtro_combustivel = st.selectbox("Filtrar por Combustível", tipos_combustivel)
        
    with col2:
        veiculos = ["Todos"] + list(df['placa_veiculo'].unique())
        filtro_veiculo = st.selectbox("Filtrar por Veículo", veiculos)

    # Aplicar filtros
    filtered_df = df.copy()
    if filtro_combustivel != "Todos":
        filtered_df = filtered_df[filtered_df['tipo_combustivel'] == filtro_combustivel]
    if filtro_veiculo != "Todos":
        filtered_df = filtered_df[filtered_df['placa_veiculo'] == filtro_veiculo]

    if not filtered_df.empty:
        # Exibir métricas
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total de Abastecimentos", len(filtered_df))
        col_m2.metric("Total Gasto Filtrado", f"R$ {filtered_df['valor_total'].sum():,.2f}")
        col_m3.metric("Litros Filtrados", f"{filtered_df['litros'].sum():,.1f} L")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Obter o centro geométrico para a câmera do mapa
        lat_center = filtered_df['latitude'].mean()
        lon_center = filtered_df['longitude'].mean()

        # Configurar a visualização inicial do PyDeck
        view_state = pdk.ViewState(
            latitude=lat_center,
            longitude=lon_center,
            zoom=13,
            pitch=45,
            bearing=0
        )
        
        # Camada de Mapa de Calor (Heatmap)
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=filtered_df,
            opacity=0.9,
            get_position=["longitude", "latitude"],
            aggregation="SUM",
            # Usamos o total gasto ou litros como peso para o mapa de calor? 
            # Como padrão, cada ponto tem o mesmo peso. Se quisermos que abastecimentos maiores sejam mais intensos:
            get_weight="litros", 
        )
        
        # Camada de Dispersão (Pontos individuais por cima para interatividade se quiser)
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position=["longitude", "latitude"],
            get_color="[255, 107, 53, 100]", # Cor primária do app com transparência
            get_radius=80,
            pickable=True,
            auto_highlight=True
        )

        st.markdown("#### Densidade de Consumo (Litros)")
        # Renderizar o mapa via PyDeck usando o tema Streamlit (dark/light)
        r = pdk.Deck(
            layers=[heatmap_layer, scatter_layer],
            initial_view_state=view_state,
            tooltip={"text": "Placa: {placa_veiculo}\nCombustível: {tipo_combustivel}\nLitros: {litros}\nValor: R${valor_total}"},
            map_style=pdk.map_styles.DARK # Força o fundo escuro do mapa casando com o tema
        )

        st.pydeck_chart(r, use_container_width=True)
        
    else:
        st.warning("Nenhum abastecimento encontrado para os filtros selecionados.")
        
else:
    if df.empty:
        st.warning("Não há dados de abastecimentos registrados.")
    else:
        st.error("Os dados de abastecimento não possuem as colunas 'latitude' e 'longitude' necessárias para o mapa.")
