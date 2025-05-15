import os
import requests
from pathlib import Path
from datetime import datetime
import json
import sys
from dotenv import load_dotenv


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

VERSION_URL = "https://api.github.com/repos/AndreyGdula/autojus/releases/latest"
UPDATE_LOG = Path(__file__).parent / "autojusLog.json"
TOKEN = os.getenv("Ajpikey")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_latest_version(url):
    """Obtem o arquivo JSON com a versão mais recente."""
    global download_url
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        version = data.get('name')
        version = version.replace("v", "")
        download_url = data.get('assets')[0].get('browser_download_url')
        return version, download_url
    except Exception as e:
        return None
    

def check_for_update(current_version):
    """Verifica se há uma versão mais recente disponível e altera a data de última verificação no arquivo autojusLog.json."""
    if not UPDATE_LOG.exists():
        with open(UPDATE_LOG, "w") as file:
            json.dump({"last-check": "01-01-2000"}, file)  # Data inicial padrão

    latest_version = get_latest_version(VERSION_URL)
    if latest_version is None:
        return None

    if latest_version[0] == current_version:
        return 0
    else:
        current_date = datetime.today().strftime("%d-%m-%Y")
        with open(UPDATE_LOG, "w") as file:
            json.dump({"last-check": current_date}, file)
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
        response = requests.get(get_latest_version(VERSION_URL)[1], stream=True)
        response.raise_for_status()  # Lança uma exceção se o download falhar

        # Salva o arquivo na pasta Downloads
        with open(installer_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        os.startfile(installer_path)  # Abre o instalador automaticamente
        return True
    except Exception as e:
        return False
