from PySide6.QtGui import QKeyEvent, Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout
from settings.loader import load_settings
from widgets.general.reader_top_bar import ReaderTopBar
from pathlib import Path
from widgets.reader.model import ReaderModel
from widgets.reader.page import Page

class ReaderView(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # the model holds all the data; this class only holds the gui stuff
        self.model = ReaderModel()

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

        self.page = Page()
        self.main_layout.addWidget(self.page)

    def keyPressEvent(self, event: QKeyEvent, /) -> None:

        match event.key():
            case Qt.Key.Key_H:
                self._prev_page()
            case Qt.Key.Key_A:
                self._prev_page()

            case Qt.Key.Key_L:
                self._next_page()
            case Qt.Key.Key_D:
                self._next_page()


        return super().keyPressEvent(event)

    def _next_page(self) -> int:
        page_number_index = self.model.next_page()
        self.page.change_page(self.model.image_paths[page_number_index])
        self.top_bar.page.update_current(page_number_index + 1)
        return page_number_index

    def _prev_page(self) -> int:
        page_number_index = self.model.prev_page()
        self.page.change_page(self.model.image_paths[page_number_index])
        self.top_bar.page.update_current(page_number_index + 1)
        return page_number_index

    def load_manga(self, image_paths: list[Path]) -> None:
        self.model.load_manga(image_paths)

        self.top_bar.page.update_limit(len(image_paths))
        self.image_paths = image_paths
        self.page.change_page(image_paths[0])
