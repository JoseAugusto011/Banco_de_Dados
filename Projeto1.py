import mysql.connector


class DatabaseFactory:
    def __init__(self, host, user, password, database):
        self.db_connection = None # Conecta ao banco de dados MySQL
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def create_database_connection(self):
        try:
            self.db_connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            print("Conexão com o banco de dados estabelecida.")
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados:", err)


class FoodDatabase:
    def __init__(self, db_connection):
        self.mydb = db_connection
        self.mycursor = self.mydb.cursor()
        self.TableAlreadyExists = False
        
    def create_table(self):
        if self.TableAlreadyExists:
            print("\nFalha ao Criar - Tabela já existe")
            return
        else:
            try:
                table = """CREATE TABLE food_table (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            flavor VARCHAR(255),
                            price FLOAT,
                            food_type VARCHAR(255),
                            origin_region VARCHAR(255),
                            availability BOOLEAN,
                            image_url VARCHAR(255)
                        )"""
                self.mycursor.execute(table)
                self.TableAlreadyExists = True 
                print("Tabela criada com sucesso.")
            except mysql.connector.Error as err:
                print("Erro ao criar tabela:", err)
                
    def get_connection_id(self):
        # Retorna o id da conexão
        print("\nConection Id:", self.mydb.connection_id)

    def insert_food(self, name, flavor, price, food_type, origin_region, availability, image_url):
        try:
            sql = """INSERT INTO food_table 
                    (name, flavor, price, food_type, origin_region, availability, image_url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            val = (name, flavor, price, food_type, origin_region, availability, image_url)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(self.mycursor.rowcount, "registro inserido.")
        except mysql.connector.Error as err:
            print("Erro ao inserir comida:", err)

    def delete_food(self, food_id):
        try:
            self.mycursor.execute("DELETE FROM food_table WHERE id = %s", (food_id,))
            self.mydb.commit()
            print("Comida com ID", food_id, "excluída com sucesso.")
            print(self.mycursor.rowcount, "registro(s) excluído(s).")
        except mysql.connector.Error as err:
            print("Erro ao excluir comida:", err)

    def update_food(self, food_id, name, flavor, price, food_type, origin_region, availability, image_url):
        try:
            sql = """UPDATE food_table 
                     SET name = %s, flavor = %s, price = %s, food_type = %s, origin_region = %s, availability = %s, image_url = %s 
                     WHERE id = %s"""
            val = (name, flavor, price, food_type, origin_region, availability, image_url, food_id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(self.mycursor.rowcount, "registro(s) atualizado(s).")
        except mysql.connector.Error as err:
            print("Erro ao atualizar comida:", err)

    def search_food(self, food_id):
        try:
            self.mycursor.execute("SELECT * FROM food_table WHERE id = %s", (food_id,))
            if self.mycursor.rowcount == 0:
                print("Nenhum registro encontrado - ID não existe")
            else:
                myresult = self.mycursor.fetchall()
                for x in myresult:
                    print("Comida encontrada:\n")
                    print("ID:", x[0])
                    print("Nome:", x[1])
                    print("Sabor:", x[2])
                    print("Preço:", x[3])
                    print("Tipo de comida:", x[4])
                    print("Região de origem:", x[5])
                    print("Disponibilidade:", "Disponível" if x[6] else "Indisponível")
                    print("URL da imagem:", x[7], "\n")
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)

    def show_table(self):
        if not self.TableAlreadyExists:
            print("\nFalha ao Mostrar - Tabela não existe")
            return
        else:
            try:
                self.mycursor.execute("SELECT * FROM food_table")
                print("Registros encontrados:\n")
                myresult = self.mycursor.fetchall()
                if len(myresult) == 0:
                    print("Nenhum registro retornado")
                else:
                    
                    print("ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                    for x in myresult:
                        print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|", x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])

                    
                    # for x in myresult:
                    #     print("ID:", x[0])
                    #     print("Nome:", x[1])
                    #     print("Sabor:", x[2])
                    #     print("Preço:", x[3])
                    #     print("Tipo de comida:", x[4])
                    #     print("Região de origem:", x[5])
                    #     print("Disponibilidade:", "Disponível" if x[6] else "Indisponível")
                    #     print("URL da imagem:", x[7], "\n")
            except mysql.connector.Error as err:
                print("Erro ao mostrar tabela:", err)

    def clear_table(self):
        if not self.TableAlreadyExists:
            print("\nFalha ao Limpar - Tabela não existe")
            return
        else:
            try:
                self.mycursor.execute("DELETE FROM food_table")
                print("Tabela limpa com sucesso.")
            except mysql.connector.Error as err:
                print("Erro ao limpar tabela:", err)

    def delete_table(self):
        if not self.TableAlreadyExists:
            print("\nFalha ao Excluir - Tabela não existe")
            return
        else:
            try:
                self.mycursor.execute("DROP TABLE IF EXISTS food_table")
                self.TableAlreadyExists = False
                print("Tabela excluída com sucesso.")
            except mysql.connector.Error as err:
                print("Erro ao excluir tabela:", err)

    def close_connection(self):
        try:
            if self.mycursor:
                self.mycursor.close()
            if self.mydb:
                self.mydb.close()
            print("Conexão fechada com sucesso.")
        except mysql.connector.Error as err:
            print("Erro ao fechar conexão:", err)

def Menu(food_db):
    opcao = -1
    
    while opcao != 0:
        print("\n1 - Inserir comida")
        print("2 - Excluir comida")
        print("3 - Atualizar comida")
        print("4 - Buscar comida")
        print("5 - Mostrar tabela")
        print("6 - Limpar tabela")
        print("7 - Apagar tabela")
        print("0 - Sair")
        
        opcao = int(input("\nDigite a opção desejada: "))
        
        if opcao == 1:
            dadosComida = []
            print("\nInsira os dados da comida\n")
            print("Insira o nome da comida:")
            dadosComida.append(input())
            print("Insira o sabor da comida:")
            dadosComida.append(input())
            print("Insira o preço da comida:")
            dadosComida.append(float(input()))
            print("Insira o tipo da comida:")
            dadosComida.append(input())
            print("Insira a região de origem da comida:")
            dadosComida.append(input())
            print("Insira a disponibilidade da comida (1 para disponível, 0 para indisponível):")
            dadosComida.append(bool(int(input())))
            print("Insira a URL da imagem da comida:")
            dadosComida.append(input())
            print("\n") 
            
            food_db.insert_food(dadosComida[0], dadosComida[1], dadosComida[2], dadosComida[3], dadosComida[4], dadosComida[5], dadosComida[6])
                     
        elif opcao == 2:
            print("\nInsira o ID da comida que deseja excluir:")
            comida_id = int(input())
            food_db.delete_food(comida_id)
        
        elif opcao == 3:
            print("\nInsira o ID da comida que deseja atualizar:")
            comida_id = int(input())
            dadosComida = food_db.search_food(comida_id)
            
            if dadosComida:
                print("Comida encontrada. Insira as alterações desejadas:")
                print("Deseja alterar o nome da comida? (s/n):")
                
                if input() == "s":
                    novo_nome = input("Insira o novo nome da comida: ")
                else:
                    novo_nome = dadosComida[1]
                
                print("Deseja alterar o sabor da comida? (s/n):")
                if input() == "s":
                    novo_sabor = input("Insira o novo sabor da comida: ")
                else:
                    novo_sabor = dadosComida[2]
                
                print("Deseja alterar o preço da comida? (s/n):")
                if input() == "s":
                    novo_preco = float(input("Insira o novo preço da comida: "))
                else:
                    novo_preco = dadosComida[3]
                
                print("Deseja alterar o tipo da comida? (s/n):")
                if input() == "s":
                    novo_tipo = input("Insira o novo tipo da comida: ")
                else:
                    novo_tipo = dadosComida[4]
                
                print("Deseja alterar a região de origem da comida? (s/n):")
                if input() == "s":
                    nova_regiao = input("Insira a nova região de origem da comida: ")
                else:
                    nova_regiao = dadosComida[5]
                
                print("Deseja alterar a disponibilidade da comida? (s/n):")
                if input() == "s":
                    nova_disponibilidade = bool(int(input("Insira a nova disponibilidade da comida (1 para disponível, 0 para indisponível): ")))
                else:
                    nova_disponibilidade = dadosComida[6]
                
                print("Deseja alterar a URL da imagem da comida? (s/n):")
                if input() == "s":
                    nova_url_imagem = input("Insira a nova URL da imagem da comida: ")
                else:
                    nova_url_imagem = dadosComida[7]
                
                food_db.update_food(comida_id, novo_nome, novo_sabor, novo_preco, novo_tipo, nova_regiao, nova_disponibilidade, nova_url_imagem)
            else:
                print("Comida não encontrada.")
            
        
        elif opcao == 4:
            print("\nInsira o ID da comida que deseja buscar:")
            comida_id = int(input())
            food_db.search_food(comida_id)
            
        elif opcao == 5:
            food_db.show_table()
            
        elif opcao == 7:
            if input("Deseja realmente deletar a tabela? (s/n):") == "s":
                food_db.delete_table() 
                print("Tabela deletada com sucesso")
             
        elif opcao == 6:
            if input("Deseja realmente limpar a tabela? (s/n):") == "s":
                food_db.clear_table() 
                print("Tabela limpa com sucesso")
            
        elif opcao == 0:
            print("Saindo...") 
            food_db.clear_table()
            food_db.delete_table()       
            food_db.close_connection()
           
        else:
            print("Opção inválida")

if __name__ == "__main__":
    db_factory = DatabaseFactory(host="localhost", user="root", password="jasbhisto", database="MyFoodMenu")
    db_factory.create_database_connection()
    
    if db_factory.db_connection != None:
        food_db = FoodDatabase(db_factory.db_connection)
        food_db.create_table()
        
        print("Bem-vindo ao sistema de gerenciamento de comidas!")
        print(food_db.get_connection_id())
        print("Existe tabela de comidas? ", food_db.TableAlreadyExists)
        
        
        # Inserindo mais 100 dados de comidas brasileiras no banco de dados
        food_db.insert_food("Pamonha", "Doce", 6.00, "Sobremesa", "Centro-Oeste", True, "https://www.example.com/pamonha.jpg")
        food_db.insert_food("Bolo de Rolo", "Doce", 12.00, "Sobremesa", "Nordeste", True, "https://www.example.com/bolo_de_rolo.jpg")
        food_db.insert_food("Carne de Sol", "Salgado", 35.00, "Prato Principal", "Nordeste", True, "https://www.example.com/carne_de_sol.jpg")
        food_db.insert_food("Queijo Coalho", "Salgado", 8.00, "Entrada", "Nordeste", True, "https://www.example.com/queijo_coalho.jpg")
        food_db.insert_food("Cuscuz", "Doce", 10.00, "Prato Principal", "Nordeste", True, "https://www.example.com/cuscuz.jpg")
        food_db.insert_food("Tutu de Feijão", "Salgado", 18.00, "Prato Principal", "Sudeste", True, "https://www.example.com/tutu_de_feijao.jpg")
        food_db.insert_food("Paçoca", "Doce", 4.00, "Sobremesa", "Nordeste", True, "https://www.example.com/pacoca.jpg")
        food_db.insert_food("Buchada de Bode", "Salgado", 40.00, "Prato Principal", "Nordeste", True, "https://www.example.com/buchada_de_bode.jpg")
        food_db.insert_food("Sarapatel", "Salgado", 28.00, "Prato Principal", "Nordeste", True, "https://www.example.com/sarapatel.jpg")
        food_db.insert_food("Rapadura", "Doce", 2.50, "Sobremesa", "Nordeste", True, "https://www.example.com/rapadura.jpg")
        food_db.insert_food("Baião de Dois", "Salgado", 22.00, "Prato Principal", "Nordeste", True, "https://www.example.com/baiao_de_dois.jpg")
        food_db.insert_food("Maniçoba", "Salgado", 32.00, "Prato Principal", "Norte", True, "https://www.example.com/manicoba.jpg")
        food_db.insert_food("Vatapá", "Salgado", 25.00, "Prato Principal", "Nordeste", True, "https://www.example.com/vatapa.jpg")
        food_db.insert_food("Açaí na Tigela", "Doce", 15.00, "Sobremesa", "Norte", True, "https://www.example.com/acai_na_tigela.jpg")
        food_db.insert_food("Caruru", "Salgado", 18.00, "Prato Principal", "Nordeste", True, "https://www.example.com/caruru.jpg")
        food_db.insert_food("Cocada", "Doce", 3.50, "Sobremesa", "Nordeste", True, "https://www.example.com/cocada.jpg")
        food_db.insert_food("Canjica", "Doce", 7.00, "Sobremesa", "Nordeste", True, "https://www.example.com/canjica.jpg")
        food_db.insert_food("Capirotada", "Doce", 8.00, "Sobremesa", "Nordeste", True, "https://www.example.com/capirotada.jpg")
        food_db.insert_food("Arroz de Carreteiro", "Salgado", 28.00, "Prato Principal", "Sul", True, "https://www.example.com/arroz_de_carreteiro.jpg")
        food_db.insert_food("Churrasco", "Salgado", 40.00, "Prato Principal", "Sul", True, "https://www.example.com/churrasco.jpg")
        food_db.insert_food("Pastel de Feira", "Salgado", 5.00, "Salgado", "Sudeste", True, "https://www.example.com/pastel_de_feira.jpg")
        food_db.insert_food("Feijão Tropeiro", "Salgado", 20.00, "Prato Principal", "Sudeste", True, "https://www.example.com/feijao_tropeiro.jpg")
        food_db.insert_food("Curau", "Doce", 8.00, "Sobremesa", "Sudeste", True, "https://www.example.com/curau.jpg")
        food_db.insert_food("Canjiquinha", "Doce", 9.00, "Sobremesa", "Sudeste", True, "https://www.example.com/canjiquinha.jpg")
        food_db.insert_food("Arroz Doce", "Doce", 7.00, "Sobremesa", "Sudeste", True, "https://www.example.com/arroz_doce.jpg")
        food_db.insert_food("Bolo de Fubá", "Doce", 10.00, "Sobremesa", "Sudeste", True, "https://www.example.com/bolo_de_fuba.jpg")
        food_db.insert_food("Feijão Verde", "Salgado", 15.00, "Prato Principal", "Nordeste", True, "https://www.example.com/feijao_verde.jpg")
        food_db.insert_food("Pamonha", "Doce", 6.00, "Sobremesa", "Centro-Oeste", True, "https://www.example.com/pamonha.jpg")
        food_db.insert_food("Bolo de Rolo", "Doce", 12.00, "Sobremesa", "Nordeste", True, "https://www.example.com/bolo_de_rolo.jpg")
        food_db.insert_food("Carne de Sol", "Salgado", 35.00, "Prato Principal", "Nordeste", True, "https://www.example.com/carne_de_sol.jpg")
        food_db.insert_food("Queijo Coalho", "Salgado", 8.00, "Entrada", "Nordeste", True, "https://www.example.com/queijo_coalho.jpg")
        food_db.insert_food("Cuscuz", "Doce", 10.00, "Prato Principal", "Nordeste", True, "https://www.example.com/cuscuz.jpg")
        food_db.insert_food("Tutu de Feijão", "Salgado", 18.00, "Prato Principal", "Sudeste", True, "https://www.example.com/tutu_de_feijao.jpg")
        food_db.insert_food("Paçoca", "Doce", 4.00, "Sobremesa", "Nordeste", True, "https://www.example.com/pacoca.jpg")
        food_db.insert_food("Buchada de Bode", "Salgado", 40.00, "Prato Principal", "Nordeste", True, "https://www.example.com/buchada_de_bode.jpg")
        food_db.insert_food("Sarapatel", "Salgado", 28.00, "Prato Principal", "Nordeste", True, "https://www.example.com/sarapatel.jpg")
        food_db.insert_food("Rapadura", "Doce", 2.50, "Sobremesa", "Nordeste", True, "https://www.example.com/rapadura.jpg")
        food_db.insert_food("Baião de Dois", "Salgado", 22.00, "Prato Principal", "Nordeste", True, "https://www.example.com/baiao_de_dois.jpg")
        food_db.insert_food("Maniçoba", "Salgado", 32.00, "Prato Principal", "Norte", True, "https://www.example.com/manicoba.jpg")
        food_db.insert_food("Vatapá", "Salgado", 25.00, "Prato Principal", "Nordeste", True, "https://www.example.com/vatapa.jpg")
        food_db.insert_food("Açaí na Tigela", "Doce", 15.00, "Sobremesa", "Norte", True, "https://www.example.com/acai_na_tigela.jpg")
        food_db.insert_food("Caruru", "Salgado", 18.00, "Prato Principal", "Nordeste", True, "https://www.example.com/caruru.jpg")
        food_db.insert_food("Cocada", "Doce", 3.50, "Sobremesa", "Nordeste", True, "https://www.example.com/cocada.jpg")
        food_db.insert_food("Canjica", "Doce", 7.00, "Sobremesa", "Nordeste", True, "https://www.example.com/canjica.jpg")
        food_db.insert_food("Capirotada", "Doce", 8.00, "Sobremesa", "Nordeste", True, "https://www.example.com/capirotada.jpg")
        food_db.insert_food("Arroz de Carreteiro", "Salgado", 28.00, "Prato Principal", "Sul", True, "https://www.example.com/arroz_de_carreteiro.jpg")
        food_db.insert_food("Churrasco", "Salgado", 40.00, "Prato Principal", "Sul", True, "https://www.example.com/churrasco.jpg")
        food_db.insert_food("Pastel de Feira", "Salgado", 5.00, "Salgado", "Sudeste", True, "https://www.example.com/pastel_de_feira.jpg")
        food_db.insert_food("Feijão Tropeiro", "Salgado", 20.00, "Prato Principal", "Sudeste", True, "https://www.example.com/feijao_tropeiro.jpg")
        food_db.insert_food("Curau", "Doce", 8.00, "Sobremesa", "Sudeste", True, "https://www.example.com/curau.jpg")
        food_db.insert_food("Canjiquinha", "Doce", 9.00, "Sobremesa", "Sudeste", True, "https://www.example.com/canjiquinha.jpg")
        food_db.insert_food("Arroz Doce", "Doce", 7.00, "Sobremesa", "Sudeste", True, "https://www.example.com/arroz_doce.jpg")
        food_db.insert_food("Bolo de Fubá", "Doce", 10.00, "Sobremesa", "Sudeste", True, "https://www.example.com/bolo_de_fuba.jpg")
        food_db.insert_food("Feijão Verde", "Salgado", 15.00, "Prato Principal", "Nordeste", True, "https://www.example.com/feijao_verde.jpg")
        # Adicione mais comidas conforme necessário

                
                
        
        
        
        Menu(food_db)
      