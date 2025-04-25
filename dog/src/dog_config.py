from argparse import Namespace

class DogConfig:
    def __init__(self, args: Namespace) -> None:
        self.args = args

    def show_tabs(self) -> bool:
        return self.args.show_tabs or \
               self.args.t or \
               self.args.show_all

    def show_nonprinting(self) -> bool:
        return self.args.show_nonprinting or \
               self.args.t or \
               self.args.e or \
               self.args.show_all

    def show_ends(self) -> bool:
        return self.args.show_ends or \
               self.args.show_all or \
               self.args.e 

    def show_all_line_numbers(self) -> bool:
        return self.args.number and not self.show_nonblank_line_numbers()

    def show_nonblank_line_numbers(self) -> bool:
        return self.args.number_nonblank

    def show_version(self) -> bool:
        return self.args.version

    def squeeze_blank_lines(self) -> bool:
        return self.args.squeeze_blank

    def get_filepaths(self) -> list[str]:
        return self.args.FILE
