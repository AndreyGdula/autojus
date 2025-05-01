import urllib.request
import json
import os
import requests
from pathlib import Path

VERSION_URL = "https://api.github.com/repos/AndreyGdula/autojus/releases/latest"

def get_latest_version(url):
    """Obtem o arquivo JSON com a versão mais recente."""
    global download_url
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            data = json.loads(content)
            version = data.get('name')
            version = version.replace("v", "")
            download_url = data.get('assets')[0].get('browser_download_url')
            return version, download_url
    except Exception as e:
        return None
    

def check_for_update(current_version):
    """Verifica se há uma versão mais recente disponível."""
    latest_version = get_latest_version(VERSION_URL)
    if latest_version == current_version:
        return 0
    else:
        return latest_version
    
def download_update():
    """Baixa o instalador mais recente para a pasta Downloads do usuário."""
    try:
        # Obtém o caminho da pasta Downloads do usuário
        downloads_folder = Path.home() / "Downloads"
        downloads_folder.mkdir(parents=True, exist_ok=True)  # Garante que a pasta existe

        # Define o caminho para salvar o instalador
        installer_path = downloads_folder / "AutoJus_Setup.exe"

        # Faz o download do instalador
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Lança uma exceção se o download falhar

        # Salva o arquivo na pasta Downloads
        with open(installer_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        os.startfile(installer_path)  # Abre o instalador automaticamente
        return True
    except Exception as e:
        return False
