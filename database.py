"""
Módulo de banco de dados baseado em JSON - Gestão de Bomba de Gasolina
Substitui a lógica do SQLite por arquivos JSON mapeando os mesmos dados.
"""

import json
import os
from datetime import datetime, timedelta
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    for file_name in ["tanques.json", "abastecimentos.json", "reabastecimentos_tanque.json"]:
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

def read_json(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json(file_name, data):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ============================================================
# Funções de consulta - Tanques
# ============================================================

def get_tanques():
    """Retorna todos os tanques como DataFrame DataFrame"""
    data = read_json("tanques.json")
    return pd.DataFrame(data)

def get_tanque_by_id(tanque_id):
    """Retorna um tanque pelo ID (dicionário)."""
    data = read_json("tanques.json")
    for t in data:
        if t["id"] == tanque_id:
            return t
    return None

def atualizar_nivel_tanque(tanque_id, novo_nivel):
    data = read_json("tanques.json")
    for t in data:
        if t["id"] == tanque_id:
            t["nivel_atual_litros"] = novo_nivel
            break
    write_json("tanques.json", data)

# ============================================================
# Funções de consulta - Abastecimentos
# ============================================================

def registrar_abastecimento(placa, tipo_combustivel, litros, valor_litro, tanque_id):
    tanque = get_tanque_by_id(tanque_id)
    if not tanque:
        return False, "Tanque não encontrado."

    if tanque["nivel_atual_litros"] < litros:
        return False, f"Estoque insuficiente. Disponível: {tanque['nivel_atual_litros']:.1f}L"

    # Atualizar tanque
    atualizar_nivel_tanque(tanque_id, tanque["nivel_atual_litros"] - litros)

    # Registrar abastecimento
    abastecimentos = read_json("abastecimentos.json")
    novo_id = max([a.get("id", 0) for a in abastecimentos], default=0) + 1
    
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    valor_total = litros * valor_litro

    abastecimentos.append({
        "id": novo_id,
        "data_hora": agora,
        "placa_veiculo": placa.upper(),
        "tipo_combustivel": tipo_combustivel,
        "litros": litros,
        "valor_litro": round(valor_litro, 2),
        "valor_total": round(valor_total, 2),
        "tanque_id": tanque_id
    })
    
    write_json("abastecimentos.json", abastecimentos)
    return True, "Abastecimento registrado com sucesso!"

def get_abastecimentos(data_inicio=None, data_fim=None, placa=None, tipo=None):
    data = read_json("abastecimentos.json")
    if not data:
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    df['data_hora'] = pd.to_datetime(df['data_hora'])

    if data_inicio:
        df = df[df['data_hora'].dt.date >= pd.to_datetime(data_inicio).date()]
    if data_fim:
        df = df[df['data_hora'].dt.date <= pd.to_datetime(data_fim).date()]
    if placa:
        df = df[df['placa_veiculo'].str.contains(placa.upper(), na=False)]
    if tipo:
        df = df[df['tipo_combustivel'] == tipo]

    return df.sort_values(by="data_hora", ascending=False)

def get_consumo_diario(dias=30):
    data = read_json("abastecimentos.json")
    if not data:
        return pd.DataFrame(columns=["data", "tipo_combustivel", "total_litros", "total_valor", "qtd_abastecimentos"])
        
    df = pd.DataFrame(data)
    data_limite = (datetime.now() - timedelta(days=dias)).date()
    df['data'] = pd.to_datetime(df['data_hora']).dt.date
    df = df[df['data'] >= data_limite]
    
    res = df.groupby(['data', 'tipo_combustivel']).agg(
        total_litros=('litros', 'sum'),
        total_valor=('valor_total', 'sum'),
        qtd_abastecimentos=('id', 'count')
    ).reset_index()
    return res

def get_consumo_mensal(meses=12):
    data = read_json("abastecimentos.json")
    if not data:
        return pd.DataFrame(columns=["mes", "tipo_combustivel", "total_litros", "total_valor", "qtd_abastecimentos"])
    
    df = pd.DataFrame(data)
    data_limite = (datetime.now() - timedelta(days=meses*30)).date()
    df['data'] = pd.to_datetime(df['data_hora']).dt.date
    df = df[df['data'] >= data_limite]
    df['mes'] = pd.to_datetime(df['data_hora']).dt.strftime('%Y-%m')
    
    res = df.groupby(['mes', 'tipo_combustivel']).agg(
        total_litros=('litros', 'sum'),
        total_valor=('valor_total', 'sum'),
        qtd_abastecimentos=('id', 'count')
    ).reset_index()
    return res

def get_veiculos_abastecidos_hoje():
    data = read_json("abastecimentos.json")
    hoje = datetime.now().date()
    placas = set()
    for d in data:
        if datetime.strptime(d["data_hora"], "%Y-%m-%d %H:%M:%S").date() == hoje:
            placas.add(d["placa_veiculo"])
    return len(placas)

def get_resumo_hoje():
    data = read_json("abastecimentos.json")
    hoje = datetime.now().date()
    ontem = hoje - timedelta(days=1)
    
    df = pd.DataFrame(data)
    if df.empty:
        return {
            "litros_hoje": 0, "faturamento_hoje": 0, "abastecimentos_hoje": 0, "veiculos_hoje": 0,
            "litros_ontem": 0, "faturamento_ontem": 0, "abastecimentos_ontem": 0, "veiculos_ontem": 0,
        }
        
    df['data'] = pd.to_datetime(df['data_hora']).dt.date
    df_hoje = df[df['data'] == hoje]
    df_ontem = df[df['data'] == ontem]
    
    return {
        "litros_hoje": df_hoje['litros'].sum() if not df_hoje.empty else 0,
        "faturamento_hoje": df_hoje['valor_total'].sum() if not df_hoje.empty else 0,
        "abastecimentos_hoje": len(df_hoje),
        "veiculos_hoje": df_hoje['placa_veiculo'].nunique() if not df_hoje.empty else 0,
        "litros_ontem": df_ontem['litros'].sum() if not df_ontem.empty else 0,
        "faturamento_ontem": df_ontem['valor_total'].sum() if not df_ontem.empty else 0,
        "abastecimentos_ontem": len(df_ontem),
        "veiculos_ontem": df_ontem['placa_veiculo'].nunique() if not df_ontem.empty else 0,
    }

def get_resumo_mes():
    data = read_json("abastecimentos.json")
    mes_atual = datetime.now().strftime("%Y-%m")
    mes_anterior = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    
    df = pd.DataFrame(data)
    if df.empty:
        return {
            "litros_mes": 0, "faturamento_mes": 0, "abastecimentos_mes": 0, "veiculos_mes": 0,
            "litros_mes_ant": 0, "faturamento_mes_ant": 0, "abastecimentos_mes_ant": 0, "veiculos_mes_ant": 0,
        }
        
    df['mes'] = pd.to_datetime(df['data_hora']).dt.strftime('%Y-%m')
    df_mes = df[df['mes'] == mes_atual]
    df_mes_ant = df[df['mes'] == mes_anterior]
    
    return {
        "litros_mes": df_mes['litros'].sum() if not df_mes.empty else 0,
        "faturamento_mes": df_mes['valor_total'].sum() if not df_mes.empty else 0,
        "abastecimentos_mes": len(df_mes),
        "veiculos_mes": df_mes['placa_veiculo'].nunique() if not df_mes.empty else 0,
        "litros_mes_ant": df_mes_ant['litros'].sum() if not df_mes_ant.empty else 0,
        "faturamento_mes_ant": df_mes_ant['valor_total'].sum() if not df_mes_ant.empty else 0,
        "abastecimentos_mes_ant": len(df_mes_ant),
        "veiculos_mes_ant": df_mes_ant['placa_veiculo'].nunique() if not df_mes_ant.empty else 0,
    }

# ============================================================
# Funções de consulta - Reabastecimentos dos tanques
# ============================================================

def registrar_reabastecimento_tanque(tanque_id, litros, fornecedor=""):
    tanque = get_tanque_by_id(tanque_id)
    if not tanque:
        return False, "Tanque não encontrado."

    novo_nivel = tanque["nivel_atual_litros"] + litros
    if novo_nivel > tanque["capacidade_litros"]:
        return False, f"Excede capacidade. Espaço disponível: {tanque['capacidade_litros'] - tanque['nivel_atual_litros']:.1f}L"

    # Atualiza tanque
    atualizar_nivel_tanque(tanque_id, novo_nivel)

    # Registra reabastecimento
    reabs = read_json("reabastecimentos_tanque.json")
    novo_id = max([r.get("id", 0) for r in reabs], default=0) + 1
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    reabs.append({
        "id": novo_id,
        "tanque_id": tanque_id,
        "data_hora": agora,
        "litros_adicionados": litros,
        "fornecedor": fornecedor
    })
    
    write_json("reabastecimentos_tanque.json", reabs)
    return True, "Reabastecimento registrado com sucesso!"

def get_historico_reabastecimentos(tanque_id=None):
    reabs = read_json("reabastecimentos_tanque.json")
    tanques = read_json("tanques.json")
    
    if not reabs or not tanques:
        return pd.DataFrame()
        
    df_reabs = pd.DataFrame(reabs)
    df_tanques = pd.DataFrame(tanques)
    
    df = pd.merge(df_reabs, df_tanques[['id', 'nome', 'tipo_combustivel']], left_on='tanque_id', right_on='id', how='left')
    df = df.rename(columns={'nome': 'tanque_nome'})
    
    if tanque_id:
        df = df[df['tanque_id'] == tanque_id]
        
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    return df.sort_values(by="data_hora", ascending=False)

# Inicializar
init_db()
