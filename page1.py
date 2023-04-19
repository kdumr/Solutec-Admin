import tkinter as tk

def esconder_botao():
    # Função para esconder o botão quando o botão 'Esconder' é clicado
    botao2.grid_remove()

# Criação da janela
janela = tk.Tk()

# Criação dos botões
botao1 = tk.Button(janela, text='Botão 1')
botao1.grid(row=0, column=0)

botao2 = tk.Button(janela, text='Botão 2')
botao2.grid(row=0, column=1)

botao_esconder = tk.Button(janela, text='Esconder', command=esconder_botao)
botao_esconder.grid(row=1, column=0, columnspan=2)

# Iniciar o loop principal do tkinter
janela.mainloop()
