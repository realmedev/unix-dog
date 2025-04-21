import sys
import utils
import argparse

consecutive_blank_lines = 0
line_number = 1
LINE_ADJUSTMENT = 8

class FileProcessor:
    def __init__(self, filepath: str, args: argparse.Namespace):
        self.filepath = filepath
        self.args = args

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
        if self._is_blank_line(line):
            return self._process_blank_line(self.args)
        else:
            return self._process_regular_line(line, self.args)

    def _is_control(self, c: int) -> bool:
        return c >= 0 and c < 32

    def _process_control(self, c: str, c_value: int, args: argparse.Namespace) -> str:
        if c == "\n":
            if args.show_ends or args.show_all or args.e:
                return "$\n"
            else:
                return c
        elif c == "\t":
            if args.show_tabs or args.t:
                return "^I"
            else:
                return c
        else:
            if args.show_nonprinting or args.t or args.e or args.show_all:
                return "^{0}".format(chr(c_value + 64))

        return ""

    def _is_alphanumeric(self, c: int) -> bool:
        return c >= 32 and c < 127

    def _process_alphanumeric(self, c: str) -> str:
        return c

    def _is_del(self, c: int) -> bool:
        return c == 127

    def _process_del(self, args: argparse.Namespace) -> str:
        if args.show_nonprinting or args.t or args.e or args.show_all:
           return "^?"
        return ""

    def _is_extended_ascii(self, c: int) -> bool:
        return c > 127 and c < 256

    def _process_extended_ascii(self, c_value: int, args: argparse.Namespace) -> str:
        if args.show_nonprinting or args.t or args.e or args.show_all:
            if c_value < 160:
                return "M-^{0}".format(chr(c_value - 128 + 64))
            else:
                if c_value == 255:
                    return "M-^?"
                else:
                    return "M-{0}".format(chr(c_value - 160 + 32))

        return ""

    def _is_blank_line(self, line: str) -> bool:
        return line.strip() == ""

    def _process_blank_line(self, args: argparse.Namespace):
        global line_number
        global consecutive_blank_lines
        consecutive_blank_lines += 1

        if consecutive_blank_lines > 1 and args.squeeze_blank:
            return ""

        line_end = "$" if args.show_ends or args.show_all or args.e else ""

        output = ""

        if args.number_nonblank:
            utils.print_unbuffered_line("{}".format(line_end))
            output = f"{line_end}"
        elif args.number:
            adjustment = len(line_end) + LINE_ADJUSTMENT
            utils.print_unbuffered_line("{0}  {1}".format(line_number, line_end).rjust(adjustment))
            line_number += 1
            output = f"{line_number}  {line_end}"
        else:
            utils.print_unbuffered_line("{}".format(line_end))
            line_number += 1
            output = f"{line_end}"

        return output

    def _process_regular_line(self, line: str, args: argparse.Namespace) -> str:
        global line_number
        global consecutive_blank_lines

        consecutive_blank_lines = 0

        output = ""

        for c in line:
            c_value = ord(c)
            if self._is_alphanumeric(c_value):
                output += self._process_alphanumeric(c)
            elif self._is_control(c_value):
                output += self._process_control(c, c_value, args)
            elif self._is_del(c_value):
                output += self._process_del(args)
            elif self._is_extended_ascii(c_value):
                output += self._process_extended_ascii(c_value, args)
            else:
                print("Unrecognized character", file=sys.stderr)
                return "" 

        if args.number or args.number_nonblank:
            adjustment = len(output) + LINE_ADJUSTMENT
            utils.print_unbuffered("{0}  {1}".format(line_number, output).rjust(adjustment))
        else:
            utils.print_unbuffered(output)

        line_number += 1
        return output
