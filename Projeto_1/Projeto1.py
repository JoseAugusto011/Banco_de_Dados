import mysql.connector

from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
                # table = """CREATE TABLE food_table (
                #             id INT AUTO_INCREMENT PRIMARY KEY,
                #             name VARCHAR(255),
                #             flavor VARCHAR(255),
                #             price FLOAT,
                #             food_type VARCHAR(255),
                #             origin_region VARCHAR(255),
                #             availability BOOLEAN,
                #             image_url VARCHAR(255)
                #         )"""
                
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

    def search_food_by_flavor(self, flavor):
        try:
            
            self.mycursor.execute("SELECT * FROM food_table WHERE flavor = %s",(flavor,))
            myresult = self.mycursor.fetchall()
            
            if len(myresult) == 0:
                print("Nenhum registro encontrado - Sabor não existe")
                
            else:
                print("Registros encontrados:\n")
                print("ID | Nome | Sabor | Preço | Tipo de comida | Região de origem | Disponibilidade | URL da imagem\n")
                
                for x in myresult:
                    print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|",
                          x[5], "|", "Disponível" if x[6] else "Indisponível", "|", x[7])
                    
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
            
    def search_food_by_price_between(self, price1, price2):
        
        if price1 < 0 or price2 < 0:
            print("Preço inválido")
            return
        
        try:
            
            self.mycursor.execute(
                "SELECT * FROM food_table WHERE price BETWEEN %s AND %s", (price1, price2))
            
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


# Funções de retorno de colunas

    def return_column_Price(self):
        retorno = []
        self.mycursor.execute("SELECT price FROM food_table")
        # Recupera os resultados da consulta
        prices = self.mycursor.fetchall()
        for price in prices:
            retorno.append(price[0])  # Adiciona o preço à lista de retorno
        return retorno

    def return_column_boolean(self):
        retorno = []
        self.mycursor.execute("SELECT availability FROM food_table")
        availabilities = self.mycursor.fetchall()
        for availability in availabilities:
            retorno.append(availability[0])
        return retorno

    def return_column_name(self):
        retorno = []
        self.mycursor.execute("SELECT name FROM food_table")
        names = self.mycursor.fetchall()
        for name in names:
            retorno.append(name[0])
        return retorno

    def return_column_flavor(self):
        retorno = []
        self.mycursor.execute("SELECT flavor FROM food_table")
        flavors = self.mycursor.fetchall()
        for flavor in flavors:
            retorno.append(flavor[0])
        return retorno

    def return_column_food_type(self):
        retorno = []
        self.mycursor.execute("SELECT food_type FROM food_table")
        food_types = self.mycursor.fetchall()
        for food_type in food_types:
            retorno.append(food_type[0])
        return retorno

    def return_column_origin_region(self):
        retorno = []
        self.mycursor.execute("SELECT origin_region FROM food_table")
        origin_regions = self.mycursor.fetchall()
        for origin_region in origin_regions:
            retorno.append(origin_region[0])
        return retorno




    # Relatórios e descrições da tabela        

    def DescribeTable(self):
        
        if not self.TableAlreadyExists:
            print("\nFalha ao Descrever - Tabela não existe")
            return
        else:
            
            """id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            flavor VARCHAR(255),
                            price FLOAT,
                            food_type VARCHAR(255),
                            origin_region VARCHAR(255),
                            availability BOOLEAN,
                            image_url VARCHAR(255)"""
            
            # Descrever informações: Qtd de elementos cadastrados, valor total das colunas numéricas, média dos valores das colunas numéricas, mediana, valor máximo e mínimo das colunas numéricas
            
            price  = self.return_column_Price()
            boolean = self.return_column_boolean()
            
            ft = self.return_column_food_type()
            regorg = self.return_column_origin_region()
            name = self.return_column_name()
            flavor = self.return_column_flavor()
            
            if len(price) == 0 or len(boolean) == 0 or len(ft) == 0 or len(regorg) == 0 or len(name) == 0 or len(flavor) == 0:
                
                print("Tabelas vagas - Não é possível descrever")       
                return
            
            else:
            
                priceN = np.array(price)
                booleaN = np.array(boolean)
                
                nameN = np.array(name)
                ftN = np.array(ft)
                regorgN = np.array(regorg)
                flavorN = np.array(flavor)
                
                
                
                print("Relatório de Descrição da Tabela - Colunas Númericas\n\n")              
                
                print("Coluna Availability: \n")
                print("QtdElementos| ValorTotal| Média| Mediana| ValorMáximo| ValorMínimo")
                print(len(booleaN), "          |", np.sum(booleaN), "        |", np.mean(booleaN), "       |", np.median(booleaN), "         |", np.max(booleaN), "        |", np.min(booleaN))    
                plt.hist(booleaN)  
                    
                print("\n\nColuna Price: ")
                print("QtdElementos| Avaliaveis| NaoAvaliaveis| ProporcaoAvaliabilidade")
                print(len(priceN), "         |", np.sum(priceN), "      |",len(priceN)-np.sum(priceN) , "     |", np.sum(priceN)/len(priceN))
                plt.hist(priceN)
                
                print("\n\nRelatório de Descrição da Tabela - Colunas Categóricas\n\n")
                
                print("Coluna Name: ")
                print("QtdElementos| ElementosUnicos| ElementosMaisFrequentes| FrequenciaElementosMaisFrequentes")
                print(len(nameN), "     |", len(np.unique(nameN)), "            |", Counter(nameN).most_common(1)[0][0], "          |", Counter(nameN).most_common(1)[0][1])
                
                print("\n\nColuna Flavor: ")
                print("QtdElementos| ElementosUnicos| ElementosMaisFrequentes| FrequenciaElementosMaisFrequentes")
                print(len(flavorN), "       |", len(np.unique(flavorN)), "      |", Counter(flavorN).most_common(1)[0][0], "        |", Counter(flavorN).most_common(1)[0][1])
                
                
                print("\n\nColuna FoodType: ")
                print("QtdElementos| ElementosUnicos| ElementosMaisFrequentes| FrequenciaElementosMaisFrequentes")
                print(len(ftN), "       |", len(np.unique(ftN)), "      |", Counter(ftN).most_common(1)[0][0], "            |", Counter(ftN).most_common(1)[0][1])
                
                print("\n\nColuna OriginRegion: ")
                print("QtdElementos| ElementosUnicos| ElementosMaisFrequentes| FrequenciaElementosMaisFrequentes")
                print(len(regorgN), "       |", len(np.unique(regorgN)), "      |", Counter(regorgN).most_common(1)[0][0], "            |", Counter(regorgN).most_common(1)[0][1])
                
    
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
    
    
    def food_menu(self):
        opcao = -1

        while opcao != 0:
            print("\n1 - Inserir comida")
            print("2 - Excluir comida")
            print("3 - Atualizar comida")
            print("4 - Buscar comida por ID")
            print("5 - Buscar comida por nome")
            print("6 - Buscar comida por tipo")
            print("7 - Buscar comida por região")
            print("8 - Buscar comida por disponibilidade")
            print("9 - Buscar comida por preço menor que")
            print("10 - Buscar comida por preço maior que")
            print("11 - Buscar comida por preço entre")
            print("12 - Buscar comida por sabor")
            print("13 - Mostrar tabela")
            print("14 - Descrever tabela")
            print("15 - Limpar tabela")
            print("16 - Apagar tabela")
            print("0 - Sair")

            opcao = int(input("\nDigite a opção desejada: "))

            if opcao == 1:
                dados_comida = []
                print("\nInsira os dados da comida\n")
                print("Insira o nome da comida:")
                dados_comida.append(input())
                print("Insira o sabor da comida:")
                dados_comida.append(input())
                print("Insira o preço da comida:")
                dados_comida.append(float(input()))
                print("Insira o tipo da comida:")
                dados_comida.append(input())
                print("Insira a região de origem da comida:")
                dados_comida.append(input())
                print(
                    "Insira a disponibilidade da comida (1 para disponível, 0 para indisponível):")
                dados_comida.append(bool(int(input())))
                print("Insira a URL da imagem da comida:")
                dados_comida.append(input())
                print("\n")

                food_db.insert_food(*dados_comida)

            elif opcao == 2:
                print("\nInsira o ID da comida que deseja excluir:")
                comida_id = int(input())
                food_db.delete_food(comida_id)

            elif opcao == 3:
                print("\nInsira o ID da comida que deseja atualizar:")
                comida_id = int(input())
                dados_comida = food_db.search_food(comida_id)

                if dados_comida:
                    print("Comida encontrada. Insira as alterações desejadas:")
                    print("Deseja alterar o nome da comida? (s/n):")

                    if input() == "s":
                        novo_nome = input("Insira o novo nome da comida: ")
                    else:
                        novo_nome = dados_comida[1]

                    print("Deseja alterar o sabor da comida? (s/n):")
                    if input() == "s":
                        novo_sabor = input("Insira o novo sabor da comida: ")
                    else:
                        novo_sabor = dados_comida[2]

                    print("Deseja alterar o preço da comida? (s/n):")
                    if input() == "s":
                        novo_preco = float(
                            input("Insira o novo preço da comida: "))
                    else:
                        novo_preco = dados_comida[3]

                    print("Deseja alterar o tipo da comida? (s/n):")
                    if input() == "s":
                        novo_tipo = input("Insira o novo tipo da comida: ")
                    else:
                        novo_tipo = dados_comida[4]

                    print("Deseja alterar a região de origem da comida? (s/n):")
                    if input() == "s":
                        nova_regiao = input(
                            "Insira a nova região de origem da comida: ")
                    else:
                        nova_regiao = dados_comida[5]

                    print("Deseja alterar a disponibilidade da comida? (s/n):")
                    if input() == "s":
                        nova_disponibilidade = bool(int(input(
                            "Insira a nova disponibilidade da comida (1 para disponível, 0 para indisponível): ")))
                    else:
                        nova_disponibilidade = dados_comida[6]

                    print("Deseja alterar a URL da imagem da comida? (s/n):")
                    if input() == "s":
                        nova_url_imagem = input(
                            "Insira a nova URL da imagem da comida: ")
                    else:
                        nova_url_imagem = dados_comida[7]

                    food_db.update_food(comida_id, novo_nome, novo_sabor, novo_preco,
                                        novo_tipo, nova_regiao, nova_disponibilidade, nova_url_imagem)
                else:
                    print("Comida não encontrada.")

            elif opcao == 4:
                print("\nInsira o ID da comida que deseja buscar:")
                comida_id = int(input())
                food_db.search_food_by_id(comida_id)

            elif opcao == 5:
                print("\nInsira o nome da comida que deseja buscar:")
                comida_nome = input()
                food_db.search_food_by_name(comida_nome)

            elif opcao == 6:
                print("\nInsira o tipo da comida que deseja buscar:")
                comida_tipo = input()
                food_db.search_food_by_type(comida_tipo)

            elif opcao == 7:
                print("\nInsira a região da comida que deseja buscar:")
                comida_regiao = input()
                food_db.search_food_by_region(comida_regiao)

            elif opcao == 8:
                print("\nInsira a disponibilidade da comida que deseja buscar (1 para disponível, 0 para indisponível):")
                disponibilidade = bool(int(input()))
                food_db.search_food_by_availability(disponibilidade)

            elif opcao == 9:
                print("\nInsira o preço máximo da comida que deseja buscar:")
                preco_max = float(input())
                food_db.search_food_by_price_less_than(preco_max)

            elif opcao == 10:
                print("\nInsira o preço mínimo da comida que deseja buscar:")
                preco_min = float(input())
                food_db.search_food_by_price_greater_than(preco_min)

            elif opcao == 11:
                print("\nInsira o preço mínimo da comida que deseja buscar:")
                preco_min = float(input())
                print("Insira o preço máximo da comida que deseja buscar:")
                preco_max = float(input())
                food_db.search_food_by_price_between(preco_min, preco_max)
                
            elif opcao == 12:
                
                print("\nInsira o sabor da comida que deseja buscar:")
                comida_sabor = input()
                food_db.search_food_by_flavor(comida_sabor)
            
            elif opcao == 13:
                food_db.show_table()

            elif opcao == 14:
                
                food_db.DescribeTable()

            elif opcao == 15:
                print("\nTem certeza que deseja limpar os registros de toda a tabela? (s/n)")
                confirmacao = input()
                if confirmacao.lower() == 's':                
                    food_db.clear_table()

            elif opcao == 16:
                print("\nTem certeza que deseja apagar toda a tabela? (s/n)")
                confirmacao = input()
                if confirmacao.lower() == 's':
                    food_db.delete_table()

            elif opcao == 0:
                print("\nEncerrando programa...")
                food_db.close_connection()

            else:
                print("\nOpção inválida. Por favor, digite novamente.")



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

    #    # food_db.search_food_by_name("Feijão Verde")
    #     food_db.search_food_by_id(10)
    #     food_db.search_food_by_name("Arroz Doce")
        
    #     food_db.update_food(10, "Feijão Verde", "Salgado", 15.00, "Prato Principal",
    #                         "Nordeste", True, "https://www.example.com/feijao_verde.jpg")
        
    #     food_db.search_food_by_id(10)
        
    #     food_db.delete_food(10)
        
    #     food_db.search_food_by_id(10)
        
    #     food_db.search_food_by_name("Feijão Verde")
        
    #     food_db.search_food_by_price_greater_than(20.00)

    #     food_db.clear_table()
    #     food_db.delete_table()
    #     food_db.close_connection()
    
        food_db.food_menu()
        
        

    except mysql.connector.Error as err:
        print("Erro ao criar tabela:", err)
