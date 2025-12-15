import unittest
from settings import settings
from settings import loader

class TestSettings(unittest.TestCase):
    def setUp(self) -> None:
        loader._reset_for_tests()

    def test_loadCorrectDefaultSettings(self):
        default = settings.Settings()
        loaded = loader.load_settings()

        self.assertEqual(default, loaded)
