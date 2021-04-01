#!/usr/bin/env python3

"""Entry point."""

from dropit.cli import parse_args
from dropit.dropbox_explorer import put_file, get_file


def main():
    """Parse arguments, upload/download file to/from Dropbox."""

    command, source_path, destination_path, use_force, share = parse_args()
    if command == "get":
        get_file(source_path, destination_path, use_force)
    else:
        put_file(source_path, destination_path, use_force, share)


if __name__ == "__main__":
    main()
