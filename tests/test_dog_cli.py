from argparse import Action
import unittest

from dog.cli import dog_cli as cli

def has_option(action: Action) -> bool:
    return len(action.option_strings) != 0

class DogCliTest(unittest.TestCase):
    def setUp(self):
        self.parser = cli.create_parser()

    def test_program_name(self):
        expected_prog = "dog"
        self.assertEqual(expected_prog, self.parser.prog, "Unexpected program name")

    def test_description(self):
        expected_description = "Concatenate FILE(s) to standard output.\n\nWith no FILE, or when FILE is -, read standard input."
        self.assertEqual(expected_description, self.parser.description, "Description mismatch")

    def test_epilog(self):
        expected_epilog = "Full documentation <https://github.com/itsrealme-dev/unix-clones>"
        self.assertEqual(expected_epilog, self.parser.epilog, "Epilog mismatch")

    def test_registered_args(self):
        expected_args = [
            ["-h", "--help"],
            ["-A", "--show-all"],
            ["-b", "--number-nonblank"],
            ["-e"],
            ["-E", "--show-ends"],
            ["-n", "--number"],
            ["-s", "--squeeze-blank"],
            ["-t"],
            ["-T", "--show-tabs"],
            ["-u"],
            ["-v", "--show-nonprinting"],
            ["--version"],
            "FILE"
        ]

        registered_args = self.parser._actions

        for action in registered_args:
            if has_option(action):
                print(f"Testing arg: {action.option_strings}")
                self.assertIn(action.option_strings, expected_args, "Unexpected argument")
            else:
                print(f"Testing arg: {action.dest}")
                self.assertIn(action.dest, expected_args, "Unexpected argument")
