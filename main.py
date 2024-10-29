import json
import pandas as pd
from src.ColetarDatas import coletarDatas
from src.coletarPresençaAlunos import coletarPresençaAlunos
from src.determinarFrequencia import determinarFrequencia
from src.utils import presença, DataFrameOfPresença, presençaPorcentagem, totalDePresenças, presençaMensal
from src.presençaMensal import mensal
from src.gerarRelatorioFaltasPorTurno import gerar_relatorio_faltas_por_turno


print('Coletando as Datas...')
coletarDatas()
print('Coletando as Presenças dos Alunos...')
coletarPresençaAlunos()
print('Determinando as Frequencias...')
determinarFrequencia()
print("Determinando as presenças mensais")
jsonParaPresencaMensal = DataFrameOfPresença
with open('./assetsGenerate/jsonParaPresencaMensal.json', 'w') as f:
    json.dump(jsonParaPresencaMensal, f, indent=4, default=str)
print("Determinando frequencia mensal...")
json_path = './assetsGenerate/jsonParaPresencaMensal.json'






porcentagemTotal = {key: f"{value/totalDePresenças * 100:.1f}%" for key, value in presençaPorcentagem.items()}
DataFrameOfPresença[f'Porcentagem. Total:{totalDePresenças}'] = porcentagemTotal                
presença[f'Porcentagem. Total:{totalDePresenças}'] = porcentagemTotal                

with open('./assetsGenerate/presença.json', 'w') as f:
    json.dump(presença, f, indent=4, default=str)
    

with open('./assetsGenerate/DataFrameOfPresença.json', 'w') as f:
    json.dump(DataFrameOfPresença, f, indent=4, default=str)

print()
print('Arquivos criados com sucesso na pasta AssetsGenerate:') 

print("presença.json - apenas um json do dict presença")
print("jsonParaPresencaMensal.json - dict utilizado para calcular a presença mensal")
print("DataFrameOfPresença - Dict utilizado para gerar a planilha")
print()


print('Gerando relatório mensal de faltas por turno...')
gerar_relatorio_faltas_por_turno()
print("Planilha de relatório mensal de falta/turno criada com sucesso!")
print()

mensal()
df_mensal = pd.DataFrame(presençaMensal)
#df_mensal.to_csv("./assetsGenerate/Presença.csv")
with open('./assetsGenerate/presençaMensal.json', 'w') as f:
    json.dump(presençaMensal, f, indent=4, default=str)


df = pd.DataFrame(DataFrameOfPresença)
df = df.rename_axis("Aluno") 
with pd.ExcelWriter('./assetsGenerate/Chamada GeralABAS.xlsx') as writer:
    df.to_excel(writer, sheet_name='Geral')
    df_mensal.to_excel(writer, sheet_name='Mensal')

df.to_csv('./assetsGenerate/Chamada Geral.csv')
print('Planilha "Chamada Geral" criada com sucesso!')
