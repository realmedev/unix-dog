import sys
import argparse

def parse_args():
    parser = create_parser()
    return parser.parse_args()

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


