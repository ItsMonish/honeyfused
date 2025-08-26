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


app_log = logging.getLogger("app")


def main():
    args = parseArguments()
    conf = parseConfig(args.config)
    cleanupList = []
    fsthreads: List[threading.Thread] = []
    logging.basicConfig(
        level=logging.ERROR, format="%(filename)s:%(lineno)d - %(message)s"
    )
    fs_log = logging.getLogger()
    alert_log = logging.getLogger("alert")
    alert_log.setLevel(logging.INFO)
    if args.fs_debug:
        fs_log.setLevel(logging.DEBUG)
    if args.debug:
        app_log.setLevel(logging.INFO)
    if args.out is not None:
        alertFormatter = logging.Formatter("%(asctime)s - %(message)s")
        alertFileHandler = logging.FileHandler(args.out)
        alertFileHandler.setFormatter(alertFormatter)
        alert_log.addHandler(alertFileHandler)
        alert_log.propagate = False
    try:
        for _ in range(conf["decoys"]):
            target = choice(conf["targets"])
            conf["targets"].remove(target)
            if target not in FILE_CONFIGS:
                logging.error(
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
            app_log.info("[ii]: Mounting a filesystem and files on {}".format(target))
        while True:
            continue
    except RuntimeError:
        app_log.error("[!!]: Mount point busy or doesn't exist")
    except KeyboardInterrupt:
        for it in cleanupList:
            os.system("umount {}".format(it))
            os.rmdir(it)
        app_log.info("[ii]: Unmounted filesystems and exitting...")


def FSThread(target: str, dPath: str) -> None:
    fuse.FUSE(HoneyFileSystem(target), dPath, foreground=True)


def parseArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="HoneyFused",
        description="A tool to deploy a decoy filesystem for intrusion detection",
    )
    parser.add_argument(
        "-f",
        "--fs-debug",
        action="store_true",
        help="Enable verbose debug output for FUSE filesystem",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable verbose debug output for application",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=str,
        help="Path to output file for alerts. Defaults to stdout",
    )
    parser.add_argument("-c", "--config", type=str, help="Path to configuration file")
    args = parser.parse_args()
    return args


def parseConfig(confPath: str | None) -> dict:
    if confPath is None:
        confPath = "./config.yml"
    con = dict()
    try:
        with open(confPath) as f:
            con = safe_load(f)
    except YAMLError as e:
        app_log.error("[!!]: Error reading config")
        app_log.error(e)
        exit(1)
    except FileNotFoundError:
        app_log.error("[!!]: No config file found at {}".format(confPath))
    return con


if __name__ == "__main__":
    main()
