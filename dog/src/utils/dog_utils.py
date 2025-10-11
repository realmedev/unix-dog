from cli import dog_config as dc

def print_unbuffered(data: str = ""):
    print(data, flush=True, end="")

def print_unbuffered_line(data=""):
    print(data, flush=True)

def is_blank_line(line: str) -> bool:
        return line.strip() == ""
