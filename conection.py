import requests
import tkinter
import sys
import urllib.request
import json
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter import messagebox

def conectar(urlConfig, urlDownload, version, nome_do_programa):
    try:
        # Realizar a solicitação HTTP
        response = requests.get(urlConfig)
        # Verificar o código de status da resposta
        if response.status_code == 200:
            # Se a resposta foi bem-sucedida, obter o conteúdo da resposta
            config = json.loads(response.text)
            content = config["version"]
            print(f'Versão escrita WEB: {content}')

            # Obter a versão mais recente do conteúdo
            latest_version = version

            # Comparar a versão mais recente com a versão atualmente instalada
            if latest_version < content:
                result = messagebox.askyesno(f"Versão atual: {version}", f"Uma nova versão está disponível: {content} \nDeseja instalar?")
                # Verificar o resultado
                if result:
                    def choose_directory():
                        root = tkinter.Tk() 
                        root.withdraw()
                        return filedialog.askdirectory()

                    def download_file(url, file_name, progress_bar):
                        try:
                            def show_progress(block_num, block_size, total_size):
                                percent = int((block_num * block_size * 100) / total_size)
                                progress_bar['value'] = percent
                                progress_bar.update()

                            urllib.request.urlretrieve(url, file_name, show_progress)
                            return True
                        except urllib.error.URLError:
                            messagebox.showerror("Erro", "Não foi possível estabelecer conexão com a URL")
                            return False

                    def show_download_progress(url, file_name):
                        install_dir = choose_directory()
                        if install_dir == "":
                            messagebox.showerror("Erro!", f"A instalação foi cancelada.")
                            sys.exit()

                        progress_window = Toplevel()
                        progress_window.title("Baixando...")
                        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
                        progress_bar.pack(padx=20, pady=20)
                        
                        # Obtém as dimensões da tela
                        screen_width = progress_window.winfo_screenwidth()
                        screen_height = progress_window.winfo_screenheight()

                        # Calcula a posição x e y da janela de loading
                        x = int((screen_width / 2) - 150)
                        y = int((screen_height / 2) - 50)

                        progress_window.geometry(f"+{x}+{y}")

                        download_success = download_file(url, f"{install_dir}/{file_name}", progress_bar)

                        progress_window.destroy()
                        if download_success:
                            messagebox.showinfo("Download Concluído", f"O arquivo {file_name} foi baixado com sucesso.")
                        else:
                            messagebox.showerror("Erro de Download", "Não foi possível baixar o arquivo.")
                        
                        sys.exit()

                    url = urlDownload
                    file_name = f'macsetup.exe'
                    
                    show_download_progress(url, file_name)
                else:
                    messagebox.showwarning(f"Versão atual: {version}", f"Você está usando uma versão antiga do aplicativo!\nNova versão disponível: {content}")

        else:
            messagebox.showerror("Erro", f"Erro ao verificar a versão mais recente: {response.status_cod}")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível verificar novas versões do aplicativo, parece que você está sem conexão.")
