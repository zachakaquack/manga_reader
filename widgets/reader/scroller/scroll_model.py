from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QImage, Qt


class ScrollerModel:
    def __init__(self):

        self.page_number_index: int = 0
        self.current_pixels_scrolled: int = 0
        self.image_paths: list[Path] = []

        self._images: list[QImage] = []
        self._images_scaled: list[QImage] = []
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

    def create_images(self) -> tuple[list[QImage], list[QImage]]:
        if len(self.image_paths) < 1:
            raise IndexError("Too few images:", len(self.image_paths))

        for path in self.image_paths:
            image = QImage(path)
            self._images.append(image)

            # TODO: fix magic number (1000)
            # 1000 fits whether you have the menu open or not
            # 1000 because the width() of the widget is not set at runtime
            scaled = image.scaled(
                QSize(1000, 12345),
                aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                mode=Qt.TransformationMode.FastTransformation
            )

            self._images_scaled.append(scaled)

            if len(self.ranges) < 1:
                previous = 0
            else:
                previous = self.ranges[-1]
            self.ranges.append(previous + scaled.height())

        return self._images, self._images_scaled
    
    def get_pixels_to_image_index(self, image_index: int) -> int:
        total_pixels = 0
        for i in range(len(self.image_paths)):
            current_height = self._images_scaled[i].height()
            if i == image_index:
                return total_pixels

            total_pixels += current_height

        return 0
