from tkinter import *
from tkinter import ttk
from page1 import Page1
from page2 import Page2
import tkinter.messagebox as messagebox

nomeDoPrograma = "Formatador de MAC V2"
icone = "icone.ico"

root = Tk()
root.geometry("400x400")
root.configure(bg="#131515")
root.resizable(False, False)
root.title(nomeDoPrograma)
root.iconbitmap(icone)

# Primeira página
page1 = Page1(root, switch_page_func=lambda: switch_page(page2))
page1.pack(fill="both", expand=True)

# Segunda página
page2 = Page2(root, switch_page_func=lambda: switch_page(page1))

# Função para alternar entre as páginas
def switch_page(page):
    page.tkraise()



title_label = Label(page1, text="Digite o MAC:", font=("Arial", 16), fg="#ffffff", bg=root["bg"]).pack(pady=10)

text_entry = Entry(page1, width=20, font=("Arial", 14))
text_entry.pack(pady=1)

lista = []
def save_text(event=None):
    textInput = text_entry.get().replace(":", "").replace("-","")
    if len(textInput) != 12:
        messagebox.showerror("Erro", "Texto deve ter no máximo 12 caracteres")
    else:
        mac = '{}:{}:{}:{}:{}:{}'.format(textInput[:2], textInput[2:4], textInput[4:6], textInput[6:8], textInput[8:10], textInput[10:])
        if mac in lista:
            messagebox.showerror("Erro", "Este MAC já está na lista")
            text_entry.delete(0, END)
        else:
            lista.append(mac)
            text_entry.delete(0, END)
            display_text.config(state="normal")
            display_text.insert(END, mac + "\n")
            display_text.config(state="disabled")
            print(lista)

text_entry.bind("<Return>", save_text)
title_label = Label(page1, text="MAC's copiados:", font=("Arial", 16), fg="#ffffff", bg=root["bg"]).pack(pady=10)

display_text = Text(page1, width=20, height=5, font=("Arial", 14), bg ="#f0f0f0")
display_text.pack(pady=10)
display_text.config(state="disabled")


save_button = Button(page1, text="Salvar", font=("Arial", 14), command=save_text, bg="#00bfff", fg="#ffffff")
save_button.pack(pady=10)


root.mainloop()
