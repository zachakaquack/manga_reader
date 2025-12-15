from pathlib import Path
from PySide6.QtGui import QPixmap, QResizeEvent, Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout


class MangaPage(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._pixmap: QPixmap | None = None
        self._pixmap_scaled: QPixmap | None = None

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel()
        self.main_layout.addWidget(self.label)

    def change_page(self, image_path: Path):
        pm = QPixmap(image_path)
        self._pixmap = pm

        self._pixmap_scaled= self._pixmap.scaled(
            self.size(),
            aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
            mode=Qt.TransformationMode.FastTransformation
        )

        self.label.setPixmap(self._pixmap_scaled)

        # TODO: cache the image

    def resizeEvent(self, event: QResizeEvent, /) -> None:

        # reload the first opening to get the actual scale
        if self._pixmap is not None:
            self._pixmap_scaled= self._pixmap.scaled(
                self.size(),
                aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                mode=Qt.TransformationMode.FastTransformation
            )

            self.label.setPixmap(self._pixmap_scaled)
        return super().resizeEvent(event)
