import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Tabela PratoTipico
        
        print("Criando tabelas...")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PratoTipico (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255),
                descricao TEXT,
                preco FLOAT,
                categoria VARCHAR(50),
                regiaoOrigem VARCHAR(100),
                disponibilidade BOOLEAN,
                quantidade INT DEFAULT 0  # Adicionando a coluna quantidade
            )
        """)

       
        print("Tabelas prato típico criada com sucesso!")
        # Tabela Cliente
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cliente (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255),
                email VARCHAR(255),
                telefone VARCHAR(20),
                torceFlamengo TINYINT(1),
                assisteOnePiece TINYINT(1),
                cidade VARCHAR(100)
            )
        """)
        print("Tabela cliente criada com sucesso!")

        
        # Tabela Venda
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_id INT,
                formaPagamento VARCHAR(50),
                statusPagamento VARCHAR(50),
                data DATE,
                FOREIGN KEY (cliente_id) REFERENCES Cliente(id)
            )
        """)
        print("Tabela venda criada com sucesso!")
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ItemVenda (
            id INT AUTO_INCREMENT PRIMARY KEY,
            venda_id INT,
            pratoTipico_id INT,
            quantidade INT,
            valorUnitario FLOAT,
            FOREIGN KEY (venda_id) REFERENCES Venda(id),
            FOREIGN KEY (pratoTipico_id) REFERENCES PratoTipico(id)
                )
            """)
        print("Tabela ItemVenda criada com sucesso!")

    def adicionar_stored_procedure(self):
        try:
            # Definição da stored procedure
            self.cursor.execute("""
                CREATE PROCEDURE IF NOT EXISTS Atualizar_Disponibilidade (IN prato_id INT, IN nova_quantidade INT)
                BEGIN
                    UPDATE PratoTipico SET disponibilidade = (nova_quantidade > 0) WHERE id = prato_id;
                END
            """)
            self.conn.commit()
            print("Stored procedure adicionada com sucesso.")
        except Exception as e:
            print("Erro ao adicionar a stored procedure:", e)

    def remover_stored_procedure(self):
        try:
            # Remoção da stored procedure
            self.cursor.execute("DROP PROCEDURE IF EXISTS Atualizar_Disponibilidade")
            self.conn.commit()
            print("Stored procedure removida com sucesso.")
        except Exception as e:
            print("Erro ao remover a stored procedure:", e)
    
    def create_view(self,db):
        try:
            self.cursor.execute("""
                CREATE VIEW IF NOT EXISTS PratosDisponiveis AS
                SELECT * FROM PratoTipico WHERE disponibilidade = 1
            """)
            self.conn.commit()
            print("View criada com sucesso.")
        except Exception as e:
            print("Erro ao criar a view:", e)
    
    def close_connection(self):
        self.conn.close()

class PratoTipico:
    def __init__(self, db, nome, descricao, preco, categoria, regiaoOrigem, disponibilidade=False, quantidade=0):
        self.db = db
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.regiaoOrigem = regiaoOrigem
        self.disponibilidade = disponibilidade
        self.quantidade = quantidade
        print("Prato típico criado com sucesso!")
        



    def inserir(self):
        try:
            print("Inserindo prato típico...")
            query = "INSERT INTO PratoTipico (nome, descricao, preco, categoria, regiaoOrigem, disponibilidade, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (self.nome, self.descricao, self.preco, self.categoria, self.regiaoOrigem, self.disponibilidade, self.quantidade)
            self.db.cursor.execute(query, values)
            self.db.conn.commit()
            print("Prato típico inserido com sucesso!")
        except Exception as e:
            print("Erro ao inserir prato típico:", e)


    @staticmethod
    def pesquisar_por_nome(db, nome):
        try:
            query = "SELECT * FROM PratoTipico WHERE nome = %s"
            db.cursor.execute(query, (nome,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    def pesquisar_por_categoria(db, categoria):
        try:
            query = "SELECT * FROM PratoTipico WHERE categoria = %s"
            db.cursor.execute(query, (categoria,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
    
    def pesquisar_por_regiaoOrigem(db, regiaoOrigem):
        try:
            query = "SELECT * FROM PratoTipico WHERE regiaoOrigem = %s"
            db.cursor.execute(query, (regiaoOrigem,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    def pesquisar_por_preco(db, preco):
        try:
            query = "SELECT * FROM PratoTipico WHERE preco = %s"
            db.cursor.execute(query, (preco,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
       
    def pesquisar_por_categoria_regiaoOrigem(db, categoria, regiaoOrigem):
        try:
            query = "SELECT * FROM PratoTipico WHERE categoria = %s AND regiaoOrigem = %s"
            db.cursor.execute(query, (categoria, regiaoOrigem))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
    
    def pesquisar_por_preco_intervalo(db, preco1, preco2):
        try:
            query = "SELECT * FROM PratoTipico WHERE preco >= %s AND preco <= %s"
            db.cursor.execute(query, (preco1, preco2))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    def pesquisar_produtos_qtd_menor_que_5(db):
        try:
            query = "SELECT * FROM PratoTipico WHERE quantidade < 5"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def atualizar_nome(db, id, nome):
        try:
            query = "UPDATE PratoTipico SET nome = %s WHERE id = %s"
            db.cursor.execute(query, (nome, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None 
        
    def atualizar_descricao(db, id, descricao):
        try:
            query = "UPDATE PratoTipico SET descricao = %s WHERE id = %s"
            db.cursor.execute(query, (descricao, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None
        
    def atualizar_preco(db, id, preco):
        try:
            query = "UPDATE PratoTipico SET preco = %s WHERE id = %s"
            db.cursor.execute(query, (preco, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None
        
    def atualizar_categoria(db, id, categoria):
        try:
            query = "UPDATE PratoTipico SET categoria = %s WHERE id = %s"
            db.cursor.execute(query, (categoria, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None
                
    def atualizar_regiaoOrigem(db, id, regiaoOrigem):
        try:
            query = "UPDATE PratoTipico SET regiaoOrigem = %s WHERE id = %s"
            db.cursor.execute(query, (regiaoOrigem, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None
        
    def atualizar_quantidade(db, id, quantidade):
        try:
            query = "UPDATE PratoTipico SET quantidade = %s WHERE id = %s"
            db.cursor.execute(query, (quantidade, id))
            db.conn.commit()
            if quantidade == 0:
                query = "UPDATE PratoTipico SET disponibilidade = 0 WHERE id = %s"
                db.cursor.execute(query, (id,))
                db.conn.commit()
        except Exception as e:
            print(e)
            return None

    def get_tamamnho_table(db):
        try:
            query = "SELECT COUNT(*) FROM PratoTipico"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
    
    def listar_todos(db):
        try:
            print("\nListando todas as comidas típicas...")
            query = "SELECT * FROM PratoTipico"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print("Erro ao listar todas as comidas típicas:", e)
            return None

    def frequencia_regiao(db):
        try:
            query = "SELECT regiaoOrigem, COUNT(*) FROM PratoTipico GROUP BY regiaoOrigem"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def frequencia_categoria(db):
        try:
            query = "SELECT categoria, COUNT(*) FROM PratoTipico GROUP BY categoria"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    def frequencia_preco(db):
        try:
            query = "SELECT preco, COUNT(*) FROM PratoTipico GROUP BY preco"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def remover(db, prato_id):
        try:
            query = "DELETE FROM PratoTipico WHERE id = %s"
            db.cursor.execute(query, (prato_id,))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

class Cliente:
    def __init__(self, db, nome, email, telefone, torceFlamengo, assisteOnePiece, cidade):
        self.db = db
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.torceFlamengo = torceFlamengo
        self.assisteOnePiece = assisteOnePiece
        self.cidade = cidade

    def inserir(self):
        query = "INSERT INTO Cliente (nome, email, telefone, torceFlamengo, assisteOnePiece, cidade) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.nome, self.email, self.telefone, self.torceFlamengo, self.assisteOnePiece, self.cidade)
        self.db.cursor.execute(query, values)
        self.db.conn.commit()

    @staticmethod
    def pesquisar_por_nome(db, nome):
        try:
            query = "SELECT * FROM Cliente WHERE nome = %s"
            db.cursor.execute(query, (nome,))
            return db.cursor.fetchall()
        except Exception as e:  
            print(e)
            return None
        
    @staticmethod
    def pesquisar_por_email(db, email):
        try:
            query = "SELECT * FROM Cliente WHERE email = %s"
            db.cursor.execute(query, (email,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def pesquisar_por_cidade(db, cidade):
        try:
            query = "SELECT * FROM Cliente WHERE cidade = %s"
            db.cursor.execute(query, (cidade,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
    
    def pesquisar_por_torceFlamengo(db, torceFlamengo):
        try:
            query = "SELECT * FROM Cliente WHERE torceFlamengo = %s"
            db.cursor.execute(query, (torceFlamengo,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    def pesquisar_por_assisteOnePiece(db, assisteOnePiece):
        try:
            query = "SELECT * FROM Cliente WHERE assisteOnePiece = %s"
            db.cursor.execute(query, (assisteOnePiece,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    def atualizar_nome(db, id, nome):
        try:
            query = "UPDATE Cliente SET nome = %s WHERE id = %s"
            db.cursor.execute(query, (nome, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None 
        
    def atualizar_email(db, id, email):
        try:
            query = "UPDATE Cliente SET email = %s WHERE id = %s"
            db.cursor.execute(query, (email, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

    def atualizar_telefone(db, id, telefone):
        try:
            query = "UPDATE Cliente SET telefone = %s WHERE id = %s"
            db.cursor.execute(query, (telefone, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

    def atualizar_torceFlamengo(db, id, torceFlamengo):
        try:
            query = "UPDATE Cliente SET torceFlamengo = %s WHERE id = %s"
            db.cursor.execute(query, (torceFlamengo, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

    def atualizar_assisteOnePiece(db, id, assisteOnePiece):
        try:
            query = "UPDATE Cliente SET assisteOnePiece = %s WHERE id = %s"
            db.cursor.execute(query, (assisteOnePiece, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

    def atualizar_cidade(db, id, cidade):
        try:
            query = "UPDATE Cliente SET cidade = %s WHERE id = %s"
            db.cursor.execute(query, (cidade, id))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def listar_todos(db):
        try:
            query = "SELECT * FROM Cliente"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def listar_por_id(db, id):
        try:
            query = "SELECT * FROM Cliente WHERE id = %s"
            db.cursor.execute(query, (id,))
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

        
    @staticmethod
    def remover(db, cliente_id):
        try:
            query = "DELETE FROM Cliente WHERE id = %s"
            db.cursor.execute(query, (cliente_id,))
            db.conn.commit()
        except Exception as e:
            print(e)
            return None

# class Venda:
#     def __init__(self, db, cliente_id, formaPagamento, statusPagamento, data):
#         self.db = db
#         self.cliente_id = cliente_id
#         self.formaPagamento = formaPagamento
#         self.statusPagamento = statusPagamento
#         self.data = data           
            

#     def inserir(self):
#         try:
#             # Insere a venda no banco de dados
#             query = "INSERT INTO Venda (cliente_id, formaPagamento, statusPagamento, data) VALUES (%s, %s, %s, %s)"
#             values = (self.cliente_id, self.formaPagamento, self.statusPagamento, self.data)
#             self.db.cursor.execute(query, values)
#             venda_id = self.db.cursor.lastrowid  # Obtém o ID da venda inserida
#             self.db.conn.commit()

#             # Aplica desconto se o cliente for elegível
#             cliente = Cliente.listar_por_id(self.db, self.cliente_id)
#             if cliente:
#                 cliente = cliente[0]
#                 if cliente[4] or (cliente[5] and cliente[6] == 'Sousa'):  # Ajuste na lógica de comparação
#                     self.aplicar_desconto(venda_id, 0.1)

#             print("Venda registrada com sucesso!")
#         except Exception as e:
#             print("Erro ao registrar a venda:", e)

#     def aplicar_desconto(self, venda_id, desconto):
#         try:
#             # Consulta SQL para obter o total da venda
#             query = """
#                 SELECT SUM(iv.quantidade * pt.preco) AS total
#                 FROM ItemVenda iv
#                 INNER JOIN PratoTipico pt ON iv.pratoTipico_id = pt.id
#                 WHERE iv.venda_id = %s
#             """
#             self.db.cursor.execute(query, (venda_id,))
#             total_venda = self.db.cursor.fetchone()

#             # Verifica se o total da venda é válido antes de aplicar o desconto
#             if total_venda and total_venda[0] is not None:
#                 total_venda = total_venda[0]
#                 valor_desconto = total_venda * desconto
#                 total_com_desconto = total_venda - valor_desconto

#                 # Atualiza o total da venda com o desconto aplicado
#                 query_update = "UPDATE Venda SET total = %s WHERE id = %s"
#                 self.db.cursor.execute(query_update, (total_com_desconto, venda_id))
#                 self.db.conn.commit()

#                 print("Desconto aplicado com sucesso!")
#             else:
#                 print("Erro ao aplicar desconto: total da venda inválido")
#         except Exception as e:
#             print("Erro ao aplicar desconto:", e)

class Venda:
    def __init__(self, db, cliente_id, formaPagamento, statusPagamento, data):
        self.db = db
        self.cliente_id = cliente_id
        self.formaPagamento = formaPagamento
        self.statusPagamento = statusPagamento
        self.data = data           

    def inserir(self):
        try:
            # Insere a venda no banco de dados
            query = "INSERT INTO Venda (cliente_id, formaPagamento, statusPagamento, data) VALUES (%s, %s, %s, %s)"
            values = (self.cliente_id, self.formaPagamento, self.statusPagamento, self.data)
            self.db.cursor.execute(query, values)
            venda_id = self.db.cursor.lastrowid  # Obtém o ID da venda inserida
            self.db.conn.commit()

            # Calcular o valor total da venda
            total_venda = self.calcular_total_venda(venda_id)
            print("Total da venda:", total_venda)
            print("venda_id:", venda_id)

            print("Venda registrada com sucesso!")
        except Exception as e:
            print("Erro ao registrar a venda:", e)

    def calcular_total_venda(self, venda_id):
        try:
            # Consulta SQL para calcular o total da venda
            query = """
                SELECT SUM(iv.quantidade * pt.preco) AS total
                FROM ItemVenda iv
                INNER JOIN PratoTipico pt ON iv.pratoTipico_id = pt.id
                WHERE iv.venda_id = %s
            """
            self.db.cursor.execute(query, (venda_id,))
            total_venda = self.db.cursor.fetchone()

            # Retorna o total da venda se encontrado
            if total_venda and total_venda[0] is not None:
                return total_venda[0]
            else:
                return 0
        except Exception as e:
            print("Erro ao calcular o total da venda:", e)
            return 0






class ItemVenda:
    
    def __init__(self, db, venda_id, pratoTipico_id, quantidade, valorUnitario):
        self.db = db
        self.venda_id = venda_id
        self.pratoTipico_id = pratoTipico_id
        self.quantidade = quantidade
        self.valorUnitario = valorUnitario

    def inserir(self):
        try:
            # Verifica se o produto está disponível
            if self.verificar_disponibilidade():
                # Insere o item de venda no banco de dados
                query = "INSERT INTO ItemVenda (venda_id, pratoTipico_id, quantidade, valorUnitario) VALUES (%s, %s, %s, %s)"
                values = (self.venda_id, self.pratoTipico_id, self.quantidade, self.valorUnitario)
                self.db.cursor.execute(query, values)
                self.db.conn.commit()
                print("Item de venda registrado com sucesso!")
            else:
                print("O produto não está disponível no estoque. Item de venda não registrado.")
        except Exception as e:
            print("Erro ao registrar o item de venda:", e)

    def verificar_disponibilidade(self):
        try:
            # Verifica se o produto associado ao item de venda está disponível no estoque
            query = "SELECT disponibilidade FROM PratoTipico WHERE id = %s"
            self.db.cursor.execute(query, (self.pratoTipico_id,))
            disponibilidade = self.db.cursor.fetchone()
            if disponibilidade and disponibilidade[0]:  # Verifica se a disponibilidade é True
                return True
            else:
                return False
        except Exception as e:
            print("Erro ao verificar disponibilidade do produto:", e)
            return False


    @staticmethod
    def listar_todos(db):
        try:
            query = "SELECT * FROM ItemVenda"
            db.cursor.execute(query)
            return db.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def remover(db, item_id):
        query = "DELETE FROM ItemVenda WHERE id = %s"
        db.cursor.execute(query, (item_id,))
        db.conn.commit()

def main():
    host = "localhost"
    user = "root"
    password = "jasbhisto"
    database = "food_db"
    
    # Conectar ao banco de dados
    db = Database(host, user, password, database)

    print("Conectado ao banco de dados!")
    # Criar as tabelas
    db.create_tables()

    # Adicionar a stored procedure
    db.adicionar_stored_procedure()
    
    print("Inserindo dados...")
    # Inserir os pratos típicos
    prato1 = PratoTipico(db, "Feijoada", 'Prato tipico brasileiro', 50.00, 'Principal', 'Sudeste', True, 10)
    prato1.inserir()
    prato2 = PratoTipico(db, "Churrasco", 'Prato tipico brasileiro', 40.00, 'Principal', 'Sul', True, 20)
    prato2.inserir()
    prato3 = PratoTipico(db, "Acarajé", 'Prato típico baiano', 20.00, 'Principal', 'Nordeste', True, 15)
    prato3.inserir()
    
    print("\ninserindo cliente...")
    # Criar um cliente
    cliente1 = Cliente(db, "João", "joao@email.com", "123456789", True, False, "Rio de Janeiro")
    cliente1.inserir()
    print("\nAdicionando ao carrinho...")
    # Realizar uma compra de 2 produtos
    
    print("\nListando todos os clientes:")
    clientes = Cliente.listar_todos(db)
    print(clientes)

    # Selecionando o ID do primeiro cliente da lista (índice 0)
    cliente_id = clientes[0][0]

    print("\nCliente selecionado:")
    print(cliente_id)

    # Criando a data no formato correto
    data = datetime.strptime("2024-04-29", "%Y-%m-%d")

    # Criando a venda com o ID do cliente selecionado e a data correta
    venda = Venda(db, cliente_id, "Cartão de Crédito", "Pago", data)
    venda.inserir()



    # # Listar todos os itens de venda após a compra
    # print("\nListando todos os itens de venda após a compra:")
    # itens = ItemVenda.listar_todos(db)
    
    # for item in itens:
    #     print(item)

    # Fechar conexão com o banco de dados
    db.close_connection()

if __name__ == "__main__":
    main()
