import pytest
from main import (
    get_connection,
    adicionar_produto,
    consultar_quantidade,
    remover_produto
)

@pytest.fixture(autouse=True)
def preparar_banco_de_dados():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM produtos;")
    conn.commit()
    cur.close()
    conn.close()
    yield

def test__adicionar_novo_produto():
    resposta = adicionar_produto("Caderno", 10)
    assert resposta == "Sucesso: Produto adicionado/atualizado."
    assert consultar_quantidade("Caderno") == 10

def test_somar_quantidade_produto_existente():
    adicionar_produto("Lápis", 5)
    resposta = adicionar_produto("Lápis", 15)
    
    assert resposta == "Sucesso: Produto adicionado/atualizado."
    assert consultar_quantidade("Lápis") == 20

def test_remover_produto_sucesso():
    adicionar_produto("Borracha", 10)
    resposta = remover_produto("Borracha", 4)
    
    assert resposta == "Sucesso: Retirada efetuada."
    assert consultar_quantidade("Borracha") == 6

def test_impedir_estoque_negativo():
    adicionar_produto("Caneta TS02", 8)
    resposta = remover_produto("Caneta TS02", 10)
    
    assert resposta == "Erro: Saldo insuficiente no banco."
    assert consultar_quantidade("Caneta TS02") == 8

def test_consultar_saldo():
    adicionar_produto("Regra", 3)
    
    assert consultar_quantidade("Regra") == 3
    assert consultar_quantidade("Estojo") is None