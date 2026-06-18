from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from app.frontend.gui.pallette import *
from app.frontend.components import TitleBar, STTTestSection, YOLOSection, TTSSection, ControllerTestSection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rhythm Game YOLO")
        self.setMinimumSize(600, 500)
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(18)
        layout.setContentsMargins(24, 24, 24, 24)

        self.title_bar = TitleBar()
        layout.addWidget(self.title_bar)

        self.stt_section = STTTestSection()
        layout.addWidget(self.stt_section)

        self.yolo_section = YOLOSection()
        layout.addWidget(self.yolo_section)

        self.tts_section = TTSSection()
        layout.addWidget(self.tts_section)

        self.controller_test = ControllerTestSection()
        layout.addWidget(self.controller_test)

        layout.addStretch()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {DEEP_BLACK}; }}
            QWidget {{ color: {ELECTRIC_BLUE}; font-family: 'Segoe UI', sans-serif; }}
            #title {{ font-size: 28px; font-weight: bold; color: {NEON_PURPLE}; }}
            #section-label {{ font-size: 14px; color: {NEON_CYAN}; }}
            QPushButton#accent-btn {{
                background-color: {DARK_PURPLE};
                border: 1px solid {NEON_PURPLE};
                color: {NEON_MAGENTA};
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }}
            QPushButton#accent-btn:hover {{ background-color: {NEON_PURPLE}; color: {DEEP_BLACK}; }}
            QPushButton#toggle-btn {{
                background-color: {DARK_PURPLE};
                border: 1px solid {NEON_GREEN};
                color: {NEON_GREEN};
                padding: 6px 14px;
                border-radius: 4px;
            }}
            QPushButton#toggle-btn:checked {{ background-color: {NEON_GREEN}; color: {DEEP_BLACK}; }}
            QTextEdit {{
                background-color: {DARK_PURPLE};
                border: 1px solid {NEON_CYAN};
                color: {NEON_CYAN};
                font-size: 13px;
            }}
            QComboBox {{
                background-color: {DARK_PURPLE};
                border: 1px solid {ELECTRIC_BLUE};
                color: {ELECTRIC_BLUE};
                padding: 6px;
            }}
        """)
