import unittest

from utils import dog_utils
from unittest.mock import patch, Mock

class DogUtilsTestCase(unittest.TestCase):
    def test_is_blank_line(self):
        line = ""
        self.assertTrue(dog_utils.is_blank_line(line))

    def test_is_not_blank_line(self):
        line = "RandomTextWhichShouldNotBeABlankLineCertainly123456"
        self.assertFalse(dog_utils.is_blank_line(line))

    @patch("builtins.print")
    def test_print_unbuffered(self, mock_print):
        data = "Line to be printed out"
        dog_utils.print_unbuffered(data)
        mock_print.assert_called_with(data, flush=True, end="")

    @patch("builtins.print")
    def test_print_unbuffered_line(self, mock_print):
        data = "Line to be printed with newline"
        dog_utils.print_unbuffered_line(data)
        mock_print.assert_called_with(data, flush=True)