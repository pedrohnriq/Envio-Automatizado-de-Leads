from datetime import datetime, timedelta
from conexao import conexao
import pandas as pd

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


    data_formatada = data_fim.strftime('%Y-%m-%d')
    nome_arquivo = f"Leads EDT {data_formatada}.xlsx"

    edt.to_excel(nome_arquivo, index=False)
    print(f"Planilha Excel gerada com sucesso: {nome_arquivo}")

