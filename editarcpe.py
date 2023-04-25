import requests
import json
from pynput.keyboard import Key, Listener
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter import messagebox
from conection import *
from api import urlLicense, urlInfoLicense, urlCreate, urlInfo, usuario, senha, endpoint, urlStatus, urlCpeinfo, urlResetarCPE, urlAtualizarCPE
import customtkinter
import time
import threading
from tktooltip import ToolTip
from main import urlConfig

fundoDisplay = "#1f2124"

customtkinter.set_default_color_theme("blue")

def editarCPE(lista, usuario, senha):
    try:
        window = customtkinter.CTk()
        window.geometry('315x350')
        window.configure(bg='#333333')
        window.withdraw()
        def fechar():
            license_window.destroy()
            window.destroy()
        license_window = Toplevel(window)
        
        license_window.configure(bg='#333333')
        license_window.title(f"Editar CPE")

        response = requests.get(urlConfig)
        if response.status_code == 200:
                # Se a resposta foi bem-sucedida, obter o conteúdo da resposta
                config = json.loads(response.text)
                firmwareRequestsConfig = config["firmwareAtual"]
        else:
            messagebox.showwarning(f'Erro {response.status_code}', "Não foi possível identificar o firmware mais recente disponível\nÉ recomendado reiniciar o programa")

        largura_tela = license_window.winfo_screenwidth()
        altura_tela = license_window.winfo_screenheight()
        largura_janela = int(largura_tela * 0.60)  # 80% da largura da tela
        altura_janela = int(altura_tela * 0.50)  # 60% da altura da tela
        x_janela = int((largura_tela - largura_janela) / 2)  # Centralize na largura da tela
        y_janela = int((altura_tela - altura_janela) / 2)  # Centralize na altura da tela
        license_window.geometry(f"{largura_janela}x{altura_janela}+{x_janela}+{y_janela}")
        license_window.minsize(width=largura_janela, height=altura_janela)
        licenseFrame = Frame(license_window, bg=fundoDisplay, highlightthickness=0)
        #licenseFrameDisplay = Frame(licenseFrame, bg='white', width=10, height=10)
        licenseFrame.pack(fill="x")
        #licenseFrameDisplay.pack()

        # Criação de um Canvas com scrollbar
        canvas = Canvas(licenseFrame, bg=fundoDisplay, highlightthickness=0)

        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(licenseFrame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        licenseFrameDisplay = Frame(canvas, bg=fundoDisplay, width=10, height=10)
        canvas.create_window((0, 0), window=licenseFrameDisplay, anchor='nw')

        # Configuração do canvas para expandir com o tamanho do conteúdo
        licenseFrameDisplay.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        licenseFrameDisplay.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        # Criação dos cabeçalhos da tabela
        label_cpe = Label(licenseFrameDisplay, text="CPE", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
        label_info = Label(licenseFrameDisplay, text="Info", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
        label_status = Label(licenseFrameDisplay, text="Status", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
        label_firmware = Label(licenseFrameDisplay, text="Firmware", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)

        # Posicionamento dos cabeçalhos da tabela com o gerenciador de layout grid
        label_cpe.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        label_info.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        label_status.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        label_firmware.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        cpeNotFound = []

        def cpe_click(cpe):
            if cpe in cpeNotFound:
                messagebox.showerror("Erro", "Este CPE não foi encontrado no Flashman.")
            else:
                    responseLicenseStatus = requests.get(f'{urlCpeinfo}{cpe}', auth=(usuario, senha))
                    apiJson = responseLicenseStatus.json()
                    
                    identificador_unico = apiJson.get("_id")
                    ip_wan = apiJson.get("wan_ip")
                    ip_publico = apiJson.get("ip")
                    firmware_instalado = apiJson.get("installed_release")
                    use_tr069 = apiJson.get("use_tr069")
                    modo_operacao = apiJson.get("bridge_mode_enabled")
                    tipo_conexao = apiJson.get("connection_type")
                    mesh_mode = apiJson.get("mesh_mode")
                    pppoe_user = apiJson.get("pppoe_user")
                    pppoe_pass= apiJson.get("pppoe_password")

                    canal_wifi24ghz = apiJson.get("wifi_channel")
                    wifi_ModoOperacao24 = apiJson.get("wifi_mode")
                    ssid_wifi24ghz = apiJson.get("wifi_ssid")
                    senha_wifi24ghz = apiJson.get("wifi_password")
                    wifi_potenciaSinal24 = apiJson.get("wifi_power")

                    canal_wifi5ghz = apiJson.get("wifi_channel_5ghz")
                    wifi_ModoOperacao5 = apiJson.get("wifi_mode_5ghz")
                    ssid_wifi5ghz = apiJson.get("wifi_ssid_5ghz")
                    senha_wifi5ghz = apiJson.get("wifi_password_5ghz")
                    wifi_potenciaSinal5 = apiJson.get("wifi_power_5ghz")
                    capable5ghz = apiJson.get("wifi_is_5ghz_capable")

                    cpeInfo_window = Toplevel(window)
                    cpeInfo_window.configure(bg="#333333")
                    cpeInfo_window.title("Informações do CPE")
                    largura_tela2 = license_window.winfo_screenwidth()
                    altura_tela2 = license_window.winfo_screenheight()
                    largura_janela2 = int(largura_tela2 * 0.70)  # 80% da largura da tela
                    altura_janela2 = int(altura_tela2 * 0.65)  # 60% da altura da tela
                    x_janela2 = int((largura_tela2 - largura_janela2) / 2)  # Centralize na largura da tela
                    y_janela2 = int((altura_tela2 - altura_janela2) / 2)  # Centralize na altura da tela
                    cpeInfo_window.geometry(f"{largura_janela2}x{altura_janela2}+{x_janela2}+{y_janela2}")
                    cpeFrame = Frame(cpeInfo_window, bg="white", highlightthickness=0)
                    cpeFrame.pack()
                    
                    # Criação dos labels
                    responseLicenseOnOff = requests.put(f'{urlStatus}{cpe}/upstatus', auth=(usuario, senha))
                    if responseLicenseOnOff.json().get("success") == True:
                        status_data = Label(cpeFrame, text="Online", foreground="white", bg="#00bd19", relief="flat", width=15, font=("Roboto", 10))
                    elif responseLicenseOnOff.json().get("success") == False:
                        status_data = Label(cpeFrame, text="Offline", foreground="#404040", relief="flat", width=15, font=("Roboto", 10))
                    else:
                        if responseLicenseOnOff.json().get("success") == False:
                            status_data = Label(cpeFrame, text="Não encontrado", foreground="#404040", relief="flat", width=15, font=("Roboto", 10))
                        else:
                            status_data = Label(cpeFrame, text=f'{responseLicenseOnOff.json().get("message")}', foreground="red", relief="flat", width=15, font=("Roboto", 10))
                    if use_tr069 == True:
                        use_tr069_label = Label(cpeFrame, text="TR-069", width=10, fg="white", bg="#4db6ac", font=("Roboto", 10))
                    else:
                        use_tr069_label = Label(cpeFrame, text="Firmware", width=10, fg="white", background="#4db6ac", font=("Roboto", 10))
                    status_label = Label(cpeFrame, text="Status", relief="flat", width=15, pady=5, font=("Roboto", 10))
                    #usuario_pppoe_label = Label(cpeFrame, text="Usuário PPPoE", relief="flat", width=20, pady=5, font=("Roboto", 10))
                    identificador_unico_label = Label(cpeFrame, text="Identificador único", relief="flat", width=20, pady=5, font=("Roboto", 10))
                    ip_wan_label = Label(cpeFrame, text="IP WAN", relief="flat", width=15, pady=5, font=("Roboto", 10))
                    ip_publico_label = Label(cpeFrame, text="IP público", relief="flat", width=15, pady=5, font=("Roboto", 10))
                    firmware_instalado_label = Label(cpeFrame, text="Firmware instalado", relief="flat", width=17, pady=5, font=("Roboto", 10))

                    titulo_Modo = Label(cpeFrame, text="Modo", relief="flat", width=0, pady=10, font=("Roboto", 13))
                    modo_operacao_label = Label(cpeFrame, text="Modo de operação", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    mesh_mode_label = Label(cpeFrame, text="Mesh", relief="flat", width=17, pady=5, font=("Roboto", 10)) 
                    tipo_conexao_label = Label(cpeFrame, text="Tipo de conexão", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    pppoe_user_label = Label(cpeFrame, text="Usuário PPPoE", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    pppoe_pass_label = Label(cpeFrame, text="Senha PPPoE", relief="flat", width=17, pady=5, font=("Roboto", 10))

                    titulo_wifi = Label(cpeFrame, text="Wi-Fi | 2.4 Ghz", relief="flat", width=0, pady=10, font=("Roboto", 13))

                    canal_wifi_label24ghz = Label(cpeFrame, text="Canal do Wifi", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    largura_banda_label24ghz = Label(cpeFrame, text="Largura de banda", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    modoOperacao_label24ghz = Label(cpeFrame, text="Modo de operação", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    ssid_wifi_label24ghz = Label(cpeFrame, text="SSID do Wi-Fi", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    senha_wifi_label24ghz = Label(cpeFrame, text="Senha do Wi-Fi", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    potencia_sinal_label24ghz = Label(cpeFrame, text="Potência do sinal", relief="flat", width=17, pady=5, font=("Roboto", 10))

                    titulo_wifi5g = Label(cpeFrame, text="Wi-Fi | 5 Ghz", relief="flat", width=0, pady=10, font=("Roboto", 13))

                    canal_wifi_label5ghz = Label(cpeFrame, text="Canal do Wifi", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    largura_banda_label5ghz = Label(cpeFrame, text="Largura de banda", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    modoOperacao_label5ghz = Label(cpeFrame, text="Modo de operação", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    ssid_wifi_label5ghz = Label(cpeFrame, text="SSID do Wi-Fi", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    senha_wifi_label5ghz = Label(cpeFrame, text="Senha do Wi-Fi", relief="flat", width=17, pady=5, font=("Roboto", 10))
                    potencia_sinal_label5ghz = Label(cpeFrame, text="Potência do sinal", relief="flat", width=17, pady=5, font=("Roboto", 10))


                    def verificar_opcao_comboOperacao(*args):
                        # Função de callback para verificar a opção selecionada no combobox 1
                        if comboOperacao.get() == 'Modo Bridge / Modo AP':
                            # Se 'Opção 1' estiver selecionada, desabilita o combobox 2
                            comboConexao['state'] = 'disabled'
                            ToolTip(comboConexao, "Este CPE está em modo bridge! Para alterar os dados da WAN, retire o CPE do modo bridge primeiro.")
                        else:
                            # Caso contrário, habilita o combobox 2
                            comboConexao['state'] = 'normal'
                    comboOperacao = ttk.Combobox(cpeFrame, state='readonly')
                    comboOperacao['values'] = ('Modo Roteador', 'Modo Bridge / Modo AP')
                    if modo_operacao == False:
                        comboOperacao.current(0)
                    elif modo_operacao == True:
                        comboOperacao.current(1)
                    comboOperacao.bind('<<ComboboxSelected>>', verificar_opcao_comboOperacao)

                    comboMesh = ttk.Combobox(cpeFrame, state='readonly')
                    if use_tr069 == False:
                        comboMesh['values'] = ('Desabilitado', 'Cabo', 'Cabo e Wi-Fi 2.4 GHz', 'Cabo e Wi-Fi 5.0 GHz', 'Cabo e ambos Wi-Fi')
                        if mesh_mode == 0:
                            comboMesh.current(0)
                        elif mesh_mode == 1:
                            comboMesh.current(1)
                        elif mesh_mode == 2:
                            comboMesh.current(2)
                        elif mesh_mode == 3:
                            comboMesh.current(3)
                        elif mesh_mode == 4:
                            comboMesh.current(4)
                    else:
                        comboMesh['values'] = ('Desabilitado', 'Cabo')
                        if mesh_mode == 0:
                            comboMesh.current(0)
                        elif mesh_mode == 1:
                            comboMesh.current(1)

                    comboConexao = ttk.Combobox(cpeFrame, state='readonly')
                    comboConexao['values'] = ('PPPoE', 'DHCP')
                    if tipo_conexao == "pppoe":
                        comboConexao.current(0)
                    elif tipo_conexao == "dhcp":
                        comboConexao.current(1)

                    comboCanalwifi24 = ttk.Combobox(cpeFrame, state='readonly')
                    comboCanalwifi24['values'] = ('auto', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')
                    if canal_wifi24ghz == "auto":
                        comboCanalwifi24.current(0)
                    elif canal_wifi24ghz == "1":
                        comboCanalwifi24.current(1)
                    elif canal_wifi24ghz == "2":
                        comboCanalwifi24.current(2)
                    elif canal_wifi24ghz == "3":
                        comboCanalwifi24.current(3)
                    elif canal_wifi24ghz == "4":
                        comboCanalwifi24.current(4)
                    elif canal_wifi24ghz == "5":
                        comboCanalwifi24.current(5)
                    elif canal_wifi24ghz == "6":
                        comboCanalwifi24.current(6)
                    elif canal_wifi24ghz == "7":
                        comboCanalwifi24.current(7)
                    elif canal_wifi24ghz == "8":
                        comboCanalwifi24.current(8)
                    elif canal_wifi24ghz == "9":
                        comboCanalwifi24.current(9)
                    elif canal_wifi24ghz == "10":
                        comboCanalwifi24.current(10)
                    elif canal_wifi24ghz == "11":
                        comboCanalwifi24.current(11)

                    comboCanalwifi5 = ttk.Combobox(cpeFrame, state='readonly')
                    comboCanalwifi5['values'] = ('auto', '36', '40', '44', '48', '52', '60', '64', '149', '153', '157', '161', '165')
                    if capable5ghz == True:  
                        if canal_wifi5ghz == "auto":
                            comboCanalwifi5.current(0)
                        elif canal_wifi5ghz == "36":
                            comboCanalwifi5.current(1)
                        elif canal_wifi5ghz == "40":
                            comboCanalwifi5.current(2)
                        elif canal_wifi5ghz == "44":
                            comboCanalwifi5.current(3)
                        elif canal_wifi5ghz == "48":
                            comboCanalwifi5.current(4)
                        elif canal_wifi5ghz == "52":
                            comboCanalwifi5.current(5)
                        elif canal_wifi5ghz == "60":
                            comboCanalwifi5.current(6)
                        elif canal_wifi5ghz == "64":
                            comboCanalwifi5.current(7)
                        elif canal_wifi5ghz == "149":
                            comboCanalwifi5.current(8)
                        elif canal_wifi5ghz == "153":
                            comboCanalwifi5.current(9)
                        elif canal_wifi5ghz == "157":
                            comboCanalwifi5.current(10)
                        elif canal_wifi5ghz == "161":
                            comboCanalwifi5.current(11)
                        elif canal_wifi5ghz == "165":
                            comboCanalwifi5.current(12)
                    else:
                        comboCanalwifi5 = ttk.Combobox(cpeFrame, state='disable')

                    comboLargurabanda24 = ttk.Combobox(cpeFrame, state='disable')
                    comboLargurabanda24['values'] = ('auto', '40 MHz', '20 MHz')
                    comboLargurabanda24.current(0)

                    comboLargurabanda5 = ttk.Combobox(cpeFrame, state='disable')
                    comboLargurabanda5['values'] = ('auto', '40 MHz', '20 MHz')
                    if capable5ghz == True:
                        comboLargurabanda5.current(0)
                    else:
                        comboLargurabanda5 = ttk.Combobox(cpeFrame, state='disable')

                    comboModoOperacao24 = ttk.Combobox(cpeFrame)
                    comboModoOperacao24['values'] = ('BGN', 'G')
                    if wifi_ModoOperacao24 == "11n":
                        comboModoOperacao24.current(0)
                    elif wifi_ModoOperacao24 == "11g":
                        comboModoOperacao24.current(1)

                    comboModoOperacao5 = ttk.Combobox(cpeFrame)
                    comboModoOperacao5['values'] = ('AC', 'N')
                    if capable5ghz == True:
                        if wifi_ModoOperacao5 == "11ac":
                            comboModoOperacao5.current(0)
                        elif wifi_ModoOperacao5 == "11na":
                            comboModoOperacao5.current(1)
                    else:
                        comboModoOperacao5 = ttk.Combobox(cpeFrame, state='disable')

                    comboPotenciaSinal24 = ttk.Combobox(cpeFrame, state='readonly')
                    comboPotenciaSinal24['values'] = ('100%', '75%', '50%', '25%')
                    if wifi_potenciaSinal24 == 100:
                        comboPotenciaSinal24.current(0)
                    elif wifi_potenciaSinal24 == 75:
                        comboPotenciaSinal24.current(2)
                    elif wifi_potenciaSinal24 == 50:
                        comboPotenciaSinal24.current(3)
                    elif wifi_potenciaSinal24 == 25:
                        comboPotenciaSinal24.current(4)

                    comboPotenciaSinal5 = ttk.Combobox(cpeFrame, state='readonly')
                    comboPotenciaSinal5['values'] = ('100%', '75%', '50%', '25%')
                    if capable5ghz == True:
                        if wifi_potenciaSinal5 == 100:
                            comboPotenciaSinal5.current(0)
                        elif wifi_potenciaSinal5 == 75:
                            comboPotenciaSinal5.current(2)
                        elif wifi_potenciaSinal5 == 50:
                            comboPotenciaSinal5.current(3)
                        elif wifi_potenciaSinal5 == 25:
                            comboPotenciaSinal5.current(4)
                    else:
                        comboPotenciaSinal5 = ttk.Combobox(cpeFrame, state='disable')

                    pppoe_user_entry = Entry(cpeFrame)
                    pppoe_pass_entry = Entry(cpeFrame)

                    ssid_wifi_entry24ghz = Entry(cpeFrame)
                    senha_wifi_entry24ghz = Entry(cpeFrame)
                    
                    ssid_wifi_entry5ghz = Entry(cpeFrame)
                    senha_wifi_entry5ghz = Entry(cpeFrame)

                    if tipo_conexao == "dhcp":
                        pppoe_user_entry.config(state="disabled")
                        pppoe_pass_entry.config(state="disabled")

                        ToolTip(pppoe_user_entry, "Este CPE está em modo bridge! Para alterar os dados de PPPoE, retire o CPE do modo bridge primeiro.")
                        ToolTip(pppoe_pass_entry, "Este CPE está em modo bridge! Para alterar os dados de PPPoE, retire o CPE do modo bridge primeiro.")

                    pppoe_user_entry.insert(0, pppoe_user)
                    pppoe_pass_entry.insert(0, pppoe_pass)

                    ssid_wifi_entry24ghz.insert(0, ssid_wifi24ghz)
                    senha_wifi_entry24ghz.insert(0, senha_wifi24ghz)
                    if capable5ghz == True:
                        ssid_wifi_entry5ghz.insert(0, ssid_wifi5ghz)
                        senha_wifi_entry5ghz.insert(0, senha_wifi5ghz)
                    else:
                        ssid_wifi_entry5ghz.config(state="disable")
                        senha_wifi_entry5ghz.config(state="disable")


                    #ipv6_enabled_label = Label(cpeFrame, text="Habilitar IPv6", relief="flat", width=17, pady=5, font=("Roboto", 10))

                    # Posicionamento dos labels
                    use_tr069_label.grid(row=1, column=0, padx=10)
                    status_label.grid(row=0, column=1)
                    identificador_unico_label.grid(row=0, column=3)
                    ip_wan_label.grid(row=0, column=4)
                    ip_publico_label.grid(row=0, column=5)
                    firmware_instalado_label.grid(row=0, column=6)
                
                    # Seção Modo

                    titulo_Modo.grid(row=2, column=0, pady=10)

                    modo_operacao_label.grid(row=3, column=1)
                    comboOperacao.grid(row=4, column=1)

                    mesh_mode_label.grid(row=3, column=3)
                    comboMesh.grid(row=4, column=3)

                    tipo_conexao_label.grid(row=3, column=4)
                    comboConexao.grid(row=4, column=4)

                    pppoe_user_label.grid(row=3, column=5)
                    pppoe_user_entry.grid(row=4, column=5)

                    pppoe_pass_label.grid(row=3, column=6)
                    pppoe_pass_entry.grid(row=4, column=6)
                    
                    # Seção Wi-Fi | 2.4 Ghz

                    titulo_wifi.grid(row=5, column=0, pady=10, sticky="nswe")

                    canal_wifi_label24ghz.grid(row=6, column=1)
                    comboCanalwifi24.grid(row=7, column=1)

                    largura_banda_label24ghz.grid(row=6, column=3)
                    comboLargurabanda24.grid(row=7, column=3)

                    modoOperacao_label24ghz.grid(row=6, column=4)
                    comboModoOperacao24.grid(row=7, column=4)
                    
                    ssid_wifi_label24ghz.grid(row=8, column=1)
                    ssid_wifi_entry24ghz.grid(row=9, column=1)

                    senha_wifi_label24ghz.grid(row=8, column=3)
                    senha_wifi_entry24ghz.grid(row=9, column=3)

                    potencia_sinal_label24ghz.grid(row=8, column=4)
                    comboPotenciaSinal24.grid(row=9, column=4)

                    # Seção Wi-Fi | 5 Ghz

                    titulo_wifi5g.grid(row=10, column=0, pady=10, sticky="nswe")

                    canal_wifi_label5ghz.grid(row=11, column=1)
                    comboCanalwifi5.grid(row=12, column=1)

                    largura_banda_label5ghz.grid(row=11, column=3)
                    comboLargurabanda5.grid(row=12, column=3)

                    modoOperacao_label5ghz.grid(row=11, column=4)
                    comboModoOperacao5.grid(row=12, column=4)
                    
                    ssid_wifi_label5ghz.grid(row=13, column=1)
                    ssid_wifi_entry5ghz.grid(row=14, column=1)

                    senha_wifi_label5ghz.grid(row=13, column=3)
                    senha_wifi_entry5ghz.grid(row=14, column=3)

                    potencia_sinal_label5ghz.grid(row=13, column=4)
                    comboPotenciaSinal5.grid(row=14, column=4)
                    
                    
                    # Dados da tabela
                    #usuario_pppoe_data = Label(cpeFrame, text=pppoe_user)
                    identificador_unico_data = Label(cpeFrame, text=identificador_unico, relief="flat", width=20)
                    ip_wan_data = Label(cpeFrame, text=ip_wan, relief="flat", width=15)
                    ip_publico_data = Label(cpeFrame, text=ip_publico, relief="flat", width=15)
                    firmware_instalado_data = Label(cpeFrame, text=firmware_instalado, relief="flat", width=17)

                    # Posicionamento dos dados
                    status_data.grid(row=1, column=1)
                    #usuario_pppoe_data.grid(row=1, column=2)
                    identificador_unico_data.grid(row=1, column=3)
                    ip_wan_data.grid(row=1, column=4)
                    ip_publico_data.grid(row=1, column=5)
                    firmware_instalado_data.grid(row=1, column=6)
                    
        def resetarCPE(cpe):
            responseLicense = requests.put(f'{urlStatus}{cpe}/upstatus', auth=(usuario, senha))
            status = responseLicense.json().get("success")
            if status == True:
                payloadLicense = {
                "content": {
                "bridgeEnabled": 0,
                "mesh_mode": 0,
                "connection_type:": "pppoe",
                "ipv6_enabled": 1,
                "pppoe_user": "glnk",
                "pppoe_password": "gigalinkinet!",
                "wifi_ssid": "Gigarouter",
                "wifi_password": "gigarouteractivation",
                "wifi_channel": "auto",
                "wifi_band": "auto",
                "wifi_power": 100,

                "wifi_ssid_5ghz": "Gigarouter-5GHz",
                "wifi_password_5ghz": "gigarouteractivation",
                "wifi_channel_5ghz": "auto",
                "wifi_band_5ghz": "auto",
                "wifi_power_5ghz": 100,

            }
            }
                responseLicenseReset = requests.put(f'{urlResetarCPE}{cpe}', auth=(usuario, senha), json=payloadLicense)
                
                
                askReset = messagebox.askyesno("?", f"Deseja resetar o CPE: '{cpe}' para as configurações padrões?")
                if askReset:
                    try:
                        message = responseLicenseReset.json().get("message")
                        if message is not None:
                            messagebox.showerror("Erro", f"{message}")
                        else:
                            messagebox.showinfo("OK", f"O CPE: '{cpe}' foi resetado com sucesso!")
                    except Exception as e:
                        messagebox.showerror("Erro!", f"Ocorreu um erro:\n {e}")
            else:
                messagebox.showerror("Erro", "O CPE não está online!")

        def mudarDHCP(cpe):
            responseLicense = requests.put(f'{urlStatus}{cpe}/upstatus', auth=(usuario, senha))
            status = responseLicense.json().get("success")
            if status == True:
                payloadLicenseDHCP = { "content": { 'mesh_mode': 0, "bridgeEnabled": 0, 'connection_type': 'dhcp' }}
                
                askDhcp = messagebox.askyesno("?", f"Deseja alterar o CPE: '{cpe}' para as DHCP?")
                if askDhcp:
                    try:
                        responseLicenseDHCP = requests.put(f'{urlResetarCPE}{cpe}', auth=(usuario, senha), json=payloadLicenseDHCP)
                        responseLicenseDHCPStatus = requests.get(f'{urlResetarCPE}{cpe}', auth=(usuario, senha))
                        message = responseLicenseDHCP.json().get("message")
                        if message is not None:
                            messagebox.showerror("Erro", f"{message}")
                        elif responseLicenseDHCPStatus.json().get("connection_type") != "dhcp":
                            messagebox.showerror("Erro", f"Houve um erro e o CPE não foi alterado para dhcp")
                        else:
                            messagebox.showinfo("OK", f"O CPE: '{cpe}' foi alterado para DHCP com sucesso!")
                    except Exception as e:
                        messagebox.showerror("Erro!", f"Ocorreu um erro:\n {e}")
            else:
                messagebox.showerror("Erro", "O CPE não está online!")

        def atualizarFirmware(cpe):
            responseLicense = requests.put(f'{urlStatus}{cpe}/upstatus', auth=(usuario, senha))
            status = responseLicense.json().get("success")
            if status == True:
                askAtualizarFirmware = messagebox.askyesno("?", f"Deseja atualizar o firmware do CPE: '{cpe}' para: {firmwareRequestsConfig}")
                if askAtualizarFirmware:
                    payloadFirmware = { 'do_update': 'true' }
                    responseFirmware = requests.put(f'{urlAtualizarCPE}{cpe}/{firmwareRequestsConfig}', auth=(usuario, senha), json=payloadFirmware)
                    if responseFirmware.json().get("success") == False:
                        messagebox.showerror("Erro", f"Não foi possível atualizar o firmware do CPE: {cpe}")
                    else:
                        messagebox.showinfo("OK", f"O firmware do CPE: {cpe} está sendo atualizado para: {firmwareRequestsConfig}\nNão desligue ou desconecte o CPE da rede antes do mesmo reiniciar.")  
            else:
                messagebox.showerror("Erro", "O CPE não está online!")
        for i in range(len(lista)):
            
            responseLicense = requests.put(f'{urlStatus}{lista[i]}/upstatus', auth=(usuario, senha))
            responseLicenseStatus = requests.get(f'{urlCpeinfo}{lista[i]}', auth=(usuario, senha))

            message = responseLicense.json().get("message")
            status = responseLicense.json().get("success")

            botao = customtkinter.CTkButton(licenseFrameDisplay, text=lista[i], command=lambda i=lista[i]: cpe_click(i))
            botaoResetarCPE = customtkinter.CTkButton(licenseFrameDisplay, text="Resetar CPE", command=lambda i=lista[i]: resetarCPE(i))
            botaoMudarDHCP = customtkinter.CTkButton(licenseFrameDisplay, text="Mudar para DHCP", command=lambda i=lista[i]: mudarDHCP(i))


            label_cpe = Label(licenseFrameDisplay, text=lista[i])
            if message is not None and "4644" in message:
                label_info = Label(licenseFrameDisplay, text="CPE Não encontrado", foreground="red", background=fundoDisplay)
                cpeNotFound.append(lista[i])
                label_status = Label(licenseFrameDisplay, text="Offline", foreground="#e8e8e8", background=fundoDisplay)
            else:
                label_info = Label(licenseFrameDisplay, text="CPE Encontrado", foreground="green", background=fundoDisplay)
                label_firmwareInfo = Label(licenseFrameDisplay, text=responseLicenseStatus.json().get("release"), foreground="#e8e8e8", background=fundoDisplay)
                if status == True:
                    
                    if responseLicenseStatus.json().get("use_tr069") == True:
                        botaoMudarDHCP.configure(state="disabled")
                        label_firmwareInfo = Label(licenseFrameDisplay, text="TR-069", foreground="#e8e8e8", background=fundoDisplay)

                    label_status = Label(licenseFrameDisplay, text="Online", foreground="#00ff00", background=fundoDisplay)
                    botaoResetarCPE.grid(row=i+1, column=4, padx=5, pady=5, sticky="w")
                    botaoMudarDHCP.grid(row=i+1, column=5, padx=5, pady=5, sticky="w")
                    botaoAtualizarFirmware = customtkinter.CTkButton(licenseFrameDisplay, text="Atualizar Firmware", command=lambda i=lista[i]: atualizarFirmware(i))
                    botaoAtualizarFirmware.grid(row=i+1, column=6, padx=5, pady=5, sticky="w")
                    
                elif status == False:
                    label_status = Label(licenseFrameDisplay, text="Offline", foreground="#e8e8e8", background=fundoDisplay)
                else:
                    if responseLicense.json().get("success") == False:
                        label_status = Label(licenseFrameDisplay, text="Não encontrado", foreground="#e8e8e8", background=fundoDisplay)
                    else:
                        label_status = Label(licenseFrameDisplay, text=f'{responseLicense.json().get("message")}', foreground="red", background=fundoDisplay)

            # Posicionamento dos labels das linhas da tabela com o gerenciador de layout grid
            botao.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
            label_info.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
            label_status.grid(row=i+1, column=2, padx=5, pady=5, sticky="w")
            label_firmwareInfo.grid(row=i+1, column=3, padx=5, pady=5, sticky="w")
            
        def display():
            time.sleep(1)
            # Criação dos cabeçalhos da tabela
            label_cpe = Label(licenseFrameDisplay, text="CPE", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
            label_info = Label(licenseFrameDisplay, text="Info", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
            label_status = Label(licenseFrameDisplay, text="Status", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
            label_firmware = Label(licenseFrameDisplay, text="Firmware", font=("Helvetica", 12, "bold"), fg="white", bg=fundoDisplay)
 
            # Posicionamento dos cabeçalhos da tabela com o gerenciador de layout grid
            label_cpe.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            label_info.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            label_status.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            label_firmware.grid(row=0, column=3, padx=5, pady=5, sticky="w")
            for i in range(len(lista)):
            
                responseLicense = requests.put(f'{urlStatus}{lista[i]}/upstatus', auth=(usuario, senha))
                responseLicenseStatus = requests.get(f'{urlCpeinfo}{lista[i]}', auth=(usuario, senha))

                message = responseLicense.json().get("message")
                status = responseLicense.json().get("success")

                botao = customtkinter.CTkButton(licenseFrameDisplay, text=lista[i], command=lambda i=lista[i]: cpe_click(i))
                botaoResetarCPE = customtkinter.CTkButton(licenseFrameDisplay, text="Resetar CPE", command=lambda i=lista[i]: resetarCPE(i))
                botaoMudarDHCP = customtkinter.CTkButton(licenseFrameDisplay, text="Mudar para DHCP", command=lambda i=lista[i]: mudarDHCP(i))


                label_cpe = Label(licenseFrameDisplay, text=lista[i])
                if message is not None and "4644" in message:
                    label_info = Label(licenseFrameDisplay, text="CPE Não encontrado", foreground="red", background=fundoDisplay)
                    cpeNotFound.append(lista[i])
                    label_status = Label(licenseFrameDisplay, text="Offline", foreground="#e8e8e8", background=fundoDisplay)
                else:
                    label_info = Label(licenseFrameDisplay, text="CPE Encontrado", foreground="green", background=fundoDisplay)
                    label_firmwareInfo = Label(licenseFrameDisplay, text=responseLicenseStatus.json().get("release"), foreground="#e8e8e8", background=fundoDisplay)
                    if status == True:
                        
                        if responseLicenseStatus.json().get("use_tr069") == True:
                            botaoMudarDHCP.configure(state="disabled")
                            label_firmwareInfo = Label(licenseFrameDisplay, text="TR-069", foreground="#e8e8e8", background=fundoDisplay)

                        label_status = Label(licenseFrameDisplay, text="Online", foreground="#00ff00", background=fundoDisplay)
                        botaoResetarCPE.grid(row=i+1, column=4, padx=5, pady=5, sticky="w")
                        botaoMudarDHCP.grid(row=i+1, column=5, padx=5, pady=5, sticky="w")
                        botaoAtualizarFirmware = customtkinter.CTkButton(licenseFrameDisplay, text="Atualizar Firmware", command=lambda i=lista[i]: atualizarFirmware(i))
                        botaoAtualizarFirmware.grid(row=i+1, column=6, padx=5, pady=5, sticky="w")
                        
                    elif status == False:
                        label_status = Label(licenseFrameDisplay, text="Offline", foreground="#e8e8e8", background=fundoDisplay)
                    else:
                        if responseLicense.json().get("success") == False:
                            label_status = Label(licenseFrameDisplay, text="Não encontrado", foreground="#e8e8e8", background=fundoDisplay)
                        else:
                            label_status = Label(licenseFrameDisplay, text=f'{responseLicense.json().get("message")}', foreground="red", background=fundoDisplay)

                # Posicionamento dos labels das linhas da tabela com o gerenciador de layout grid
                botao.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
                label_info.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
                label_status.grid(row=i+1, column=2, padx=5, pady=5, sticky="w")
                label_firmwareInfo.grid(row=i+1, column=3, padx=5, pady=5, sticky="w")

                # Posicionamento dos labels das linhas da tabela com o gerenciador de layout grid
                botao.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
                label_info.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
                label_status.grid(row=i+1, column=2, padx=5, pady=5, sticky="w")
            destroy_loading_frame()

        def loadingFrame():
            global loading_frame
            loading_frame = Frame(license_window, bg="gray")
            loading_frame.place(x=0, y=0, relwidth=1, relheight=1)

            loading_label = Label(loading_frame, text="Carregando...", font=("Arial", 16), fg="white", bg="gray")
            loading_label.pack(expand=True)

            loading_frame.lift()
            for widget in licenseFrameDisplay.winfo_children():
                widget.destroy()
            t = threading.Thread(target=display)
            t.start()
        buttonFrame = Frame(license_window, bg=fundoDisplay)
        buttonFrame.pack()
        # Crie os botões
        def destroy_loading_frame():
            loading_frame.destroy()

        botao_atualizar = Button(license_window, width=30, text="Atualizar", bg="#3498db", fg="#FFFFFF", font=("Arial", 16), command=loadingFrame)
        botao_atualizar.pack(pady=10)

        #start_update_thread()
        license_window.protocol("WM_DELETE_WINDOW", fechar)
        window.mainloop()
        
    except Exception as erro:
        messagebox.showerror("Erro", f"Houve um erro! {erro}")
