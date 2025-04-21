import utils
import sys

consecutive_blank_lines = 0
line_number = 1
LINE_ADJUSTMENT = 8

class FileProcessor:

    def is_control(self, c):
        return c >= 0 and c < 32

    def process_control(self, c, c_value, args):
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

    def is_alphanumeric(self, c):
        return c >= 32 and c < 127

    def process_alphanumeric(self, c):
        return c

    def is_del(self, c):
        return c == 127

    def process_del(self, args):
        if args.show_nonprinting or args.t or args.e or args.show_all:
           return "^?"
        return ""

    def is_extended_ascii(self, c):
        return c > 127 and c < 256

    def process_extended_ascii(self, c_value, args):
        if args.show_nonprinting or args.t or args.e or args.show_all:
            if c_value < 160:
                return "M-^{0}".format(chr(c_value - 128 + 64))
            else:
                if c_value == 255:
                    return "M-^?"
                else:
                    return "M-{0}".format(chr(c_value - 160 + 32))

        return ""

    def is_blank_line(self, line):
        return line.strip() == ""

    def process_blank_line(self, args):
        global line_number
        global consecutive_blank_lines
        consecutive_blank_lines += 1

        if consecutive_blank_lines > 1 and args.squeeze_blank:
            return

        line_end = "$" if args.show_ends or args.show_all or args.e else ""

        if args.number_nonblank:
            utils.print_unbuffered_line("{}".format(line_end))
        elif args.number:
            adjustment = len(line_end) + LINE_ADJUSTMENT
            utils.print_unbuffered_line("{0}  {1}".format(line_number, line_end).rjust(adjustment))
            line_number += 1
        else:
            utils.print_unbuffered_line("{}".format(line_end))
            line_number += 1

    def process_regular_line(self, line, args):
        global line_number
        global consecutive_blank_lines

        consecutive_blank_lines = 0

        output = ""

        for c in line:
            c_value = ord(c)
            if self.is_alphanumeric(c_value):
                output += self.process_alphanumeric(c)
            elif self.is_control(c_value):
                output += self.process_control(c, c_value, args)
            elif self.is_del(c_value):
                output += self.process_del(args)
            elif self.is_extended_ascii(c_value):
                output += self.process_extended_ascii(c_value, args)
            else:
                print("Unrecognized character", file=sys.stderr)
                return -1

        if args.number or args.number_nonblank:
            adjustment = len(output) + LINE_ADJUSTMENT
            utils.print_unbuffered("{0}  {1}".format(line_number, output).rjust(adjustment))
        else:
            utils.print_unbuffered(output)

        line_number += 1

    def process_line(self,line, args):
        if self.is_blank_line(line):
            self.process_blank_line(args)
        else:
            self.process_regular_line(line, args)


