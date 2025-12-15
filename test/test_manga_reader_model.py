import unittest
from pathlib import Path
from widgets.reader.manga.manga_model import MangaModel

class TestMangaReaderModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = MangaModel()
        self.model.image_paths = [Path.cwd()] * 3
        self.model.page_number_index = 1

    def test_incrementPageNumberValidMangaReader(self):
        # simple increment from 1 -> 2
        target = self.model.page_number_index + 1
        self.assertEqual(target, self.model.next_page())

    def test_incrementPageNumberInvalidMangaReader(self):
        # should be 2 because it can't increment to the next page
        target = 2 
        self.assertEqual(target, self.model.next_page())

    def test_decrementPageNumberValidMangaReader(self):
        # simple decrement from 1 -> 0
        target = 0 
        self.assertEqual(target, self.model.prev_page())

    def test_decrementPageNumberInvalidMangaReader(self):
        # should be 0 because it can't decrement to the prev page
        target = 0 
        self.assertEqual(target, self.model.prev_page())

    def test_notEnoughPagesWhenLoadingManga(self):
        with self.assertRaises(IndexError):
            self.model.load_manga([])

    def test_loadsCorrectAmountOfManga(self):
        target = 3
        self.model.load_manga([Path.cwd()] * 3)

        self.assertEqual(target, len(self.model.image_paths))
