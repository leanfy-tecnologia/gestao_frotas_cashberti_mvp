"""
Funções auxiliares para formatação e cálculos.
"""


def formatar_reais(valor):
    """Formata valor em Reais brasileiro."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_litros(litros):
    """Formata quantidade de litros."""
    return f"{litros:,.1f}L".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_placa(placa):
    """Formata placa no padrão Mercosul."""
    placa = placa.upper().replace("-", "").replace(" ", "")
    if len(placa) == 7:
        return f"{placa[:3]}-{placa[3:]}"
    return placa


def calcular_delta(atual, anterior):
    """Calcula a variação percentual entre dois valores."""
    if anterior == 0:
        return None
    return ((atual - anterior) / anterior) * 100


def delta_formatado(atual, anterior):
    """Retorna string formatada do delta para st.metric."""
    delta = calcular_delta(atual, anterior)
    if delta is None:
        return None
    return f"{delta:+.1f}%"


# Cores do tema
CORES = {
    "primaria": "#FF6B35",
    "secundaria": "#2EC4B6",
    "sucesso": "#20BF55",
    "perigo": "#E71D36",
    "aviso": "#FFBA08",
    "info": "#3A86FF",
    "gasolina_comum": "#FF6B35",
    "gasolina_aditivada": "#2EC4B6",
    "diesel": "#3A86FF",
    "bg_card": "#1A1F2E",
    "bg_dark": "#0E1117",
    "texto": "#FAFAFA",
}

CORES_COMBUSTIVEL = {
    "Gasolina Comum": "#FF6B35",
    "Gasolina Aditivada": "#2EC4B6",
    "Diesel S10": "#3A86FF",
}
