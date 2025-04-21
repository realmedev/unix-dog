import sys
import cli
import file_processor as fp

def process_files(args):
    for file in args.FILE:
        for line in file:
            file_proc = fp.FileProcessor()
            file_proc.process_line(line, args)

def run_cli():
    args = cli.parse_args()

    if args.version:
        print("Version 1.0")
        sys.exit(0)

    process_files(args)

if __name__ == "__main__":
    run_cli()
