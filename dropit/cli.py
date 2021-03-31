"""CLI parser."""

import argparse


def parse_args():
    """Parse input parameters.

    :return: command, src_file, dest_file, [force flag]
    """
    parser = argparse.ArgumentParser(description="Get/Put file from Dropbox")
    parser.add_argument(dest="command", choices=["get", "put"])
    parser.add_argument("-f", "--force",
                        help="force update file (remove from dropbox if "
                             "already exists and upload)",
                        action="store_true", default=False)
    parser.add_argument(dest="src_path")
    parser.add_argument(dest="dest_path")

    args = parser.parse_args()

    return args.command, args.src_path, args.dest_path, args.force