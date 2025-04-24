import json
import datetime
import urllib.request

UPDATE_CONFIG_FILE = "update_config.json"
UPDATE_INFO_URL = "https://SEU_LINK_DIRECT_DO_JSON_NO_DRIVE"

def load_last_check():
    try:
        with open(UPDATE_CONFIG_FILE, "r") as file:
            data = json.load(file)
            return datetime.datetime.strptime(data["last_check"], "%Y-%m-%d").date()
    except (FileNotFoundError, KeyError, ValueError):
        return None

def save_last_check(date):
    with open(UPDATE_CONFIG_FILE, "w") as file:
        json.dump({"last_check": date.strftime("%Y-%m-%d")}, file)

def should_check_update(days=3):
    last_check = load_last_check()
    today = datetime.date.today()
    if not last_check or (today - last_check).days >= days:
        return True
    return False

def get_remote_version():
    try:
        with urllib.request.urlopen(UPDATE_INFO_URL) as response:
            data = json.load(response)
            return data["version"]
    except Exception as e:
        print(f"Erro ao verificar atualização: {e}")
        return None

def check_for_update(current_version, days=3, force=False):
    if force or should_check_update(days):
        remote_version = get_remote_version()
        save_last_check(datetime.date.today())
        if remote_version and remote_version != current_version:
            return True, remote_version
    return False, None
