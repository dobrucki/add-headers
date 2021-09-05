import os
import sys
import argparse
import glob

def parse_arguments():
  parser = argparse.ArgumentParser(description="Adds copyright headers to source files")

  default_header_file = "header.txt"
  parser.add_argument(
    "--header",
    help="header file (default: {})".format(default_header_file),
    default=default_header_file
  )

  parser.add_argument(
    "pattern",
    metavar="PATTERN",
    help="source files search pattern",
  )

  return parser.parse_args()


def find_source_files(pattern):
  return glob.glob(pattern, recursive=True)


def process_source_files(files, headerFile):
  with open(headerFile, 'r') as f:
    headerLines = f.readlines()

  for file in files:
    write_header(file, headerLines)

def write_header(file, headerLines):
  with open(file, 'r') as org:
      lines = org.readlines()
      tmpFile = file + ".tmp"
      with open(tmpFile, 'w') as tmp:
        if len(lines) > 0 and lines[0].startswith("#!"):
          tmp.writelines(lines[0])
          tmp.writelines(headerLines)
          tmp.writelines(lines[1:])
        else:
          tmp.writelines(headerLines)
          tmp.writelines(lines)
  os.remove(file)
  os.rename(tmpFile, file)


def main():

  arguments = parse_arguments()

  files = find_source_files(arguments.pattern)
  process_source_files(files, arguments.header)

  return 0


if __name__ == "__main__":
  sys.exit(main())