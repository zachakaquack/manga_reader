from pathlib import Path
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout
from widgets.components.button import Button


class Home(QFrame):

    load_manga = Signal(list)
    load_scroller = Signal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        manga_pages = [
            Path("./assets/test/manga_page_1.png"),
            Path("./assets/test/manga_page_2.png"),
            Path("./assets/test/manga_page_3.png"),
            Path("./assets/test/manga_page_4.png"),
            Path("./assets/test/manga_page_5.png"),
        ]

        scroller_pages = [
            Path("./assets/test/scroller_page_1.png"),
            Path("./assets/test/scroller_page_2.png"),
            Path("./assets/test/scroller_page_3.png"),
            Path("./assets/test/scroller_page_4.png"),
            Path("./assets/test/scroller_page_5.png"),
        ]

        test_manga = Button("test manga")
        test_scroller = Button("test scroller")

        test_manga.clicked.connect(lambda _: self.load_manga.emit(manga_pages))
        test_scroller.clicked.connect(lambda _: self.load_scroller.emit(scroller_pages))

        self.main_layout.addWidget(test_manga)
        self.main_layout.addWidget(test_scroller)
