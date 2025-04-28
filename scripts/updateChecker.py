import urllib.request
import json
import os

FILE_ID = "1xqjL0toYQ3E4Fh7FuPnPLVGEp2p2CVMS"
VERSION_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
DOWNLOAD_ID = "1U-ZyjPfnJPYia64cn4gP9M3F9dHsc-zB"
DOWNLOAD_URL = f"https://drive.google.com/uc?export=download&id={DOWNLOAD_ID}"

def get_latest_version(url):
    """Obtem o arquivo JSON com a versão mais recente."""
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            data = json.loads(content)
            version = data.get('version')
            return version
    except Exception as e:
        print(f"Erro ao obter a versão mais recente: {e}")
        return None
    

def check_for_update(current_version):
    """Verifica se há uma versão mais recente disponível."""
    latest_version = get_latest_version(VERSION_URL)
    if latest_version == current_version:
        return 0
    else:
        return latest_version
    
def download_update():
    """Baixa a versão mais recente"""
    current_exe = os.path.abspath(__file__) # Caminho do arquivo atual
    new_exe = current_exe + ".new"
    
    urllib.request.urlretrieve(DOWNLOAD_URL, new_exe)
    os.remove(current_exe)
    os.rename(new_exe, current_exe)
    return True
