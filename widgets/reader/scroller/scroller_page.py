# SCROLLER PAGE: THIS MEANS MANHWA AND MANWHA (both are scrolling)
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QSizePolicy, QVBoxLayout
from widgets.components.button import Button


class ScrollerPage(QScrollArea):

    next_chapter = Signal()
    scroll_amount_changed = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._pixmaps: list[QPixmap] = []
        self._pixmaps_scaled: list[QPixmap] = []
        self._pages: list[QLabel] = []

        self.setStyleSheet(
            """
            QFrame{
                background: transparent;
            }
            """
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.main_widget = QFrame(self)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        self.verticalScrollBar().valueChanged.connect(self.scroll_amount_changed)

    def scroll_to_value(self, value: int) -> None:
        self.verticalScrollBar().setValue(value)

    def load_pages(self, scaled_pixmaps: list[QPixmap]):
        for scaled in scaled_pixmaps:
            page = QLabel()
            page.setPixmap(scaled)

            self._pages.append(page)
            self.main_layout.addWidget(page)


        self.main_layout.addSpacing(20)
        button = Button("Next Chapter")
        self.main_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        # add some extra spacing to both the page number updates, and you have the ability
        # to now only see the last page if you want to
        magic_height_spacing = scaled_pixmaps[-1].height() // 2
        self.main_layout.addSpacing(magic_height_spacing)
