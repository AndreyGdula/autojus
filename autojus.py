import fitz  # PyMuPDF
import pandas as pd
import re
import os
import subprocess as sb
from openpyxl import load_workbook


# Função para extrair texto do PDF
def extrair_texto_pdf(pdf_path):
    texto = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            texto += page.get_text("text") + "\n"
    return texto

# Expressões regulares para capturar as informações
padrao_processo = r"Processo nº: (\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})"
padrao_autor = r"Autor: (.+)"
padrao_advogado = r"Advogado: (.+) - OAB (\d+)"
padrao_data = r"Data de Distribuição: (\d{1,2}/\d{1,2}/\d{2,4})"


def extrair_dados_processos(pdf_path):
    texto_extraido = extrair_texto_pdf(pdf_path)

    # Encontrando todas as ocorrências
    arquivo = os.path.splitext(os.path.basename(pdf_path))[0]
    processos = re.findall(padrao_processo, texto_extraido)
    autores = re.findall(padrao_autor, texto_extraido)
    advogados_oab = re.findall(padrao_advogado, texto_extraido)
    datas = re.findall(padrao_data, texto_extraido)

    # Organizando os dados em uma lista
    dados = []
    for i in range(len(processos)):
        advogado, oab = advogados_oab[i]
        dados.append([arquivo, processos[i], autores[i], advogado, oab, datas[i]])

    return dados


while True:
    pdf_path = input("Caminho do arquivo PDF: ") # Caminho do PDF
    if os.path.exists(pdf_path):
        break
    else:
        print("Arquivo não encontrado. Tente novamente.")

excel_path = "output/processos_extraidos.xlsx" # Caminho do Excel

dados_processos = extrair_dados_processos(pdf_path) # Extraindo os dados

# Criando um DataFrame com os novos dados
df_novo = pd.DataFrame(dados_processos, columns=["Arquivo", "Número do Processo", "Autor", "Advogado", "OAB", "Data de Distribuição"])

# Verificando se o arquivo Excel já existe
if os.path.exists(excel_path):
    df_existente = pd.read_excel(excel_path)
    if df_existente["Número do Processo"].str.contains(df_novo["Número do Processo"].iloc[0]).any():
        confirm_edit = input(f"O processo {df_novo['Número do Processo'].iloc[0]} já existe no arquivo Excel. Deseja atualizar as informações? [s/n] ")
        if confirm_edit.lower() == "s":
            df_final = pd.concat([df_existente, df_novo]).drop_duplicates(subset=["Número do Processo"], keep="last")
        else:
            print("Operação cancelada.")
            df_final = df_existente 
    else:
        df_final = pd.concat([df_existente, df_novo]).drop_duplicates(subset=["Número do Processo"], keep="last")
else:
    df_final = df_novo

# Garantir que a coluna "Arquivo" fique na coluna A
def mover_coluna_arquivo_para_a(excel_path):
    wb = load_workbook(excel_path)
    ws = wb.active

    # Encontrar a coluna "Arquivo" e movê-la para a posição A
    for col_idx, cell in enumerate(ws[1], start=1):
        if cell.value == "Arquivo":
            ws.move_range(f"{cell.column_letter}1:{cell.column_letter}{ws.max_row}", rows=0, cols=1 - col_idx)
            break

    wb.save(excel_path)
    wb.close()

df_final.to_excel(excel_path, index=False)
mover_coluna_arquivo_para_a(excel_path)
sb.run(["python", "format_table.py", excel_path])  # Formatar arquivo Excel

print(f"Processos extraídos e atualizados em {excel_path}")
