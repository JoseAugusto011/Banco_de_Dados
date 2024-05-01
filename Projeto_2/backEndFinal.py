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
        
    def pesquisar_por_nome(self, nome):
        query = "SELECT * FROM Cliente WHERE nome = %s"
        self.db.cursor.execute(query, (nome,))
        return self.db.cursor.fetchall()
    
    def pesquisar_por_email_login(self, email_login):
        query = "SELECT * FROM Cliente WHERE email_login = %s"
        self.db.cursor.execute(query, (email_login,))
        return self.db.cursor.fetchall()
    
    def Verificar_login(self, email_login, senha_login):
        
        query = "SELECT * FROM Cliente WHERE email_login = %s AND senha_login = %s"
        self.db.cursor.execute(query, (email_login, senha_login))
        return self.db.cursor.fetchall()
    
    
        
        
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

    def calcular_valor_total_venda(self, id_venda):
        query = "SELECT SUM(ItemVenda.quantidade * Estoque.preco) FROM ItemVenda INNER JOIN Estoque ON ItemVenda.id_produto = Estoque.id WHERE id_venda = %s"

        self.db.cursor.execute(query, (id_venda,))
        result = self.db.cursor.fetchone()[0]
        return result if result is not None else 0

    def aplicar_desconto(self, id_cliente, valor_total):
        query = "SELECT torceFlamengo, assisteOnePiece, cidade FROM Cliente WHERE id = %s"
        self.db.cursor.execute(query, (id_cliente,))
        cliente_info = self.db.cursor.fetchone()
        desconto = Decimal('0')
        if cliente_info[0] or cliente_info[1] or cliente_info[2] == 'Sousa':
            # Convertendo o valor total para Decimal antes de aplicar o desconto
            valor_total_decimal = Decimal(str(valor_total))
            # Desconto de 10% para clientes que torcem pelo Flamengo, assistem One Piece ou são de Sousa
            desconto = valor_total_decimal * Decimal('0.1')  
        # Arredonda o desconto para duas casas decimais e retorna o valor total com desconto
        return (valor_total_decimal - desconto).quantize(Decimal('0.01'))


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
        query = "INSERT INTO ItemVenda (id_venda, id_produto, quantidade) VALUES (%s, %s, %s)"
        self.db.cursor.execute(query, (id_venda, id_produto, quantidade))
        self.db.connection.commit()

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
    print("Objetos dos gerenciadores criados com sucesso!")

    # Lista de alimentos para inserir no estoque
    alimentos = [
        ("Feijão", "Feijão carioquinha", Decimal('5.0'), "Grãos", "Sudeste", True, 100),
        ("Arroz", "Arroz branco", Decimal('10.0'), "Grãos", "Sudeste", True, 150),
        ("Cuscuz", "Cuscuz nordestino", Decimal('3.0'), "Grãos", "Nordeste", True, 80),
        ("Paçoca", "Doce de amendoim", Decimal('2.5'), "Doces", "Nordeste", False, 0),
        ("Tapioca", "Tapioca com coco", Decimal('4.0'), "Grãos", "Nordeste", True, 50),
        ("Vatapá", "Prato típico da Bahia", Decimal('15.0'), "Pratos Quentes", "Nordeste", True, 30),
        ("Moqueca", "Moqueca de peixe", Decimal('20.0'), "Pratos Quentes", "Nordeste", True, 40),
        ("Carne de Sol", "Carne de sol com mandioca", Decimal('25.0'), "Pratos Quentes", "Nordeste", True, 60),
        ("Canjica", "Doce de milho", Decimal('8.0'), "Doces", "Sudeste", True, 70),
        ("Pamonha", "Pamonha recheada", Decimal('6.0'), "Doces", "Sudeste", True, 90),
        ("Feijoada", "Prato típico brasileiro", Decimal('30.0'), "Pratos Quentes", "Sudeste", True, 120),
        ("Acarajé", "Bolinho de feijão fradinho", Decimal('7.0'), "Petiscos", "Nordeste", True, 50),
        ("Bolo de rolo", "Bolo de rolo de goiabada", Decimal('12.0'), "Doces", "Nordeste", True, 40),
        ("Escondidinho", "Prato de carne com purê de mandioca", Decimal('18.0'), "Pratos Quentes", "Nordeste", True, 80),
        ("Coxinha", "Salgado de frango", Decimal('3.5'), "Petiscos", "Sudeste", True, 100),
        ("Quindim", "Doce de coco e gemas", Decimal('5.5'), "Doces", "Sudeste", True, 60),
        ("Buchada de bode", "Prato típico do Nordeste", Decimal('35.0'), "Pratos Quentes", "Nordeste", True, 30),
        ("Farofa", "Farofa de dendê", Decimal('6.0'), "Acompanhamentos", "Nordeste", True, 70),
        ("Mungunzá", "Canjica salgada", Decimal('9.0'), "Pratos Quentes", "Nordeste", True, 40),
        ("Tacacá", "Prato típico da região Norte", Decimal('12.0'), "Pratos Quentes", "Norte", True, 50),
        ("Xinxim de galinha", "Prato típico da Bahia", Decimal('22.0'), "Pratos Quentes", "Nordeste", True, 30),
        ("Baião de dois", "Prato típico do Nordeste", Decimal('18.0'), "Pratos Quentes", "Nordeste", True, 60),
        ("Torta capixaba", "Prato típico do Espírito Santo", Decimal('25.0'), "Pratos Quentes", "Sudeste", True, 40),
        ("Tutu de feijão", "Feijão cozido com farinha de mandioca", Decimal('10.0'), "Pratos Quentes", "Sudeste", True, 80),
        ("Pão de queijo", "Pão de queijo mineiro", Decimal('3.0'), "Petiscos", "Sudeste", True, 120),
        ("Cuscuz paulista", "Prato típico de São Paulo", Decimal('15.0'), "Pratos Quentes", "Sudeste", True, 50),
        ("Virado à paulista", "Prato típico de São Paulo", Decimal('20.0'), "Pratos Quentes", "Sudeste", True, 60),
        ("Sorvete de tapioca", "Sorvete de tapioca com coco", Decimal('7.0'), "Sobremesas", "Nordeste", True, 100),
        ("Cajuzinho", "Doce de amendoim em formato de caju", Decimal('4.0'), "Doces", "Nordeste", True, 80),
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