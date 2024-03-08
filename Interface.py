import tkinter as tk
from tkinter import messagebox
from Projeto1 import FoodDatabase, DatabaseFactory


class FoodApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplicativo de Comidas Típicas")

        self.food_db = FoodDatabase()

        self.button_menu = tk.Button(master, text="Menu", command=self.list_all_food)
        self.button_menu.pack()

        self.button_favorite = tk.Button(master, text="Prato Predileto", command=self.search_food)
        self.button_favorite.pack()

        self.button_insert = tk.Button(master, text="Inserir", command=self.insert_food)
        self.button_insert.pack()

        self.button_remove = tk.Button(master, text="Remover", command=self.remove_food)
        self.button_remove.pack()

        self.button_exit = tk.Button(master, text="Sair", command=self.master.quit)
        self.button_exit.pack()

    def list_all_food(self):
        # Implemente a lógica para listar todas as comidas típicas
        print

    def search_food(self):
        # Implemente a lógica para procurar uma comida específica
        pass

    def insert_food(self):
        # Implemente a lógica para inserir uma nova comida
        pass

    def remove_food(self):
        # Implemente a lógica para remover uma comida
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()
