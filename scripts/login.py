import requests
import base64
import json
import os

def load_users():
    """Carrega os usuários do arquivo JSON hospedado no GitHub."""
    url = "https://api.github.com/repos/AndreyGdula/autojus-users/contents/users.json"
    headers = {
        "Authorization": f"token {os.getenv('AUTOJUS_KEY')}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Faz a requisição para obter o arquivo
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        file_data = response.json()

        if 'content' not in file_data:
            raise ValueError("A resposta da API não contém a chave 'content'.")

        # Decodifica o conteúdo Base64 do arquivo
        decoded_content = base64.b64decode(file_data['content']).decode('utf-8')
        user_data = json.loads(decoded_content)
        return user_data['users']

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None
    except Exception as e:
        print(f"Error loading users: {e}")
        return None
    
def auth(username, password, usuarios=load_users()):
    """Verifica o login do usuário e confirma se está ativo
    
    Args: 
        username (str): Nome de usuário
        password (str): Senha do usuário
        usuarios (list): Lista de usuários carregados do arquivo JSON
    Returns:
        bool: True -> se o usuário estiver ativo e as credenciais estiverem corretas
        bool: False -> se não estiver ativo
        None: se o usuário não existir
    """
    for users in usuarios:
        if users['username'] == username and users['password'] == password:
            if users.get('active', False):
                return True
            else:
                return False
    return None
