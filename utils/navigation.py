"""
Componente de Navegação no Topo
"""
import streamlit as st

def header_menu():
    st.markdown("""
    <style>
        /* Ocultar barra lateral padrão do Streamlit completamente */
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        
        /* Ajustar o visual do link para parecer menu integrado */
        div[data-testid="stPageLink-NavLink"] {
            border: 1px solid transparent;
            text-align: center;
        }
        
        div[data-testid="stPageLink-NavLink"] > a {
            justify-content: center;
        }
        
        /* Logo na mesma linha do menu */
        .header-logo-inline {
            font-size: 1.2rem;
            font-weight: 700;
            color: #FAFAFA;
            margin-top: 8px; /* alinhar visualmente com os botoes */
        }
        
        .header-logo-inline span.highlight {
            background: linear-gradient(135deg, #FF6B35, #FF8C61);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* --- ESTILOS GLOBAIS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Cards de métricas */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1A1F2E 0%, #1E2538 100%);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.85rem !important;
            color: rgba(255,255,255,0.6) !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #FAFAFA !important;
        }
        
        /* Títulos */
        h1 {
            background: linear-gradient(135deg, #FF6B35, #FF8C61);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
        }
        
        /* Divider */
        hr {
            border-color: rgba(255,255,255,0.06) !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            padding: 8px 16px;
            border: 1px solid rgba(255,255,255,0.06);
        }
        
        .stTabs [aria-selected="true"] {
            background: rgba(255, 107, 53, 0.15) !important;
            border-color: #FF6B35 !important;
        }
        
        /* Plotly charts container */
        [data-testid="stPlotlyChart"] {
            background: linear-gradient(135deg, #1A1F2E 0%, #1E2538 100%);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        /* Hero banner */
        .hero-banner {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C61 50%, #2EC4B6 100%);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 24px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
        }
        
        .hero-banner h2 {
            color: white !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin-bottom: 8px !important;
            -webkit-text-fill-color: white !important;
        }
        
        .hero-banner p {
            color: rgba(255,255,255,0.9) !important;
            font-size: 1.1rem !important;
            margin: 0 !important;
        }
        
        /* Quick stats */
        .quick-stat {
            background: linear-gradient(135deg, #1A1F2E 0%, #1E2538 100%);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .quick-stat .icon {
            font-size: 2.5rem;
            margin-bottom: 8px;
        }
        
        .quick-stat .value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #FAFAFA;
        }
        
        .quick-stat .label {
            font-size: 0.8rem;
            color: rgba(255,255,255,0.5);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0E1117;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.15);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.25);
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            border-color: #FF6B35;
            box-shadow: 0 0 15px rgba(255, 107, 53, 0.2);
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
        }
        
        /* Selectbox, inputs */
        [data-testid="stSelectbox"], [data-testid="stNumberInput"], [data-testid="stTextInput"] {
            border-radius: 8px;
        }
        
        /* Success/error messages */
        .stAlert {
            border-radius: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    import base64
    import os
    
    # Função para converter imagem em base64 e embutir no HTML
    def get_image_base64(path):
        try:
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception:
            return ""
            
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "image.png")
    logo_base64 = get_image_base64(logo_path)
    
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" style="height:80px; margin-right: 12px; vertical-align: middle;">' if logo_base64 else ''

    # Renderizar Menu de Navegação na mesma linha
    c_logo, c1, c2, c3, c4 = st.columns([3.5, 1.6, 1.6, 1.6, 1.7], vertical_alignment="center")
    
    with c_logo:
        st.markdown(f'<div class="header-logo-inline">{img_tag}<span class="highlight"></span> CashBerti - Gestão de Frotas</div>', unsafe_allow_html=True)
        
    with c1:
        st.page_link("pages/1_Dashboard.py", label="Dashboard")
        
    with c2:
        st.page_link("pages/3_Tanques.py", label="Tanques")
        
    with c3:
        st.page_link("pages/4_Historico.py", label="Histórico")

    with c4:
        st.page_link("pages/5_📍_Mapa_de_Calor.py", label="Mapa de Calor")
        
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
