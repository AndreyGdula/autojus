import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess as sb
import os


class InterfaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal
        self.title("AutomaticJus")
        self.geometry("600x400")
        ctk.set_appearance_mode("System")  # Modo claro ou escuro
        ctk.set_default_color_theme("blue")  # Tema azul

        # Título
        self.label_title = ctk.CTkLabel(self, text="Processador de Arquivos Jurídicos", font=("Arial", 20))
        self.label_title.pack(pady=20)

        # Botão para selecionar e processar arquivo
        self.btn_processar = ctk.CTkButton(self, text="Selecionar e Processar Arquivo", command=self.processar_arquivo)
        self.btn_processar.pack(pady=20)

        # Área de mensagens
        self.text_output = ctk.CTkTextbox(self, width=500, height=150)
        self.text_output.pack(pady=20)

    def processar_arquivo(self):
        # Selecionar arquivo
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF e Word", "*.pdf *.docx *.doc")])
        if not arquivo:
            return

        # Verificar extensão do arquivo
        if not (arquivo.lower().endswith(".pdf") or arquivo.lower().endswith(".docx") or arquivo.lower().endswith(".doc")):
            messagebox.showerror("Erro", "Arquivo inválido. Por favor, insira um arquivo PDF ou Word.")
            return

        # Executar o script principal
        try:
            self.text_output.insert("end", f"Processando o arquivo: {arquivo}\n")
            sb.run(["python", "autojus.py", arquivo], check=True)
            self.text_output.insert("end", "Arquivo extraído com sucesso\n")
        except sb.CalledProcessError as e:
            self.text_output.insert("end", f"Erro ao processar o arquivo: {e}\n")
            messagebox.showerror("Erro", "Ocorreu um erro ao processar o arquivo.")
        except Exception as e:
            self.text_output.insert("end", f"Erro inesperado: {e}\n")
            messagebox.showerror("Erro", "Ocorreu um erro inesperado.")


if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()