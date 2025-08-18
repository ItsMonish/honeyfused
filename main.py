import argparse
import logging
from filesystem import HoneyFileSystem
import mfusepy as fuse

MOUNT_POINT = "/tmp/testing"


def main():
    args = parseArguments()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    try:
        fuse.FUSE(HoneyFileSystem(), MOUNT_POINT, foreground=True)
    except RuntimeError:
        print("[!!]: Mount point busy or doesn't exist")


def parseArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="HoneyFused",
        description="A tool to deploy a decoy filesystem for intrusion detection",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable verbose debug output"
    )
    parser.add_argument("-c", "--config", type=str, help="Path to configuration file")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
