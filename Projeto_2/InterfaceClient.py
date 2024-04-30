import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backEndFinal import Database, PratoTipico, Cliente, Venda, ItemVenda

class ListaPratosWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Lista de Pratos Típicos")
        
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
            self.table.insert("", "end", values=("Nenhum prato típico encontrado", "", "", "", "", "", ""))

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
