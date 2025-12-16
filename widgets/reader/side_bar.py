from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from settings.loader import load_settings


class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        settings = load_settings()
        self.setFixedWidth(settings.side_bar.width)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.setObjectName("reader_side_bar")
        self.setStyleSheet(
            f"""
            #reader_side_bar{{
                background-color: {settings.colors.reader_top_bar_background};
            }}
            QLabel{{
                color: {settings.colors.main_text};
            }}

            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
