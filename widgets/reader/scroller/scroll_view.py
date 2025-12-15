from PySide6.QtGui import QKeyEvent, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout
from settings.loader import load_settings
from widgets.reader.scroller.scroll_model import ScrollerModel
from widgets.reader.scroller.scroller_page import ScrollerPage
from widgets.reader.top_bar import ReaderTopBar
from pathlib import Path
from widgets.reader.manga.manga_page import MangaPage
from widgets.reader.side_bar import SideBar

class ScrollerView(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # the model holds all the data; this class only holds the gui stuff
        self.model = ScrollerModel()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        settings = load_settings()
        self.setObjectName("scroller_reader_view")
        self.setStyleSheet(
            f"""
            #scroller_reader_view{{
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
        self.page = ScrollerPage()
        self.side_bar = SideBar()

        self.top_bar.open_menu_button.connect(self._toggle_menu)
        # self.page.

        self.main_layout.addWidget(self.top_bar)

        # thge layout that holds the main page and the menu
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)


        self.bottom_layout.addWidget(self.page)
        self.bottom_layout.addWidget(self.side_bar)
        self.main_layout.addLayout(self.bottom_layout)

    def _toggle_menu(self) -> None:
        if self.side_bar.isHidden():
            self.side_bar.show()
        else:
            self.side_bar.hide()

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

            case Qt.Key.Key_Tab:
                self._toggle_menu()


        return super().keyPressEvent(event)

    def _next_page(self) -> int:
        pixels = self.model.next_page()
        self.page.scroll_to_value(pixels)

        self.top_bar.page.update_current(self.model.page_number_index + 1)
        return self.model.page_number_index

    def _prev_page(self) -> int:
        pixels = self.model.prev_page()
        self.page.scroll_to_value(pixels)

        self.top_bar.page.update_current(self.model.page_number_index + 1)
        return self.model.page_number_index

    def load_manga(self, image_paths: list[Path]) -> None:

        self.model.load_manga(image_paths)

        # it's easier and more efficient to calculate all of the pm's inside this;
        # the get_pixels_to_image function requires the images themselves
        _, scaled_pixmaps = self.model.create_pixmaps()
        self.page.load_pages(scaled_pixmaps)
        self.page.scroll_to_value(0)

        self.top_bar.page.update_limit(len(image_paths))

