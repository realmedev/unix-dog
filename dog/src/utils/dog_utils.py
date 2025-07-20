from src.cli import dog_config as dc

def print_unbuffered(data: str = ""):
    print(data, flush=True, end="")

def print_unbuffered_line(data=""):
    print(data, flush=True)

def is_blank_line(line: str) -> bool:
        return line.strip() == ""

def format_output(line: str, line_number: int, dog_config: dc.DogConfig) -> str:
    if dog_config.show_nonblank_line_numbers():
        if line in ["$\n", "\n"]:
            return line
        else:
            return f"{line_number}  {line}".rjust(len(line) + dog_config.get_line_adjustment())
    elif dog_config.show_all_line_numbers():
        return f"{line_number}  {line}".rjust(len(line) + dog_config.get_line_adjustment())
    else:
        return line

def step_line(line: str, dog_config: dc.DogConfig) -> int:
    if is_blank_line(line):
        if dog_config.show_all_line_numbers():
            return 1
    else:
        if dog_config.show_all_line_numbers() or dog_config.show_nonblank_line_numbers():
            return 1
    return 0
