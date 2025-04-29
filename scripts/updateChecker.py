import urllib.request
import json
import os
import requests
import sys
import shutil
import time

FILE_ID = "1xqjL0toYQ3E4Fh7FuPnPLVGEp2p2CVMS"
VERSION_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
DOWNLOAD_URL = "https://github.com/AndreyGdula/autojus/releases/download/v1.0.1/AutoJus.exe"

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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_exe = os.path.join(current_dir, "AutoJus.exe")
    new_exe = "AutoJus-Update.exe"

    while os.path.exists(current_exe):
        try:
            os.rename(current_exe, current_exe)  # Tenta renomear — falha se estiver rodando
            break
        except PermissionError:
            time.sleep(1)

    # Baixa a nova versão
    res = requests.get(DOWNLOAD_URL)
    if res.status_code == 200:
        with open(new_exe, 'wb') as f:
            f.write(res.content)
    else:
        sys.exit(1)

    # Substitui o executável antigo
    if os.path.exists(current_exe):
        os.remove(current_exe)
    shutil.move(new_exe, current_exe)
    os.startfile(current_exe)
    return True