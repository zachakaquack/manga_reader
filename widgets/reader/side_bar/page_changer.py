from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy
from settings.loader import load_settings
from widgets.components.button import Button


class PageChanger(QFrame):

    increment = Signal()
    decrement = Signal()
    switch_to_big_view = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        settings = load_settings()

        decrement = Button("<")
        self.page_button = Button("Page 123")
        increment = Button(">")

        decrement.clicked.connect(self.decrement)
        self.page_button.clicked.connect(lambda: self.switch_to_big_view.emit("Page"))
        increment.clicked.connect(self.increment)

        # TODO: maybe change to not be fixed? has to be fixed due
        # to stupid layout behavior with qpushbuttons
        decrement.setFixedWidth(settings.side_bar.arrow_button_fixed_width)
        increment.setFixedWidth(settings.side_bar.arrow_button_fixed_width)

        for button in [decrement, self.page_button, increment]:
            button.setFixedHeight(settings.side_bar.button_height)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            self.main_layout.addWidget(button)
