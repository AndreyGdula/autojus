import json
import datetime
import os
import urllib.request

# Caminho dinâmico para os arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
UPDATE_LOG_FILE = os.path.join(BASE_DIR, "updateLog.json")  # Caminho para updateLog.json
UPDATE_INFO_URL = "https://drive.google.com/uc?export=download&id=1xqjL0toYQ3E4Fh7FuPnPLVGEp2p2CVMS"

def load_last_check():
    """Carrega a data da última verificação de atualização."""
    try:
        with open(UPDATE_LOG_FILE, "r") as file:
            data = json.load(file)
            return datetime.datetime.strptime(data["last-check"], "%d-%m-%Y").date()
    except (FileNotFoundError, KeyError, ValueError):
        return None

def save_last_check(date):
    """Salva a data da última verificação de atualização no arquivo."""
    try:
        with open(UPDATE_LOG_FILE, "w") as file:
            json.dump({"last-check": date.strftime("%d-%m-%Y")}, file)
    except Exception as e:
        print(f"Erro ao salvar a data da última verificação: {e}")

def should_check_update(days=3):
    """Verifica se já passou o intervalo necessário para checar atualizações."""
    last_check = load_last_check()
    today = datetime.date.today()
    if not last_check or (today - last_check).days >= days:
        return True
    return False

def get_remote_version():
    """Obtém a versão mais recente do servidor remoto."""
    try:
        with urllib.request.urlopen(UPDATE_INFO_URL) as response:
            data = json.load(response)
            return data["version"]
    except Exception as e:
        print(f"Erro ao verificar atualização: {e}")
        return None

def check_for_update(current_version, days=3, force=False):
    """
    Verifica se há uma nova versão disponível.
    :param current_version: Versão atual do aplicativo.
    :param days: Intervalo de dias para verificar atualizações.
    :param force: Força a verificação, ignorando o intervalo.
    :return: (bool, str) - True e a nova versão se houver atualização, False e None caso contrário.
    """
    if force or should_check_update(days):
        remote_version = get_remote_version()
        save_last_check(datetime.date.today())
        if remote_version and remote_version != current_version:
            return True, remote_version
    return False, None
