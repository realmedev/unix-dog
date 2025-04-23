import sys
import cli
import file_processor as fp
import utils

def process_files(args):
    for filepath in args.FILE:
        file_proc = fp.FileProcessor(filepath, args)
        file_proc.open()

        while (line := file_proc.getline()) != "":
            output = file_proc.process_line(line)
            output = utils.format_output(output, args)
            utils.print_unbuffered(output)

        file_proc.close()

def run_cli():
    args = cli.parse_args()

    if args.version:
        print("Version 1.0")
        sys.exit(0)

    process_files(args)

if __name__ == "__main__":
    run_cli()
