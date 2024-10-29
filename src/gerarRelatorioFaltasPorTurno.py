from collections import defaultdict
import pandas as pd
from datetime import datetime
from src.utils import prod

def gerar_relatorio_faltas_por_turno():
    faltas_por_mes_1turno = defaultdict(int)
    faltas_por_mes_2turno = defaultdict(int)

    meses = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Tenta converter a coluna para datetime, e usa 'coerce' para valores inválidos
    prod.iloc[:, 3] = pd.to_datetime(prod.iloc[:, 3], errors='coerce')

    for index, row in prod.iterrows():
        # Converte a data para datetime se ainda for string
        if isinstance(row.iloc[3], str):
            try:
                row.iloc[3] = datetime.strptime(row.iloc[3], '%Y-%m-%d')
            except ValueError:
                # Se a conversão falhar, pula a linha
                continue

        # Verifica se o valor da terceira coluna é equivalente a TRUE ou VERDADEIRO
        if ((row.iloc[2] == "TRUE" or row.iloc[2] == "VERDADEIRO") and not pd.isnull(row.iloc[3]) and (row.iloc[4] == "VERDADEIRO" or row.iloc[4] == "TRUE")):
            mes = row.iloc[3].strftime('%B')  # Extrai o mês como string
            # Incrementa o contador para o mês correspondente
            faltas_por_mes_1turno[mes] += 1
        elif ((row.iloc[2] == "TRUE" or row.iloc[2] == "VERDADEIRO") and not pd.isnull(row.iloc[3]) and (row.iloc[4] == "FALSO" or row.iloc[4] == "FALSE")):
            mes = row.iloc[3].strftime('%B')  # Extrai o mês como string
            # Incrementa o contador para o mês correspondente
            faltas_por_mes_2turno[mes] += 1

    data = {
        'Mês': [],
        'Primeiro turno': [],
        'Segundo turno': []
    }

    for mes in meses:
        data['Mês'].append(mes)
        data['Primeiro turno'].append(faltas_por_mes_1turno[mes])
        data['Segundo turno'].append(faltas_por_mes_2turno[mes])

    df = pd.DataFrame(data)

    # Adiciona a coluna "Turno"
    df_melted = df.melt(id_vars=['Mês'], var_name='Turno', value_name='Faltas')

    # Salva o DataFrame em um arquivo CSV
    df_melted.to_csv('faltas_por_turno.csv', index=False, sep=';')

    return df_melted
