import unittest

from settings import settings
from settings import loader

class Tester(unittest.TestCase):
    def setUp(self) -> None:
        loader._reset_for_tests()

    def test_loadCorrectSettings(self):
        default = settings.Settings()
        loaded = loader.load_settings()

        self.assertEqual(default, loaded)

if __name__ == "__main__":
    unittest.main()
