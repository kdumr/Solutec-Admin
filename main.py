import tkinter
import pyautogui
import pyperclip
import pynput
import time
import threading
import requests
import customtkinter
import json
from loading import *
from pynput.keyboard import Key, Listener
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter import messagebox
from conection import *
from editarcpe import *

from api import urlLicense, urlInfoLicense, urlCreate, urlInfo, usuario, senha, endpoint


with open('config.json', 'r') as arquivo:
    config = json.load(arquivo)
version = config['version']
icone = "icone.ico"
titulo = f"Solutec Admin - Versão: {version}"

# URL do arquivo a ser baixado
urlDownload = 'https://raw.githubusercontent.com/kdumr/Solutec-Admin/main/macsetup.exe'

urlConfig = 'https://raw.githubusercontent.com/kdumr/Solutec-Admin/main/config.json'

class Main:
    def main():
        window = tkinter.Tk()
        window.title(titulo)
        window.geometry('350x380')
        window.wm_minsize(350, 380)
        window.iconbitmap(icone)
        window.configure(bg='#333333')
        

        # Pagina de Colar Macs
        colarmac_frame = tkinter.Frame(bg='#333333')
        
        texto1 = tkinter.Label(colarmac_frame, text="Use a [END] para colar os mac's\nem sequência", bg='#333333', fg="white", font=("Arial", 11))
        texto2 = tkinter.Label(colarmac_frame, text="Use a tecla [HOME] para colar\nUM mac por vez", bg='#333333', fg="white", font=("Arial", 11))
        texto3 = tkinter.Label(colarmac_frame, text="Use a tecla [PAGE DOWN] para colar\nos macs na vertical", bg='#333333', fg="white", font=("Arial", 11))
        texto4 = tkinter.Label(colarmac_frame, text="Use a tecla [DELETE] para\nvoltar ao menu", bg='#333333', fg="red", font=("Arial", 11, "bold"))

        texto1.grid(row=0, column=0, sticky="news", pady=20, padx=0)
        texto2.grid(row=1, column=0, sticky="news", pady=20, padx=0)
        texto3.grid(row=2, column=0, sticky="news", pady=20, padx=0)
        texto4.grid(row=3, column=0, sticky="news", pady=50, padx=0)

        frame = tkinter.Frame(bg='#333333')
        caixa_mac = tkinter.Entry(frame, width=15, font=("Arial", 14))
        caixa_mac.focus_set()

        lista = []
        def cancelar(key):
            if key == Key.home:
                return False

        def show(key):
            if key == Key.home:
                # Bloquear Mouse
                i = 0
                while True:
                    pyperclip.copy(lista[i])
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                    i += 1
                    if i == len(lista):
                        break
                    else:
                        with Listener(on_press=cancelar) as listener:
                            listener.join()
                messagebox.showinfo("OK", "Os MAC's foram colados com sucesso")
                return False
                
            if key == Key.end:
                # Bloquear Mouse   
                original_position = pyautogui.position()
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(-100, -100)
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey(',')
                pyautogui.hotkey('enter')
                # Desbloquear Mouse
                mouse_listener.stop()
                pyautogui.moveTo(original_position)
                pyautogui.FAILSAFE = True
                messagebox.showinfo("OK", "Os MAC's foram colados com sucesso")
                return False
            
            if key == Key.delete:
                return False
        
            if key == Key.page_down:
                # Bloquear Mouse
                original_position = pyautogui.position()
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(-100, -100)
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                # Desbloquear Mouse
                mouse_listener.stop()
                pyautogui.moveTo(original_position)
                pyautogui.FAILSAFE = True
                messagebox.showinfo("OK", "Os MAC's foram colados com sucesso")
                return False

        def send(event=None):
            textInput = caixa_mac.get().replace(":", "").replace("-","")
            if len(textInput) != 12:
                messagebox.showerror("Erro", "Texto deve ter no máximo 12 caracteres")
                caixa_mac.delete(0, END)
            else:
                mac = '{}:{}:{}:{}:{}:{}'.format(textInput[:2], textInput[2:4], textInput[4:6], textInput[6:8], textInput[8:10], textInput[10:])
                if mac in lista:
                    messagebox.showerror("Erro", "Este MAC já está na lista")
                    caixa_mac.delete(0, END)
                else:
                    lista.append(mac)
                    caixa_mac.delete(0, END)
                    display_text.config(state="normal")
                    totalMac_label.config(text=f"MAC's registrados: {len(lista)}")
                    display_text.delete(1.0, END)
                    for item in lista:
                        display_text.insert(END, str(item) + "\n")
                    display_text.config(state="disabled")
        def remove(event=None):
            textInput = caixa_apagarmac.get().replace(":", "").replace("-","")
            mac = '{}:{}:{}:{}:{}:{}'.format(textInput[:2], textInput[2:4], textInput[4:6], textInput[6:8], textInput[8:10], textInput[10:])
            if mac in lista:
                lista.remove(mac)
                caixa_apagarmac.delete(0, END)
                totalMac_label.config(text=f"MAC's registrados: {len(lista)}")
                display_text.config(state="normal")
                display_text.delete(1.0, END)
                display_text.config(state="disabled")
                for item in lista:
                    display_text.config(state="normal")
                    display_text.insert(END, str(item) + "\n")
                    display_text.config(state="disabled")
            else:
                messagebox.showerror("Erro", "Este MAC não existe na lista!")
                caixa_apagarmac.delete(0, END)

        def limparLista():
            lista.clear()
            display_text.config(state="normal")
            display_text.delete(1.0, END)
            display_text.config(state="disabled")
            totalMac_label.config(text=f"MAC's registrados: {len(lista)}")

        caixa_mac.bind("<Return>", send)

        def colarMac():
            if lista != []:
                frame.pack_forget()
                colarmac_frame.pack()
                t = threading.Thread(target=start_listener)
                t.start()
            else:
                messagebox.showerror(title="Error", message="A lista de MAC está vazia.")

        def start_listener():
            with Listener(on_press=show) as listener:
                listener.join()
                colarmac_frame.pack_forget()
                frame.pack()
        def apiError(erro=""):
            messagebox.showerror("Error", f"Houve um erro de conexão com a API:\n{erro}")
        def login():
            global usuario
            global senha
            if usuario == "" and senha == "":
                def logar(user, passw):
                    try:
                        responseLicense = requests.get(f"https://flashman.gigalink.net.br/api/v2/device/update/", auth=(user, passw)).status_code
                        if responseLicense == 401:
                            messagebox.showerror("Error", "Usuário ou senha inválidos\n(Ou talvez você não tenha permissão para acessar a API)")
                        elif responseLicense == 404:
                            global usuario
                            global senha
                            usuario = user
                            senha = passw
                            messagebox.showinfo("Logado!", "Você está logado!")
                            login_window.destroy()
                            gerenciar_cpe()
                    except Exception as erro:
                        apiError(erro)
                        
                login_window = Toplevel(window)
                login_window.configure(bg='#333333')
                login_window.title(f"{titulo} - Login")
                login_window.iconbitmap(icone)
                login_window.geometry('400x250')
                login_window.resizable(False, False)

                loginFrame = Frame(login_window, bg='#333333')
                loginFrame.pack()

                tituloLogin_label = tkinter.Label(loginFrame, text="Login", bg='#333333', fg="#3498db", font=("Arial", 40))
                tituloLogin_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=8)
                tituloLoginDesc_label = tkinter.Label(loginFrame, text="(Utilize suas credenciais de login do Flashman)", bg='#333333', fg="#3498db", font=("Arial", 10))
                tituloLoginDesc_label.grid(row=1, column=0, columnspan=2, sticky="news", pady=5)

                username_Label = tkinter.Label(loginFrame, text="Usuário:", bg='#333333', fg="#FFFFFF", font=("Arial", 13))
                username_Label.grid(row=2, column=0, sticky="w", pady=0)
                username_entry = Entry(loginFrame, width=20, font=("Arial", 13))
                username_entry.grid(row=2, column=1, sticky="w", pady=10)
                
                senha_Label = tkinter.Label(loginFrame, text="Senha:", bg='#333333', fg="#FFFFFF", font=("Arial", 13))
                senha_Label.grid(row=3, column=0, sticky="w", pady=0)
                senha_entry = Entry(loginFrame, width=20, show="*", font=("Arial", 13))
                senha_entry.grid(row=3, column=1, sticky="w", pady=10)


                botao_entrar = Button(loginFrame, text="LOGAR", bg="#3498db", fg="#FFFFFF", font=("Arial", 16), command=lambda: logar(username_entry.get(), senha_entry.get()))
                botao_entrar.grid(row=4, column=0, columnspan=2)
            else:
                gerenciar_cpe()

        # Segunda janela (Gerenciar CPE)
        
        def gerenciar_cpe():
            def display():
                try:
                    displayLCPE_text.delete(0.1, END)
                    displayLStatus_text.delete(0.1, END)
                    displayLLicense_text.delete(0.1, END)
                    for i in range(len(lista)):
                        payloadLicense = {'id': lista[i]}
                        response = requests.get(f'{urlInfo}{lista[i]}', auth=(usuario, senha))
                        responseLicense = requests.put(urlInfoLicense, auth=(usuario, senha), json=payloadLicense)

                        saida = responseLicense.json().get("status")

                        displayLCPE_text.insert(END, f"{lista[i]}" + "\n")

                        displayLStatus_text.tag_configure("verde", foreground="green")
                        displayLStatus_text.tag_configure("vermelho", foreground="red")
                        displayLStatus_text.tag_configure("amarelo", foreground="yellow")
                        displayLStatus_text.tag_configure("azul", foreground="blue")
                        # Aplica o estilo ao texto
                        displayLLicense_text.tag_configure("verde", foreground="green")
                        displayLLicense_text.tag_configure("vermelho", foreground="red")
                        displayLLicense_text.tag_configure("amarelo", foreground="yellow")
                        displayLLicense_text.tag_configure("azul", foreground="blue")
                        
                        codigo = response.status_code
                        if codigo == 404:
                            displayLStatus_text.insert(END, f"CPE não encontrado" + "\n", "vermelho")
                            cpeNotFound.append(lista[i])
                            displayLLicense_text.insert(END, "Desconhecido" + "\n", "amarelo")
                        elif codigo == 200:
                            displayLStatus_text.insert(END, f"CPE encontrado" + "\n", "verde")

                            if saida == True:
                                displayLLicense_text.insert(END, "Desbloqueado" + "\n", "verde")
                            elif saida == False:
                                saidaLicense = f"Bloqueado"
                                displayLLicense_text.insert(END, "Bloqueado" + "\n", "vermelho")
                            else:
                                if responseLicense.json().get("success") == False:
                                    displayLLicense_text.insert(END, "Não encontrada" + "\n", "vermelho")
                                else:
                                    displayLLicense_text.insert(END, f'{responseLicense.json().get("message")}' + "\n", "vermelho")
                except Exception as erro:
                    apiError(erro)
                    license_window.destroy()
                    window.deiconify()

            def blockLicense():
                global loading_frameBlock
                loading_frameBlock = Frame(license_window, bg="white")
                loading_frameBlock.place(x=0, y=0, relwidth=1, relheight=1)

                lbl = ImageLabel(loading_frameBlock, background="white")
                lbl.pack(expand=True)
                lbl.load('img/loading.gif')

                loading_frameBlock.lift()
                t = threading.Thread(target=blockLicenseDEF)
                t.start()
            def destroy_blockLicense():
                loading_frameBlock.destroy()

            def blockLicenseDEF():
                try:
                    payloadLicense = {'ids': lista,'block': "true"}
                    response = requests.put(urlLicense, auth=(usuario, senha), json=payloadLicense)
                    saidaLicense = response.json().get("success", "Error")
                    codigo = response.status_code
                    display()
                    destroy_blockLicense()
                    block_frame = Frame(license_window, bg="red")
                    block_frame.place(x=0, y=0, relwidth=1, relheight=1)

                    block_label = Label(block_frame, text="Os CPE's foram BLOQUEADOS", font=("Arial", 16), fg="white", bg="red")
                    block_label.pack(expand=True)
                    block_frame.lift()
                    time.sleep(2)
                    block_frame.destroy()
                    
                    return None
                except Exception as erro:
                    apiError(erro)
                    destroy_blockLicense()
            
            def unlockLicense():
                global loading_frameUnlock
                loading_frameUnlock = Frame(license_window, bg="white")
                loading_frameUnlock.place(x=0, y=0, relwidth=1, relheight=1)

                lbl = ImageLabel(loading_frameUnlock, background="white")
                lbl.pack(expand=True)
                lbl.load('img/loading.gif')

                loading_frameUnlock.lift()
                t = threading.Thread(target=unlockLicenseDEF)
                t.start()
            def destroy_unlockLicense():
                loading_frameUnlock.destroy()

            def unlockLicenseDEF():
                try:
                    payloadLicense = {'ids': lista,'block': "false"}
                    response = requests.put(urlLicense, auth=(usuario, senha), json=payloadLicense)
                    saidaLicense = response.json().get("success", "Error")
                    codigo = response.status_code
                    display()
                    destroy_unlockLicense()
                    unlock_frame = Frame(license_window, bg="green")
                    unlock_frame.place(x=0, y=0, relwidth=1, relheight=1)

                    block_label = Label(unlock_frame, text="Os CPE's foram DESBLOQUEADOS", font=("Arial", 16), fg="white", bg="green")
                    block_label.pack(expand=True)
                    unlock_frame.lift()
                    time.sleep(2)
                    unlock_frame.destroy()
                    return None
                except Exception as erro:
                    destroy_unlockLicense()
                    apiError(erro)
            def create():
                global loading_frameCreate
                loading_frameCreate = Frame(license_window, bg="white")
                loading_frameCreate.place(x=0, y=0, relwidth=1, relheight=1)

                lbl = ImageLabel(loading_frameCreate, background="white")
                lbl.pack(expand=True)
                lbl.load('img/loading.gif')

                loading_frameCreate.lift()
                t = threading.Thread(target=createLoading)
                t.start()
            def destroy_createLoading():
                loading_frameCreate.destroy()
            def createLoading():
                    try:
                        displayLCPE_text.delete(0.1, END)
                        for i in range(len(cpeNotFound)):
                            payloadCreate = {"content": {"mac_address": cpeNotFound[i], "pppoe_user": "glnk", "pppoe_password": "gigalinkinet!", "wifi_ssid": "Gigarouter", "wifi_password": "gigarouteractivation", "wifi_channel": "auto", "wifi_band": "auto", "wifi_mode": "11g"}}
                            response = requests.put(urlCreate, auth=(usuario, senha), json=payloadCreate)
                            response.json()
                        display()
                        destroy_createLoading()
                        create_frame = Frame(license_window, bg="green")
                        create_frame.place(x=0, y=0, relwidth=1, relheight=1)

                        block_label = Label(create_frame, text="Os registros dos CPE's foram criados", font=("Arial", 16), fg="white", bg="green")
                        block_label.pack(expand=True)
                        create_frame.lift()
                        time.sleep(2)
                        create_frame.destroy()
                    except Exception as erro:
                        apiError(erro)
                        return None

            if lista == []:
                messagebox.showerror("Erro", "A lista de MAC está vazia.")
            else:
                def abrirJanelaEditarCPE():
                    try:
                        editarCPE(lista, usuario, senha)
                    except Exception as erro:
                        apiError(erro)

                cpeNotFound = []
                def voltar():
                    license_window.destroy()
                    window.deiconify()
                window.withdraw()

                license_window = Toplevel(window)
                license_window.protocol("WM_DELETE_WINDOW", fechar_janela)
                license_window.configure(bg='#333333')
                license_window.title(f"{titulo} - Gerenciar CPE")
                license_window.iconbitmap(icone)
                largura_tela = license_window.winfo_screenwidth()
                altura_tela = license_window.winfo_screenheight()
                largura_janela = int(largura_tela * 0.36)  # 80% da largura da tela
                altura_janela = int(altura_tela * 0.60)  # 60% da altura da tela
                x_janela = int((largura_tela - largura_janela) / 2)  # Centralize na largura da tela
                y_janela = int((altura_tela - altura_janela) / 2)  # Centralize na altura da tela
                license_window.geometry(f"{largura_janela}x{altura_janela}+{x_janela}+{y_janela}")

                license_window.minsize(width=largura_janela, height=altura_janela)

                licenseFrame = Frame(license_window, bg='#333333')
                licenseFrameDisplay = Frame(licenseFrame, bg='#333333')
                licenseFrame.pack()
                

                tituloL_label = tkinter.Label(licenseFrame, text="Gerenciar CPE", bg='#333333', fg="#3498db", font=("Arial", 15))
                tituloL_label.pack()

                licenseFrameDisplay.pack()

                cpeText = Label(licenseFrameDisplay, text="MAC do CPE", bg='#333333', fg="#3498db", font=("Arial", 12))
                cpeText.grid(row=0, column=0, sticky="n")
                statusText = Label(licenseFrameDisplay, text="Status do CPE", bg='#333333', fg="#3498db", font=("Arial", 12))
                statusText.grid(row=0, column=1, sticky="n")
                licenseText = Label(licenseFrameDisplay, text="Status da Licença", bg='#333333', fg="#3498db", font=("Arial", 12))
                licenseText.grid(row=0, column=2, sticky="n")

                displayLCPE_text = Text(licenseFrameDisplay, width=20, height=15, bg="#000000", fg="white", font=("Courier New", 10))
                displayLCPE_text.grid(row=1, column=0)

                displayLStatus_text = Text(licenseFrameDisplay, width=20, height=15, bg="#000000", fg="white", font=("Courier New", 10))
                displayLStatus_text.grid(row=1, column=1, padx=5)

                displayLLicense_text = Text(licenseFrameDisplay, width=20, height=15, bg="#000000", fg="white", font=("Courier New", 10))
                displayLLicense_text.grid(row=1, column=2)

                # Crie um frame para os botões
                buttonFrame = Frame(license_window, bg="white")
                buttonFrame.pack()

                # Crie os botões
                botao_desbloquear = Button(buttonFrame, text="Desbloquear Licença", bg="#2ecc71", fg="#FFFFFF", font=("Arial", 16), command=unlockLicense)
                botao_desbloquear.pack(side=LEFT)

                botao_bloquear = Button(buttonFrame, text="Bloquear Licença", bg="#e74c3c", fg="#FFFFFF", font=("Arial", 16), command=blockLicense)
                botao_bloquear.pack(side=RIGHT)

                botao_editar = Button(license_window, width=30, text="Editar CPE", bg="#3498db", fg="#FFFFFF", font=("Arial", 16), command=abrirJanelaEditarCPE)
                botao_editar.pack(pady=10)
                botao_voltar = Button(license_window, width=30, text="Voltar para o menu", bg="#3498db", fg="#FFFFFF", font=("Arial", 16), command=voltar)
                botao_voltar.pack(pady=10)

                display()
                if len(cpeNotFound) > 0:
                    ask = messagebox.askyesno(titulo, "Deseja criar um registro para os CPE's não encontrados?")
                    if ask:
                        create()
                    else:
                        display()

        # Creating widgets
        titulo_label = tkinter.Label(frame, text="Solutec Admin", bg='#333333', fg="#3498db", font=("Arial", 15))
        digiteMac_label = tkinter.Label(frame, text="Digite o Mac:", bg='#333333', fg="#FFFFFF", font=("Arial", 13))

        frameDisplay = Frame(frame)
        display_text = Text(frameDisplay, width=20, height=5, font=("Arial", 13))
        display_text.pack(side=LEFT, fill=BOTH, expand=True)
        # Cria a barra de rolagem vertical
        scrollbar = Scrollbar(frameDisplay, orient="vertical", command=display_text.yview)

        scrollbar.pack(side=RIGHT, fill=Y)
        display_text.config(yscrollcommand=scrollbar.set)

        display_label = tkinter.Label(frame, text="Lista de MAC's", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        totalMac_label = tkinter.Label(frame, text=f"MAC's registrados: {len(lista)}", bg='#333333', fg="#FFFFFF", font=("Arial", 13))
        apagarmac_label = tkinter.Label(frame, text="Apagar MAC:", bg='#333333', fg="#FFFFFF", font=("Arial", 13))
        caixa_apagarmac = tkinter.Entry(frame, width=15, font=("Arial", 14))
        caixa_apagarmac.bind("<Return>", remove)
        apagarLista_button = tkinter.Button(frame, text="Apagar lista", bg="#e74c3c", fg="#FFFFFF", font=("Arial", 16), command=limparLista)
        colarMac_button = tkinter.Button(frame, text="Colar MAC's", bg="#3498db", fg="#FFFFFF", font=("Arial", 16), command=colarMac)
        licenca_button = tkinter.Button(frame, text="Gerenciar CPE", bg="#3498db", fg="#FFFFFF", font=("Arial", 16), command=login)

        # Placing widgets on the screen
        titulo_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=10)

        digiteMac_label.grid(row=1, column=0, sticky="we")
        caixa_mac.grid(row=1, column=1, padx=0, sticky="news")

        display_label.grid(row=2, column=0, columnspan=2, sticky="news")
        
        frameDisplay.grid(row=3, column=0, columnspan=2, sticky="news")
        
        totalMac_label.grid(row=4, column=0, columnspan=2, sticky="news")

        apagarmac_label.grid(row=5, column=0, sticky="we") 
        caixa_apagarmac.grid(row=5, column=1, padx=0, pady=10, sticky="news") 
        apagarLista_button.grid(row=6, column=0, columnspan=2, sticky="news", pady=5)
        
        colarMac_button.grid(row=7, column=0, columnspan=1, pady=1)
        licenca_button.grid(row=7, column=1, columnspan=1, pady=1, sticky="e")

        #alterar_licenca()
        frame.pack()
        colarmac_frame.pack_forget()
        def fechar_janela():
            # Incluir código para encerrar o programa aqui
            print("Fechou")
            window.destroy()  # Fechar a janela principal do tkinter
        window.mainloop()

if __name__ == "__main__":
    try:
        conectar(urlConfig, urlDownload, version, titulo)
        # Executa o código
        Main.main()
    except Exception as e:
        # Cria um arquivo .txt e salva o erro do aplicativo
        messagebox.showerror("Erro", f"Houve um erro! {e}")