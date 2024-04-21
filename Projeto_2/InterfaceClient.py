import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from backEndFinal import Database, PratoTipico, Cliente, Venda, ItemVenda

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas de Pratos Típicos")
        self.root.geometry("400x300")

        self.db = Database("localhost", "root", "jasbhisto", "food_db")

        self.frame_inicio = tk.Frame(self.root)
        self.frame_inicio.pack()

        self.frame_cadastro_login = tk.Frame(self.root)

        self.frame_lista_produtos = tk.Frame(self.root)

        self.frame_compra = tk.Frame(self.root)

        self.mostrar_tela_inicio()

    def mostrar_tela_inicio(self):
        # Limpar os widgets do frame de início, se houver algum
        for widget in self.frame_inicio.winfo_children():
            widget.destroy()
        
        # Desempacotar outros frames, se estiverem visíveis
        self.frame_cadastro_login.pack_forget()
        self.frame_lista_produtos.pack_forget()
        self.frame_compra.pack_forget()

        self.frame_inicio.pack()  # Empacotar o frame de início

        label_inicio = tk.Label(self.frame_inicio, text="Bem-vindo ao Sistema de Vendas")
        label_inicio.pack(pady=10)

        btn_cadastro = tk.Button(self.frame_inicio, text="Cadastro", command=self.mostrar_tela_cadastro)
        btn_cadastro.pack(pady=5)

        btn_login = tk.Button(self.frame_inicio, text="Login", command=self.mostrar_tela_login)
        btn_login.pack(pady=5)


    def mostrar_tela_cadastro(self):
        self.frame_inicio.pack_forget()

        label_cadastro = tk.Label(self.frame_cadastro_login, text="Preencha os dados para se cadastrar:")
        label_cadastro.grid(row=0, column=0, columnspan=2, pady=10)

        label_nome = tk.Label(self.frame_cadastro_login, text="Nome:")
        label_nome.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(self.frame_cadastro_login)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        label_email = tk.Label(self.frame_cadastro_login, text="Email:")
        label_email.grid(row=2, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(self.frame_cadastro_login)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        label_telefone = tk.Label(self.frame_cadastro_login, text="Telefone:")
        label_telefone.grid(row=3, column=0, padx=5, pady=5)
        self.entry_telefone = tk.Entry(self.frame_cadastro_login)
        self.entry_telefone.grid(row=3, column=1, padx=5, pady=5)

        label_cidade = tk.Label(self.frame_cadastro_login, text="Cidade:")
        label_cidade.grid(row=4, column=0, padx=5, pady=5)
        self.entry_cidade = tk.Entry(self.frame_cadastro_login)
        self.entry_cidade.grid(row=4, column=1, padx=5, pady=5)

        label_torce_flamengo = tk.Label(self.frame_cadastro_login, text="Torce para o Flamengo:")
        label_torce_flamengo.grid(row=5, column=0, padx=5, pady=5)
        self.var_torce_flamengo = tk.BooleanVar()
        self.check_torce_flamengo = tk.Checkbutton(self.frame_cadastro_login, variable=self.var_torce_flamengo)
        self.check_torce_flamengo.grid(row=5, column=1, padx=5, pady=5)

        label_assiste_one_piece = tk.Label(self.frame_cadastro_login, text="Assiste One Piece:")
        label_assiste_one_piece.grid(row=6, column=0, padx=5, pady=5)
        self.var_assiste_one_piece = tk.BooleanVar()
        self.check_assiste_one_piece = tk.Checkbutton(self.frame_cadastro_login, variable=self.var_assiste_one_piece)
        self.check_assiste_one_piece.grid(row=6, column=1, padx=5, pady=5)

        btn_cadastrar = tk.Button(self.frame_cadastro_login, text="Cadastrar", command=self.realizar_cadastro)
        btn_cadastrar.grid(row=7, column=0, columnspan=2, pady=10)

        btn_voltar = tk.Button(self.frame_cadastro_login, text="Voltar", command=self.mostrar_tela_inicio)
        btn_voltar.grid(row=8, column=0, columnspan=2)

        self.frame_cadastro_login.pack()

    def realizar_cadastro(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        telefone = self.entry_telefone.get()
        cidade = self.entry_cidade.get()
        torce_flamengo = self.var_torce_flamengo.get()
        assiste_one_piece = self.var_assiste_one_piece.get()

        cliente = Cliente(nome, email, telefone, torce_flamengo, assiste_one_piece, cidade)
        cliente.inserir(self.db)

        if cliente is None:
            messagebox.showerror("Erro", "Erro ao cadastrar cliente!")
        else:
            messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
            #self.frame_cadastro_login.pack_forget()  # Desempacotar o frame de cadastro
            self.mostrar_tela_inicio()  # Chamar o método para mostrar a tela inicial


    def mostrar_tela_login(self):
        # Limpar os widgets do frame de login, se houver algum
        for widget in self.frame_cadastro_login.winfo_children():
            widget.destroy()

        # Desempacotar outros frames, se estiverem visíveis
        self.frame_inicio.pack_forget()
        self.frame_lista_produtos.pack_forget()
        self.frame_compra.pack_forget()

        label_login = tk.Label(self.frame_cadastro_login, text="Digite seu email para fazer login:")
        label_login.grid(row=0, column=0, columnspan=2, pady=10)

        self.entry_email_login = tk.Entry(self.frame_cadastro_login)
        self.entry_email_login.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        btn_login = tk.Button(self.frame_cadastro_login, text="Login", command=app.efetuar_login)  # Corrigido aqui
        btn_login.grid(row=2, column=0, pady=5)

        btn_voltar = tk.Button(self.frame_cadastro_login, text="Voltar", command=self.mostrar_tela_inicio)
        btn_voltar.grid(row=2, column=1, pady=5)

        self.frame_cadastro_login.pack()


    def mostrar_tela_lista_produtos(self):
        self.frame_lista_produtos.pack_forget()

        self.frame_lista_produtos = tk.Frame(self.root)
        self.frame_lista_produtos.pack()

        label_lista_produtos = tk.Label(self.frame_lista_produtos, text="Lista de Produtos")
        label_lista_produtos.grid(row=0, column=0, columnspan=2, pady=10)
        
    

        produtos = PratoTipico.listar_todos(self.db)
        
        print(produtos)
        for idx, produto in enumerate(produtos):
            nome_produto = produto[1]
            descricao_produto = produto[2]
            preco_produto = produto[3]

            label_nome_produto = tk.Label(self.frame_lista_produtos, text=nome_produto)
            label_nome_produto.grid(row=idx+1, column=0, padx=5, pady=5)

            label_descricao_produto = tk.Label(self.frame_lista_produtos, text=descricao_produto)
            label_descricao_produto.grid(row=idx+1, column=1, padx=5, pady=5)

            label_preco_produto = tk.Label(self.frame_lista_produtos, text=f"Preço: R${preco_produto:.2f}")
            label_preco_produto.grid(row=idx+1, column=2, padx=5, pady=5)

            btn_comprar = tk.Button(self.frame_lista_produtos, text="Comprar", command=lambda idx=idx: self.mostrar_tela_compra(idx))
            btn_comprar.grid(row=idx+1, column=3, padx=5, pady=5)

    def mostrar_tela_compra(self, idx_produto):
        self.frame_lista_produtos.pack_forget()

        self.frame_compra = tk.Frame(self.root)
        self.frame_compra.pack()

        produto_selecionado = PratoTipico.listar_todos(self.db)[idx_produto]

        label_nome_produto = tk.Label(self.frame_compra, text=produto_selecionado[1])
        label_nome_produto.grid(row=0, column=0, padx=5, pady=5)

        label_descricao_produto = tk.Label(self.frame_compra, text=produto_selecionado[2])
        label_descricao_produto.grid(row=1, column=0, padx=5, pady=5)

        label_preco_produto = tk.Label(self.frame_compra, text=f"Preço: R${produto_selecionado[3]:.2f}")
        label_preco_produto.grid(row=2, column=0, padx=5, pady=5)

        label_quantidade = tk.Label(self.frame_compra, text="Quantidade:")
        label_quantidade.grid(row=3, column=0, padx=5, pady=5)
        self.entry_quantidade = tk.Entry(self.frame_compra)
        self.entry_quantidade.grid(row=3, column=1, padx=5, pady=5)

        btn_efetuar_compra = tk.Button(self.frame_compra, text="Efetuar Compra", command=self.efetuar_compra)
        btn_efetuar_compra.grid(row=4, column=0, columnspan=2, pady=10)

        btn_voltar = tk.Button(self.frame_compra, text="Voltar", command=self.mostrar_tela_lista_produtos)
        btn_voltar.grid(row=5, column=0, columnspan=2)
    
    def efetuar_compra(self):
        
        quantidade = int(self.entry_quantidade.get())

        produtos = PratoTipico.listar_todos(self.db)

        if not produtos:
            messagebox.showerror("Erro", "Não há produtos disponíveis.")
            return

        produto_selecionado = produtos[0]  # Selecionando o primeiro produto por padrão
        preco_produto = produto_selecionado[3]

        # Verificando se o cliente digitou um índice válido
        try:
            idx_produto = int(simpledialog.askstring("Selecionar Produto", "Digite o índice do produto que deseja comprar:"))
            if idx_produto < 0 or idx_produto >= len(produtos):
                raise ValueError
            produto_selecionado = produtos[idx_produto]
            preco_produto = produto_selecionado[3]
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Índice inválido.")
            return

        preco_total = quantidade * preco_produto

        venda = Venda(self.cliente_logado.id_cliente, preco_total)
        venda.inserir(self.db)

        item_venda = ItemVenda(produto_selecionado[0], venda.id_venda, quantidade, preco_total)
        item_venda.inserir(self.db)

        messagebox.showinfo("Compra", "Compra efetuada com sucesso!")
        
    def efetuar_login(self):
        email = self.entry_email_login.get()

        # Verificar se o email está na tabela de clientes
        cliente = Cliente.pesquisar_por_email(self.db, email)
        
        if cliente is not None:
            messagebox.showinfo("Login", "Login efetuado com sucesso! Bem-vindo!")
            # Após o login bem-sucedido, chame a próxima tela
            self.mostrar_tela_lista_produtos()
        else:
            messagebox.showerror("Login", "Email não encontrado!")


root = tk.Tk()
app = Interface(root)
root.mainloop()
