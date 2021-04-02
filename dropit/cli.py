"""CLI parser."""

import argparse


def parse_args():
    """Parse input parameters.

    :return: dictionary with parsed arguments
    """
    parser = argparse.ArgumentParser(description="Get/Put file "
                                                 "from/to Dropbox")
    sub_parser = parser.add_subparsers(dest="command")

    put = sub_parser.add_parser(name="put",
                                help="Put local file to Dropbox",
                                description="Put local file to Dropbox")
    put.add_argument("-f", "--force",
                     help="force update file (rewrite file if it "
                          "already exists)",
                     action="store_true", default=False)
    put.add_argument("-s", "--share",
                     help="get url for file from Dropbox. Be careful. "
                          "File would be visible for everyone",
                     action="store_true", default=False)
    put.add_argument(dest="src_path",
                     help="Source file path")
    put.add_argument(dest="dest_path",
                     help="Destination file path")

    get = sub_parser.add_parser(name="get",
                                help="Get file from Dropbox "
                                     "to local storage",
                                description="Get file from Dropbox to local "
                                            "storage")
    get.add_argument("-f", "--force",
                     help="force update file (rewrite file if it "
                          "already exists)",
                     action="store_true", default=False)
    get.add_argument(dest="src_path",
                     help="Source file path")
    get.add_argument(dest="dest_path",
                     help="Destination file path")

    sub_parser.add_parser(name="logout",
                          help="Remove all user tokens",
                          description="Remove all user tokens")

    args = parser.parse_args()

    if args.command == "put":
        return {"command": args.command,
                "src_path": args.src_path,
                "dest_path": args.dest_path,
                "force": args.force,
                "share": args.share}
    if args.command == "get":
        return {"command": args.command,
                "src_path": args.src_path,
                "dest_path": args.dest_path,
                "force": args.force}
    else:
        return {"command": args.command}
