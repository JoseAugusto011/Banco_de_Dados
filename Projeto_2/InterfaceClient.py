import tkinter as tk
from datetime import datetime 
from tkinter import ttk
from tkinter import messagebox
from backEndFinal import Database, EstoqueManager, ClienteManager, VendaManager, ItemVendaManager


class ListaPratosWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.cliente_id = None  # Inicializa o ID do cliente como None
        self.master.title("Lista de Pratos Típicos")
        self.master.state('zoomed')  

        self.create_widgets()

    def create_widgets(self):
        self.prato_frame = tk.Frame(self.master)
        self.prato_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.prato_frame)
        self.table_frame.pack(expand=True, fill=tk.BOTH)

        self.table = ttk.Treeview(self.table_frame)
        self.table["columns"] = ("Nome", "Descrição", "Preço", "Categoria", "Região de Origem", "Disponibilidade", "Quantidade")
        self.table.heading("#0", text="", anchor=tk.W)
        self.table.heading("Nome", text="Nome", anchor=tk.W)
        self.table.heading("Descrição", text="Descrição", anchor=tk.W)
        self.table.heading("Preço", text="Preço", anchor=tk.W)
        self.table.heading("Categoria", text="Categoria", anchor=tk.W)
        self.table.heading("Região de Origem", text="Região de Origem", anchor=tk.W)
        self.table.heading("Disponibilidade", text="Disponibilidade", anchor=tk.W)
        self.table.heading("Quantidade", text="Quantidade", anchor=tk.W)
        
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("Nome", width=180, stretch=tk.NO)
        self.table.column("Descrição", width=300, stretch=tk.NO)
        self.table.column("Preço", width=100, stretch=tk.NO)
        self.table.column("Categoria", width=150, stretch=tk.NO)  
        self.table.column("Região de Origem", width=130, stretch=tk.NO)  
        self.table.column("Disponibilidade", width=100, stretch=tk.NO)
        self.table.column("Quantidade", width=100, stretch=tk.NO)

        self.table.pack(expand=True, fill=tk.BOTH)

        self.atualizar_lista_pratos()

        # Botões
        self.btn_cadastro = tk.Button(self.prato_frame, text="Cadastro", command=self.abrir_cadastro, bg="red", fg="black")
        self.btn_cadastro.pack(anchor=tk.E)

        self.btn_login = tk.Button(self.prato_frame, text="Login", command=self.abrir_login, bg="red", fg="black")
        self.btn_login.pack(anchor=tk.E)

        # Variáveis de entrada e botões
        self.nome_entry = None
        self.email_entry = None
        self.telefone_entry = None
        self.cidade_entry = None
        self.torcedor_var = None
        self.assistir_var = None

        # Frame para o sistema de compra
        self.compra_frame = tk.Frame(self.master)
        self.compra_frame.pack(side=tk.RIGHT, fill=tk.Y)

    def atualizar_lista_pratos(self):
        self.table.delete(*self.table.get_children())
        estoque_manager = EstoqueManager(self.db)
        self.pratos = estoque_manager.listar_todos()
        if self.pratos:
            for prato in self.pratos:
                disponibilidade = "Disponível" if prato[6] else "Indisponível"
                self.table.insert("", "end", values=(prato[1], prato[2], prato[3], prato[4], prato[5], disponibilidade, prato[7]))
                # Diminuir o tamanho da fonte do nome do prato
                self.table.tag_configure("small", font=("TkDefaultFont", 8))
                self.table.item(self.table.selection(), tags=("small",))  # Aplica o estilo de fonte ao item

    def limpar_labels(self):
        # Limpa o texto dos labels que exibem os itens selecionados e a forma de pagamento
        for entry in self.quantidade_entries:
            entry.delete(0, tk.END)
        

    def abrir_cadastro(self):
        self.cadastro_window = tk.Toplevel(self.master)
        self.cadastro_window.title("Cadastro de Cliente")

        tk.Label(self.cadastro_window, text="Preencha os dados para se cadastrar:").pack()

        tk.Label(self.cadastro_window, text="Nome:").pack()
        self.nome_entry = tk.Entry(self.cadastro_window)
        self.nome_entry.pack()

        tk.Label(self.cadastro_window, text="E-mail:").pack()
        self.email_entry = tk.Entry(self.cadastro_window)
        self.email_entry.pack()

        tk.Label(self.cadastro_window, text="Senha:").pack()
        self.senha_entry = tk.Entry(self.cadastro_window, show="*")
        self.senha_entry.pack()

        tk.Label(self.cadastro_window, text="Telefone:").pack()
        self.telefone_entry = tk.Entry(self.cadastro_window)
        self.telefone_entry.pack()

        tk.Label(self.cadastro_window, text="Cidade:").pack()
        self.cidade_entry = tk.Entry(self.cadastro_window)
        self.cidade_entry.pack()

        self.torcedor_var = tk.BooleanVar()
        tk.Checkbutton(self.cadastro_window, text="Torcedor do Flamengo", variable=self.torcedor_var).pack()

        self.assistir_var = tk.BooleanVar()
        tk.Checkbutton(self.cadastro_window, text="Assiste One Piece", variable=self.assistir_var).pack()

        tk.Button(self.cadastro_window, text="Cadastrar", command=self.salvar_cliente).pack()

    def salvar_cliente(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get() # Adicionado para capturar a senha
        telefone = self.telefone_entry.get()
        cidade = self.cidade_entry.get()
        torce_flamengo = self.torcedor_var.get() # Atualizado para usar o nome correto da variável
        assiste_one_piece = self.assistir_var.get() # Atualizado para usar o nome correto da variável

        # Verifica se todos os campos estão preenchidos
        if nome and email and senha and telefone and cidade:
            cliente_manager = ClienteManager(self.db)
            # Alterado o método inserir para incluir a senha
            cliente_manager.inserir(nome, email, senha, telefone, torce_flamengo, assiste_one_piece, cidade)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.cadastro_window.destroy()
            self.atualizar_lista_pratos()  # Atualiza a lista após o cadastro
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def abrir_login(self):
        self.login_window = tk.Toplevel(self.master)
        self.login_window.title("Login de Cliente")

        tk.Label(self.login_window, text="Entre com seu e-mail e senha:").pack()

        tk.Label(self.login_window, text="E-mail:").pack()
        self.email_login_entry = tk.Entry(self.login_window)
        self.email_login_entry.pack()

        tk.Label(self.login_window, text="Senha:").pack()
        self.senha_login_entry = tk.Entry(self.login_window, show="*")
        self.senha_login_entry.pack()

        tk.Button(self.login_window, text="Logar", command=self.verificar_login).pack()

    def verificar_login(self):
        email_login = self.email_login_entry.get()
        senha_login = self.senha_login_entry.get()

        if email_login and senha_login:
            cliente_manager = ClienteManager(self.db)
            # Verifica o login e obtém o ID do cliente
            self.cliente_id = cliente_manager.Verificar_login(email_login, senha_login)
            if self.cliente_id:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.login_window.destroy()
                self.abrir_sistema_de_compra()
            else:
                messagebox.showerror("Erro", "E-mail ou senha incorretos.")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def abrir_sistema_de_compra(self):
        # Limpa o frame de compra antes de adicionar novos elementos
        for widget in self.compra_frame.winfo_children():
            widget.destroy()

        # Adicione os controles para seleção de quantidade ao lado de cada item
        self.quantidade_entries = []
        for prato in self.pratos:
            label = tk.Label(self.compra_frame, text=prato[1], font=("TkDefaultFont", 7))  # Reduz a fonte do nome do prato
            label.pack()
            quantidade_entry = tk.Entry(self.compra_frame, font=("TkDefaultFont", 7))  # Reduz a fonte da entrada de quantidade
            quantidade_entry.pack()
            self.quantidade_entries.append(quantidade_entry)

        # Adicione um botão para finalizar a compra
        tk.Button(self.compra_frame, text="Comprar", command=self.finalizar_compra).pack()

        # Adicione um botão para visualizar os dados do cliente logado
        tk.Button(self.compra_frame, text="Ver Meus Dados", command=self.ver_dados_cliente).pack()

    def ver_dados_cliente(self):
        # Crie uma janela pop-up para exibir os dados do cliente
        dados_cliente_window = tk.Toplevel(self.master)
        dados_cliente_window.title("Meus Dados")

        # Obtenha os dados do cliente do banco de dados
        cliente_manager = ClienteManager(self.db)
        dados_cliente = cliente_manager.obter_cliente_por_id(self.cliente_id)

        # Exiba os dados do cliente na janela pop-up
        tk.Label(dados_cliente_window, text="ID: " + str(dados_cliente["id"])).pack()
        tk.Label(dados_cliente_window, text="Nome: " + dados_cliente["nome"]).pack()
        tk.Label(dados_cliente_window, text="E-mail: " + dados_cliente["email"]).pack()
        tk.Label(dados_cliente_window, text="Senha: " + dados_cliente["senha"]).pack()
        tk.Label(dados_cliente_window, text="Telefone: " + dados_cliente["telefone"]).pack()
        tk.Label(dados_cliente_window, text="Cidade: " + dados_cliente["cidade"]).pack()
        tk.Label(dados_cliente_window, text="Torcedor do Flamengo: " + ("Sim" if dados_cliente["torce_flamengo"] else "Não")).pack()
        tk.Label(dados_cliente_window, text="Assiste One Piece: " + ("Sim" if dados_cliente["assiste_one_piece"] else "Não")).pack()



    def finalizar_compra(self):
        itens_selecionados = []  # Lista para armazenar os itens selecionados e suas quantidades
        total_pago_sem_desconto = 0  # Variável para armazenar o total a ser pago sem desconto
        total_pago = 0  # Variável para armazenar o total a ser pago
        desconto_aplicado = False  # Variável para rastrear se o desconto foi aplicado
        erro = False  # Variável para rastrear se houve algum erro

        # Processar os itens selecionados e calcular o total a ser pago sem desconto
        for i, prato in enumerate(self.pratos):
            quantidade_texto = self.quantidade_entries[i].get()
            if quantidade_texto:
                try:
                    quantidade = int(quantidade_texto)
                    if quantidade < 0:
                        erro = True
                        messagebox.showerror("Erro", f"Quantidade inválida para {prato[1]}: {quantidade_texto}")
                    elif quantidade > prato[7]:
                        erro = True
                        messagebox.showerror("Erro", f"Quantidade de {prato[1]} excede o estoque disponível.")
                    else:
                        preco_unitario = float(prato[3])  # Convertendo para float
                        total_pago_sem_desconto_item = quantidade * preco_unitario
                        total_pago_sem_desconto += total_pago_sem_desconto_item  # Adiciona o valor total do item ao total geral sem desconto

                        # Armazena o nome do prato, quantidade e total do item sem desconto
                        itens_selecionados.append((prato[1], quantidade, total_pago_sem_desconto_item))

                        # Verifica se o cliente atende a alguma das condições para desconto
                        if self.cliente_id:  # Verifica se o cliente está logado
                            cliente_manager = ClienteManager(self.db)
                            if cliente_manager.cliente_torce_para_flamengo(self.cliente_id) or cliente_manager.cliente_assiste_one_piece(self.cliente_id) or cliente_manager.cliente_eh_de_sousa(self.cliente_id):
                                desconto_aplicado = True  # Indica que o desconto será aplicado
                except ValueError:
                    erro = True
                    messagebox.showerror("Erro", f"Número de itens inválido para {prato[1]}: {quantidade_texto}")

        # Aplicar o desconto se aplicável
        if desconto_aplicado:
            total_pago = total_pago_sem_desconto * 0.9  # Aplica o desconto de 10%
        else:
            total_pago = total_pago_sem_desconto  # Mantém o total sem desconto se nenhum desconto for aplicado

        # Se não houve erros, exibir os itens selecionados, o total sem desconto e o total com desconto
        if not erro:
            # Criar uma janela pop-up para exibir os itens selecionados e a forma de pagamento
            popup = tk.Toplevel()
            popup.title("Itens Selecionados")

            mensagem = "Você selecionou os seguintes itens:\n"
            for item in itens_selecionados:
                mensagem += f"{item[1]} unidades de {item[0]} - Total sem desconto: R${item[2]:.2f}\n"
            mensagem += f"\nTotal sem desconto: R${total_pago_sem_desconto:.2f}\n"
            mensagem += f"Total a ser pago (com desconto, caso tenha vai ser de 10%): R${total_pago:.2f}\n"

            # Exibir mensagem
            tk.Label(popup, text=mensagem).pack()

            # Adicionar opções de pagamento
            tk.Label(popup, text="Selecione a forma de pagamento:").pack()
            opcao_pagamento = tk.StringVar()
            opcao_pagamento.set("Pix")  # Opção padrão
            tk.OptionMenu(popup, opcao_pagamento, "Pix", "Boleto", "Cartão", "Berries").pack()

            # Função para inserir a venda e os itens da venda no banco de dados
            def inserir_venda():
                # Inserir a venda no banco de dados
                venda_manager = VendaManager(self.db)
                data_venda = datetime.now().strftime("%Y-%m-%d")
                forma_pagamento = opcao_pagamento.get()  # Obtém a forma de pagamento selecionada
                status_pagamento = "Pago"  # Define o status de pagamento como "Pago"
                venda_id = venda_manager.inserir(self.cliente_id, data_venda, forma_pagamento, status_pagamento)  # Obtém o ID da venda recém-inserida

                # Inserir os itens da venda no banco de dados
                item_venda_manager = ItemVendaManager(self.db)
                for i, prato in enumerate(self.pratos):
                    quantidade_texto = self.quantidade_entries[i].get()
                    if quantidade_texto:
                        quantidade = int(quantidade_texto)
                        id_produto = prato[0]  # Obtém o ID do produto
                        item_venda_manager.inserir(venda_id, id_produto, quantidade)

                # Exibe uma mensagem de sucesso
                messagebox.showinfo("Sucesso", "Compra efetivada com sucesso!")

                # Limpa a lista de itens selecionados
                itens_selecionados.clear()

                # Fecha a janela de pop-up após a inserção no banco de dados
                popup.destroy()

                 # Limpa os labels que exibem os itens selecionados e a forma de pagamento
                self.limpar_labels()

            # Adicionar botão para confirmar o pagamento e inserir no banco de dados
            tk.Button(popup, text="Confirmar Pagamento", command=inserir_venda).pack()





def main():
    root = tk.Tk()
    db = Database(host="localhost", user="root", password="010203", database="comidas_tipicas")
    ListaPratosWindow(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()
