from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer, QRect, QSize, QUrl
from PyQt6.QtGui import QColor, QIcon, QFontDatabase, QFont, QDesktopServices
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QGraphicsColorizeEffect, QFrame
from pathlib import Path
import sys
import subprocess as sb 
import os
import json
from datetime import datetime
from autojus import main
from scripts.updateChecker import check_for_update, download_update

app_version = "1.0.2"

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.flag_export = False  # Flag da condição do botão de exportar
        self.flag_menu = False  # Flag da condição do menu

        # Definindo as cores e constantes
        self.background_color = "#1e1e1e"
        self.color1 = "#2b2b2b"
        self.color2 = "#3b8ed0"
        self.color3 = "#212121"
        self.color1_hover = "#4c4c4d"
        self.color2_hover = "#285e89"
        self.color_disabled = "#1e4668"
        self.color_confirm = "#025f17"
        self.window_width = 600
        self.window_height = 400

        # Definindo as fontes e icones
        if getattr(sys, "frozen", False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(__file__)
        font1_path = os.path.join(self.base_path, "assets", "JosefinSans-VariableFont_wght.ttf")
        font2_path = os.path.join(self.base_path, "assets", "WorkSans-MediumItalic.ttf")
        menu_icon_path = os.path.join(self.base_path, "assets", "menu.svg")
        close_icon_path = os.path.join(self.base_path, "assets", "close.svg")
        update_icon_path = os.path.join(self.base_path, "assets", "update.svg")
        historical_icon_path = os.path.join(self.base_path, "assets", "historical.svg")
        self.font_id = QFontDatabase.addApplicationFont(font1_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font_label_id = QFontDatabase.addApplicationFont(font2_path)
        self.font_label = QFontDatabase.applicationFontFamilies(self.font_label_id)[0]

        # Configuração da janela principal
        self.setWindowTitle("Process Export System")
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        self.setStyleSheet(f"background-color: {self.background_color}; color: white")

        # Widget de fundo para o blur
        self.blur_background = QPushButton(self)
        self.blur_background.setGeometry(0, 0, self.window_width, self.window_height)
        self.blur_background.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                border: none;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.5);
            }
        """)
        self.blur_background.clicked.connect(self.toggle_menu)  # Fechar o menu ao clicar no fundo
        self.blur_background.hide()

        # Burger menu
        self.btn_burger_menu = QPushButton(self)
        self.btn_burger_menu.setIconSize(QSize(24, 24))
        self.btn_burger_menu.setIcon(QIcon(menu_icon_path))
        self.btn_burger_menu.setGeometry(10, 25, 40, 40)
        self.btn_burger_menu.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.color1_hover};
            }}
        """)
        self.btn_burger_menu.clicked.connect(self.toggle_menu)

        # Frame do burger menu
        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(-200, 0, 200, self.window_height)
        self.menu_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color1};
                border-right: 2px solid {self.color2};
            }}
        """)

        self.btn_close_menu = QPushButton(self.menu_frame)
        self.btn_close_menu.setIconSize(QSize(24, 24))
        self.btn_close_menu.setIcon(QIcon(close_icon_path))
        self.btn_close_menu.setGeometry(160, 10, 30, 30)
        self.btn_close_menu.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: gray;
            }
        """)
        self.btn_close_menu.clicked.connect(self.toggle_menu)

        # Adicionando opções ao menu
        self.menu_label = QLabel("Menu", self.menu_frame)
        self.menu_label.setGeometry(20, 10, 100, 30)
        self.menu_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none;")
        self.menu_label.setFont(QFont(self.font_label, 18))

        self.menu_option1 = QPushButton(" Verificar atualização", self.menu_frame)
        self.menu_option1.setGeometry(-2, 100, 200, 40)
        self.menu_option1.setIcon(QIcon(update_icon_path))
        self.menu_option1.setIconSize(QSize(16, 16))
        self.menu_option1.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color1};
                color: white;
                font-weight: bold;
                border: 1px solid gray;
                border-left: none;
                border-right: none;
                text-align: left;
                padding-left: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.color3};
            }}
        """)
        self.menu_option1.clicked.connect(lambda: self.verificar_updade())

        self.menu_option2 = QPushButton(" Histórico", self.menu_frame)
        self.menu_option2.setGeometry(-2, 139, 200, 40)
        self.menu_option2.setIcon(QIcon(historical_icon_path))
        self.menu_option2.setIconSize(QSize(16, 16))
        self.menu_option2.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color1};
                color: white;
                font-weight: bold;
                border: 1px solid gray;
                border-left: none;
                border-right: none;
                text-align: left;
                padding-left: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.color3};
            }}
        """)
        self.menu_option2.clicked.connect(lambda: self.open_historical())

        self.label_version = QLabel(f"v{app_version}", self.menu_frame)
        self.label_version.setGeometry(15, 365, 50, 30)
        self.label_version.setStyleSheet("color: gray; font-size: 12px; font-weight: bold; border: none;")

        # Tela principal
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
        self.container_excel.setGeometry(50, 178, 500, 40)
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

        # Frame de aviso de atualização
        self.warning_frame = QFrame(self)
        self.warning_frame.setGeometry(0, 0, self.window_width, 30)
        self.warning_frame.setStyleSheet(f"""
            background-color: {self.color1};
            color: white;
            font-size: 13px;
            font-family: {self.font_family};
        """)
        self.warning_frame.hide()

        self.warning_label = QLabel(f"A versão {self.ultima_verificacao()} já está disponível.", self.warning_frame)
        self.warning_label.setGeometry(30, 0, 200, 30)

        self.download_btn = QPushButton("Baixar", self.warning_frame)
        self.download_btn.setGeometry(220, 0, 50, 30)
        self.download_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color1};
                color: {self.color2};
                font-weight: bold;
                font-family: {self.font_family};
                border: none;
                text-decoration: underline;
            }}
            QPushButton:hover {{
                color: {self.color2_hover};
            }}
        """)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(lambda: download_update())

        self.close_warning_frame = QPushButton(self.warning_frame)
        self.close_warning_frame.setIconSize(QSize(16, 16))
        self.close_warning_frame.setIcon(QIcon(close_icon_path))
        self.close_warning_frame.setGeometry(self.window_width-30, 0, 30, 30)
        self.close_warning_frame.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: gray;
            }}
        """)
        self.close_warning_frame.clicked.connect(lambda: self.warning_frame.hide())

    def toggle_menu(self):
        """Mostra ou oculta o menu hambúrguer."""
        if self.flag_menu:
            # Ocultar o menu e o blur
            self.animate_menu(-200)
            self.flag_menu = False
            self.blur_background.hide()
        else:
            # Mostrar o menu e o blur
            self.blur_background.show()
            self.blur_background.raise_() # Sobreposição do blur na jenala principal
            self.menu_frame.raise_() # Sobreposição do menu
            self.animate_menu(0)
            self.flag_menu = True

    def animate_menu(self, target_x):
        """Anima o menu hambúrguer para abrir ou fechar."""
        self.animation = QPropertyAnimation(self.menu_frame, b"geometry")
        self.animation.setDuration(300)  # Duração da animação em ms
        self.animation.setStartValue(self.menu_frame.geometry())
        self.animation.setEndValue(QRect(target_x, 0, 200, self.window_height))
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()

    def selecionar_arquivo_pdf(self):
        """Seleciona o arquivo do processo de entrada."""
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
        """Selecionar o arquivo excel para exportação."""
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
        """Exporta os dados do processo para o Excel."""
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
        """Anima o botão de exportação após a conclusão."""
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
        """Volta ao style original do botão."""
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
        """Animar o texto do botão de exportação."""
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
        """Exibir uma caixa de diálogo de confirmação."""
        return QMessageBox.question(self, "Confirmação", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes
    
    def verificar_updade(self):
        """Verifica se há atualizações disponíveis."""
        if check_for_update(app_version) == 0:
            QMessageBox.information(self, "Atualização", "Você já está na versão mais recente.")
        else:
            if self.confirm(f"A versão {check_for_update(app_version)[0]} já está disponível, Deseja atualizar?"):
                try:
                    download_update()
                    QApplication.quit()
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao baixar a atualização: {e}")
            else:
                return
    
    def ultima_verificacao(self):
        """Retorna quando foi a última verificação automática de atualização."""
        UPDATE_LOG_PATH = Path(__file__).parent / "scripts" / "updateLog.json"
        intervalo_dias = 1
        try:
            with open(UPDATE_LOG_PATH, "r") as file:
                data = json.load(file)
                last_check = datetime.strptime(data["last-check"], "%d-%m-%Y").date()
                today = datetime.today().date()
                if not last_check or (today - last_check).days >= intervalo_dias:
                    if check_for_update(app_version) == 0: # 0 == Atualizado
                        return 0
                    else:
                        self.warning_frame.show()
                        return check_for_update(app_version)[0]
                else:
                    return 0
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao ler o arquivo de log: {e}")
            return 0

    def open_historical(self):
        QMessageBox.information(self, "Histórico", "Recurso em desenvolvimento.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec())
