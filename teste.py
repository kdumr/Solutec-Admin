from tkinter import *



# Função para adicionar um label
def adicionar_label():
    novo_label = Label(frame_labels, text="Novo Label")
    novo_label.pack()

# Criação da janela do tkinter
root = Tk()

# Criação do frame para os labels
frame_labels = Frame(root)
frame_labels.pack()

# Criação do botão de adicionar label
botao_adicionar = Button(root, text="Adicionar Label", command=adicionar_label)
botao_adicionar.pack()

# Inicia o loop de eventos do tkinter
root.mainloop()
