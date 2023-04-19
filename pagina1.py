import tkinter as tk

class Pagina1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Página 1")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Trocar para página 2",
                           command=lambda: controller.mostrar_pagina("Pagina2"))
        button.pack()
