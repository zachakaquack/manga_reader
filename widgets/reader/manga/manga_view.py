from PySide6.QtCore import Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout
from widgets.reader.manga.bottom_bar import BottomBar
from settings.loader import load_settings
from widgets.reader.top_bar import ReaderTopBar
from pathlib import Path
from widgets.reader.manga.manga_model import MangaModel
from widgets.reader.manga.manga_page import MangaPage
from widgets.reader.side_bar.side_bar import SideBar


class MangaView(QFrame):

    navigate_back = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # the model holds all the data; this class only holds the gui stuff
        self.model = MangaModel()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        settings = load_settings()
        self.setObjectName("manga_reader_view")
        self.setStyleSheet(
            f"""
            #manga_reader_view{{
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

        self.top_bar = ReaderTopBar()
        self.page = MangaPage()
        self.side_bar = SideBar()
        self.bottom_bar = BottomBar()

        self.top_bar.open_menu_button.connect(self._toggle_menu)
        self.top_bar.navigate_back.connect(self.navigate_back.emit)

        self.page.page_clicked.connect(self.evaluate_change_page_on_click)
        self.side_bar.prev_page.connect(self._prev_page)
        self.side_bar.next_page.connect(self._next_page)

        self.main_layout.addWidget(self.top_bar)

        # thge layout that holds the main page, menu, and bottom bar
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)

        # the layout the holds the main page and the bottom bar
        self.page_bar_layout = QVBoxLayout()
        self.page_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.page_bar_layout.setSpacing(0)

        self.page_bar_layout.addWidget(self.page)
        self.page_bar_layout.addWidget(self.bottom_bar)
        self.bottom_layout.addLayout(self.page_bar_layout)
        self.bottom_layout.addWidget(self.side_bar)

        self.main_layout.addLayout(self.bottom_layout)

    def evaluate_change_page_on_click(self, event: QMouseEvent) -> int:
        index = self.model.evaluate_change_page_on_click(event, self.page.width())
        self._go_to_page_index(index)
        return index

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

            case Qt.Key.Key_Return:
                self._toggle_menu()

        return super().keyPressEvent(event)

    def _next_page(self) -> int:
        page_number_index = self.model.next_page()
        self._go_to_page_index(page_number_index)
        return page_number_index

    def _prev_page(self) -> int:
        page_number_index = self.model.prev_page()
        self._go_to_page_index(page_number_index)
        return page_number_index

    def _go_to_page_index(self, index: int) -> None:
        self.page.change_page(self.model.image_paths[index])
        self.bottom_bar.set_bar_filled_count(index + 1)
        self.top_bar.page.update_current(index + 1)
        self.side_bar.change_page_in_changer(index + 1)

    def load_manga(self, image_paths: list[Path]) -> None:
        self.model.load_manga(image_paths)

        self.top_bar.page.update_limit(len(image_paths))
        self.bottom_bar.set_bar_total_count(len(image_paths))
        self.bottom_bar.set_bar_filled_count(1)
        self.side_bar.change_page_in_changer(1)

        self.page.change_page(self.model.image_paths[0])
