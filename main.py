import argparse
from typing import List
from generator.fileConfigs import FILE_CONFIGS
from filesystem import HoneyFileSystem
import logging
import mfusepy as fuse
import os
from random import choice
import threading
from yaml import safe_load, YAMLError


def main():
    args = parseArguments()
    conf = parseConfig()
    cleanupList = []
    fsthreads: List[threading.Thread] = []
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    try:
        for _ in range(conf["decoys"]):
            target = choice(conf["targets"])
            conf["targets"].remove(target)
            if target not in FILE_CONFIGS:
                print(
                    "[!!]: Option {} in config.yml is not found or supported".format(
                        target
                    )
                )
                exit(1)
            dPath: str = str(FILE_CONFIGS[target]["directory"])
            if not os.path.exists(dPath):
                os.mkdir(dPath)
                cleanupList.append(dPath)
            fsthreads.append(
                threading.Thread(
                    target=FSThread,
                    args=(
                        target,
                        dPath,
                    ),
                )
            )
            fsthreads[-1].start()
            print("[ii]: Mounted a filesystem on {}".format(target))
        while True:
            continue
    except RuntimeError:
        print("[!!]: Mount point busy or doesn't exist")
    except KeyboardInterrupt:
        for it in cleanupList:
            os.system("umount {}".format(it))
            os.rmdir(it)
        print("[ii]: Exitting...")


def FSThread(target: str, dPath: str) -> None:
    fuse.FUSE(HoneyFileSystem(target), dPath, foreground=True)


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


def parseConfig() -> dict:
    con = dict()
    try:
        with open("./config.yml") as f:
            con = safe_load(f)
    except YAMLError as e:
        print("[!!]: Error reading config")
        print(e)
    return con


if __name__ == "__main__":
    main()
