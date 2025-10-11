import sys
from cli import dog_cli as dp
from cli import dog_config as dc
from core import dog_file_processor as fp
from utils import dog_utils as du

def process_files(dog_config: dc.DogConfig):
    file_proc = fp.FileProcessor(dog_config)
    for filepath in dog_config.get_filepaths():
        try:
            output = file_proc.process_file(filepath)
            du.print_unbuffered(output)
        except FileNotFoundError:
            du.print_unbuffered_line("No such file or directory")
        except PermissionError:
            du.print_unbuffered_line("Permission denied")
        except IOError:
            du.print_unbuffered_line("Error while reading the file")

def run_cli():
    args = dp.parse_args()
    dog_config = dc.DogConfig(args)

    if dog_config.show_version():
        print("Version 1.0")
        sys.exit(0)

    process_files(dog_config)

if __name__ == "__main__":
    run_cli()
