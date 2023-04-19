import tkinter as tk

class Pagina2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Página 2")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Trocar para página 1",
                           command=lambda: controller.mostrar_pagina("Pagina1"))
        button.pack()
