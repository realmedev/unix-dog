import unittest
import itertools

from unittest.mock import Mock
from dog.cli.dog_config import DogConfig

class TestDogConfig(unittest.TestCase):
    def setUp(self):
        self.mock_args = Mock()

    def test_show_tabs(self):
        combinations = list(itertools.product([True, False], [True, False], [True, False]))

        for combination in combinations:
            self.mock_args.show_tabs = combination[0]
            self.mock_args.t = combination[1]
            self.mock_args.show_all = combination[2]

            dog_config = DogConfig(self.mock_args)

            if True in combination:
                self.assertTrue(dog_config.show_tabs())
            else:
                self.assertFalse(dog_config.show_tabs())

    def test_show_nonprinting(self):
        combinations = list(itertools.product([True, False], [True, False], [True, False], [True, False]))

        for combination in combinations:
            self.mock_args.show_nonprinting = combination[0]
            self.mock_args.t = combination[1]
            self.mock_args.e = combination[2]
            self.mock_args.show_all = combination[3]

            dog_config = DogConfig(self.mock_args)

            if True in combination:
                self.assertTrue(dog_config.show_nonprinting())
            else:
                self.assertFalse(dog_config.show_nonprinting())

    def test_show_ends(self):
        combinations = list(itertools.product([True, False], [True, False], [True, False]))

        for combination in combinations:
            self.mock_args.show_ends = combination[0]
            self.mock_args.show_all = combination[1]
            self.mock_args.e = combination[2]

            dog_config = DogConfig(self.mock_args)

            if True in combination:
                self.assertTrue(dog_config.show_ends())
            else:
                self.assertFalse(dog_config.show_ends())

    def test_show_all_line_numbers(self):
        combinations = list(itertools.product([True, False], [True, False]))

        for combination in combinations:
            self.mock_args.number = combination[0]
            self.mock_args.number_nonblank = combination[1]

            dog_config = DogConfig(self.mock_args)

            if self.mock_args.number == True and self.mock_args.number_nonblank == False:
                self.assertTrue(dog_config.show_all_line_numbers())
            else:
                self.assertFalse(dog_config.show_all_line_numbers())

    def test_show_nonblank_line_numbers(self):
        self.mock_args.number_nonblank = True
        dog_config = DogConfig(self.mock_args)
        self.assertTrue(dog_config.show_nonblank_line_numbers())

        self.mock_args.number_nonblank = False
        dog_config = DogConfig(self.mock_args)
        self.assertFalse(dog_config.show_nonblank_line_numbers())

    def test_show_version(self):
        self.mock_args.version = True
        dog_config = DogConfig(self.mock_args)
        self.assertTrue(dog_config.show_version())

        self.mock_args.version = False
        dog_config = DogConfig(self.mock_args)
        self.assertFalse(dog_config.show_version())

    def test_squeeze_blank_lines(self):
        self.mock_args.squeeze_blank = True
        dog_config = DogConfig(self.mock_args)
        self.assertTrue(dog_config.squeeze_blank_lines())

        self.mock_args.squeeze_blank = False
        dog_config = DogConfig(self.mock_args)
        self.assertFalse(dog_config.squeeze_blank_lines())

    def test_get_filepaths(self):
        self.mock_args.FILE = ["/test/file/path"]
        dog_config = DogConfig(self.mock_args)
        expected_filepaths = self.mock_args.FILE
        self.assertEqual(expected_filepaths, dog_config.get_filepaths())

    def test_get_line_adjustment(self):
        self.mock_args.no_args_set = None
        dog_config = DogConfig(self.mock_args)
        self.assertEqual(dog_config.get_line_adjustment(), 8)