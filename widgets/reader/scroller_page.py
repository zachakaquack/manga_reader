# SCROLLER PAGE: THIS MEANS MANHWA AND MANWHA (both are scrolling)
from pathlib import Path
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QPixmap, QResizeEvent, QShowEvent, Qt
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QSizePolicy, QVBoxLayout
from widgets.components.button import Button


class ScrollerPage(QScrollArea):

    next_chapter = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._pixmaps: list[QPixmap] = []
        self._pixmaps_scaled: list[QPixmap] = []
        self._pages: list[QLabel] = []

        self.setStyleSheet(
            """
            QFrame{
                background: transparent;
            }
            """
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.main_widget = QFrame(self)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def load_pages(self, image_paths: list[str]):
        for path in image_paths:
            pm = QPixmap(path)

            self._pixmaps.append(pm)
            # self._pixmaps_scaled.append(scaled)



    def change_page(self, image_path: Path):
        pass

    def showEvent(self, event: QShowEvent, /) -> None:
        if(len(self._pixmaps) < 1):
            return

        for pm in self._pixmaps:
            # width = self.width() - self.verticalScrollBar().width()
            # TODO: change to make the verticalScrollBar's width not a magic number
            # it's 100 by default and apparently this function runs before a resize event
            width = self.width() - 16

            scaled = pm.scaled(
                # self.size(),
                QSize(width, 123456789),
                aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                mode=Qt.TransformationMode.FastTransformation
            )
            self._pixmaps_scaled.append(scaled)

        for scaled_pm in self._pixmaps_scaled:
            page = QLabel()
            page.setPixmap(scaled_pm)

            self._pages.append(page)
            self.main_layout.addWidget(page)

        # at the very end, add the "next chapter" button
        self.main_layout.addSpacing(20)

        next_chapter = Button("Next Chapter")
        next_chapter.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        next_chapter.clicked.connect(self.next_chapter)

        self.main_layout.addWidget(next_chapter, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(20)

        return super().showEvent(event)

    # def resizeEvent(self, arg__1: QResizeEvent, /) -> None:
        # for pm in self._pixmaps:
        #     # width = self.width() - self.verticalScrollBar().width()
        #     # TODO: change to make the verticalScrollBar's width not a magic number
        #     # 
        #     width = self.width() - 16
        #
        #     scaled = pm.scaled(
        #         # self.size(),
        #         QSize(width, 123456789),
        #         aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
        #         mode=Qt.TransformationMode.FastTransformation
        #     )
        #     self._pixmaps_scaled.append(scaled)
        # print("finished")
        # return super().resizeEvent(arg__1)

    # def resizeEvent(self, event: QResizeEvent, /) -> None:
    #
    #     if(len(self._pixmaps_scaled) < 1):
    #         return
    #
    #     for scaled_pm in self._pixmaps_scaled:
    #         page = QLabel()
    #         page.setPixmap(scaled_pm)
    #
    #         self._pages.append(page)
    #         self.main_layout.addWidget(page)
    #
    #     # at the very end, add the "next chapter" button
    #     self.main_layout.addSpacing(20)
    #
    #     next_chapter = Button("Next Chapter")
    #     next_chapter.setSizePolicy(
    #         QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
    #     )
    #     next_chapter.clicked.connect(self.next_chapter)
    #
    #     self.main_layout.addWidget(next_chapter, alignment=Qt.AlignmentFlag.AlignCenter)
    #     self.main_layout.addSpacing(20)
    #
    #     return super().resizeEvent(event)
