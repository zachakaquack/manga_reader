from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout
from settings.loader import load_settings
from widgets.general.reader_top_bar import ReaderTopBar


class MangaReaderView(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        settings = load_settings()
        self.setObjectName("manga_reader_view")
        self.setStyleSheet(
            f"""
            #manga_reader_view{{
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


        self.top_bar = ReaderTopBar()
        self.main_layout.addWidget(self.top_bar)

