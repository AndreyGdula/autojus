from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer, QRect, QSize
from PyQt6.QtGui import QColor, QIcon, QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QGraphicsColorizeEffect, QFrame, QTableWidget, QTableWidgetItem
from pathlib import Path
import sys
import subprocess as sb 
import os
from datetime import datetime
from autojus import main
from scripts.updateChecker import check_for_update, download_update
from scripts.login import auth
from scripts.cripto import Cripto

app_version = "1.0.1"

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.flag_export = False  # Flag da condição do botão de exportar
        self.flag_menu = False  # Flag da condição do menu
        self.cripto = Cripto()

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

        # Definindo as fontes e icones e constantes
        if getattr(sys, "frozen", False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(__file__)
        font1_path = os.path.join(self.base_path, "assets", "JosefinSans-VariableFont_wght.ttf")
        font2_path = os.path.join(self.base_path, "assets", "WorkSans-MediumItalic.ttf")
        self.menu_icon_path = os.path.join(self.base_path, "assets", "menu.svg")
        self.close_icon_path = os.path.join(self.base_path, "assets", "close.svg")
        self.update_icon_path = os.path.join(self.base_path, "assets", "update.svg")
        self.historical_icon_path = os.path.join(self.base_path, "assets", "historical.svg")
        self.login_icon_path = os.path.join(self.base_path, "assets", "login.svg")
        self.logout_icon_path = os.path.join(self.base_path, "assets", "logout.svg")
        self.view_icon_path = os.path.join(self.base_path, "assets", "view.svg")
        self.viewoff_icon_path = os.path.join(self.base_path, "assets", "view_off.svg")
        self.account_icon_path = os.path.join(self.base_path, "assets", "account.svg")
        self.search_icon_path = os.path.join(self.base_path, "assets", "search.svg")
        self.delete_icon_path = os.path.join(self.base_path, "assets", "delete.svg")
        self.font_id = QFontDatabase.addApplicationFont(font1_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font_label_id = QFontDatabase.addApplicationFont(font2_path)
        self.font_label = QFontDatabase.applicationFontFamilies(self.font_label_id)[0]
        self.AUTOJUS_LOG_PATH = Path(__file__).parent / "scripts" / "autojusLog.json"
        self.autojus_log_cripto = self.cripto.load_json_cripto(self.AUTOJUS_LOG_PATH)
        self.SESSION_PATH = Path(__file__).parent / "scripts" / "session.json"

        # Configuração da janela principal
        self.setWindowTitle("AutoJus")
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
        self.btn_burger_menu.setIcon(QIcon(self.menu_icon_path))
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
        self.btn_close_menu.setIcon(QIcon(self.close_icon_path))
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
        self.menu_option1.setIcon(QIcon(self.update_icon_path))
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
        self.menu_option2.setIcon(QIcon(self.historical_icon_path))
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

        self.menu_option3 = QPushButton(" Login", self.menu_frame)
        self.menu_option3.setGeometry(-2, 178, 200, 40)
        self.menu_option3.setIcon(QIcon(self.login_icon_path))
        self.menu_option3.setIconSize(QSize(16, 16))
        self.menu_option3.setStyleSheet(f"""
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
        self.menu_option3.clicked.connect(lambda: self.login())

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
        self.close_warning_frame.setIcon(QIcon(self.close_icon_path))
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

        # User Frame
        self.user_frame = QFrame(self.menu_frame)
        self.user_frame.setGeometry(0, self.window_height-50, 200, 50)
        self.user_frame.setStyleSheet(f"""
            background-color: {self.background_color};
        """)
        
        self.icon_user = QPushButton(" Convidado", self.user_frame)
        self.icon_user.setGeometry(10, 10, 180, 30)
        self.icon_user.setIconSize(QSize(32, 32))
        self.icon_user.setIcon(QIcon(self.account_icon_path))
        self.icon_user.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-family: {self.font_family};
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: transparent;
            }}
        """)

        # Carregando o usuário
        username = self.carregar_sessao()
        if username: # Se o usuário estiver logado
            self.icon_user.setText(f" {username.capitalize()}")
            self.menu_option3.setText(" Logout")
            self.menu_option3.setIcon(QIcon(self.logout_icon_path))
            self.menu_option3.clicked.connect(lambda: self.logout())
        else:
            self.icon_user.setText(" Convidado")

        # Tela de login
        self.login_window = QWidget(self)
        self.login_window.setGeometry(0, 0, self.window_width, self.window_height)
        self.login_window.setStyleSheet(f"""
            background-color: {self.background_color};
            color: white;
            font-family: {self.font_family};
        """)

        self.login_label = QLabel("LOGIN", self.login_window)
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label.setGeometry(50, 32, 500, 30)
        self.login_label.setStyleSheet(f"""font-size: 20px; font-weight: bold;""")
        self.login_label.setFont(QFont(self.font_label, 24))

        self.entry_username = QLineEdit(self.login_window)
        self.entry_username.setPlaceholderText("Usuário")
        self.entry_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry_username.setGeometry(100, 100, 400, 40)
        self.entry_username.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color2};
                background-color: {self.color1};
                color: white;
                font-weight: bold;
            }}
            QLineEdit:hover {{
                background-color: {self.color1_hover};
                border: 2px solid {self.color2_hover};
            }}
        """)
        self.entry_username.textChanged.connect(self.verificar_campos_login)

        self.container_password = QWidget(self.login_window)
        self.container_password.setGeometry(100, 178, 400, 40)
        self.container_password.setStyleSheet(f"""
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

        self.entry_password = QLineEdit(self.container_password)
        self.entry_password.setPlaceholderText("Senha")
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.entry_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry_password.setGeometry(0, 0, 400, 40)
        self.entry_password.setStyleSheet(f"""
            padding: 10px;
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
            border: none;
            background-color: transparent;
            color: white;
        """)
        self.entry_password.textChanged.connect(self.verificar_campos_login)  # Conecta o sinal

        self.view_password = QPushButton(self.container_password)
        self.view_password.setIconSize(QSize(16, 16))
        self.view_password.setIcon(QIcon(self.view_icon_path))
        self.view_password.setGeometry(360, 0, 40, 40)
        self.view_password.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border-radius: 20px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border: 2px solid {self.color2_hover};
            }}
        """)
        self.view_password.clicked.connect(lambda: self.show_password())

        self.btn_login = QPushButton("Login", self.login_window)
        self.btn_login.setGeometry(100, 260, 400, 40)
        self.btn_login.setEnabled(False)  # Inicialmente desabilitado
        self.btn_login.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 20px;
                border: 2px solid {self.color_disabled};
                background-color: {self.color_disabled};
                color: gray;
                font-weight: bold;
                font-family: {self.font_family};
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border-color: {self.color2_hover};
            }}
        """)
        self.btn_login.clicked.connect(lambda: self.autenticar())

        self.btn_close = QPushButton(self)
        self.btn_close.setIconSize(QSize(24, 24))
        self.btn_close.setIcon(QIcon(self.close_icon_path))
        self.btn_close.setGeometry(self.window_width-50, 30, 30, 30)
        self.btn_close.setStyleSheet(f"""
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
        self.btn_close.hide()

        self.warning_login = QLabel("", self.login_window)
        self.warning_login.setGeometry(100, 224, 400, 30)
        self.warning_login.setFont(QFont(self.font_label, 8))
        self.warning_login.setStyleSheet("color: red")
        self.warning_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_login.hide()
        self.login_window.hide()

        self.label_version = QLabel(f"v{app_version}", self.user_frame)
        self.label_version.setGeometry(165, 35, 30, 10)
        self.label_version.setStyleSheet("color: gray; font-size: 10px; font-weight: bold; border: none; text-align: right;")


        # Janela do histórico
        self.historico_log = self.autojus_log_cripto.get("historico", []) # Json com o histórico
        self.historico_window = QWidget(self)
        self.historico_window.setGeometry(0, 0, self.window_width, self.window_height)
        self.historico_window.setStyleSheet(f"background-color: {self.background_color}; color: white")
        self.historico_window.hide()

        # Campo de pesquisa
        self.container_search = QWidget(self.historico_window)
        self.container_search.setGeometry(60, 30, self.window_width-165, 30)
        self.container_search.setStyleSheet(f"""
            QWidget {{
                padding: 10px;
                border-radius: 15px;
                border: 2px solid {self.color1};
                background-color: {self.color1};
                color: white;
                font-weight: bold;
            }}
        """)
        self.search_icon = QPushButton(self.container_search)
        self.search_icon.setGeometry(0, 0, 30, 30)
        self.search_icon.setIcon(QIcon(self.search_icon_path))
        self.search_icon.setIconSize(QSize(18, 18))
        self.search_icon.setEnabled(False)
        self.search_icon.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border-radius: 15px
                font-weight: bold;
            }}
        """)
        self.search_entry = QLineEdit(self.container_search)
        self.search_entry.setGeometry(30, 0, self.window_width-205, 30)
        self.search_entry.setPlaceholderText("Pesquisa")
        self.search_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 0px;
                font-size: 12px
            }}
        """)
        self.search_entry.textChanged.connect(lambda: self.pesquisar_historico())

        # Apagar histórico
        self.delete_icon = QPushButton(self.historico_window)
        self.delete_icon.setIcon(QIcon(self.delete_icon_path))
        self.delete_icon.setIconSize(QSize(24, 24))
        self.delete_icon.setGeometry(self.window_width-90, 30, 30, 30)
        self.delete_icon.setStyleSheet(f"""
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
        self.delete_icon.clicked.connect(lambda: self.apagar_historico())

        # Tabela
        self.historico_table = QTableWidget(self.historico_window)
        self.historico_table.setGeometry(0, 75, self.window_width-10, self.window_height-90)
        self.historico_table.setColumnCount(3)
        self.historico_table.setHorizontalHeaderLabels(['Data/Hora', 'Arquivo de origem', 'Arquivo de destino'])
        self.historico_table.setRowCount(len(self.historico_log))
        self.historico_table.setColumnWidth(0, 115)  # Data
        self.historico_table.setColumnWidth(1, 230)  # Origem
        self.historico_table.setColumnWidth(2, 230)  # Destino
        self.historico_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.color1};
                color: white;
                border: none;
            }}
            QHeaderView::section {{
                background-color: {self.background_color};
                font-weight: bold;
            }}
        """)


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

        # Se estiver fechando o menu, traga o botão para frente ao final da animação
        if target_x < 0:
            self.animation.finished.connect(self.btn_burger_menu.raise_)


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
        if not self.verificar_limite_exportar():
            self.btn_exportar.setEnabled(False)
            return

        if self.flag_export:
            self.resetar_botao()

        # Obter path da área de trabalho
        desktop_path = Path.home() / "Desktop"
        if not excel_path:
            excel_path = desktop_path / "processos_extraidos.xlsx"

        try:
            main(pdf_path, excel_path, self.confirm)
            self.historico_log.append({
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "origem": Path(pdf_path).name,
                "destino": Path(excel_path).name,
            })
            self.cripto.save_json_cripto(self.AUTOJUS_LOG_PATH, {"historico": self.historico_log})
            self.animar_botao()

        except sb.CalledProcessError as e:
            QMessageBox.critical(self, "Erro", f"Erro ao processar o arquivo: {e}")
        except PermissionError:
            QMessageBox.critical(self, "Erro", f"Parece que você está com o arquivo Excel aberto, feche-o antes de exportar.")
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
        self.cripto.save_json_cripto(self.AUTOJUS_LOG_PATH, {"last-check": datetime.today().strftime("%d-%m-%Y")})
        try:
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
        except TypeError:
            QMessageBox.critical(self, "Erro", "Erro ao encontrar o token de verificação de atualização")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao verificar atualização: {e}")
    

    def ultima_verificacao(self):
        """Retorna quando foi a última verificação automática de atualização."""
        intervalo_dias = 15
        try:
            data = self.autojus_log_cripto
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
        except KeyError:
            return 0
        except Exception as e:
            QMessageBox.critical(self, f"Erro", f"Erro ao checar a última verificação de atualização: {e}")
            return 0


    def open_historical(self):
        """Exibir o histórico de arquivos exportados"""
        self.historico_window.show()
        self.toggle_menu()
        self.btn_close.show()
        self.btn_close.raise_()
        self.btn_close.clicked.connect(lambda: [self.historico_window.hide(), self.btn_close.hide()])

        if not self.historico_log:
            self.historico_vazio("Histórico vazio")
        else:
            self.historico_table.setSpan(0, 0, 1, 1)
            self.historico_table.setRowCount(len(self.historico_log))
            for i, item in enumerate(self.historico_log):
                self.historico_table.setItem(i, 0, QTableWidgetItem(item["data"]))
                self.historico_table.setItem(i, 1, QTableWidgetItem(item["origem"]))
                self.historico_table.setItem(i, 2, QTableWidgetItem(item["destino"]))
            for row in range(self.historico_table.rowCount()):
                item = self.historico_table.item(row, 0)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def apagar_historico(self):
        """Apagar o histórico de exportações do usuário."""
        self.historico_log = []
        self.cripto.save_json_cripto(self.AUTOJUS_LOG_PATH, {"historico": self.historico_log})
        self.historico_vazio("Histórico vazio")

    def historico_vazio(self, msg):
        self.historico_table.setRowCount(1)
        item = QTableWidgetItem(msg)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.historico_table.setItem(0, 0, item)
        self.historico_table.setItem(0, 1, QTableWidgetItem(""))
        self.historico_table.setItem(0, 2, QTableWidgetItem(""))
        self.historico_table.setSpan(0, 0, 1, 3)

    def pesquisar_historico(self):
        """Filtra e exibe os itens procurados no search_entry"""
        pesquisa = self.search_entry.text().lower().strip()
        if not pesquisa:
            resultados = self.historico_log
        else:
            resultados = [
                item for item in self.historico_log
                if pesquisa in item["data"].lower()
                or pesquisa in item["origem"].lower()
                or pesquisa in item["destino"].lower()
            ]
        
        self.historico_table.setSpan(0, 0, 1, 1)
        if not resultados:
            self.historico_vazio("O termo digitado não foi encontrado.")
        else:
            self.historico_table.setRowCount(len(resultados))
            for i, item in enumerate(resultados):
                self.historico_table.setItem(i, 0, QTableWidgetItem(item["data"]))
                self.historico_table.setItem(i, 1, QTableWidgetItem(item["origem"]))
                self.historico_table.setItem(i, 2, QTableWidgetItem(item["destino"]))


    def login(self):
        """Exibir a tela de login do usuário."""
        self.toggle_menu() # Fechar o menu
        self.menu_option3.clicked.connect(lambda: self.logout())
        QTimer.singleShot(200, self.show_login_window) # Esperar 300ms para abrir a tela de login


    def logout(self):
        """Faz o logout do usuário."""
        self.limpar_sessao()
        self.icon_user.setText(" Convidado")
        self.menu_option3.setText(" Login")
        self.menu_option3.setIcon(QIcon(self.login_icon_path))
        self.menu_option3.clicked.connect(lambda: self.login())


    def show_login_window(self):
        """Exibir a janela de login."""
        self.login_window.show()
        self.btn_close.clicked.connect(lambda: [self.login_window.hide(), self.btn_close.hide()])
        self.btn_close.raise_()
        self.btn_close.show()


    def verificar_campos_login(self):
        """Habilita o botão de login se os campos de usuário e senha estiverem preenchidos."""
        self.entry_username.setStyleSheet(f"""
            border-radius: 20px;
            border: 2px solid {self.color2};
            background-color: {self.color1};
        """)
        self.entry_password.setStyleSheet(f"""
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
            border: none;
            background-color: transparent;
            color: white;
        """)
        self.view_password.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border-radius: 20px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.color2_hover};
                border: 2px solid {self.color2_hover};
            }}
        """)
        if self.entry_username.text() and self.entry_password.text():
            self.btn_login.setEnabled(True)
            self.btn_login.setStyleSheet(f"""
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
        else:
            self.btn_login.setEnabled(False)
            self.btn_login.setStyleSheet(f"""
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


    def autenticar(self):
        """Autentica o usuário."""
        username = self.entry_username.text()
        password = self.entry_password.text()

        if auth(username, password) is True: # Sucesso no login
            self.login_window.hide()
            self.menu_option3.setText(" Logout")
            self.menu_option3.setIcon(QIcon(self.logout_icon_path))
            self.icon_user.setText(f" {username.capitalize()}")
            self.toggle_menu() # Abrir o menu
            self.salvar_sessao(username)

        elif auth(username, password) is False: # Usuário inativo
            self.entry_username.setStyleSheet(f"""
                QLineEdit {{
                    border-radius: 20px;
                    border: 2px solid red;
                    background-color: {self.color1};
                }}
                QLineEdit:hover {{
                    background-color: {self.color1_hover};
                    border: 2px solid red;
                }}
            """)
            self.entry_password.setStyleSheet(f"""
                QLineEdit {{
                    border-radius: 20px;
                    border: 2px solid red;
                    background-color: {self.color1};
                }}
                QLineEdit:hover {{
                    background-color: {self.color1_hover};
                    border: 2px solid red;
                }}
            """)
            self.view_password.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border-radius: 20px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: gray;
                }}
            """)
            self.btn_login.setStyleSheet(f"""
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
            self.btn_login.setEnabled(False)
            self.warning_login.setText("Seu usuário está inativo.")
            self.warning_login.show()

        else: # Credencias incorretas
            self.entry_password.clear()
            self.entry_username.setStyleSheet(f"""
                QLineEdit {{
                    border-radius: 20px;
                    border: 2px solid red;
                    background-color: {self.color1};
                }}
                QLineEdit:hover {{
                    background-color: {self.color1_hover};
                    border: 2px solid red;
                }}
            """)
            self.entry_password.setStyleSheet(f"""
                QLineEdit {{
                    border-radius: 20px;
                    border: 2px solid red;
                    background-color: {self.color1};
                }}
                QLineEdit:hover {{
                    background-color: {self.color1_hover};
                    border: 2px solid red;
                }}
            """)
            self.view_password.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border-radius: 20px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: gray;
                }}
            """)
            self.warning_login.setText("Usuário ou senha incorretos.")
            self.warning_login.show()


    def show_password(self):
        """Exibe ou oculta a senha."""
        if self.entry_password.echoMode() == QLineEdit.EchoMode.Password:
            self.entry_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.view_password.setIcon(QIcon(self.viewoff_icon_path))
        else:
            self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.view_password.setIcon(QIcon(self.view_icon_path))


    def verificar_limite_exportar(self):
        """Verifica o limite de exportações para usuários não logados."""
        limit_export = 5
        days_limit = 1

        if not self.AUTOJUS_LOG_PATH.exists():
            self.cripto.save_json_cripto(self.AUTOJUS_LOG_PATH, {"export-count": 0, "last-export": None})

        export_data = self.autojus_log_cripto
        if not export_data:
            export_data = {"export-count": 0, "last-export": None}
        
        if "export-count" not in export_data or "last-export" not in export_data:
            export_data["export-count"] = 0
            export_data["last-export"] = None

        if self.icon_user.text().strip() != "Convidado":
            return True
        
        last_export = export_data.get("last-export")
        if last_export:
            last_export_date = datetime.strptime(last_export, "%d-%m-%Y %H:%M:%S")
            time_diff = datetime.now() - last_export_date

            if time_diff.days >= days_limit:
                export_data["export-count"] = 0
        
        if export_data["export-count"] >= limit_export:
            QMessageBox.critical(self, "Limite de Exportação", "Você atingiu o limite de exportações para usuários não logados.")
            self.entry_path_pdf.clear()
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
            return False
        
        export_data["export-count"] += 1
        export_data["last-export"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.cripto.save_json_cripto(self.AUTOJUS_LOG_PATH, export_data)

        return True
    

    def salvar_sessao(self, username):
        """Salvar a sessão atual do usuário."""
        self.cripto.save_json_cripto(self.SESSION_PATH, {"username": username})

    def carregar_sessao(self):
        """Carregar a sessão atual do usuário."""
        session_data = self.cripto.load_json_cripto(self.SESSION_PATH)
        return session_data.get("username") if session_data else None
    
    def limpar_sessao(self):
        """Limpar a sessão atual do usuário."""
        self.cripto.save_json_cripto(self.SESSION_PATH, {"username": None})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec())
