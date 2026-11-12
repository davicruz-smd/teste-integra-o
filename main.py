import psycopg2
import os
from psycopg2 import sql

os.environ["PGCLIENTENCODING"] = "utf-8"

def get_connection():
    return psycopg2.connect(
        dbname="produto_teste",
        user="postgres",
        password="root",
        host="localhost",
        client_encoding="utf-8"
    )

def adicionar_produto(nome, quantidade):
    if quantidade <= 0:
        return "Erro: Quantidade deve ser maior que zero."
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = """
        INSERT INTO produtos (nome, quantidade)
        VALUES (%s, %s)
        ON CONFLICT (nome)
        DO UPDATE SET quantidade = produtos.quantidade + EXCLUDED.quantidade;
        """
        cur.execute(query, (nome, quantidade))
        conn.commit()
        return "Sucesso: Produto adicionado/atualizado."
    except Exception as e:
        conn.rollback()
        return f"Erro: {e}"
    finally:
        cur.close()
        conn.close()

def consultar_quantidade(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT quantidade FROM produtos WHERE nome = %s", (nome,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def remover_produto(nome, quantidade):
    if quantidade <= 0:
        return "Erro: Quantidade inválida."
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE nome = %s", (quantidade, nome))
        if cur.rowcount == 0:
            return "Erro: Produto não encontrado."
        conn.commit()
        return "Sucesso: Retirada efetuada."
    except psycopg2.errors.CheckViolation:
        conn.rollback()
        return "Erro: Saldo insuficiente no banco."
    except Exception as e:
        conn.rollback()
        return f"Erro: {e}"
    finally:
        cur.close()
        conn.close()

get_connection()