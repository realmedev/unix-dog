from argparse import Namespace

LINE_ADJUSTMENT = 8

def print_unbuffered(data: str = ""):
    print(data, flush=True, end="")

def print_unbuffered_line(data=""):
    print(data, flush=True)

def is_blank_line(line: str) -> bool:
        return line.strip() == ""

def format_output(line: str, line_number: int, args: Namespace) -> str:
    if args.number_nonblank:
        if line in ["$\n", "\n"]:
            return line
        else:
            return f"{line_number}  {line}".rjust(len(line) + LINE_ADJUSTMENT)
    elif args.number:
        return f"{line_number}  {line}".rjust(len(line) + LINE_ADJUSTMENT)
    else:
        return line
