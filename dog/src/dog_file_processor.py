import sys
import dog_utils
import dog_config as dc

class FileProcessor:
    def __init__(self, filepath: str, dog_config: dc.DogConfig):
        self.filepath = filepath
        self.dog_config = dog_config
        self.consecutive_blank_lines = 0

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

    def _is_control(self, c: int) -> bool:
        return c >= 0 and c < 32

    def _process_control(self, c: str, c_value: int) -> str:
        if c == "\n":
            if self.dog_config.show_ends(): 
                return "$\n"
            else:
                return c
        elif c == "\t":
            if self.dog_config.show_nonprinting(): 
                return "^{0}".format(chr(c_value + 64))

        return ""

    def _is_alphanumeric(self, c: int) -> bool:
        return c >= 32 and c < 127

    def _process_alphanumeric(self, c: str) -> str:
        return c

    def _is_del(self, c: int) -> bool:
        return c == 127

    def _process_del(self) -> str:
        if self.dog_config.show_nonprinting():
           return "^?"
        return ""

    def _is_extended_ascii(self, c: int) -> bool:
        return c > 127 and c < 256

    def _process_extended_ascii(self, c_value: int) -> str:
        if self.dog_config.show_nonprinting():
            if c_value < 160:
                return "M-^{0}".format(chr(c_value - 128 + 64))
            else:
                if c_value == 255:
                    return "M-^?"
                else:
                    return "M-{0}".format(chr(c_value - 160 + 32))

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
            c_value = ord(c)
            if self._is_alphanumeric(c_value):
                output += self._process_alphanumeric(c)
            elif self._is_control(c_value):
                output += self._process_control(c, c_value)
            elif self._is_del(c_value):
                output += self._process_del()
            elif self._is_extended_ascii(c_value):
                output += self._process_extended_ascii(c_value)
            else:
                print("Unrecognized character", file=sys.stderr)
                return "" 

        return output
