import sys
from io import TextIOWrapper

from utils import dog_utils as du
from cli import dog_config as dc

class FileProcessor:
    def __init__(self, dog_config: dc.DogConfig):
        self.consecutive_blank_lines = 0
        self.dog_config = dog_config
        self.line_processor = _LineProcessor(dog_config)

    def process_file(self, filepath: str):
        self._reset_blank_count()
        line_number = 1
        output = ""

        file = self._open(filepath)

        while (line := file.readline()) != "":
            if du.is_blank_line(line):
                self._increment_blank_count()
                if self._skip_blank():
                    continue
            else:
                self._reset_blank_count()

            output += self.line_processor.process_line(line, line_number)
            line_number += self._get_line_increment(line)

        self._close(file)

        return output

    def _open(self, filepath: str):
        file = None
        if filepath == "-":
            file = sys.stdin
        else:
            file = open(filepath, "r")
        return file

    def _close(self, file: TextIOWrapper):
        file.close()

    def _increment_blank_count(self) -> None:
        self.consecutive_blank_lines += 1

    def _reset_blank_count(self) -> None:
        self.consecutive_blank_lines = 0

    def _skip_blank(self) -> bool:
        return (self.consecutive_blank_lines > 1) and self.dog_config.squeeze_blank_lines()

    def _get_line_increment(self, line: str) -> int:
        if du.is_blank_line(line):
            if self.dog_config.show_all_line_numbers():
                return 1
        else:
            if self.dog_config.show_all_line_numbers() or \
               self.dog_config.show_nonblank_line_numbers():
                return 1
        return 0

class _LineProcessor:
    def __init__(self, dog_config: dc.DogConfig):
        self.dog_config = dog_config

    def process_line(self, line: str, line_number: int) -> str:
        output_line = line
        if du.is_blank_line(line):
            output_line = self._process_blank_line()
        else:
            output_line = self._process_regular_line(line)
        output_line = self._format_line(output_line, line_number)
        return output_line

    def _process_blank_line(self):
        return "$\n" if self.dog_config.show_ends() else "\n"

    def _process_regular_line(self, line: str) -> str:
        output = ""

        for c in line:
            if self._is_alphanumeric(c):
                output += self._process_alphanumeric(c)
            elif self._is_control(c):
                output += self._process_control(c)
            elif self._is_del(c):
                output += self._process_del()
            elif self._is_extended_ascii(c):
                output += self._process_extended_ascii(c)
            else:
                print("Unrecognized character", file=sys.stderr)
                return ""

        return output

    def _format_line(self, line: str, line_number: int) -> str:
        if self.dog_config.show_nonblank_line_numbers():
            if line in ["$\n", "\n"]:
                return line
            return f"{line_number}  {line}".rjust(len(line) + self.dog_config.get_line_adjustment())

        if self.dog_config.show_all_line_numbers():
            return f"{line_number}  {line}".rjust(len(line) + self.dog_config.get_line_adjustment())

        return line

    def _is_control(self, c: str) -> bool:
        return ord(c) >= 0 and ord(c) < 32

    def _process_control(self, c: str) -> str:
        if c == "\n":
            if self.dog_config.show_ends():
                return "$\n"
            return c

        if c == "\t":
            if self.dog_config.show_tabs():
                return "^I"
            return c

        if self.dog_config.show_nonprinting():
            return f"^{chr(ord(c) + 64)}"

        return ""

    def _is_alphanumeric(self, c: str) -> bool:
        return ord(c) >= 32 and ord(c) < 127

    def _process_alphanumeric(self, c: str) -> str:
        return c

    def _is_del(self, c: str) -> bool:
        return ord(c) == 127

    def _process_del(self) -> str:
        if self.dog_config.show_nonprinting():
            return "^?"
        return ""

    def _is_extended_ascii(self, c: str) -> bool:
        return ord(c) > 127 and ord(c) < 256

    def _process_extended_ascii(self, c: str) -> str:
        if self.dog_config.show_nonprinting():
            if ord(c) < 160:
                return f"M-^{chr(ord(c) - 128 + 64)}"

            if (ord(c)) == 255:
                return "M-^?"

            return f"M-{chr(ord(c) - 160 + 32)}"

        return ""
