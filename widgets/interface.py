from pathlib import Path
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from settings.loader import load_settings
from widgets.home.home import Home
from widgets.other.switcher import Switcher
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

        self.main_switcher = Switcher()
        self.home = Home()
        self.manga_view = MangaView()
        self.scroller_view = ScrollerView()

        self.home.load_manga.connect(self.load_manga)
        self.home.load_scroller.connect(self.load_scroller)

        self.main_switcher.addSwitcher("home", self.home)
        self.main_switcher.addSwitcher("manga_view", self.manga_view)
        self.main_switcher.addSwitcher("scroller_view", self.scroller_view)
        self.main_switcher.setMainSwitch("home")

        self.main_layout.addWidget(self.main_switcher)

    def load_manga(self, image_paths: list[Path]):
        self.main_switcher.switchTo("manga_view")
        self.manga_view.load_manga(image_paths)

    def load_scroller(self, image_paths: list[Path]):
        self.main_switcher.switchTo("scroller_view")
        self.scroller_view.load_manga(image_paths)
