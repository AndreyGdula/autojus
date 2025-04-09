from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer
from PyQt6.QtGui import QColor, QIcon, QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QGraphicsColorizeEffect
from pathlib import Path
import sys
import subprocess as sb
from autojus import main


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.flag_export = False # Flag da condição do botão de exportar

        # Definindo as cores
        self.color1 = "#2b2b2b"
        self.color2 = "#3b8ed0"
        self.color1_hover = "#4c4c4d"
        self.color2_hover = "#285e89"
        self.color_disabled = "#1e4668"
        self.color_confirm = "#025f17"

        # Definindo as fontes
        self.font_id = QFontDatabase.addApplicationFont("assets/JosefinSans-VariableFont_wght.ttf")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font_label_id = QFontDatabase.addApplicationFont("assets/WorkSans-MediumItalic.ttf")
        self.font_label = QFontDatabase.applicationFontFamilies(self.font_label_id)[0]

        # Configuração da janela principal
        self.setWindowTitle("AutomaticJus")
        self.setWindowIcon(QIcon("assets/autojus_icon.ico"))
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(600, 400)

        # Label
        self.label_title = QLabel("Extraia seus processos para o Excel", self)
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setGeometry(50, 30, 500, 30)
        self.label_title.setFont(QFont(self.font_label, 24))

        # container_pdf de entrada de arquivo
        self.container_pdf = QWidget(self)
        self.container_pdf.setGeometry(50, 100, 500, 40)
        self.container_pdf.setStyleSheet(f"""
            QWidget {{
                background-color: {self.color1};
                border: 2px solid {self.color2};
                border-radius: 20px;
            }}
            QWidget:hover {{
                background-color: {self.color1_hover};
                border: 2px solid {self.color2_hover};
        }}
        """)

        self.entry_path_pdf = QLineEdit(self.container_pdf)
        self.entry_path_pdf.setPlaceholderText("Caminho do arquivo do processo")
        self.entry_path_pdf.setGeometry(10, 2, 375, 36)
        self.entry_path_pdf.setReadOnly(True)
        self.entry_path_pdf.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_path_pdf.setStyleSheet(f"""
            padding: 10px;
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
            border: none;
            background-color: transparent;
            color: white;
        """)

        self.btn_path_pdf = QPushButton("Selecionar", self.container_pdf)
        self.btn_path_pdf.setGeometry(380, 0, 120, 40)
        self.btn_path_pdf.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color2};
                background-color: {self.color2};
                color: white;
                font-weight: bold;
                font-family: {self.font_family};
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border-color: {self.color2_hover};
            }}
        """)
        self.btn_path_pdf.clicked.connect(self.selecionar_arquivo_pdf)


        # container_pdf do excel
        self.container_excel = QWidget(self)
        self.container_excel.setGeometry(50, 180, 500, 40)
        self.container_excel.setStyleSheet(f"""
            QWidget {{
                background-color: {self.color1};
                border: 2px solid {self.color2};
                border-radius: 20px;
            }}
            QWidget:hover {{
                background-color: {self.color1_hover};
                border: 2px solid {self.color2_hover};
            }}
            """)
        
        self.entry_excel = QLineEdit(self.container_excel)
        self.entry_excel.setPlaceholderText("Desktop/processos_extraidos.xlsx")
        self.entry_excel.setGeometry(10, 2, 375, 36)
        self.entry_excel.setReadOnly(True)
        self.entry_excel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_excel.setStyleSheet("""
            padding: 10px;
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
            border: none;
            background-color: transparent;
            color: white;
            """)
        
        self.btn_path_excel = QPushButton("Selecionar", self.container_excel)
        self.btn_path_excel.setGeometry(380, 0, 120, 40)
        self.btn_path_excel.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color2};
                background-color: {self.color2};
                color: white;
                font-weight: bold;
                font-family: {self.font_family};
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border-color: {self.color2_hover};
            }}
            """)
        self.btn_path_excel.clicked.connect(self.selecionar_arquivo_excel)

        # Botão de exportação
        self.btn_exportar = QPushButton("Exportar", self)
        self.btn_exportar.setGeometry(50, 260, 500, 40)
        self.btn_exportar.setEnabled(False)
        self.btn_exportar.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color_disabled};
                background-color: {self.color_disabled};
                color: gray;
                font-weight: bold;
                font-family: {self.font_family};
            }}
        """)
        self.btn_exportar.clicked.connect(lambda: self.exportar(self.entry_path_pdf.text(), self.entry_excel.text()))

    def selecionar_arquivo_pdf(self):
        if self.flag_export:
            self.resetar_botao()

        # Selecionar arquivo de entrada
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo", "", "Arquivos PDF e Word (*.pdf *.docx *.doc)")
        if not pdf_path:
            return

        self.entry_path_pdf.setText(pdf_path)
        self.entry_path_pdf.setCursorPosition(len(self.entry_path_pdf.text()))
        self.btn_exportar.setEnabled(True)
        self.btn_exportar.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color2};
                background-color: {self.color2};
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border-color: {self.color2_hover};
            }}
            """)

        # Verificar extensão do arquivo
        if not (pdf_path.lower().endswith(".pdf") or pdf_path.lower().endswith(".docx") or pdf_path.lower().endswith(".doc")):
            QMessageBox.critical(self, "Erro", "Arquivo inválido. Por favor, insira um arquivo PDF ou Word.")
            return

    def selecionar_arquivo_excel(self):
        if self.flag_export:
            self.resetar_botao()

        # Selecionar local da exportação
        excel_path, _ = QFileDialog.getSaveFileName(self, "Selecione um arquivo", "", "Arquivos Excel (*.xlsx)")
        if not excel_path:
            return
        self.entry_excel.setText(excel_path)
        self.entry_excel.setCursorPosition(len(self.entry_excel.text()))

        # Verificar extensão do arquivo
        if not excel_path.lower().endswith(".xlsx"):
            QMessageBox.critical(self, "Erro", "Arquivo inválido. Por favor, insira um arquivo Excel.")
            return

    def exportar(self, pdf_path, excel_path):
        if self.flag_export:
            self.resetar_botao()

        # Obter path da área de trabalho
        desktop_path = Path.home() / "Desktop"
        if not excel_path:
            excel_path = desktop_path / "processos_extraidos.xlsx"

        try:
            main(pdf_path, excel_path, self.confirm, self.animar_botao)

        except sb.CalledProcessError as e:
            QMessageBox.critical(self, "Erro", f"Erro ao processar o arquivo: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", f"{e}")

    def animar_botao(self):
        self.flag_export = True
        effect = QGraphicsColorizeEffect(self.btn_exportar)
        self.btn_exportar.setGraphicsEffect(effect)

        # Configuração da animação
        self.anima = QPropertyAnimation(effect, b"color")
        self.anima.setDuration(250) # Duração
        self.anima.setStartValue(QColor(self.color2)) # Cor inicial
        self.anima.setEndValue(QColor(self.color_confirm)) # Cor final
        self.anima.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anima.start()
        self.anima.finished.connect(lambda: self.btn_exportar.setStyleSheet(f"""
            padding: 10px;
            border-radius: 20px;
            border: 2px solid {self.color_confirm};
            background-color: {self.color_confirm};
            color: white;
            font-weight: bold;
            font-size: 16px;
        """))
        self.animar_texto("EXPORTADO COM SUCESSO")

    def resetar_botao(self):
        self.flag_export = False

        self.btn_exportar.setGraphicsEffect(None)
        self.anima_reset = QPropertyAnimation(self.btn_exportar, b"styleSheet")
        self.anima_reset.setDuration(250)
        self.anima_reset.setStartValue(self.btn_exportar.styleSheet())
        self.anima_reset.setEndValue(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color2};
                background-color: {self.color2};
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border-color: {self.color2_hover};
            }}
        """)
        
        self.anima_reset.start()
        self.anima_reset.finished.connect(lambda: self.btn_exportar.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color2};
                background-color: {self.color2};
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border-color: {self.color2_hover};
            }}
        """))
        self.animar_texto("Exportar", 50)

    def animar_texto(self, texto_final, time=25):
        self.texto_atual = ""
        self.indice_texto = 0

        def atualizar_texto():
            if self.indice_texto < len(texto_final):
                self.texto_atual += texto_final[self.indice_texto]
                self.btn_exportar.setText(self.texto_atual)
                self.indice_texto += 1
            else:
                self.timer.stop()

        self.timer = QTimer(self)
        self.timer.timeout.connect(atualizar_texto)
        self.timer.start(time)  # Tempo de atualização em milissegundos


    def confirm(self, msg):
        return QMessageBox.question(self, "Confirmação", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec())
