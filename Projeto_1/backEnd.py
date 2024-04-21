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
            return True
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados:", err)
            return False

class FoodDatabase:
    def __init__(self, db_connection):
        self.mydb = db_connection
        self.mycursor = self.mydb.cursor()
        self.TableAlreadyExists = False

    def create_table(self):
        if self.TableAlreadyExists:
            print("\nFalha ao Criar - Tabela já existe")
            return False
        else:
            try:
             
                
                table = """CREATE TABLE IF NOT EXISTS food_table (
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
                return True
            except mysql.connector.Error as err:
                print("Erro ao criar tabela:", err)
                return False

    def get_connection_id(self):
        # Retorna o id da conexão
        print("\nConection Id:", self.mydb.connection_id)
        return self.mydb.connection_id


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
                return  False# Não insere comida com preço negativo
            
            
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            
            print(self.mycursor.rowcount, "registro inserido.")
            return True
        except mysql.connector.Error as err:
            print("Erro ao inserir comida:", err)
            return False

    def delete_food(self, food_id):
        try:
            self.mycursor.execute(
                "DELETE FROM food_table WHERE id = %s", (food_id,))
            self.mydb.commit()
            print("Comida com ID", food_id, "excluída com sucesso.")
            print(self.mycursor.rowcount, "registro(s) excluído(s).")
            return True
        except mysql.connector.Error as err:
            print("Erro ao excluir comida:", err)
            return False

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
            return True
        except mysql.connector.Error as err:
            print("Erro ao atualizar comida:", err)
            return False

    def update_price(self,food_name,new_price):
        
        try:
            
            sql = """UPDATE food_table
                    SET price = %s
                    WHERE name %s"""
                    
            val = (food_name,new_price)
            
            if new_price < 0:
                print("Preço inválido")
                return False

            self.mycursor.execute(sql,val)
            self.mydb.commit()
            print(self.mycursor.rowcount,"registro atualizado.")
            return True
        except mysql.connector.Error as err:
            print("Erro ao atualizar comida:", err)
            return False

    

# Funçõs de pesquisa
    def search_food_by_id(self, food_id):
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE id = %s", (food_id,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - ID não existe")
                return None
            else:
                #retorno = "ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n"
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                self.mydb.commit()  # Limpa o cursor
                return retorno
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None

    def search_food_by_name(self, food_name):

        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE name = %s", (food_name,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - ID não existe")
                return None
            else:
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None
            
    def search_food_by_type(self, food_type):
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE food_type = %s", (food_type,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Tipo de comida não existe")
                return None
            else:
                print("Registros encontrados:\n")
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None
            
    def search_food_by_region(self, origin_region):
        
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE origin_region = %s", (origin_region,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Região de origem não existe")
                return None
            else:
                print("Registros encontrados:\n")
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None

    def search_food_by_availability(self, availability):
        
        try: 
            
            self.mycursor.execute("SELECT * FROM food_table WHERE availability = %s",(availability,))
            myresult = self.mycursor.fetchall()
            
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Disponibilidade não existe")
                return None
                
            else:
                
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None

    def search_food_by_flavor(self, flavor):
        try:
            
            self.mycursor.execute("SELECT * FROM food_table WHERE flavor = %s",(flavor,))
            myresult = self.mycursor.fetchall()
            
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Sabor não existe")
                return None
                
            else:
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)        
            return None    

    # Consulta de comida por preço (menor que) e (maior que)
    
    def search_food_by_price_less_than(self, price):
        
        if price < 0:
            print("Preço inválido")
            return None
        
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE price < %s", (price,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Preço não existe")
                return None
            else:
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
            

            
        except mysql.connector.Error as err:
            
            print("Erro ao buscar comida:", err)
            return None
            
    def search_food_by_price_greater_than(self, price):
        
        if price < 0:
            print("Preço inválido")
            return None
        
        try:
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE price > %s", (price,))
            myresult = self.mycursor.fetchall()
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Preço não existe")
                return None
            else:
                print("Registros encontrados:\n")
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                self.mydb.commit()  # Limpa o cursor
                return retorno
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None
            
    def search_food_by_price_between(self, price1, price2):
        
        if price1 < 0 or price2 < 0:
            print("Preço inválido")
            return None
        
        try:
            
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE price BETWEEN %s AND %s", (price1, price2))
            
            myresult = self.mycursor.fetchall()
            
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Preço não existe")
                return None
                
            else:
                retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                self.mydb.commit()  # Limpa o cursor
                return retorno
            
        except mysql.connector.Error as err:
            print("Erro ao buscar comida:", err)
            return None
# Mostrar elementos

    def show_table(self):
        if not self.TableAlreadyExists:
            print("\nFalha ao Mostrar - Tabela não existe")
            return None
        else:
            try:
                self.mycursor.execute("SELECT * FROM food_table")
                print("Registros encontrados:\n")
                myresult = self.mycursor.fetchall()
                if len(myresult) == 0:
                    print("Nenhum registro retornado")
                    return None
                else:

                      retorno = []
                for x in myresult:
                    #retorno += str(x[0]) + " | " + x[1] + " | " + x[2] + " | " + str(x[3]) + " | " + x[4] + " | " + x[5] + " | " + "Disponível" if x[6] else "Indisponível" + " | " + x[7] + "\n"               
                    retorno.append(x)
                    
                    self.mydb.commit()  # Limpa o cursor
                    return retorno
            except mysql.connector.Error as err:
                print("Erro ao mostrar tabela:", err)
                return None

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
            return False
        else:
            try:
                self.mycursor.execute("DELETE FROM food_table")
                print("Tabela limpa com sucesso.")
                return True
            except mysql.connector.Error as err:
                print("Erro ao limpar tabela:", err)
                return False

    def delete_table(self):
        if not self.TableAlreadyExists:
            print("\nFalha ao Excluir - Tabela não existe")
            return False
        else:
            try:
                self.mycursor.execute("DROP TABLE IF EXISTS food_table")
                self.TableAlreadyExists = False
                print("Tabela excluída com sucesso.")
                return True
            except mysql.connector.Error as err:
                print("Erro ao excluir tabela:", err)
                return False

    def close_connection(self):
        try:
            if self.mycursor:
                self.mycursor.close()
            if self.mydb:
                self.mydb.close()
            print("Conexão fechada com sucesso.")
            return True
        except mysql.connector.Error as err:
            print("Erro ao fechar conexão:", err)
            return False
