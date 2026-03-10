"""
Funções para criação de gráficos Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
from utils.helpers import CORES, CORES_COMBUSTIVEL


# Layout base para todos os gráficos
LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA", family="sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
)


def grafico_consumo_diario(df):
    """Gráfico de barras empilhadas do consumo diário por tipo de combustível."""
    if df.empty:
        return _grafico_vazio("Sem dados de consumo diário")

    fig = px.bar(
        df,
        x="data",
        y="total_litros",
        color="tipo_combustivel",
        color_discrete_map=CORES_COMBUSTIVEL,
        labels={
            "data": "Data",
            "total_litros": "Litros",
            "tipo_combustivel": "Combustível"
        },
        barmode="stack",
    )

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Consumo Diário (Litros)", font=dict(size=16)),
        xaxis=dict(
            showgrid=False,
            tickformat="%d/%m",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
        ),
        height=350,
    )

    return fig


def grafico_consumo_mensal(df):
    """Gráfico de barras do consumo mensal."""
    if df.empty:
        return _grafico_vazio("Sem dados de consumo mensal")

    fig = px.bar(
        df,
        x="mes",
        y="total_litros",
        color="tipo_combustivel",
        color_discrete_map=CORES_COMBUSTIVEL,
        labels={
            "mes": "Mês",
            "total_litros": "Litros",
            "tipo_combustivel": "Combustível"
        },
        barmode="group",
    )

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Consumo Mensal (Litros)", font=dict(size=16)),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
        ),
        height=350,
    )

    return fig


def grafico_faturamento_diario(df):
    """Gráfico de linha do faturamento diário."""
    if df.empty:
        return _grafico_vazio("Sem dados de faturamento")

    # Agregar por dia (sem split por tipo)
    df_agg = df.groupby("data").agg({"total_valor": "sum"}).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_agg["data"],
        y=df_agg["total_valor"],
        mode="lines+markers",
        line=dict(color=CORES["primaria"], width=2.5),
        marker=dict(size=5),
        fill="tozeroy",
        fillcolor="rgba(255, 107, 53, 0.1)",
        name="Faturamento",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Faturamento Diário (R$)", font=dict(size=16)),
        xaxis=dict(
            showgrid=False,
            tickformat="%d/%m",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickprefix="R$ ",
        ),
        height=350,
        showlegend=False,
    )

    return fig


def grafico_veiculos_por_dia(df):
    """Gráfico de barras da quantidade de abastecimentos por dia."""
    if df.empty:
        return _grafico_vazio("Sem dados de abastecimentos")

    # Agregar por dia
    df_agg = df.groupby("data").agg({"qtd_abastecimentos": "sum"}).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_agg["data"],
        y=df_agg["qtd_abastecimentos"],
        marker_color=CORES["secundaria"],
        marker_line_width=0,
        opacity=0.85,
        name="Abastecimentos",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Abastecimentos por Dia", font=dict(size=16)),
        xaxis=dict(
            showgrid=False,
            tickformat="%d/%m",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
        ),
        height=350,
        showlegend=False,
    )

    return fig


def gauge_tanque(nome, nivel_atual, capacidade, cor="#FF6B35"):
    """Cria um gauge (medidor) para o nível do tanque."""
    percentual = (nivel_atual / capacidade * 100) if capacidade > 0 else 0

    # Cor dinâmica baseada no nível
    if percentual < 20:
        bar_color = CORES["perigo"]
    elif percentual < 40:
        bar_color = CORES["aviso"]
    else:
        bar_color = cor

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=nivel_atual,
        number=dict(
            suffix=" L",
            font=dict(size=28, color="#FAFAFA"),
        ),
        title=dict(
            text=nome,
            font=dict(size=13, color="#FAFAFA"),
        ),
        gauge=dict(
            axis=dict(
                range=[0, capacidade],
                tickwidth=1,
                tickcolor="rgba(255,255,255,0.3)",
                dtick=capacidade / 5,
            ),
            bar=dict(color=bar_color, thickness=0.75),
            bgcolor="rgba(255,255,255,0.05)",
            borderwidth=0,
            steps=[
                dict(range=[0, capacidade * 0.2], color="rgba(231, 29, 54, 0.15)"),
                dict(range=[capacidade * 0.2, capacidade * 0.4], color="rgba(255, 186, 8, 0.1)"),
                dict(range=[capacidade * 0.4, capacidade], color="rgba(32, 191, 85, 0.08)"),
            ],
            threshold=dict(
                line=dict(color="#FAFAFA", width=2),
                thickness=0.8,
                value=nivel_atual,
            ),
        ),
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FAFAFA"),
        height=250,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


def grafico_distribuicao_combustivel(df):
    """Gráfico de pizza da distribuição de combustível."""
    if df.empty:
        return _grafico_vazio("Sem dados")

    df_agg = df.groupby("tipo_combustivel").agg({"total_litros": "sum"}).reset_index()

    cores = [CORES_COMBUSTIVEL.get(t, "#888") for t in df_agg["tipo_combustivel"]]

    fig = go.Figure(go.Pie(
        labels=df_agg["tipo_combustivel"],
        values=df_agg["total_litros"],
        marker=dict(colors=cores, line=dict(width=2, color="#0E1117")),
        textinfo="label+percent",
        textfont=dict(size=12),
        hole=0.45,
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FAFAFA"),
        title=dict(text="Distribuição por Combustível", font=dict(size=16)),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
    )

    return fig


def _grafico_vazio(mensagem="Sem dados disponíveis"):
    """Retorna um gráfico vazio com mensagem."""
    fig = go.Figure()
    fig.add_annotation(
        text=mensagem,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="rgba(255,255,255,0.5)"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig
