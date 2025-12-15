import unittest
from pathlib import Path
from widgets.reader.scroller.scroll_model import ScrollerModel

class TestScrollerReaderModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ScrollerModel()
        self.model.image_paths = [
                Path("/home/zach/Desktop/python/reader/assets/test/SMALL_scroller_page.png"),
                Path("/home/zach/Desktop/python/reader/assets/test/SMALL_scroller_page.png"),
                Path("/home/zach/Desktop/python/reader/assets/test/SMALL_scroller_page.png"),
        ]
        self.model.page_number_index = 1
        self.model.create_images()

    def test_incrementPageNumberPixelsScrolledScrollerReader(self):
        # next_page returns the pixels to scroll in the qscrollarea
        # each scroller_page is 200x1000
        # the image's height gets scaled up to 5000 because 200 * 5 = 1000 (1000 is goal width)
        # pixels should be (index + 1) * 5000
        one_image_height = self.model._images_scaled[0].height()
        target_pixels = one_image_height * (self.model.page_number_index + 1)
        self.assertEqual(target_pixels, self.model.next_page())

    def test_decrementPageNumberPixelsScrolledScrollerReader(self):
        # prev_page returns the pixels to scroll in the qscrollarea
        # each scroller_page is 200x1000
        # the image's height gets scaled up to 5000 because 200 * 5 = 1000 (1000 is goal width)
        # pixels should be (index - 1) * 5000
        one_image_height = self.model._images_scaled[0].height()
        target_pixels = one_image_height * (self.model.page_number_index - 1)
        self.assertEqual(target_pixels, self.model.prev_page())

    def test_incrementPageNumberInvalidScrollerReader(self):
        # the image's height gets scaled up to 5000 because 200 * 5 = 1000 (1000 is goal width)
        # pixels should be (index - 1) * 5000
        self.model.page_number_index = 2
        one_image_height = self.model._images_scaled[0].height()

        # target is the same, because we can't skip forward any pages
        target_pixels = one_image_height * (self.model.page_number_index)
        self.assertEqual(target_pixels, self.model.next_page())

    def test_decrementPageNumberInvalidScrollerReader(self):
        # the image's height gets scaled up to 5000 because 200 * 5 = 1000 (1000 is goal width)
        # pixels should be (index - 1) * 5000
        self.model.page_number_index = 0
        one_image_height = self.model._images_scaled[0].height()

        # target is the same, because we can't skip forward any pages
        target_pixels = one_image_height
        self.assertEqual(target_pixels, self.model.next_page())
