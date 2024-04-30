import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backEndFinal import Database, PratoTipico, Cliente, Venda, ItemVenda

<<<<<<< HEAD
class ListaPratosWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Lista de Pratos Típicos")
=======
class Interface:
    def __init__(self, root):
        self.produto_selecionado_idx = None 
        self.cliente_logado = None  # Adicionando atributo para armazenar informações do cliente logado
        self.root = root
        self.root.title("Sistema de Vendas de Pratos Típicos")
        self.root.geometry("400x300")

        self.db = Database("localhost", "root", "jasbhisto", "food_db")

        self.frame_inicio = tk.Frame(self.root)
        self.frame_cadastro_login = tk.Frame(self.root)
        self.frame_lista_produtos = tk.Frame(self.root)
        self.frame_compra = tk.Frame(self.root)

        self.mostrar_tela_inicio()
        
    def selecionar_produto(self, idx):
        self.produto_selecionado_idx = idx
        self.mostrar_tela_compra(idx)

    def mostrar_tela_inicio(self):
        # Limpar os widgets do frame de início, se houver algum
        for widget in self.frame_inicio.winfo_children():
            widget.destroy()
>>>>>>> fd1367fd92c1e102f2bf20a6d857cc82bad283dc
        
        self.create_widgets()

    def create_widgets(self):
        self.table_frame = tk.Frame(self.master)
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
        self.table.column("Nome", width=150, stretch=tk.NO)
        self.table.column("Descrição", width=200, stretch=tk.NO)
        self.table.column("Preço", width=100, stretch=tk.NO)
        self.table.column("Categoria", width=120, stretch=tk.NO)  
        self.table.column("Região de Origem", width=130, stretch=tk.NO)  
        self.table.column("Disponibilidade", width=100, stretch=tk.NO)
        self.table.column("Quantidade", width=100, stretch=tk.NO)

        self.table.pack(expand=True, fill=tk.BOTH)

        self.atualizar_lista_pratos()

        # Botões
        self.btn_cadastro = tk.Button(self.master, text="Cadastro", command=self.abrir_cadastro, bg="red", fg="black")
        self.btn_cadastro.place(relx=0.85, rely=0.95, anchor=tk.CENTER)

        self.btn_login = tk.Button(self.master, text="Login", command=self.abrir_login, bg="red", fg="black")
        self.btn_login.place(relx=0.95, rely=0.95, anchor=tk.CENTER)

        # Variáveis de entrada e botões
        self.nome_entry = None
        self.email_entry = None
        self.telefone_entry = None
        self.cidade_entry = None
        self.torcedor_var = None
        self.assistir_var = None

    def atualizar_lista_pratos(self):
        self.table.delete(*self.table.get_children())
        pratos = PratoTipico.listar_todos(self.db)
        if pratos:
            for prato in pratos:
                disponibilidade = "Disponível" if prato[6] else "Indisponível"
                self.table.insert("", "end", values=(prato[1], prato[2], prato[3], prato[4], prato[5], disponibilidade, prato[7]))
        else:
<<<<<<< HEAD
            self.table.insert("", "end", values=("Nenhum prato típico encontrado", "", "", "", "", "", ""))
=======
            messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
            self.mostrar_tela_inicio()  # Chamar o método para mostrar a tela inicial
>>>>>>> fd1367fd92c1e102f2bf20a6d857cc82bad283dc

    def abrir_cadastro(self):
        self.cadastro_window = tk.Toplevel(self.master)
        self.cadastro_window.title("Cadastro de Cliente")

<<<<<<< HEAD
        tk.Label(self.cadastro_window, text="Preencha os dados para se cadastrar:").pack()

        tk.Label(self.cadastro_window, text="Nome:").pack()
        self.nome_entry = tk.Entry(self.cadastro_window)
        self.nome_entry.pack()
=======
    def mostrar_tela_login(self):
        for widget in self.frame_cadastro_login.winfo_children():
            widget.destroy()

        self.frame_inicio.pack_forget()
        self.frame_lista_produtos.pack_forget()
        self.frame_compra.pack_forget()
>>>>>>> fd1367fd92c1e102f2bf20a6d857cc82bad283dc

        tk.Label(self.cadastro_window, text="E-mail:").pack()
        self.email_entry = tk.Entry(self.cadastro_window)
        self.email_entry.pack()

        tk.Label(self.cadastro_window, text="Telefone:").pack()
        self.telefone_entry = tk.Entry(self.cadastro_window)
        self.telefone_entry.pack()

<<<<<<< HEAD
        tk.Label(self.cadastro_window, text="Cidade:").pack()
        self.cidade_entry = tk.Entry(self.cadastro_window)
        self.cidade_entry.pack()
=======
        btn_login = tk.Button(self.frame_cadastro_login, text="Login", command=self.efetuar_login)
        btn_login.grid(row=2, column=0, pady=5)
>>>>>>> fd1367fd92c1e102f2bf20a6d857cc82bad283dc

        self.torcedor_var = tk.BooleanVar()
        tk.Checkbutton(self.cadastro_window, text="Torcedor do Flamengo", variable=self.torcedor_var).pack()

        self.assistir_var = tk.BooleanVar()
        tk.Checkbutton(self.cadastro_window, text="Assiste One Piece", variable=self.assistir_var).pack()

        tk.Button(self.cadastro_window, text="Cadastrar", command=self.salvar_cliente).pack()

<<<<<<< HEAD
    def salvar_cliente(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        cidade = self.cidade_entry.get()
        torcedor_flamengo = self.torcedor_var.get()
        assistir_one_piece = self.assistir_var.get()

        # Verifica se todos os campos estão preenchidos
        if nome and email and telefone and cidade:
            cliente = Cliente(self.db, nome, email, telefone, torcedor_flamengo, assistir_one_piece, cidade)
            cliente.inserir()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.master.focus_force()
            # Fecha a janela de cadastro após exibir a mensagem de sucesso
            self.cadastro_window.destroy()
=======
    def mostrar_tela_lista_produtos(self):
        frame_scroll = tk.Frame(self.root)
        frame_scroll.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame_scroll)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_scroll, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame_lista_produtos = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_lista_produtos, anchor=tk.NW)

        label_lista_produtos = tk.Label(frame_lista_produtos, text="Lista de Produtos")
        label_lista_produtos.grid(row=0, column=0, columnspan=2, pady=10)

        produtos = PratoTipico.listar_todos(self.db)

        for idx, produto in enumerate(produtos):
            nome_produto = produto[1]
            descricao_produto = produto[2]
            preco_produto = produto[3]

            label_nome_produto = tk.Label(frame_lista_produtos, text=nome_produto)
            label_nome_produto.grid(row=idx + 1, column=0, padx=5, pady=5)

            label_descricao_produto = tk.Label(frame_lista_produtos, text=descricao_produto)
            label_descricao_produto.grid(row=idx + 1, column=1, padx=5, pady=5)

            label_preco_produto = tk.Label(frame_lista_produtos, text=f"Preço: R${preco_produto:.2f}")
            label_preco_produto.grid(row=idx + 1, column=2, padx=5, pady=5)

            btn_comprar = tk.Button(frame_lista_produtos, text="Comprar", command=lambda idx=idx: self.mostrar_tela_compra(idx))
            btn_comprar.grid(row=idx + 1, column=3, padx=5, pady=5)

        frame_lista_produtos.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))



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

        if quantidade <= 0:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto_selecionado = PratoTipico.listar_todos(self.db)[self.produto_selecionado_idx]
        preco_produto = produto_selecionado[3]
        preco_total = quantidade * preco_produto

        if self.cliente_logado is None:
            messagebox.showerror("Erro", "Nenhum cliente logado.")
            return

        venda = Venda(self.cliente_logado.id_cliente, preco_total)
        venda.inserir(self.db)

        item_venda = ItemVenda(produto_selecionado[0], venda.id_venda, quantidade, preco_total)
        item_venda.inserir(self.db)

        messagebox.showinfo("Compra", "Compra efetuada com sucesso!")
        
    def efetuar_login(self):
        email = self.entry_email_login.get()

        cliente = Cliente.pesquisar_por_email(self.db, email)
        
        if cliente is not None:
            self.cliente_logado = cliente
            messagebox.showinfo("Login", "Login efetuado com sucesso! Bem-vindo!")
            self.mostrar_tela_lista_produtos()
>>>>>>> fd1367fd92c1e102f2bf20a6d857cc82bad283dc
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def abrir_login(self):
        self.login_window = tk.Toplevel(self.master)
        self.login_window.title("Login de Cliente")

        # Adicionando preenchimento aos widgets da janela de login
        padx = 20
        pady = 15

        tk.Label(self.login_window, text="Por favor, faça o login:").pack(pady=(pady, 0))

        tk.Label(self.login_window, text="Nome:").pack(pady=(0, pady))
        self.nome_login_entry = tk.Entry(self.login_window)
        self.nome_login_entry.pack(pady=(0, pady), padx=padx)

        tk.Label(self.login_window, text="E-mail:").pack(pady=(0, pady))
        self.email_login_entry = tk.Entry(self.login_window)
        self.email_login_entry.pack(pady=(0, pady), padx=padx)

        tk.Button(self.login_window, text="Acessar", command=self.fazer_login).pack(pady=(pady, 0))

    def fazer_login(self):
        nome = self.nome_login_entry.get()
        email = self.email_login_entry.get()

        # Consulta o banco de dados para verificar se o cliente existe
        cliente = Cliente.buscar_por_nome_email(self.db, nome, email)

        if cliente:
            # Se o cliente existir, fecha a janela de login e exibe a mensagem de sucesso
            self.login_window.destroy()
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")
        else:
            # Se o cliente não existir, exibe uma mensagem de erro
            messagebox.showerror("Erro", "Cliente não encontrado. Verifique o nome e o e-mail fornecidos.")

def main():
    root = tk.Tk()
    root.title("Aplicativo de Pratos Típicos")
    root.state('zoomed')  # Inicia maximizado (janela completa)
    db = Database("localhost", "root", "010203", "food_db")
    ListaPratosWindow(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()
