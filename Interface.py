import tkinter as tk
<<<<<<< Updated upstream
from tkinter import messagebox
from tkinter import simpledialog
#from tkinter import destroy
from tkinter import sys
=======
from tkinter import messagebox, simpledialog, sys, PhotoImage, Label, Frame, Canvas, Tk  
from tkinter import *
from tkinter import ttk, Toplevel
>>>>>>> Stashed changes
from backEnd import *
from PIL import Image, ImageTk
from tkinter.ttk import Button, Style
import requests
from io import BytesIO
import re

class Interface(Tk): # Classe que herda de Tk.Tk
    
    def __init__(self, db):
        
        super().__init__()
        self.title("Sistema de Comidas Típicas")
        self.geometry("1536x864")
        self.db = db

        # Adicione esta linha para mudar o ícone
        self.iconbitmap('Imagens_sistema\\logo.ico')

        # Carregue a imagem usando PIL e converta para PhotoImage
        image = Image.open('Imagens_sistema\\Caranguejo (5).png')
        photo = ImageTk.PhotoImage(image)

        # Crie um Canvas com a imagem
        self.canvas = Canvas(self, width=1000, height=700)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, image=photo, anchor='nw')
        self.canvas.image = photo  # mantenha uma referência à imagem

        # Criando o frame
        self.frame = Frame(self)

        # Adicione o frame ao Canvas
        self.frame_window = self.canvas.create_window(768, 432, anchor='center', window=self.frame)

        # Criando os widgets da interface no frame
        self.favorite_button = Button(self.frame, text="Menu", command=self.list_all_food)
        self.favorite_button.pack(side='top', padx=5)

        self.favorite_button = Button(self.frame, text="Prato Predileto", command=self.search_food_by_name)
        self.favorite_button.pack(side='top', padx=5)

        self.insert_button = Button(self.frame, text="Inserir", command=self.insert_food)
        self.insert_button.pack(side='top', padx=5)

        self.remove_button = Button(self.frame, text="Remover", command=self.delete_food)
        self.remove_button.pack(side='top', padx=5)

        self.update_button = Button(self.frame, text="Atualizar", command=self.update_food)
        self.update_button.pack(side='top', padx=5)

        self.update_price_button = Button(self.frame, text="Atualizar Preço", command=self.update_food_price)
        self.update_price_button.pack(side='top', padx=5)

        self.price_range_button = Button(self.frame, text="Verificar Faixa de Preço", command=self.search_food_by_price_range)
        self.price_range_button.pack(side='top', padx=5)

        self.search_name_button = Button(self.frame, text="Pesquisar por Nome", command=self.search_food_by_name)
        self.search_name_button.pack(side='top', padx=5)

        self.search_type_button = Button(self.frame, text="Pesquisar por Tipo", command=self.search_food_by_type)
        self.search_type_button.pack(side='top', padx=5)

        self.search_flavor_button = Button(self.frame, text="Pesquisar por Sabor", command=self.search_food_by_flavor)
        self.search_flavor_button.pack(side='top', padx=5)

        # Botão de saída no canto inferior direito
        self.quit_button = Button(self, text="Sair", command=self.quit)
        self.quit_button.pack(side='bottom', anchor='se')

    def list_all_food(self):
        # Chame a função show_table para obter os dados como uma lista de tuplas
        data = self.db.show_table_TK()

        # Crie um novo pop-up para a tabela
        table_popup = Toplevel(self)
        table_popup.title("Menu")

        # Crie a tabela
        table = ttk.Treeview(table_popup, columns=("ID", "Nome", "Sabor", "Preço", "Tipo de comida", "Região de origem", "Disponibilidade", "URL da imagem"), show='headings')

        # Adicione cabeçalhos à tabela
        for col in table['columns']:
            table.heading(col, text=col)

        # Adicione os dados à tabela
        for item in data:  # Comece na primeira linha
            # Substitua '1' por 'Disponível' e '0' por 'Indisponível' na coluna "Disponibilidade"
            item = list(item)
            if int(item[6]) == 1:
                item[6] = 'Disponível'
            elif int(item[6]) == 0:
                item[6] = 'Indisponível'
            table.insert('', 'end', values=item)

        # Empacote a tabela
        table.pack(fill='both', expand=True)
        
    
    def insert_food(self):
        name = input("Digite o nome da comida: ")
        flavor = input("Digite o sabor da comida: ")
        price = float(input("Digite o preço da comida: "))
        food_type = input("Digite o tipo de comida: ")
        origin_region = input("Digite a região de origem da comida: ")
        availability = input("A comida está disponível? (S/N): ").upper() == "S"
        image_url = input("Digite a URL da imagem da comida: ")

        # Chamando o método insert_food da classe FoodDatabase
        self.db.insert_food(name, flavor, price, food_type, origin_region, availability, image_url)
        
    def update_food(self):
        food_id = int(input("Digite o ID da comida que deseja atualizar: "))
        name = input("Digite o novo nome da comida: ")
        flavor = input("Digite o novo sabor da comida: ")
        price = float(input("Digite o novo preço da comida: "))
        food_type = input("Digite o novo tipo de comida: ")
        origin_region = input("Digite a nova região de origem da comida: ")
        availability = input("A comida está disponível? (S/N): ").upper() == "S"
        image_url = input("Digite a nova URL da imagem da comida: ")

                # Chamando o método update_food da classe FoodDatabase
        self.db.update_food(food_id, name, flavor, price, food_type, origin_region, availability, image_url)


    def search_food_by_name(self):
        # Pergunte ao usuário o nome da comida
        food_name = simpledialog.askstring("Input", "Qual é o nome da sua comida favorita?",
                                parent=self)
        if food_name:
            # Chame a função do backend
            result = self.db.search_food_by_name(food_name)
            if result:
                # Crie um novo pop-up
                result_popup = Toplevel(self)
                result_popup.title("Resultado")
                
                # Crie um widget Text para exibir o resultado
                text = Text(result_popup, wrap='word')
                # Formate o resultado para exibir cada registro em uma nova linha
                formatted_result = '\n'.join(result.split('|'))
                text.insert('end', formatted_result)
                text.pack(expand=True, fill='both')
            else:
                messagebox.showinfo("Resultado", "Nenhum registro encontrado - Nome não existe")


    def delete_food(self):
        food_id = tk.simpledialog.askinteger("Remover Comida", "Digite o ID da comida:")
        if food_id:
            self.db.delete_food(food_id)


    def update_food_price(self):
        food_name = tk.simpledialog.askstring("Atualizar Preço", "Digite o nome da comida:")
        new_price = tk.simpledialog.askfloat("Atualizar Preço", "Digite o novo preço:")
        if food_name and new_price:
            self.db.update_price(food_name, new_price)

    def search_food_by_price_range(self):
        price1 = tk.simpledialog.askfloat("Verificar Faixa de Preço", "Digite o preço mínimo:")
        price2 = tk.simpledialog.askfloat("Verificar Faixa de Preço", "Digite o preço máximo:")
        if price1 is not None and price2 is not None:
            self.db.search_food_by_price_between(price1, price2)

    def search_food_by_type(self):
        food_type = tk.simpledialog.askstring("Pesquisar por Tipo", "Digite o tipo de comida:")
        if food_type:
            self.db.search_food_by_type(food_type)

    def search_food_by_flavor(self):
        flavor = tk.simpledialog.askstring("Pesquisar por Sabor", "Digite o sabor da comida:")
        if flavor:
            self.db.search_food_by_flavor(flavor)
    
    def quit(self):
        self.db.clear_table()
        self.db.delete_table()
        self.db.close_connection()
        self.destroy()  # This will destroy the Tkinter window
        


        

if __name__ == "__main__":
    # Defina suas configurações de conexão ao banco de dados
    host = "localhost"
    user = "root"
    password = "010203"
    database = "db"

    # Cria uma instância da fábrica do banco de dados e estabelece a conexão
    db_factory = DatabaseFactory(host, user, password, database)
    db_factory.create_database_connection()

    # Cria uma instância do manipulador do banco de dados
    food_db = FoodDatabase(db_factory.db_connection)

    # Verifica se o banco de dados existe, e se não, cria-o
    try:
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
    
        #food_db.food_menu()
        

        # Cria uma instância da interface passando a instância do FoodDatabase
        interface = Interface(food_db)
        # Inicia o loop principal do Tkinter
        interface.mainloop()

    except mysql.connector.Error as err:
        print("Erro ao criar tabela:", err)
