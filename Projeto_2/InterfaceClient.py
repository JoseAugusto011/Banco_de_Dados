import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backEndFinal import Database, EstoqueManager, ClienteManager

class ListaPratosWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Lista de Pratos Típicos")
        self.master.state('zoomed')  

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
        estoque_manager = EstoqueManager(self.db)
        pratos = estoque_manager.listar_todos()
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
            result = cliente_manager.Verificar_login(email_login, senha_login)
            if result:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.login_window.destroy()
                # Aqui você pode adicionar o código para redirecionar ou atualizar a interface após o login
            else:
                messagebox.showerror("Erro", "E-mail ou senha incorretos.")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")


def main():
    root = tk.Tk()
    db = Database(host="localhost", user="root", password="010203", database="comidas_tipicas")
    ListaPratosWindow(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()
