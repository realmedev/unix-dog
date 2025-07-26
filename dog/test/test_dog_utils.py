import unittest

from src.utils import dog_utils
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

    def test_format_output_with_nonblank_line_numbers_and_blank_line(self):
        mock_config = Mock()
        mock_config.show_nonblank_line_numbers.return_value = True

        line = "\n"
        line_number = 1

        formatted_line = dog_utils.format_output(line, line_number, mock_config)
        self.assertEqual(line, formatted_line)

        mock_config.show_nonblank_line_numbers.assert_called()
        mock_config.show_all_line_numbers.assert_not_called()
        mock_config.get_line_adjustment.assert_not_called()

        line = "$\n"
        formatted_line = dog_utils.format_output(line, line_number, mock_config)
        self.assertEqual(line, formatted_line)

        mock_config.show_nonblank_line_numbers.assert_called()
        mock_config.show_all_line_numbers.assert_not_called()
        mock_config.get_line_adjustment.assert_not_called()

    def test_format_output_with_nonblank_line_numbers_and_non_blank_line(self):
        line_adjustment = 8

        mock_config = Mock()
        mock_config.show_nonblank_line_numbers.return_value = True
        mock_config.get_line_adjustment.return_value = line_adjustment 

        line = "This is a line of text"
        line_number = 1 

        expected_line = f"{line_number}  {line}".rjust(len(line) + line_adjustment)

        formatted_line = dog_utils.format_output(line, line_number, mock_config)
        self.assertEqual(formatted_line, expected_line)

        mock_config.show_nonblank_line_numbers.assert_called()
        mock_config.show_all_line_numbers.assert_not_called()
        mock_config.get_line_adjustment.assert_called()

    def test_format_output_with_all_line_numbers(self):
        line_adjustment = 8

        mock_config = Mock()
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = True
        mock_config.get_line_adjustment.return_value = line_adjustment 

        line = "This is a line of text"
        line_number = 1 

        expected_line = f"{line_number}  {line}".rjust(len(line) + line_adjustment)

        formatted_line = dog_utils.format_output(line, line_number, mock_config)
        self.assertEqual(formatted_line, expected_line)

        mock_config.show_nonblank_line_numbers.assert_called()
        mock_config.show_all_line_numbers.assert_called()
        mock_config.get_line_adjustment.assert_called()

    def test_format_output_without_any_formatting(self):
        mock_config = Mock()
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False

        line = "This is a line of text" 
        line_number = 1

        formatted_line = dog_utils.format_output(line, line_number, mock_config)
        self.assertEqual(line, formatted_line)

        mock_config.show_nonblank_line_numbers.assert_called()
        mock_config.show_all_line_numbers.assert_called()
        mock_config.get_line_adjustment.assert_not_called()

    def test_step_line_with_blankLine_with_show_all_line_numbers_flag(self):
        mock_config = Mock()
        mock_config.show_all_line_numbers.return_value = True

        line = "\n"
        expected_step = 1

        step = dog_utils.step_line(line, mock_config)
        self.assertEqual(step, expected_step)

        mock_config.show_all_line_numbers.assert_called()

    def test_step_line_with_blankLine_without_show_all_line_numbers_flag(self):
        mock_config = Mock()
        mock_config.show_all_line_numbers.return_value = False

        line = "\n"
        expected_step = 0

        step = dog_utils.step_line(line, mock_config)
        
        self.assertEqual(step, expected_step)
        mock_config.show_all_line_numbers.assert_called()
        mock_config.show_nonblank_line_numbers.assert_not_called()

    def test_step_line_with_nonblank_line_with_show_all_line_numbers_flag(self):
        mock_config = Mock()
        mock_config.show_all_line_numbers.return_value = True

        line = "This is a line with text"
        expected_step = 1

        step = dog_utils.step_line(line, mock_config)

        self.assertEqual(step, expected_step)
        mock_config.show_all_line_numbers.assert_called()
        mock_config.show_nonblank_line_numbers.assert_not_called()

    def test_step_line_with_nonblank_line_and_show_nonblank_line_numbers_flag(self):
        mock_config = Mock()
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonblank_line_numbers.return_value = True

        line = "This is a line with text"
        expected_step = 1

        step = dog_utils.step_line(line, mock_config)

        self.assertEqual(step, expected_step)
        mock_config.show_all_line_numbers.assert_called()
        mock_config.show_nonblank_line_numbers.assert_called()

    def test_step_line_without_step(self):
        mock_config = Mock()
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonblank_line_numbers.return_value = False

        line = "This is a line with text"
        expected_step = 0

        step = dog_utils.step_line(line, mock_config)

        self.assertEqual(step, expected_step)
        mock_config.show_all_line_numbers.assert_called()
        mock_config.show_nonblank_line_numbers.assert_called()









    
