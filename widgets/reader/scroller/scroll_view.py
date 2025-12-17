from PySide6.QtCore import Signal
from PySide6.QtGui import QKeyEvent, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout
from settings.loader import load_settings
from widgets.reader.scroller.scroll_model import ScrollerModel
from widgets.reader.scroller.scroller_page import ScrollerPage
from widgets.reader.top_bar import ReaderTopBar
from pathlib import Path
from widgets.reader.side_bar.side_bar import SideBar


class ScrollerView(QFrame):

    navigate_back = Signal()

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
        self.page = ScrollerPage()
        self.side_bar = SideBar()

        self.top_bar.open_menu_button.connect(self._toggle_menu)
        self.top_bar.navigate_back.connect(self.navigate_back.emit)

        self.page.scroll_amount_changed.connect(self.change_scrolled_page)

        self.side_bar.prev_page.connect(self._prev_page)
        self.side_bar.next_page.connect(self._next_page)
        self.side_bar.navigate_page_index.connect(self._go_to_page_index)

        self.main_layout.addWidget(self.top_bar)

        # thge layout that holds the main page and the menu
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)

        self.bottom_layout.addWidget(self.page)
        self.bottom_layout.addWidget(self.side_bar)
        self.main_layout.addLayout(self.bottom_layout)

    def change_scrolled_page(self, scrolled_pixels: int) -> int:
        index = self.model.evaluate_scrolled_page_index(scrolled_pixels)

        # not using _go_to_page_index because it would cause an infinite loop
        self.top_bar.page.update_current(index + 1)
        self.side_bar.set_current_page_number(index + 1)
        return index

    def _toggle_menu(self) -> None:
        if self.side_bar.isHidden():
            self.side_bar.show()
        else:
            self.side_bar.hide()

    def _go_to_page_index(self, index: int):
        self.top_bar.page.update_current(index + 1)
        self.side_bar.set_current_page_number(index + 1)
        pixels = self.model.get_pixels_to_image_index(index)
        self.page.scroll_to_value(pixels)

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
        pixels = self.model.next_page()
        self.page.scroll_to_value(pixels)
        self._go_to_page_index(self.model.page_number_index)
        return self.model.page_number_index

    def _prev_page(self) -> int:
        pixels = self.model.prev_page()
        self.page.scroll_to_value(pixels)
        self._go_to_page_index(self.model.page_number_index)
        return self.model.page_number_index

    def load_manga(self, image_paths: list[Path]) -> None:

        self.model.load_manga(image_paths)

        # it's easier and more efficient to calculate all of the pm's inside this;
        # the get_pixels_to_image function requires the images themselves
        _, scaled_images = self.model.create_images()
        self.page.load_pages(scaled_images)
        self.page.scroll_to_value(0)

        self.side_bar.set_page_count(len(image_paths))
        self.side_bar.set_current_page_number(1)

        self.top_bar.page.update_limit(len(image_paths))
