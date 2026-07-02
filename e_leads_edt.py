from datetime import datetime, timedelta
from conexao import conexao
import pandas as pd
import os 

conn = conexao()

def leads_edt():
    
    hoje = datetime.now()
    
    if hoje.weekday() == 0:  # segunda-feira = 0
      data_inicio = (hoje - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
      data_fim = (hoje - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
      print("Hoje é segunda! .. extraindo informações do fim de semana!")
    
    else:
    # Caso contrário, pega apenas o dia anterior
      data_ontem = hoje - timedelta(days=1)
      data_inicio = data_ontem.replace(hour=0, minute=0, second=0, microsecond=0)
      data_fim = data_ontem.replace(hour=23, minute=59, second=59, microsecond=0)
      print("Hoje não é segunda! .. extraindo informações de ontem!")

    # Converte para formato aceito pelo SQL Server
    data_inicio_str = data_inicio.strftime('%Y-%m-%d %H:%M:%S')
    data_fim_str = data_fim.strftime('%Y-%m-%d %H:%M:%S')

    #Execuca o script SQL para extrair os dados do banco de dados (arquivo query.sql)
    with open("query.sql", "r", encoding="utf-8") as file:
        sql = file.read()
        
    
    sql = (
       sql.replace("{data_inicio_str}", data_inicio_str).replace("{data_fim_str}", data_fim_str)
    )
        
    edt = pd.read_sql(sql, conn)

    valores_vazios = ((edt['TELEFONE'].isnull()) & (edt['CELULAR'].isnull())).sum()
    print(f"Quantidade de valores vazios: {valores_vazios}")

    edt.dropna(subset=['TELEFONE', 'CELULAR'], how='all', inplace=True)

    mes_atual = data_fim.strftime('%m')
    ano_atual = data_fim.strftime('%Y')

    pasta = os.path.join("output", f"{mes_atual}{ano_atual}")
    os.makedirs(pasta, exist_ok=True)

    data_formatada = data_fim.strftime('%Y-%m-%d')
    nome_arquivo = f"Leads EDT {data_formatada}.xlsx"

    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta, nome_arquivo)

    edt.to_excel(caminho_arquivo, index=False)

    print(f"Planilha Excel gerada com sucesso: {caminho_arquivo}")
