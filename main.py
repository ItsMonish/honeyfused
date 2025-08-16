import logging
from filesystem import HoneyFileSystem
import mfusepy as fuse

MOUNT_POINT = "/tmp/testing"


def main():
    logging.basicConfig(level=logging.DEBUG)
    fuse.FUSE(HoneyFileSystem(), MOUNT_POINT, foreground=True)


if __name__ == "__main__":
    main()
