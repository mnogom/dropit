#!/usr/bin/env python3

"""Entry point."""

from dropit.cli import parse_args
from dropit.manager import put_file, get_file, logout_app


def main():
    """Parse arguments, upload/download file to/from Dropbox."""

    args = parse_args()
    if args["command"] == "get":
        get_file(args["src_path"],
                 args["dest_path"],
                 args["force"])
    elif args["command"] == "put":
        put_file(args["src_path"],
                 args["dest_path"],
                 args["force"],
                 args["share"])
    else:
        logout_app()


if __name__ == "__main__":
    main()
