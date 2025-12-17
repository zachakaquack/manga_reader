from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QSizePolicy, QVBoxLayout

from settings.loader import load_settings
from widgets.components.button import Button


class ListView(QScrollArea):

    back = Signal()
    navigate_page_index = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.settings = load_settings()

        self.setObjectName("list_view")
        self.setStyleSheet(
            f"""
                background-color: {self.settings.colors.side_bar_top_bar_background}
            """
        )

        self.main_widget = QFrame(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def open_view(self, count: int, title: str, current_page_index: int) -> None:
        self._reset()
        self._add_back_button()
        for i in range(count):
            text = f"{title} {i + 1}"
            button = Button(text)
            button.setFixedHeight(self.settings.side_bar.list_view_button_fixed_height)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            button.clicked.connect(
                lambda _, index=i: self.navigate_page_index.emit(index)
            )

            if i == current_page_index:
                button.setStyleSheet(
                    f"""
                    background-color: {self.settings.colors.side_bar_button_active_chapter};
                    color: {self.settings.colors.main_text}
                    """
                )

            self.main_layout.addWidget(button)

    def _add_back_button(self):
        back = Button("Back")
        back.setFixedHeight(self.settings.side_bar.list_view_button_fixed_height)
        back.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        back.clicked.connect(self.back)

        self.main_layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addSpacing(5)

    def _reset(self):
        while (child := self.main_layout.takeAt(0)) != None:
            if child.widget() and isinstance(child.widget(), Button):
                child.widget().deleteLater()
