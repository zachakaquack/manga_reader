from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy

from settings.loader import load_settings


class BottomBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.total_count: int
        self.current_count: int
        self.bars: list[QFrame] = []

        self.settings = load_settings()
        self.setFixedHeight(self.settings.bottom_bar.height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setStyleSheet("background-color: orange;")

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

    def set_bar_total_count(self, count: int):
        self.total_count = count
        for _ in range(count):
            f = QLabel("")
            f.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            f.setStyleSheet(
                f"background-color: {self.settings.colors.bottom_bar_background}"
            )
            self.bars.append(f)
            self.main_layout.addWidget(f)

    def set_bar_filled_count(self, count: int):
        self.filled_count = count
        for i in range(len(self.bars)):
            self.bars[i].setStyleSheet(
                f"background-color: {self.settings.colors.bottom_bar_background}"
            )

        for i in range(count):
            self.bars[i].setStyleSheet(
                f"background-color: {self.settings.colors.bottom_bar_filled_in}"
            )
