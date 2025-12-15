from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout
from settings.loader import load_settings
from widgets.components.button import Button


class ReaderTopBar(QFrame):

    open_menu_button = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        settings = load_settings()
        self.setFixedHeight(settings.reader.reader_top_bar_height)

        self.setObjectName("reader_top_bar")
        self.setStyleSheet(
            f"""
            #reader_top_bar{{
                background-color: {settings.colors.reader_top_bar_background_color};
                color: {settings.colors.main_text_color};
            }}
            QLabel{{
                color: {settings.colors.main_text_color};
            }}

            """
        )

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacerItem(
            QSpacerItem(
                1, 0,
                hData=QSizePolicy.Policy.Expanding
            )
        )

        # self.chapter = CountSlashTotal("Chapter", 100, 150)
        self.page = CountSlashTotal("Page", 1, 20)

        # self.main_layout.addWidget(self.chapter)
        self.main_layout.addWidget(self.page)

        menu_button = Button("Menu")
        menu_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        menu_button.clicked.connect(self.open_menu_button)
        self.main_layout.addWidget(menu_button)


# quite possibly the worst name for this ever
# just a label that is "name current/limit"
# like "page 7/27"
class CountSlashTotal(QFrame):
    def __init__(self, name: str, current: int, limit: int, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.name = name
        self.current = current
        self.limit = limit

        self.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(f"{self.name} {self.current}/{self.limit}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.label)

    def _refresh_label(self):
        self.label.setText(f"{self.name} {self.current}/{self.limit}")

    def update_current(self, current: int) -> None:
        self.current = current
        self._refresh_label()

    def update_limit(self, limit: int) -> None:
        self.limit = limit
        self._refresh_label()
