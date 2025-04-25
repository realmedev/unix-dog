import sys
import dog_cli
import dog_file_processor as fp
import dog_utils

def process_files(args):
    line_number = 1

    for filepath in args.FILE:
        file_proc = fp.FileProcessor(filepath, args)
        file_proc.open()

        while (line := file_proc.getline()) != "":
            output = file_proc.process_line(line)
            output = dog_utils.format_output(output, line_number, args)

            if dog_utils.is_blank_line(line):
                if args.number and not args.number_nonblank:
                    line_number += 1
            else:
                if args.number or args.number_nonblank:
                    line_number += 1

            dog_utils.print_unbuffered(output)

        file_proc.close()

def run_cli():
    args = dog_cli.parse_args()

    if args.version:
        print("Version 1.0")
        sys.exit(0)

    process_files(args)

if __name__ == "__main__":
    run_cli()
