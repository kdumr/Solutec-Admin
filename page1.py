import tkinter as tk

def show_loading_frame():
    loading_frame = tk.Frame(root, bg="red")
    loading_frame.place(x=0, y=0, relwidth=1, relheight=1)

    loading_label = tk.Label(loading_frame, text="Carregando...", font=("Arial", 16), fg="white", bg="red")
    loading_label.pack(expand=True)

    loading_frame.lift()

def hide_loading_frame():
    for widget in root.winfo_children():
        if widget.winfo_class() == "Frame":
            widget.destroy()

root = tk.Tk()
root.geometry("400x300")

welcome_label = tk.Label(root, text="Bem-vindo à minha aplicação!", font=("Arial", 24))
welcome_label.pack(pady=20)

load_button = tk.Button(root, text="Carregar", command=show_loading_frame)
load_button.pack()

process_button = tk.Button(root, text="Processar", command=lambda: root.after(5000, hide_loading_frame))
process_button.pack()

root.mainloop()
