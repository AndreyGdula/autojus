from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
import sys
import subprocess as sb
from autojus import main


class Interface(QWidget):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.setWindowTitle("AutomaticJus")
        self.setGeometry(100, 100, 600, 400)

        # Cores
        color1 = "#2b2b2b"
        color2 = "#3b8ed0"

        # Label
        self.label_title = QLabel("Extraia seus processos para o Excel", self)
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setGeometry(50, 20, 500, 30)

        # Contêiner para o QLineEdit e o botão
        self.container = QWidget(self)
        self.container.setGeometry(50, 80, 500, 40)

        # Campo de entrada
        self.entry_path_pdf = QLineEdit(self.container)
        self.entry_path_pdf.setPlaceholderText("Caminho do arquivo PDF")
        self.entry_path_pdf.setGeometry(0, 0, 450, 40)
        self.entry_path_pdf.setStyleSheet(f"""
            padding: 10px;
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
            border: 2px solid {color2};
            border-right: none;
            background-color: {color1};
            color: white;
        """)

        # Botão
        self.btn_path_pdf = QPushButton("Selecionar", self.container)
        self.btn_path_pdf.setGeometry(400, 0, 100, 40)  # Posiciona o botão no canto direito
        self.btn_path_pdf.setStyleSheet(f"""
            padding: 10px;
            border-radius: 20px;
            border: 2px solid {color2};
            background-color: {color2};
            color: white;
            font-weight: bold;
        """)
        self.btn_path_pdf.clicked.connect(self.selecionar_arquivo)

    def selecionar_arquivo(self):
        # Selecionar arquivo
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo", "", "Arquivos PDF e Word (*.pdf *.docx *.doc)")
        if not arquivo:
            return

        self.entry_path_pdf.setText(arquivo)

        # Verificar extensão do arquivo
        if not (arquivo.lower().endswith(".pdf") or arquivo.lower().endswith(".docx") or arquivo.lower().endswith(".doc")):
            QMessageBox.critical(self, "Erro", "Arquivo inválido. Por favor, insira um arquivo PDF ou Word.")
            return

        # Executar o script principal
        try:
            main(arquivo, self.confirm, self.message_callback)
            QMessageBox.information(self, "Sucesso", "Arquivo extraído com sucesso!")
        except sb.CalledProcessError as e:
            QMessageBox.critical(self, "Erro", f"Erro ao processar o arquivo: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", f"{e}")

    def confirm(self, msg):
        return QMessageBox.question(self, "Confirmação", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes
    
    def message_callback(self, msg):
        QMessageBox.information(self, "Info", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec())
