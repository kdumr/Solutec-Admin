from tkinter import *

class Page2(Frame):
    def __init__(self, parent, switch_page_func):
        super().__init__(parent, bg="red")
        
        label2 = Label(self, text="Página 2", font=("Arial", 16))
        label2.pack(pady=10)
        
        switch_button = Button(self, text="Alternar Página", font=("Arial", 14), command=switch_page_func)
        switch_button.pack(pady=10)
