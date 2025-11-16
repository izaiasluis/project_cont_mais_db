import mysql.connector
import os
from dotenv import load_dotenv
import json

load_dotenv()
MY_SQL_PASSWORD = os.getenv("MYSQL_PASSWORD") 
MY_SQL_USER = os.getenv("MYSQL_USER")
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": MY_SQL_USER,
    "password": MY_SQL_PASSWORD,
    "database": "contmais_db"
}
if not MY_SQL_PASSWORD or not MY_SQL_USER:
    raise Exception("ERRO CRÍTICO: Credenciais MySQL não carregadas. Verifique seu arquivo .env.") 

def obter_total_receitas():
    connection = None
    total_receitas = 0.0
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = """
            SELECT SUM(l.valor) FROM lancamentos l 
            JOIN plano_de_contas pc ON 
            l.id_conta_credito = pc.id_conta 
            WHERE pc.tipo_conta = 'Receita'
        """
        cursor.execute(query)
        resultado = cursor.fetchone()
        total_receitas = resultado[0] if resultado[0] is not None else 0.0
    except mysql.connector.Error as erro:
        print(f"Erro de Banco de Dados: {erro}")
    finally:
        if connection and connection.is_connected():
            connection.close()
    return total_receitas

def obter_total_despesas():
    connection = None
    total_despesas = 0.0
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = """
            SELECT SUM(l.valor) FROM lancamentos l 
            JOIN plano_de_contas pc ON 
            l.id_conta_debito = pc.id_conta 
            WHERE pc.tipo_conta IN ('Custo', 'Despesa')
        """
        cursor.execute(query)
        resultado = cursor.fetchone()
        total_despesas = resultado[0] if resultado[0] is not None else 0.0
    except mysql.connector.Error as erro:
        print(f"Erro de Banco de Dados: {erro}")
    finally:
        if connection and connection.is_connected():
            connection.close()
    return total_despesas

def calcular_dre():
    total_receitas = obter_total_receitas()
    total_despesas = obter_total_despesas()
    lucro_bruto = total_receitas - total_despesas
    dre_data = {
        "ReceitaBruta": float(total_receitas) if total_receitas is not None else 0.0,
        "CustosDespesas": float(total_despesas) if total_despesas is not None else 0.0,
        "LucroBruto": float(lucro_bruto) if lucro_bruto is not None else 0.0
    }
    print("\n---  DEMONSTRAÇÃO DO RESULTADO DO EXERCÍCIO (DRE) ---")
    print(f"| {'RECEITA BRUTA':<20} | R$ {total_receitas:>15,.2f} |")
    print(f"| {'(-) CUSTOS/DESPESAS':<20} | R$ {total_despesas:>15,.2f} |")
    print("-" * 43)
    print(f"| {'LUCRO BRUTO':<20} | R$ {lucro_bruto:>15,.2f} |")
    print("--------------------------------------------------")
    '''
    return {
        "Total de Receitas": total_receitas,
        "Total de Despesas": total_despesas,
        "Lucro Bruto": lucro_bruto 
    }
   # return dre

if __name__ == "__main__":
    calcular_dre()
    '''
    NOME_ARQUIVO_JSON = 'dre_resultado.json'
    PASTA_DESTINO = 'data' 
    

    os.makedirs(PASTA_DESTINO, exist_ok=True) 
    
    caminho_completo = os.path.join(PASTA_DESTINO, NOME_ARQUIVO_JSON)
    
    try:
        with open(caminho_completo, 'w') as f:
            json.dump(dre_data, f, indent=4)
            print(f"\nDados exportados para {caminho_completo} para o Dashboard.")
            
    except Exception as e:
        print(f"ERRO CRÍTICO AO SALVAR JSON: {e}")
    
    return dre_data

if __name__ == "__main__":
    calcular_dre()