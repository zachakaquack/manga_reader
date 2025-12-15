from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt


class ScrollerModel:
    def __init__(self):

        self.page_number_index: int = 0
        self.current_pixels_scrolled: int = 0
        self.image_paths: list[Path] = []

        self.pixmaps: list[QPixmap] = []
        self.scaled_pixmaps: list[QPixmap] = []
        self.ranges: list[int] = []

    def evaluate_scrolled_page_index(self, scrolled_pixels: int) -> int:
        for i, image_bottom in enumerate(self.ranges):
            if scrolled_pixels < image_bottom:
                self.page_number_index = i
                return i
        return 0

    def next_page(self) -> int:
        if self.page_number_index + 1 < len(self.image_paths):
            self.page_number_index += 1
            pixels = self.get_pixels_to_image_index(self.page_number_index)
            return pixels
        return self.get_pixels_to_image_index(self.page_number_index)

    def prev_page(self) -> int:
        if self.page_number_index > 0:
            self.page_number_index -= 1
            pixels = self.get_pixels_to_image_index(self.page_number_index)
            return pixels
        return self.get_pixels_to_image_index(self.page_number_index)

    def load_manga(self, image_paths: list[Path]) -> list[Path]:
        self.image_paths = image_paths
        if(len(image_paths) < 1):
            raise IndexError("Too few images:", len(image_paths))

        return image_paths

    def create_pixmaps(self) -> tuple[list[QPixmap], list[QPixmap]]:
        for path in self.image_paths:
            pixmap = QPixmap(path)
            self.pixmaps.append(pixmap)

            # TODO: fix magic number (1000)
            # 1000 fits whether you have the menu open or not
            scaled = pixmap.scaled(
                QSize(1000, 12345),
                aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                mode=Qt.TransformationMode.FastTransformation
            )

            self.scaled_pixmaps.append(scaled)

            if len(self.ranges) < 1:
                previous = 0
            else:
                previous = self.ranges[-1]
            self.ranges.append(previous + scaled.height())

        return (self.pixmaps, self.scaled_pixmaps)
    
    def get_pixels_to_image_index(self, image_index: int) -> int:
        total_pixels = 0
        for i in range(len(self.image_paths)):
            current_height = self.scaled_pixmaps[i].height()
            if i == image_index:
                return total_pixels

            total_pixels += current_height

        return 0
