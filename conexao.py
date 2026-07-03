import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def conexao():
    """
    Função para estabelecer conexão com o banco de dados SQL Server.
    """
    try:
        # Estabelece a conexão 
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            f'Server={os.getenv("Server")};'
            f'Database={os.getenv("Database")};'
            f'UID={os.getenv("usuario")};'
            f'PWD={os.getenv("pwd")};'
            'Trusted_Connection=no;'
            'Connection Timeout=30;'
        )
        print("Conexão estabelecida com sucesso.")
        return conn
    except Exception as e:
        print("Erro ao conectar:")
        print(repr(e))