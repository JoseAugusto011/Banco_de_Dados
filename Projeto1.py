import mysql.connector


class DatabaseFactory:
    def __init__(self, host, user, password, database):
        self.db_connection = None  # Conecta ao banco de dados MySQL
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_database_connection(self):
        try:
            self.db_connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
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


# Insercao e remocao e Atualização

    def insert_food(self, name, flavor, price, food_type, origin_region, availability, image_url):
        try:
            sql = """INSERT INTO food_table 
                    (name, flavor, price, food_type, origin_region, availability, image_url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            val = (name, flavor, price, food_type,
                   origin_region, availability, image_url)
            
            if price < 0:
                print("Preço inválido")
                return  # Não insere comida com preço negativo
            
            
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            
            print(self.mycursor.rowcount, "registro inserido.")
        except mysql.connector.Error as err:
            print("Erro ao inserir comida:", err)

    def delete_food(self, food_id):
        try:
            self.mycursor.execute(
                "DELETE FROM food_table WHERE id = %s", (food_id,))
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
            val = (name, flavor, price, food_type, origin_region,
                   availability, image_url, food_id)
            
            if price < 0:
                print("Preço inválido")
                return
            
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(self.mycursor.rowcount, "registro(s) atualizado(s).")
        except mysql.connector.Error as err:
            print("Erro ao atualizar comida:", err)

    def update_price(self,food_name,new_price):
        
        try:
            
            sql = """UPDATE food_table
                    SET price = %s
                    WHERE name %s"""
                    
            val = (food_name,new_price)
            
            if new_price < 0:
                print("Preço inválido")
                return

            self.mycursor.execute(sql,val)
            self.mydb.commit()
            print(self.mycursor.rowcount,"registro atualizado.")
        except mysql.connector.Error as err:
            print("Erro ao atualizar comida:", err)

    

# Funçõs de pesquisa
    def search_food_by_id(self, food_id):
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE id = %s", (food_id,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - ID não existe")
            else:
                for x in myresult:
                    print("Comida encontrada:\n")
                    print("ID:", x[0])
                    print("Nome:", x[1])
                    print("Sabor:", x[2])
                    print("Preço:", x[3])
                    print("Tipo de comida:", x[4])
                    print("Região de origem:", x[5])
                    print("Disponibilidade:",
                          "Disponível" if x[6] else "Indisponível")
                    print("URL da imagem:", x[7], "\n")
            self.mydb.commit()  # Limpa o cursor
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)

    def search_food_by_name(self, food_name):

        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE name = %s", (food_name,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - ID não existe")
            else:
                for x in myresult:
                    print("Comida encontrada:\n")
                    print("ID:", x[0])
                    print("Nome:", x[1])
                    print("Sabor:", x[2])
                    print("Preço:", x[3])
                    print("Tipo de comida:", x[4])
                    print("Região de origem:", x[5])
                    print("Disponibilidade:",
                          "Disponível" if x[6] else "Indisponível")
                    print("URL da imagem:", x[7], "\n")
            self.mydb.commit()  # Limpa o cursor
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            
    def search_food_by_type(self, food_type):
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE food_type = %s", (food_type,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Tipo de comida não existe")
            else:
                print("Registros encontrados:\n")
                print(
                    "ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                for x in myresult:
                    print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|",
                          x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])
            self.mydb.commit()  # Limpa o cursor
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            
    def search_food_by_region(self, origin_region):
        
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE origin_region = %s", (origin_region,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Região de origem não existe")
            else:
                print("Registros encontrados:\n")
                print(
                    "ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                for x in myresult:
                    print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|",
                          x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])
            self.mydb.commit()  # Limpa o cursor
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)

    def search_food_by_availability(self, availability):
        
        try: 
            
            self.mycursor.execute("SELECT * FROM food_table WHERE availability = %s",(availability,))
            myresult = self.mycursor.fetchall()
            
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Disponibilidade não existe")
                
            else:
                
                for x in myresult:
                    
                    print("Comida encontrada:\n")
                    print("ID:", x[0])
                    print("Nome:", x[1])
                    print("Preço:", x[3])
                    print("Tipo de comida:", x[4])
                    print("Região de origem:", x[5])
                    print("Disponibilidade:",
                          "Disponível" if x[6] else "Indisponível")
                    print("URL da imagem:", x[7], "\n")
            self.mydb.commit()  # Limpa o cursor
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            

    # Consulta de comida por preço (menor que) e (maior que)
    
    def search_food_by_price_less_than(self, price):
        
        if price < 0:
            print("Preço inválido")
            return
        
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE price < %s", (price,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Preço não existe")
            else:
                print("Registros encontrados:\n")
                print(
                    "ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                for x in myresult:
                    print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|",
                          x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])
            self.mydb.commit()  # Limpa o cursor
            
        except mysql.connector.Error as err:
            
            print("Erro ao buscar comida:", err)
            
    def search_food_by_price_greater_than(self, price):
        
        if price < 0:
            print("Preço inválido")
            return
        
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE price > %s", (price,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Preço não existe")
            else:
                print("Registros encontrados:\n")
                print(
                    "ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                for x in myresult:
                    print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|",
                          x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])
            self.mydb.commit()  # Limpa o cursor
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            
# Mostrar elementos

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

                    print(
                        "ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                    for x in myresult:
                        print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|",
                              x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])

            except mysql.connector.Error as err:
                print("Erro ao mostrar tabela:", err)

    def list_id(self):

        try:
            self.mycursor.execute("SELECT id FROM food_table")
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro retornado")
            else:
                print("myresults\n")
                print(myresult)
                print("\n\nID's encontrados:\n")
                count = 0
                for x in myresult:
                    print(x[0], type(x[0]))  # x[1]
                    count += 1

            print(count, " ID(s) encontrado(s).")

        except mysql.connector.Error as err:
            print("Erro ao listar ID's:", err)


# Funções para o fim da execução

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


# Menu de opções --> Função principal (Substituir posteriormente por UI)

if __name__ == "__main__":
    # Defina suas configurações de conexão ao banco de dados
    host = "localhost"
    user = "root"
    password = "jasbhisto"
    database = "food_db"

    # Cria uma instância da fábrica do banco de dados e estabelece a conexão
    db_factory = DatabaseFactory(host, user, password, database)
    db_factory.create_database_connection()

    # Cria uma instância do manipulador do banco de dados
    food_db = FoodDatabase(db_factory.db_connection)

    # Verifica se o banco de dados existe, e se não, cria-o
    try:
        food_db.create_table()

        # Exemplo de operações com o banco de dados
        food_db.create_table()
        food_db.insert_food("Pizza", "Queijo", 10.99, "Fast Food",
                            "Itália", True, "https://example.com/pizza.jpg")
        food_db.insert_food("Pamonha", "Doce", 6.00, "Sobremesa",
                            "Centro-Oeste", True, "https://www.example.com/pamonha.jpg")
        food_db.insert_food("Bolo de Rolo", "Doce", 12.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/bolo_de_rolo.jpg")
        food_db.insert_food("Carne de Sol", "Salgado", 35.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/carne_de_sol.jpg")
        food_db.insert_food("Queijo Coalho", "Salgado", 8.00, "Entrada",
                            "Nordeste", True, "https://www.example.com/queijo_coalho.jpg")
        food_db.insert_food("Cuscuz", "Doce", 10.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/cuscuz.jpg")
        food_db.insert_food("Tutu de Feijão", "Salgado", 18.00, "Prato Principal",
                            "Sudeste", True, "https://www.example.com/tutu_de_feijao.jpg")
        food_db.insert_food("Paçoca", "Doce", 4.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/pacoca.jpg")
        food_db.insert_food("Buchada de Bode", "Salgado", 40.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/buchada_de_bode.jpg")
        food_db.insert_food("Sarapatel", "Salgado", 28.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/sarapatel.jpg")
        food_db.insert_food("Rapadura", "Doce", 2.50, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/rapadura.jpg")
        food_db.insert_food("Baião de Dois", "Salgado", 22.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/baiao_de_dois.jpg")
        food_db.insert_food("Maniçoba", "Salgado", 32.00, "Prato Principal",
                            "Norte", True, "https://www.example.com/manicoba.jpg")
        food_db.insert_food("Vatapá", "Salgado", 25.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/vatapa.jpg")
        food_db.insert_food("Açaí na Tigela", "Doce", 15.00, "Sobremesa",
                            "Norte", True, "https://www.example.com/acai_na_tigela.jpg")
        food_db.insert_food("Caruru", "Salgado", 18.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/caruru.jpg")
        food_db.insert_food("Cocada", "Doce", 3.50, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/cocada.jpg")
        food_db.insert_food("Canjica", "Doce", 7.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/canjica.jpg")
        food_db.insert_food("Capirotada", "Doce", 8.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/capirotada.jpg")
        food_db.insert_food("Arroz de Carreteiro", "Salgado", 28.00, "Prato Principal",
                            "Sul", True, "https://www.example.com/arroz_de_carreteiro.jpg")
        food_db.insert_food("Churrasco", "Salgado", 40.00, "Prato Principal",
                            "Sul", True, "https://www.example.com/churrasco.jpg")
        food_db.insert_food("Pastel de Feira", "Salgado", 5.00, "Salgado",
                            "Sudeste", True, "https://www.example.com/pastel_de_feira.jpg")
        food_db.insert_food("Feijão Tropeiro", "Salgado", 20.00, "Prato Principal",
                            "Sudeste", True, "https://www.example.com/feijao_tropeiro.jpg")
        food_db.insert_food("Curau", "Doce", 8.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/curau.jpg")
        food_db.insert_food("Canjiquinha", "Doce", 9.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/canjiquinha.jpg")
        food_db.insert_food("Arroz Doce", "Doce", 7.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/arroz_doce.jpg")
        food_db.insert_food("Bolo de Fubá", "Doce", 10.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/bolo_de_fuba.jpg")
        food_db.insert_food("Feijão Verde", "Salgado", 15.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/feijao_verde.jpg")
        food_db.insert_food("Pamonha", "Doce", 6.00, "Sobremesa",
                            "Centro-Oeste", True, "https://www.example.com/pamonha.jpg")
        food_db.insert_food("Bolo de Rolo", "Doce", 12.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/bolo_de_rolo.jpg")
        food_db.insert_food("Carne de Sol", "Salgado", 35.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/carne_de_sol.jpg")
        food_db.insert_food("Queijo Coalho", "Salgado", 8.00, "Entrada",
                            "Nordeste", True, "https://www.example.com/queijo_coalho.jpg")
        food_db.insert_food("Cuscuz", "Doce", 10.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/cuscuz.jpg")
        food_db.insert_food("Tutu de Feijão", "Salgado", 18.00, "Prato Principal",
                            "Sudeste", True, "https://www.example.com/tutu_de_feijao.jpg")
        food_db.insert_food("Paçoca", "Doce", 4.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/pacoca.jpg")
        food_db.insert_food("Buchada de Bode", "Salgado", 40.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/buchada_de_bode.jpg")
        food_db.insert_food("Sarapatel", "Salgado", 28.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/sarapatel.jpg")
        food_db.insert_food("Rapadura", "Doce", 2.50, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/rapadura.jpg")
        food_db.insert_food("Baião de Dois", "Salgado", 22.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/baiao_de_dois.jpg")
        food_db.insert_food("Maniçoba", "Salgado", 32.00, "Prato Principal",
                            "Norte", True, "https://www.example.com/manicoba.jpg")
        food_db.insert_food("Vatapá", "Salgado", 25.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/vatapa.jpg")
        food_db.insert_food("Açaí na Tigela", "Doce", 15.00, "Sobremesa",
                            "Norte", True, "https://www.example.com/acai_na_tigela.jpg")
        food_db.insert_food("Caruru", "Salgado", 18.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/caruru.jpg")
        food_db.insert_food("Cocada", "Doce", 3.50, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/cocada.jpg")
        food_db.insert_food("Canjica", "Doce", 7.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/canjica.jpg")
        food_db.insert_food("Capirotada", "Doce", 8.00, "Sobremesa",
                            "Nordeste", True, "https://www.example.com/capirotada.jpg")
        food_db.insert_food("Arroz de Carreteiro", "Salgado", 28.00, "Prato Principal",
                            "Sul", True, "https://www.example.com/arroz_de_carreteiro.jpg")
        food_db.insert_food("Churrasco", "Salgado", 40.00, "Prato Principal",
                            "Sul", True, "https://www.example.com/churrasco.jpg")
        food_db.insert_food("Pastel de Feira", "Salgado", 5.00, "Salgado",
                            "Sudeste", True, "https://www.example.com/pastel_de_feira.jpg")
        food_db.insert_food("Feijão Tropeiro", "Salgado", 20.00, "Prato Principal",
                            "Sudeste", True, "https://www.example.com/feijao_tropeiro.jpg")
        food_db.insert_food("Curau", "Doce", 8.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/curau.jpg")
        food_db.insert_food("Canjiquinha", "Doce", 9.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/canjiquinha.jpg")
        food_db.insert_food("Arroz Doce", "Doce", 7.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/arroz_doce.jpg")
        food_db.insert_food("Bolo de Fubá", "Doce", 10.00, "Sobremesa",
                            "Sudeste", True, "https://www.example.com/bolo_de_fuba.jpg")
        food_db.insert_food("Feijão Verde", "Salgado", 15.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/feijao_verde.jpg")

       # food_db.search_food_by_name("Feijão Verde")
        food_db.search_food_by_id(10)
        food_db.search_food_by_name("Arroz Doce")
        
        food_db.update_food(10, "Feijão Verde", "Salgado", 15.00, "Prato Principal",
                            "Nordeste", True, "https://www.example.com/feijao_verde.jpg")
        
        food_db.search_food_by_id(10)
        
        food_db.delete_food(10)
        
        food_db.search_food_by_id(10)
        
        food_db.search_food_by_name("Feijão Verde")
        
        food_db.search_food_by_price_greater_than(20.00)

        food_db.clear_table()
        food_db.delete_table()
        food_db.close_connection()

    except mysql.connector.Error as err:
        print("Erro ao criar tabela:", err)
