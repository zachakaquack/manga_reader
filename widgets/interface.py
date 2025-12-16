from pathlib import Path
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from settings.loader import load_settings
from widgets.reader.manga.manga_view import MangaView
from widgets.reader.scroller.scroll_view import ScrollerView


class Interface(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        settings = load_settings()
        self.setObjectName("interface")
        self.setStyleSheet(
            f"""
            #interface{{
                background-color: {settings.colors.main_background};
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

        self.mangas = [
                Path("./assets/test/manga_page.png"),
                Path("./assets/test/manga_page.png"),
                Path("./assets/test/manga_page.png"),
                Path("./assets/test/manga_page.png"),
                Path("./assets/test/manga_page.png"),
            ]
        
        self.scrollers = [
                Path("./assets/test/scroller_page.png"),
                Path("./assets/test/scroller_page.png"),
                Path("./assets/test/scroller_page.png"),
                Path("./assets/test/scroller_page.png"),
                Path("./assets/test/scroller_page.png"),
            ]

        # self.load_scroller(self.scrollers)
        self.load_manga(self.mangas)

    def load_manga(self, image_paths: list[Path]):
        view = MangaView()
        view.load_manga(image_paths)
        self.main_layout.addWidget(view)

    def load_scroller(self, image_paths: list[Path]):
        view = ScrollerView()
        view.load_manga(image_paths)
        self.main_layout.addWidget(view)
