import sys
import argparse
import utils

consecutive_blank_lines = 0
line_number = 1
LINE_ADJUSTMENT = 8

def create_parser():
    parser = argparse.ArgumentParser(prog="dog",
                                     description="Concatenate FILE(s) to standard output.\n\nWith no FILE, or when FILE is -, read standard input.",
                                     usage="dog [OPTION]... [FILE]...",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="Full documentation <https://github.com/itsrealme-dev/unix-clones>")

    parser.add_argument("-A",
                        "--show-all",
                        action="store_true",
                        help="equivalent to -vET")
    parser.add_argument("-b",
                        "--number-nonblank",
                        action="store_true",
                        help="number nonempty output lines, overrides -n")
    parser.add_argument("-e",
                        action="store_true",
                        help="equivalent to -vE")
    parser.add_argument("-E",
                        "--show-ends",
                        action="store_true",
                        help="display $ at end of each line")
    parser.add_argument("-n",
                        "--number",
                        action="store_true",
                        help="number all output lines")
    parser.add_argument("-s",
                        "--squeeze-blank",
                        action="store_true",
                        help="supress repeated empty output lines")
    parser.add_argument("-t",
                        help="equivalent to -vT",
                        action="store_true")
    parser.add_argument("-T",
                        "--show-tabs",
                        action="store_true",
                        help="display TAB characters as ^I")
    parser.add_argument("-u",
                        action="store_true",
                        help="ignored")
    parser.add_argument("-v",
                        "--show-nonprinting",
                        action="store_true",
                        help="use ^ and M- notation, except for LFD and TAB")
    parser.add_argument("--version",
                        action="store_true",
                        help="output version information and exit")
    parser.add_argument("FILE",
                        nargs="*",
                        type=argparse.FileType("r"),
                        default=sys.stdin)
#    parser.add_argument("--help", help="display this help and exit")
    return parser

def is_control(c):
    return c >= 0 and c < 32

def process_control(c, c_value, args):
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

def is_alphanumeric(c):
    return c >= 32 and c < 127

def process_alphanumeric(c):
    return c

def is_del(c):
    return c == 127

def process_del(args):
    if args.show_nonprinting or args.t or args.e or args.show_all:
       return "^?"
    return ""

def is_extended_ascii(c):
    return c > 127 and c < 256

def process_extended_ascii(c_value, args):
    if args.show_nonprinting or args.t or args.e or args.show_all:
        if c_value < 160:
            return "M-^{0}".format(chr(c_value - 128 + 64))
        else:
            if c_value == 255:
                return "M-^?"
            else:
                return "M-{0}".format(chr(c_value - 160 + 32))

    return ""

def is_blank_line(line):
    return line.strip() == ""

def process_blank_line(args):
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

def process_regular_line(line, args):
    global line_number
    global consecutive_blank_lines

    consecutive_blank_lines = 0

    output = ""

    for c in line:
        c_value = ord(c)
        if is_alphanumeric(c_value):
            output += process_alphanumeric(c)
        elif is_control(c_value):
            output += process_control(c, c_value, args)
        elif is_del(c_value):
            output += process_del(args)
        elif is_extended_ascii(c_value):
            output += process_extended_ascii(c_value, args)
        else:
            print("Unrecognized character", file=sys.stderr)
            return -1

    if args.number or args.number_nonblank:
        adjustment = len(output) + LINE_ADJUSTMENT
        utils.print_unbuffered("{0}  {1}".format(line_number, output).rjust(adjustment))
    else:
        utils.print_unbuffered(output)

    line_number += 1

def process_line(line, args):
    if is_blank_line(line):
        process_blank_line(args)
    else:
        process_regular_line(line, args)

def process_files(args):
    for file in args.FILE:
        for line in file:
            process_line(line, args)

def run_cli():
    parser = create_parser()
    args = parser.parse_args()
    #print(args) 

    if args.version:
        print("Version 1.0")
        sys.exit(0)

    process_files(args)

if __name__ == "__main__":
    run_cli()
