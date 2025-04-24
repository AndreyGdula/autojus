import requests
import os
import zipfile
import shutil

# Versão atual do seu software
VERSAO_ATUAL = "1.0.0"

# Link direto para o JSON de atualização
URL_JSON = "https://drive.google.com/uc?export=download&id=1xqjL0toYQ3E4Fh7FuPnPLVGEp2p2CVMS"

def verificar_atualizacao():
    try:
        resposta = requests.get(URL_JSON)
        if resposta.status_code == 200:
            dados = resposta.json()
            nova_versao = dados["version"]
            url_download = dados["url"]

            if nova_versao != VERSAO_ATUAL:
                print(f"Nova versão disponível: {nova_versao}")
                return url_download
            else:
                print("Você já está na versão mais recente.")
        else:
            print("Erro ao verificar a atualização.")
    except Exception as e:
        print(f"Erro: {e}")
    return None

def baixar_arquivo(url, destino):
    with requests.get(url, stream=True) as r:
        with open(destino, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def atualizar():
    url_arquivo = verificar_atualizacao()
    if url_arquivo:
        print("Baixando atualização...")
        nome_arquivo = "atualizacao.zip"
        baixar_arquivo(url_arquivo, nome_arquivo)

        with zipfile.ZipFile(nome_arquivo, 'r') as zip_ref:
            zip_ref.extractall("nova_versao")

        os.remove(nome_arquivo)
        print("Atualização baixada. Reinicie o programa manualmente.")

if __name__ == "__main__":
    atualizar()
