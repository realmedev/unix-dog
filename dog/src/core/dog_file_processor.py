import sys
from io import TextIOWrapper

from utils import dog_utils
from cli import dog_config as dc

class FileProcessor:
    def __init__(self, dog_config: dc.DogConfig):
        self.dog_config = dog_config

    def process_file(self, filepath: str):
        self.consecutive_blank_lines = 0
        line_number = 1
        output = ""

        file = self._open(filepath)
        while (line := file.readline()) != "":
            output += self._process_line(line, line_number)
            line_number += self._get_line_increment(line)
        self._close(file)
        return output

    def _process_line(self, line: str, line_number: int) -> str:
        output_line = line
        if dog_utils.is_blank_line(line):
            output_line = self._process_blank_line()
        else:
            output_line = self._process_regular_line(line)
        output_line = self._format(output_line, line_number)
        return output_line

    def _open(self, filepath: str):
        file = None
        if filepath == "-":
            file = sys.stdin
        else:
            file = open(filepath, "r")
        return file

    def _close(self, file: TextIOWrapper):
        file.close()

    def _is_control(self, c: str) -> bool:
        return ord(c) >= 0 and ord(c) < 32

    def _process_control(self, c: str) -> str:
        if c == "\n":
            if self.dog_config.show_ends(): 
                return "$\n"
            else:
                return c
        elif c == "\t":
            if self.dog_config.show_tabs():
                return "^I"
            else:
                return c
        elif self.dog_config.show_nonprinting():
            return "^{0}".format(chr(ord(c) + 64))
        else:
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
                return "M-^{0}".format(chr(ord(c) - 128 + 64))
            else:
                if (ord(c)) == 255:
                    return "M-^?"
                else:
                    return "M-{0}".format(chr(ord(c) - 160 + 32))

        return ""

    def _process_blank_line(self):
        self.consecutive_blank_lines += 1
        if self.consecutive_blank_lines > 1 and self.dog_config.squeeze_blank_lines():
            return ""
        else:
            return "$\n" if self.dog_config.show_ends() else "\n"

    def _process_regular_line(self, line: str) -> str:
        self.consecutive_blank_lines = 0
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

    def _get_line_increment(self, line: str) -> int:
        if dog_utils.is_blank_line(line):
            if self.dog_config.show_all_line_numbers():
                return 1
        else:
            if self.dog_config.show_all_line_numbers() or self.dog_config.show_nonblank_line_numbers():
                return 1
        return 0

    def _format(self, line: str, line_number: int) -> str:
        if self.dog_config.show_nonblank_line_numbers():
            if line in ["$\n", "\n"]:
                return line
            else:
                return f"{line_number}  {line}".rjust(len(line) + self.dog_config.get_line_adjustment())
        elif self.dog_config.show_all_line_numbers():
            return f"{line_number}  {line}".rjust(len(line) + self.dog_config.get_line_adjustment())
        else:
            return line