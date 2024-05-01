import tkinter as tk
from tkinter import messagebox
from back import EstoqueManager, ClienteManager, VendaManager, Database

class Interface:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema de Compras")
        
        self.db = Database("localhost", "root", "jasbhisto", "comidas_tipicas")
        self.db.create_tables()
        
        self.estoque_manager = EstoqueManager(self.db)
        self.cliente_manager = ClienteManager(self.db)
        self.venda_manager = VendaManager(self.db)
        
        self.construir_tela_inicial()

    def construir_tela_inicial(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.janela)
        self.frame_principal.pack(padx=20, pady=20)

        # Rótulo de boas-vindas
        self.rotulo_boas_vindas = tk.Label(self.frame_principal, text="Bem-vindo ao Sistema de Compras")
        self.rotulo_boas_vindas.pack(pady=10)

        # Botão Continuar
        self.botao_continuar = tk.Button(self.frame_principal, text="Continuar", command=self.construir_tela_login)
        self.botao_continuar.pack(pady=5)

    def construir_tela_login(self):
        # Limpar a tela inicial
        self.frame_principal.destroy()

        # Frame de login
        self.frame_login = tk.Frame(self.janela)
        self.frame_login.pack(padx=20, pady=20)

        # Rótulo de login
        self.rotulo_login = tk.Label(self.frame_login, text="Faça login ou cadastre-se")
        self.rotulo_login.grid(row=0, column=0, columnspan=2, pady=10)

        # Botão de login
        self.botao_login = tk.Button(self.frame_login, text="Login", command=self.fazer_login)
        self.botao_login.grid(row=1, column=0, padx=5)

        # Botão de cadastro
        self.botao_cadastro = tk.Button(self.frame_login, text="Cadastro", command=self.fazer_cadastro)
        self.botao_cadastro.grid(row=1, column=1, padx=5)

    def fazer_login(self):
        # Implemente a lógica de login aqui
        messagebox.showinfo("Login", "Funcionalidade de login em construção")

    def fazer_cadastro(self):
        # Implemente a lógica de cadastro aqui
        messagebox.showinfo("Cadastro", "Funcionalidade de cadastro em construção")

    def iniciar(self):
        self.janela.mainloop()

# Criar a janela principal
janela_principal = tk.Tk()
app = Interface(janela_principal)
app.iniciar()
