import unittest

from unittest.mock import patch
from dog.utils import dog_utils

class DogUtilsTestCase(unittest.TestCase):
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