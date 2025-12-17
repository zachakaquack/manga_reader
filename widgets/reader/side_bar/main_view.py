from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from widgets.reader.side_bar.page_changer import PageChanger


class SideBarMainView(QFrame):

    next_page = Signal()
    prev_page = Signal()
    switch_to_big_view = Signal(str)

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

        self.page_changer = PageChanger()
        self.page_changer.decrement.connect(self.prev_page)
        self.page_changer.increment.connect(self.next_page)
        self.page_changer.switch_to_big_view.connect(self.switch_to_big_view)
        self.main_layout.addWidget(self.page_changer)
