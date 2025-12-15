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
                background-color: {settings.colors.main_background_color};
                color: {settings.colors.main_text_color};
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

        # self.manga_view = MangaView()
        self.manga_view = ScrollerView()
        self.main_layout.addWidget(self.manga_view)

        self.manga_view.load_manga(
            [
                Path("/home/zach/Pictures/bgs/adachi.jpeg"),
                Path("/home/zach/Pictures/bgs/adachi2.jpeg"),
                Path("/home/zach/Pictures/bgs/adachi3.jpg"),
                Path("/home/zach/Pictures/bgs/adachi4.jpg"),
                Path("/home/zach/Pictures/bgs/adachi5.jpg"),
                Path("/home/zach/Pictures/bgs/adachi6.jpg"),
            ]
        )
