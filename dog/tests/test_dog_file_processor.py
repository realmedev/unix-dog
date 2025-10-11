import unittest

from unittest.mock import patch, mock_open, Mock, MagicMock
from core.dog_file_processor import FileProcessor
from cli.dog_config import DogConfig

def convert_to_ext_ascii(c: str) -> str:
    if (ord(c) < 160):
        return "M-^{0}".format(chr(ord(c) - 128 + 64))
    else:
        if (ord(c) == 255):
            return "M-^?"
        else:
            return "M-{0}".format(chr(ord(c) - 160 + 32))

def convert_to_ctrl_ascii(c: str, dog_config: DogConfig) -> str:
    if c == "\n":
        if dog_config.show_ends():
            return "$\n"
        else:
            return c
    elif c == "\t":
        if dog_config.show_tabs():
            return "^I"
        else:
            return c
    elif dog_config.show_nonprinting():
        return "^{0}".format(chr(ord(c) + 64))
    else:
        return ""

class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_args = Mock()
        self.filepath = "test/file/path/file.txt"

    # def test_file_open_with_stdin(self):
    #     filepath = "-"
    #     open_mock = mock_open(read_data="")
    #     dog_config = Mock()

    #     with patch("builtins.open", open_mock):
    #         fp = FileProcessor(dog_config)
    #         fp.process_file(filepath)

    #     open_mock.assert_called_once()

    def test_file_processing_with_empty_file(self):
        dog_config = Mock() # irrelevant in this case
        open_mock = mock_open(read_data="")

        with patch("builtins.open", open_mock):
            fp = FileProcessor(dog_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = ""

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_tabs(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_tabs.return_value = True

        input_text = "This\tis\tsome\ttext\twith\ttabs."
        expected_output = "This^Iis^Isome^Itext^Iwith^Itabs."

        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            
            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_nonprinting(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonprinting.return_value = True
        mock_config.show_ends.return_value = True
        mock_config.show_tabs.return_value = True

        input_text = ""
        expected_output = ""

        for c in range(0, 32):
            input_text += chr(c)
            expected_output += convert_to_ctrl_ascii(chr(c), mock_config)

        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_nonprinting_and_printable_tabs(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonprinting.return_value = True
        mock_config.show_ends.return_value = True
        mock_config.show_tabs.return_value = False

        input_text = ""
        expected_output = ""

        for c in range(0, 32):
            input_text += chr(c)
            expected_output += convert_to_ctrl_ascii(chr(c), mock_config)

        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_nonprinting_and_extended_ascii(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonprinting.return_value = True

        input_text = ""
        expected_output = ""

        for c in range(128, 256):
            input_text += chr(c)
            expected_output += convert_to_ext_ascii(chr(c))

        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_del_character(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonprinting.return_value = True

        del_ordinal = 127
        input_text = chr(del_ordinal)
        expected_output = "^?"

        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_del_character_non_printable(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_nonprinting.return_value = False

        del_ordinal = 127
        input_text = chr(del_ordinal)
        expected_output = ""

        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_ends(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_ends.return_value = True

        input_text = "This is some\ntext with\nlots of line endings\n"
        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = "This is some$\ntext with$\nlots of line endings$\n"

            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_all_line_numbers(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = True
        mock_config.show_ends.return_value = False

        input_text = "This is\na text split into lines\nto demonstrate\nline numbering\nis done by file processor."
        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = "1  This is\n2  a text split into lines\n3  to demonstrate\n4  line numbering\n5  is done by file processor."
            
            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_nonblank_line_numbers(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = True
        mock_config.show_ends.return_value = False

        input_text = "This is\na text split into lines\nto demonstrate\nline numbering\nis done by file processor."
        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = "1  This is\n2  a text split into lines\n3  to demonstrate\n4  line numbering\n5  is done by file processor."
            
            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)
    
    def test_file_processing_with_show_nonblank_line_numbers_and_blank_line(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = True
        mock_config.show_ends.return_value = False

        input_text = "\n"
        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = "\n"
            
            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_show_version(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.show_version.return_value = True

        input_text = "This is some text to show that version is not handled by file processor."
        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = "This is some text to show that version is not handled by file processor."
            
            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)

    def test_file_processing_with_squeeze_blank_lines(self):
        mock_config = MagicMock(spec=DogConfig)
        mock_config.show_nonblank_line_numbers.return_value = False
        mock_config.show_all_line_numbers.return_value = False
        mock_config.squeeze_blank_lines.return_value = True
        mock_config.show_ends.return_value = False

        input_text = "This is some\n\n\n\ntext with multiple sequential empty lines."
        open_mock = mock_open(read_data=input_text)

        with patch("builtins.open", open_mock):
            fp = FileProcessor(mock_config)
            actual_output = fp.process_file(self.filepath)
            expected_output = "This is some\n\ntext with multiple sequential empty lines."
            
            open_mock.assert_called_once()
            open_mock().close.assert_called_once()
            self.assertEqual(expected_output, actual_output)