from pathlib import Path

from PySide6.QtGui import QMouseEvent


class MangaModel:
    def __init__(self):

        self.page_number_index: int = 0
        self.image_paths: list[Path] = []

    def next_page(self) -> int:
        if self.page_number_index + 1 < len(self.image_paths):
            self.page_number_index += 1
            return self.page_number_index
        return self.page_number_index

    def prev_page(self) -> int:
        if self.page_number_index <= 0:
            return self.page_number_index
        self.page_number_index -= 1
        return self.page_number_index

    def load_manga(self, image_paths: list[Path]) -> list[Path]:
        self.image_paths = image_paths
        if len(image_paths) < 1:
            raise IndexError("Too few images:", len(image_paths))

        return image_paths

    def evaluate_change_page_on_click(self, event: QMouseEvent, width: int) -> int:
        start_of_right_half = width // 2
        if event.pos().x() > start_of_right_half:
            return self.next_page()
        else:
            return self.prev_page()
