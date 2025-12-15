import unittest
from pathlib import Path
from widgets.manga_reader.model import MangaReaderModel

class TestMangaReaderModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = MangaReaderModel()
        self.model.image_paths = [Path.cwd()] * 3
        self.model.page_number_index = 1

    def test_incrementPageNumberValidMangaReader(self):
        target = self.model.page_number_index + 1
        self.assertEqual(target, self.model.next_page())

    def test_incrementPageNumberInvalidMangaReader(self):
        # should be 2 because it can't increment to the next page
        target = 2 
        self.assertEqual(target, self.model.next_page())

    def test_decrementPageNumberValidMangaReader(self):
        target = 0 
        self.assertEqual(target, self.model.prev_page())

    def test_decrementPageNumberInvalidMangaReader(self):
        # should be 0 because it can't decrement to the prev page
        target = 0 
        self.assertEqual(target, self.model.prev_page())
