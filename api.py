import requests
endpoint = "https://flashman.gigalink.net.br"
    
urlLicense = f'{endpoint}/api/v2/device/license/set'
urlInfoLicense = f'{endpoint}/api/v2/device/license/get'
urlCreate = f'{endpoint}/api/v2/device/create'
urlInfo = f'{endpoint}/api/v2/device/update/'
urlStatus = f'{endpoint}/api/v2/device/command/'
urlCpeinfo = f'{endpoint}/api/v2/device/update/'
urlResetarCPE = f'{endpoint}/api/v2/device/update/'
urlAtualizarCPE = f'{endpoint}/api/v2/device/update/'
#usuario = 'carlos.martins'
#senha = 'cama2022'
global usuario
global senha
usuario = ''
senha = ''