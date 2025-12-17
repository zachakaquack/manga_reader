from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from settings.loader import load_settings
from widgets.reader.side_bar.list_view import ListView
from widgets.reader.side_bar.main_view import SideBarMainView
from widgets.other.switcher import Switcher


class SideBar(QFrame):

    next_page = Signal()
    prev_page = Signal()
    navigate_page_index = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._page_count: int = 0
        self._page_number_index: int = 0

        settings = load_settings()
        self.setFixedWidth(settings.side_bar.width)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.setObjectName("reader_side_bar")
        self.setStyleSheet(
            f"""
            #reader_side_bar{{
                background-color: {settings.colors.side_bar_top_bar_background};
            }}
            QLabel{{
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

        self.switcher = Switcher()
        self.main_view = SideBarMainView()
        self.list_view = ListView()

        self.main_view.prev_page.connect(self.prev_page)
        self.main_view.next_page.connect(self.next_page)
        self.main_view.switch_to_big_view.connect(self._switch_to_list_view)

        self.list_view.back.connect(lambda: self.switcher.switchTo("main"))
        self.list_view.navigate_page_index.connect(self._navigate_page_index)

        self.switcher.addSwitcher("main", self.main_view)
        self.switcher.addSwitcher("list", self.list_view)

        self.main_layout.addWidget(self.switcher)

    def _navigate_page_index(self, index: int):
        self.navigate_page_index.emit(index)
        self.set_current_page_number(index + 1)
        self.switcher.switchTo("main")

    def set_current_page_number(self, number: int):
        self._page_number_index = number - 1
        self.main_view.page_changer.page_button.setText(f"Page {number}")

    def set_page_count(self, count: int):
        self._page_count = count

    def _switch_to_list_view(self, view: str):
        self.list_view.open_view(self._page_count, view, self._page_number_index)
        self.switcher.switchTo("list")
