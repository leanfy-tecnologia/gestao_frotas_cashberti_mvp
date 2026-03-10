import json
import os
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Placas de veículos fictícias
PLACAS = [
    "ABC1D23", "DEF4G56", "GHI7J89", "JKL0M12", "MNO3P45",
    "PQR6S78", "STU9V01", "VWX2Y34", "YZA5B67", "BCD8E90",
    "EFG1H23", "HIJ4K56", "KLM7N89", "NOP0Q12", "QRS3T45",
    "TUV6W78", "WXY9Z01", "ZAB2C34", "CDE5F67", "FGH8I90",
    "IJK1L23", "LMN4O56", "OPQ7R89", "RST0U12", "UVW3X45",
]

# Preços por litro (valores realistas em R$)
PRECOS = {
    "Gasolina Comum": 5.89,
    "Gasolina Aditivada": 6.29,
    "Diesel S10": 5.49,
}

def seed_jsons():
    # 1. Tanques (já criado, mas garantimos que as IDs estejam certas)
    tanques = [
        {
            "id": 1,
            "nome": "Tanque 1 - Gasolina Comum",
            "tipo_combustivel": "Gasolina Comum",
            "capacidade_litros": 15000,
            "nivel_atual_litros": 8750
        },
        {
            "id": 2,
            "nome": "Tanque 2 - Gasolina Aditivada",
            "tipo_combustivel": "Gasolina Aditivada",
            "capacidade_litros": 10000,
            "nivel_atual_litros": 5200
        },
        {
            "id": 3,
            "nome": "Tanque 3 - Diesel S10",
            "tipo_combustivel": "Diesel S10",
            "capacidade_litros": 20000,
            "nivel_atual_litros": 12300
        }
    ]
    with open(os.path.join(DATA_DIR, "tanques.json"), "w", encoding="utf-8") as f:
        json.dump(tanques, f, indent=4, ensure_ascii=False)

    tanque_map = {t["tipo_combustivel"]: t["id"] for t in tanques}

    # 2. Abastecimentos
    abastecimentos = []
    agora = datetime.now()
    abastecimento_id = 1

    for dia_offset in range(60, -1, -1):
        data = agora - timedelta(days=dia_offset)
        
        dia_semana = data.weekday()
        if dia_semana < 5:  # Seg-Sex
            qtd_abastecimentos = random.randint(8, 20)
        else:  # Sáb-Dom
            qtd_abastecimentos = random.randint(4, 12)

        for _ in range(qtd_abastecimentos):
            placa = random.choice(PLACAS)
            tipo = random.choice(list(PRECOS.keys()))

            if "Diesel" in tipo:
                litros = round(random.uniform(30, 200), 1)
            else:
                litros = round(random.uniform(10, 60), 1)

            valor_litro = round(PRECOS[tipo] * random.uniform(0.95, 1.05), 2)
            valor_total = round(litros * valor_litro, 2)

            hora = random.randint(6, 22)
            minuto = random.randint(0, 59)
            segundo = random.randint(0, 59)
            data_hora = data.replace(hour=hora, minute=minuto, second=segundo).strftime("%Y-%m-%d %H:%M:%S")

            abastecimentos.append({
                "id": abastecimento_id,
                "data_hora": data_hora,
                "placa_veiculo": placa,
                "tipo_combustivel": tipo,
                "litros": litros,
                "valor_litro": valor_litro,
                "valor_total": valor_total,
                "tanque_id": tanque_map[tipo]
            })
            abastecimento_id += 1

    with open(os.path.join(DATA_DIR, "abastecimentos.json"), "w", encoding="utf-8") as f:
        json.dump(abastecimentos, f, indent=4, ensure_ascii=False)

    # 3. Reabastecimentos dos Tanques
    reabastecimentos = []
    reabastecimento_id = 1
    fornecedores = ["Petrobras", "Raízen", "Ipiranga", "Vibra Energia"]

    for tanque in tanques:
        qtd = random.randint(3, 5)
        for _ in range(qtd):
            dia_offset = random.randint(5, 55)
            data = agora - timedelta(days=dia_offset)
            hora = random.randint(7, 18)
            data_hora = data.replace(hour=hora, minute=random.randint(0, 59)).strftime("%Y-%m-%d %H:%M:%S")

            litros = round(random.uniform(
                tanque["capacidade_litros"] * 0.3,
                tanque["capacidade_litros"] * 0.6
            ), 0)

            reabastecimentos.append({
                "id": reabastecimento_id,
                "tanque_id": tanque["id"],
                "data_hora": data_hora,
                "litros_adicionados": litros,
                "fornecedor": random.choice(fornecedores)
            })
            reabastecimento_id += 1

    with open(os.path.join(DATA_DIR, "reabastecimentos_tanque.json"), "w", encoding="utf-8") as f:
        json.dump(reabastecimentos, f, indent=4, ensure_ascii=False)

    print("✅ Dados JSON gerados com sucesso na pasta 'data'!")

if __name__ == "__main__":
    seed_jsons()
