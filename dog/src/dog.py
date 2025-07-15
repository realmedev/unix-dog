import sys
import dog_cli
import dog_file_processor as fp
import dog_utils
import dog_config as dc

def process_files(dog_config: dc.DogConfig):
    line_number = 1

    for filepath in dog_config.get_filepaths():
        file_proc = fp.FileProcessor(filepath, dog_config)
        try:
            file_proc.open()
        except FileNotFoundError:
            dog_utils.print_unbuffered_line("No such file or directory")
        except PermissionError:
            dog_utils.print_unbuffered_line("Permission denied")
        except IOError:
            dog_utils.print_unbuffered_line("Error while reading the file")
        else:
            with file_proc:
                while (line := file_proc.getline()) != "":
                    output = file_proc.process_line(line)
                    output = dog_utils.format_output(output, line_number, dog_config)
                    line_number = dog_utils.step_line(line, dog_config)
                    dog_utils.print_unbuffered(output)

def run_cli():
    args = dog_cli.parse_args()
    dog_config = dc.DogConfig(args)

    if dog_config.show_version():
        print("Version 1.0")
        sys.exit(0)

    process_files(dog_config)

if __name__ == "__main__":
    run_cli()
