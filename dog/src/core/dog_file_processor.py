import sys
from utils import dog_utils
from cli import dog_config as dc

class FileProcessor:
    def __init__(self, filepath: str, dog_config: dc.DogConfig):
        self.filepath = filepath
        self.dog_config = dog_config
        self.consecutive_blank_lines = 0

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def open(self):
        if self.filepath == "-":
            self.file = sys.stdin
        else:
            self.file = open(self.filepath, "r")

    def close(self):
        self.file.close()

    def getline(self) -> str:
        return self.file.readline()

    def process_line(self, line: str) -> str:
        if dog_utils.is_blank_line(line):
            return self._process_blank_line()
        else:
            return self._process_regular_line(line)

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
                if (c) == 255:
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
