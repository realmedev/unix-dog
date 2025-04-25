import sys
import dog_cli
import dog_file_processor as fp
import dog_utils
import dog_config as dc

def process_files(dog_config: dc.DogConfig):
    line_number = 1

    for filepath in dog_config.get_filepaths():
        file_proc = fp.FileProcessor(filepath, dog_config)
        file_proc.open()

        while (line := file_proc.getline()) != "":
            output = file_proc.process_line(line)
            output = dog_utils.format_output(output, line_number, dog_config)
            line_number = dog_utils.step_line(line, dog_config)
            dog_utils.print_unbuffered(output)

        file_proc.close()

def run_cli():
    args = dog_cli.parse_args()
    dog_config = dc.DogConfig(args)

    if dog_config.show_version():
        print("Version 1.0")
        sys.exit(0)

    process_files(dog_config)

if __name__ == "__main__":
    run_cli()
