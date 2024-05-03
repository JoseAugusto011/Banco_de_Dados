import mysql.connector
from decimal import Decimal
import matplotlib.pyplot as plt

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def create_tables(self):
        # Criação da tabela Estoque
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estoque (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            descricao TEXT,
            preco DECIMAL(10, 2),
            categoria VARCHAR(255),
            regiaoOrigem VARCHAR(255),
            disponibilidade BOOLEAN DEFAULT False,
            quantidade INT DEFAULT 0
        )
        """)
        # Criação da tabela Cliente
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cliente (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            email_login VARCHAR(255),
            senha_login VARCHAR(255),
            telefone VARCHAR(20),
            torceFlamengo BOOLEAN,
            assisteOnePiece BOOLEAN,
            cidade VARCHAR(255)
        )
        """)
        # Criação da tabela Venda
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Venda (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT,
            data_venda DATE,
            forma_pagamento VARCHAR(255),
            status_pagamento VARCHAR(255),
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
        )
        """)
        # Criação da tabela ItemVenda
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ItemVenda (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_venda INT,
            id_produto INT,
            quantidade INT,
            FOREIGN KEY (id_venda) REFERENCES Venda(id),
            FOREIGN KEY (id_produto) REFERENCES Estoque(id)
        )
        """)
        self.connection.commit()


    def close_connection(self):
        self.cursor.close()
        self.connection.close()

class EstoqueManager:
    def __init__(self, db):
        self.db = db

    def produto_existe(self, nome):
        query = "SELECT COUNT(*) FROM Estoque WHERE nome = %s"
        self.db.cursor.execute(query, (nome,))
        count = self.db.cursor.fetchone()[0]
        return count > 0

    def inserir(self, nome, descricao, preco, categoria, regiaoOrigem, disponibilidade=False, quantidade=0):
        if self.produto_existe(nome):
            print("Produto com este nome já existe. Não é possível inserir.")
            return
        query = "INSERT INTO Estoque (nome, descricao, preco, categoria, regiaoOrigem, disponibilidade, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.db.cursor.execute(query, (nome, descricao, preco, categoria, regiaoOrigem, disponibilidade, quantidade))
        self.db.connection.commit()
        print("Produto inserido com sucesso.")

    def get_quantidade(self, id):
        query = "SELECT quantidade FROM Estoque WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        return self.db.cursor.fetchone()[0]
    
    def get_nome_produto(self, id):
        query = "SELECT nome FROM Estoque WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        result = self.db.cursor.fetchone()
        return result[0] if result is not None else None



    def remover(self, id):
        query = "DELETE FROM Estoque WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        self.db.connection.commit()

    def atualizar_nome(self, id, nome):
        query = "UPDATE Estoque SET nome = %s WHERE id = %s"
        self.db.cursor.execute(query, (nome, id))
        self.db.connection.commit()

    def atualizar_descricao(self, id, descricao):
        query = "UPDATE Estoque SET descricao = %s WHERE id = %s"
        self.db.cursor.execute(query, (descricao, id))
        self.db.connection.commit()

    def atualizar_preco(self, id, preco):
        query = "UPDATE Estoque SET preco = %s WHERE id = %s"
        self.db.cursor.execute(query, (preco, id))
        self.db.connection.commit()

    def atualizar_categoria(self, id, categoria):
        query = "UPDATE Estoque SET categoria = %s WHERE id = %s"
        self.db.cursor.execute(query, (categoria, id))
        self.db.connection.commit()

    def atualizar_regiao_origem(self, id, regiaoOrigem):
        query = "UPDATE Estoque SET regiaoOrigem = %s WHERE id = %s"
        self.db.cursor.execute(query, (regiaoOrigem, id))
        self.db.connection.commit()

    def atualizar_disponibilidade(self, id, disponibilidade):
        query = "UPDATE Estoque SET disponibilidade = %s WHERE id = %s"
        self.db.cursor.execute(query, (disponibilidade, id))
        self.db.connection.commit()


    def atualizar_quantidade(self, id, quantidade):
        query = "UPDATE Estoque SET quantidade = %s WHERE id = %s"
        self.db.cursor.execute(query, (quantidade, id))
        self.db.connection.commit()
    
    def pesquisar_id_por_nome(self, nome):
        query = "SELECT id FROM Estoque WHERE nome = %s"
        cursor = self.db.connection.cursor()
        try:
            cursor.execute(query, (nome,))
            result = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        finally:
            cursor.close()
        return result
    
    def pesquisar_nome(self, name):
        query = "SELECT * FROM Estoque WHERE nome = %s"
        self.db.cursor.execute(query, (name,))
        self.db.connection.commit()
        
    def pesquisar_categoria(self, categoria):
        query = "SELECT * FROM Estoque WHERE categoria = %s"
        self.db.cursor.execute(query, (categoria,))
        self.db.connection.commit()
        
    def pesquisar_regiao_origem(self, regiaoOrigem):
        query = "SELECT * FROM Estoque WHERE regiaoOrigem = %s"
        self.db.cursor.execute(query, (regiaoOrigem,))
        self.db.connection.commit()
        
    def pesquisar_disponibilidade(self, disponibilidade):
        
        query = "SELECT * FROM Estoque WHERE disponibilidade = %s"
        self.db.cursor.execute(query, (disponibilidade,))
        self.db.connection.commit()
        
    def pesquisar_intervalo_preco(self, preco_min, preco_max):
        query = "SELECT * FROM Estoque WHERE preco >= %s AND preco <= %s"
        self.db.cursor.execute(query, (preco_min, preco_max))
        self.db.connection.commit()
        
    def pesquisar_intervalo_quantidade(self, quantidade_min, quantidade_max):
        query = "SELECT * FROM Estoque WHERE quantidade >= %s AND quantidade <= %s"
        self.db.cursor.execute(query, (quantidade_min, quantidade_max))
        self.db.connection.commit()
        
    def pesquisar_por_nao_disponibilidade(self):
        
        query = "SELECT * FROM Estoque WHERE disponibilidade = False"
        self.db.cursor.execute(query)
        self.db.connection.commit()

    def listar_todos(self):
        query = "SELECT * FROM Estoque"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def criar_view_nordeste_preco_abaixo_50(self):
        query = """
        CREATE VIEW Nordeste_Preco_Abaixo_50 AS
        SELECT * FROM Estoque
        WHERE regiaoOrigem = 'Nordeste' AND preco < 50
        """
        self.db.cursor.execute(query)
        self.db.connection.commit()
    
    def diminuir_quantidade(self, id, quantidade):
        query = "UPDATE Estoque SET quantidade = quantidade - %s WHERE id = %s"
        self.db.cursor.execute(query, (quantidade, id))
        self.db.connection.commit()

        # Verificar se a quantidade em estoque chegou a 0
        quantidade_atual = self.get_quantidade(id)
        if quantidade_atual == 0:
            # Atualizar o status de disponibilidade para "Indisponível"
            self.atualizar_disponibilidade(id, False)  # Use False para "Indisponível"




class ClienteManager:
    def __init__(self, db):
        self.db = db

    def cliente_existe(self, email_login):
        query = "SELECT COUNT(*) FROM Cliente WHERE email_login = %s"
        self.db.cursor.execute(query, (email_login,))
        count = self.db.cursor.fetchone()[0]
        return count > 0

    def inserir(self, nome, email_login, senha_login, telefone, torceFlamengo, assisteOnePiece, cidade):
        if self.cliente_existe(email_login):
            print("Cliente com este e-mail já existe. Não é possível inserir.")
            return
        query = "INSERT INTO Cliente (nome, email_login, senha_login, telefone, torceFlamengo, assisteOnePiece, cidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.db.cursor.execute(query, (nome, email_login, senha_login, telefone, torceFlamengo, assisteOnePiece, cidade))
        self.db.connection.commit()
        print("Cliente inserido com sucesso.")

    def remover(self, id):
        query = "DELETE FROM Cliente WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        self.db.connection.commit()

    def atualizar_nome(self, id, nome):
        query = "UPDATE Cliente SET nome = %s WHERE id = %s"
        self.db.cursor.execute(query, (nome, id))
        self.db.connection.commit()

    def atualizar_email_login(self, id, email_login):
        query = "UPDATE Cliente SET email_login = %s WHERE id = %s"
        self.db.cursor.execute(query, (email_login, id))
        self.db.connection.commit()

    def atualizar_senha_login(self, id, senha_login):
        query = "UPDATE Cliente SET senha_login = %s WHERE id = %s"
        self.db.cursor.execute(query, (senha_login, id))
        self.db.connection.commit()

    def atualizar_telefone(self, id, telefone):
        query = "UPDATE Cliente SET telefone = %s WHERE id = %s"
        self.db.cursor.execute(query, (telefone, id))
        self.db.connection.commit()

    def atualizar_torce_flamengo(self, id, torceFlamengo):
        query = "UPDATE Cliente SET torceFlamengo = %s WHERE id = %s"
        self.db.cursor.execute(query, (torceFlamengo, id))
        self.db.connection.commit()

    def atualizar_assiste_one_piece(self, id, assisteOnePiece):
        query = "UPDATE Cliente SET assisteOnePiece = %s WHERE id = %s"
        self.db.cursor.execute(query, (assisteOnePiece, id))
        self.db.connection.commit()

    def atualizar_cidade(self, id, cidade):
        query = "UPDATE Cliente SET cidade = %s WHERE id = %s"
        self.db.cursor.execute(query, (cidade, id))
        self.db.connection.commit()
    
    def pesquisar_por_id(self, id):
        query = "SELECT * FROM Cliente WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        return self.db.cursor.fetchall()
        
    def pesquisar_por_nome(self, nome):
        query = "SELECT * FROM Cliente WHERE nome = %s"
        self.db.cursor.execute(query, (nome,))
        return self.db.cursor.fetchall()
    
    def pesquisar_por_email_login(self, email_login):
        query = "SELECT * FROM Cliente WHERE email_login = %s"
        self.db.cursor.execute(query, (email_login,))
        return self.db.cursor.fetchall()
    
    def Verificar_login(self, email_login, senha_login):
        query = "SELECT id FROM Cliente WHERE email_login = %s AND senha_login = %s"
        self.db.cursor.execute(query, (email_login, senha_login))
        result = self.db.cursor.fetchone()  # Obtém apenas a primeira linha do resultado
        if result:
            return result[0]  # Retorna o ID do cliente se a consulta retornar algum resultado
        else:
            return None  # Retorna None se não houver correspondência para as credenciais fornecidas

    
    def obter_cliente_por_id(self, id):
        query = "SELECT * FROM Cliente WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        result = self.db.cursor.fetchone()
        if result:
            # Converte a lista para um dicionário para facilitar o acesso aos dados
            cliente = {
                "id": result[0],
                "nome": result[1],
                "email": result[2],
                "senha": result[3],
                "telefone": result[4],
                "torce_flamengo": result[5],
                "assiste_one_piece": result[6],
                "cidade": result[7]
            }
            return cliente
        else:
            return None
        
    def cliente_torce_para_flamengo(self, cliente_id):
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente:
            return cliente["torce_flamengo"]
        else:
            return False

    def cliente_assiste_one_piece(self, cliente_id):
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente:
            return cliente["assiste_one_piece"]
        else:
            return False

    def cliente_eh_de_sousa(self, cliente_id):
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente:
            return cliente["cidade"].lower() == "sousa"
        else:
            return False
        
        
    def listar_todos(self):
        query = "SELECT * FROM Cliente"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()
    


    def criar_view_sousa_onepiece_flamengo(self):
        query = """
        CREATE VIEW Sousa_OnePiece_Flamengo AS
        SELECT * FROM Cliente
        WHERE cidade = 'Sousa' AND assisteOnePiece = True AND torceFlamengo = True
        """
        self.db.cursor.execute(query)
        self.db.connection.commit()

class VendaManager:
    def __init__(self, db):
        self.db = db

    def inserir(self, id_cliente, data_venda, forma_pagamento, status_pagamento):
        query = "INSERT INTO Venda (id_cliente, data_venda, forma_pagamento, status_pagamento) VALUES (%s, %s, %s, %s)"
        self.db.cursor.execute(query, (id_cliente, data_venda, forma_pagamento, status_pagamento))
        self.db.connection.commit()
        return self.db.cursor.lastrowid  # Retorna o ID da última linha inserida



    def atualizar_forma_pagamento(self, id_venda, forma_pagamento):
        query = "UPDATE Venda SET forma_pagamento = %s WHERE id = %s"
        self.db.cursor.execute(query, (forma_pagamento, id_venda))
        self.db.connection.commit()

    def atualizar_status_pagamento(self, id_venda, status_pagamento):
        query = "UPDATE Venda SET status_pagamento = %s WHERE id = %s"
        self.db.cursor.execute(query, (status_pagamento, id_venda))
        self.db.connection.commit()

    def atualizar_id_cliente(self, id, id_cliente):
        query = "UPDATE Venda SET id_cliente = %s WHERE id = %s"
        self.db.cursor.execute(query, (id_cliente, id))
        self.db.connection.commit()

    def atualizar_data_venda(self, id, data_venda):
        query = "UPDATE Venda SET data_venda = %s WHERE id = %s"
        self.db.cursor.execute(query, (data_venda, id))
        self.db.connection.commit()



    def criar_view_produtos_mais_comprados(self):
        query = """
        CREATE VIEW IF NOT EXISTS ProdutosMaisComprados AS
        SELECT id_produto, SUM(quantidade) AS total_vendido FROM ItemVenda
        GROUP BY id_produto
        ORDER BY total_vendido DESC
        
        """
        self.db.cursor.execute(query)
        self.db.connection.commit()

    def listar_todas(self):
        query = "SELECT * FROM Venda"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()
    
    def pesquisar_produtos_comprados_entre_datas(self, data_inicial, data_final):
        query = """
        SELECT ItemVenda.id_produto, SUM(ItemVenda.quantidade) AS total_vendido
        FROM ItemVenda INNER JOIN Venda ON ItemVenda.id_venda = Venda.id
        WHERE Venda.data_venda BETWEEN %s AND %s
        GROUP BY ItemVenda.id_produto
        ORDER BY total_vendido DESC
        """
        self.db.cursor.execute(query, (data_inicial, data_final))
        return self.db.cursor.fetchall()
    
    def listar_vendas_por_cliente(self, id_cliente):
        query = "SELECT * FROM Venda WHERE id_cliente = %s"
        self.db.cursor.execute(query, (id_cliente,))
        return self.db.cursor.fetchall()
    
    def contagem_vendas_por_tipo_pagamento(self):
        query = "SELECT forma_pagamento, COUNT(*) FROM Venda GROUP BY forma_pagamento"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()
    

class ItemVendaManager:
    def __init__(self, db):
        self.db = db

    def inserir(self, id_venda, id_produto, quantidade):
        # Verificar se há quantidade suficiente no estoque
        estoque_manager = EstoqueManager(self.db)
        quantidade_atual = estoque_manager.get_quantidade(id_produto)
        if quantidade_atual < quantidade:
            print("Quantidade insuficiente no estoque.")
            return

        query = "INSERT INTO ItemVenda (id_venda, id_produto, quantidade) VALUES (%s, %s, %s)"
        self.db.cursor.execute(query, (id_venda, id_produto, quantidade))
        self.db.connection.commit()

        # Diminuir a quantidade do produto no estoque
        estoque_manager.diminuir_quantidade(id_produto, quantidade)

    def get_nome_produto(self, id_produto):
        query = "SELECT nome FROM Estoque WHERE id = %s"
        self.db.cursor.execute(query, (id_produto,))
        return self.db.cursor.fetchone()[0]

    def remover(self, id):
        query = "DELETE FROM ItemVenda WHERE id = %s"
        self.db.cursor.execute(query, (id,))
        self.db.connection.commit()

    def atualizar_id_venda(self, id, id_venda):
        query = "UPDATE ItemVenda SET id_venda = %s WHERE id = %s"
        self.db.cursor.execute(query, (id_venda, id))
        self.db.connection.commit()

    def atualizar_id_produto(self, id, id_produto):
        query = "UPDATE ItemVenda SET id_produto = %s WHERE id = %s"
        self.db.cursor.execute(query, (id_produto, id))
        self.db.connection.commit()

    def atualizar_quantidade(self, id, quantidade):
        query = "UPDATE ItemVenda SET quantidade = %s WHERE id = %s"
        self.db.cursor.execute(query, (quantidade, id))
        self.db.connection.commit()
    
    def listar_itens_por_venda(self, id_venda):
        query = "SELECT * FROM ItemVenda WHERE id_venda = %s"
        self.db.cursor.execute(query, (id_venda,))
        return self.db.cursor.fetchall()
        
        
        
        
def main():
    host = "localhost"
    user = "root"
    password = "010203"
    database = "comidas_tipicas"
    
    # Conectar ao banco de dados
    db = Database(host, user, password, database)
    db.create_tables()
    print("Tabelas criadas com sucesso!")
    
    # Criar objetos dos gerenciadores de cada entidade
    estoque_manager = EstoqueManager(db)
    venda_manager = VendaManager(db)
    cliente_manager = ClienteManager(db)  # Adicionado o gerenciador de clientes
    item_venda_manager = ItemVendaManager(db)  # Adicionado o gerenciador de itens de venda
    print("Objetos dos gerenciadores criados com sucesso!")

    # Lista de alimentos para inserir no estoque
    alimentos = [
        ("Cuscuz", "Cuscuz nordestino", Decimal('3.0'), "Grãos", "Nordeste", True, 80),
        ("Tapioca", "Tapioca com coco", Decimal('4.0'), "Grãos", "Nordeste", True, 50),
        ("Carne de Sol", "Carne de sol com mandioca", Decimal('25.0'), "Pratos Quentes", "Nordeste", True, 60),
        ("Feijoada", "Prato típico brasileiro", Decimal('30.0'), "Pratos Quentes", "Sudeste", True, 120),
        ("Acarajé", "Bolinho de feijão fradinho", Decimal('7.0'), "Petiscos", "Nordeste", True, 50),
        ("Escondidinho", "Prato de carne com purê de mandioca", Decimal('18.0'), "Pratos Quentes", "Nordeste", True, 80),
        ("Coxinha", "Salgado de frango", Decimal('3.5'), "Petiscos", "Sudeste", True, 100),
        ("Buchada de bode", "Prato típico do Nordeste", Decimal('35.0'), "Pratos Quentes", "Nordeste", True, 30),
        ("Mungunzá", "Canjica salgada", Decimal('9.0'), "Pratos Quentes", "Nordeste", True, 40),
        ("Baião de dois", "Prato típico do Nordeste", Decimal('18.0'), "Pratos Quentes", "Nordeste", True, 60),
        ("Tutu de feijão", "Feijão cozido com farinha de mandioca", Decimal('10.0'), "Pratos Quentes", "Sudeste", True, 80),
        ("Pão de queijo", "Pão de queijo mineiro", Decimal('3.0'), "Petiscos", "Sudeste", True, 120),
        ("Virado à paulista", "Prato típico de São Paulo", Decimal('20.0'), "Pratos Quentes", "Sudeste", True, 60),
        ("Maniçoba", "Prato típico paraense", Decimal('30.0'), "Pratos Quentes", "Norte", True, 40),
        ("Pirão", "Pirão de peixe", Decimal('5.0'), "Acompanhamentos", "Nordeste", True, 90),
    ]

    # Inserir alimentos no estoque
    for alimento in alimentos:
        estoque_manager.inserir(*alimento)
    
    print("Alimentos inseridos com sucesso!")

    # Fechar a conexão com o banco de dados
    db.close_connection()

if __name__ == "__main__":
    main()
