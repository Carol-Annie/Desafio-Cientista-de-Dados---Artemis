import sqlite3
import pandas as pd

query_q1 = """
SELECT 
    c.Nome,
    p.PedidoID,
    p.DataPedido,
    p.ValorTotal
FROM Clientes c
LEFT JOIN Pedidos p ON c.ClienteID = p.ClienteID
"""

query_q2 = """
SELECT 
    c.Nome,
    COUNT(p.PedidoID) AS QuantidadePedidos,
    SUM(p.ValorTotal) AS ValorTotalPedidos
FROM Clientes c
INNER JOIN Pedidos p
    ON c.ClienteID = p.ClienteID
GROUP BY 
    c.Nome;
"""

query_q3 = """
SELECT 
    p.PedidoID,
    p.DataPedido,
    p.ValorTotal
FROM Pedidos p
LEFT JOIN Pagamentos pag
    ON p.PedidoID = pag.PedidoID
WHERE pag.PagamentoID IS NULL;

"""

def mostrar_resultado(caminho_banco, dicionario_queries):

    try:
        conn = sqlite3.connect(caminho_banco)
        
        for descricao, query in dicionario_queries.items():
            print(f"\n{descricao}")
            
            try:
                df = pd.read_sql_query(query, conn)
                print(df.to_string(index=False)) 
            except Exception as e:
                print(f" Erro ao executar '{descricao}': {e}")
                
    except sqlite3.Error as e:
        print(f"Erro crítico de conexão com o banco: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":

    dic_queries = {
        "Lista de todos os clientes e seus respectivos pedidos": query_q1,
        "Total de pedidos realizados e o valor total de pedidos por cliente": query_q2,
        "Pedidos sem Pagamento": query_q3
    }

    mostrar_resultado('Loja.sqlite', dic_queries)