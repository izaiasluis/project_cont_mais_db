import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

MY_SQL_PASSWORD = os.getenv("MYSQL_PASSWORD") 
MY_SQL_USER = os.getenv("MYSQL_USER")

if not MY_SQL_PASSWORD or not MY_SQL_USER:
    raise Exception("ERRO CRÍTICO: Credenciais MySQL não carregadas. Verifique seu arquivo .env.")

def carregar_csv_para_mysql(caminho_csv):
    connection = None
    try:
        df = pd.read_csv(caminho_csv)
        print(f'LIdo {len(df)} transações do arquivo CSV.')
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user=MY_SQL_USER,
            password=MY_SQL_PASSWORD,
            database="contmais_db"
        )
        cursor = connection.cursor()
        sql_insert = """
            INSERT INTO lancamentos (
            data_lancamento, historico,valor,
            id_conta_debito, id_conta_credito
            ) VALUES (%s, %s, %s, %s, %s)"""
        
        data_inserts = []
        for index, row in df.iterrows():
            data_inserts.append((
                row['data'],
                row['historico'],
                row['valor'],
                int(row['id_conta_debito']),
                int(row['id_conta_credito'])
            ))
        cursor.executemany(sql_insert, data_inserts)
        connection.commit()
        print(f"Sucesso! {cursor.rowcount} linhas inseridas na tabela 'lancamentos'.") # <-- ADICIONADA ESTA LINHA
    except mysql.connector.Error as erro:
        print(f"Erro de Banco de Dados: {erro}")
        print("Verifique se o MySQL está ativo e se a senha no .env está correta.")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_csv}' não encontrado.")
        print("Certifique-se de que o transacoes.csv está na mesma pasta.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        
    finally:
        # Garantia de fechamento da conexão
        if connection and connection.is_connected():
            connection.close()
            print("Conexão MySQL fechada.")

if __name__ == "__main__":
    carregar_csv_para_mysql("transacoes.csv")
