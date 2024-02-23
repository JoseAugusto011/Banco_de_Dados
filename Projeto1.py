import mysql.connector

class DatabaseFactory:
    def __init__(self, host, user, password, database):
        self.db_connection = None
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



class LibraryDatabase:
    def __init__(self, db_connection):
        self.mydb = db_connection
        self.mycursor = self.mydb.cursor()
        self.TableAlreadyExists = False
        
    def get_connection_id(self):
        # Retorna o id da conexão
        print("\nConection Id:", self.mydb.connection_id)

    def create_table(self):
       
       
        if self.TableAlreadyExists:
            
            print("\nFalha ao Criar - Tabela já existe")
            return
        else:
            
                try:
                    table = "CREATE TABLE book_table (id INT AUTO_INCREMENT PRIMARY KEY, code VARCHAR(255), name VARCHAR(255), author VARCHAR(255), year INT, publisher VARCHAR(255), edition INT, pages INT, price FLOAT, quantity INT, category VARCHAR(255), language VARCHAR(255))"
                    self.mycursor.execute(table)
                    self.TableAlreadyExists = True
                    print("Tabela criada com sucesso.")
                except mysql.connector.Error as err:
                    print("Erro ao criar tabela:", err)
 
        
    def delete_table(self):
        # Deletar a tabela
        if not self.TableAlreadyExists:
            
            print("\nFalha ao Excluir - Tabela não existe")
            return
        
        else:
            try:
                
                self.mycursor.execute("DROP TABLE IF EXISTS book_table")
                self.TableAlreadyExists = False
                print("Tabela excluída com sucesso.")
                
            except mysql.connector.Error as err:
                print("Erro ao excluir tabela:", err)
                
    def clear_table(self):
        if not self.TableAlreadyExists:
            print("\nFalha ao Limpar - Tabela não existe")
            return
        else:
            try:
                self.mycursor.execute("DELETE FROM book_table")
                print("Tabela limpa com sucesso.")
            except mysql.connector.Error as err:
                print("Erro ao limpar tabela:", err)

    def insert_book(self, code, name, author, year, publisher, edition, pages, price, quantity, category, language):
        # Inserir um livro na tabela
        try:
            
            sql = "INSERT INTO book_table (code, name, author, year, publisher, edition, pages, price, quantity, category, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (code, name, author, year, publisher, edition, pages, price, quantity, category, language)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(self.mycursor.rowcount, "registro inserido.")
            
        except mysql.connector.Error as err:
            print("Erro ao inserir livro:", err)

    def delete_book(self, code):
        # Deletar um livro da tabela
        try:
            self.mycursor.execute("DELETE FROM book_table WHERE code = %s", (code,))
            self.mydb.commit()
            if self.mycursor.rowcount == 0:
                print("Nenhum registro encontrado - Código não existe")
            else:
                print("Livro de código", code, "excluído com sucesso.")
                print(self.mycursor.rowcount, "registro(s) excluído(s).")
        except mysql.connector.Error as err:
            print("Erro ao excluir livro:", err)

    def update_book(self, code, name, author, year, publisher, edition, pages, price, quantity, category, language):
        try:
            self.mycursor.execute("UPDATE book_table SET name = %s, author = %s, year = %s, publisher = %s, edition = %s, pages = %s, price = %s, quantity = %s, category = %s, language = %s WHERE code = %s", (name, author, year, publisher, edition, pages, price, quantity, category, language, code))
            self.mydb.commit()
            
            if self.mycursor.rowcount == 0:
                print("Nenhum registro encontrado - Código não existe")
            else:
                print(self.mycursor.rowcount, "registro(s) afetado(s)")
                print("Livro de código", code, "atualizado com sucesso.")
                
        except mysql.connector.Error as err:
            print("Erro ao atualizar livro:", err)
            
    def search_book(self, code):
        try:
            self.mycursor.execute("SELECT * FROM book_table WHERE code = %s", (code,))
            if self.mycursor.rowcount == 0:
                print("Nenhum registro encontrado - Código não existe")
            else:
                myresult = self.mycursor.fetchall()
                for x in myresult:
                    print("Livro encontrado:\n")
                    print("Id:", x[0], "\nCode:", x[1], "\nName:", x[2], "\nAuthor:", x[3], "\nYear:", x[4], "\nPublisher:", x[5], "\nEdition:", x[6], "\nPages:", x[7], "\nPrice:", x[8], "\nQuantity:", x[9], "\nCategory:", x[10], "\nLanguage:", x[11], "\n\n")
                return myresult
        except mysql.connector.Error as err:
            print("Erro ao buscar livro:", err)
            
    def show_table(self):
        
        if not self.TableAlreadyExists:
            print("\nFalha ao Mostrar - Tabela não existe")
            return
        
        # Mostrar a tabela
        
        else:
            try:
                self.mycursor.execute("SELECT * FROM book_table")              
              
                print("Registros encontrados:\n")
                myresult = self.mycursor.fetchall()
                if len(myresult) == 0:
                    print("Nenhum registro retornado")
                else:
                    print("Id | Code | Name | Author | Year | Publisher | Edition | Pages | Price | Quantity | Category | Language\n")
                        
                    for x in myresult:
                        print(x[0], "|", x[1], "|", x[2], "|", x[3], "|", x[4], "|", x[5], "|", x[6], "|", x[7], "|", x[8], "|", x[9], "|", x[10], "|", x[11])  
                        
            except mysql.connector.Error as err:
                print("Erro ao mostrar tabela:", err)


    def close_connection(self):
        # Fechar cursor e conexão
        try:
            if self.mycursor:
                self.mycursor.close()
            if self.mydb:
                self.mydb.close()
            print("Conexão fechada com sucesso.")
        except mysql.connector.Error as err:
            print("Erro ao fechar conexão:", err)
        

# Exemplo de uso:
if __name__ == "__main__":
    
    # Criar uma instância da classe DatabaseFactory
    db_factory = DatabaseFactory(host="localhost", user="root", password="jasbhisto", database="MyLibrary")

    # Estabelecer conexão com o banco de dados
    db_factory.create_database_connection()
    

    if db_factory.db_connection!=None:
        library_db = LibraryDatabase(db_factory.db_connection)
        
        library_db.create_table()
    
        library_db.get_connection_id()  # Retorna o id da conexão
        print("Existe tabela?", library_db.TableAlreadyExists)
        
        
        
        library_db.insert_book("123456", "Livro 1", "Autor 1", 2021, "Editora 1", 1, 100, 50.00, 10, "Categoria 1", "Português")
        library_db.insert_book("123457", "Livro 2", "Autor 2", 2020, "Editora 2", 2, 200, 100.00, 20, "Categoria 2", "Inglês")
        
        
        # print("-=-=--=-=-"*10)
        library_db.show_table()
        
        
        library_db.clear_table()        
        library_db.delete_table()        
        library_db.close_connection()
        
       
        
    