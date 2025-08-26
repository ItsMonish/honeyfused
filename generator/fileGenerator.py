from collections import defaultdict
import logging
import os
from .fileConfigs import FILE_CONFIGS
from random import randrange
from typing import Any, Callable
from time import time
import stat


class FileGenerator:
    def __init__(self, target: str) -> None:
        self.__target = target
        self.__logger = logging.getLogger("app")
        self.__files: dict[str, dict[str, Any]] = {
            "/": {
                "st_mode": (stat.S_IFDIR | 0o755),
                "st_ctime": self.__getTime(randrange(365, 730)),
                "st_mtime": self.__getTime(randrange(1, 3)),
                "st_atime": self.__getTime(randrange(1, 3)),
                "st_uid": os.getuid(),
                "st_gid": os.getgid(),
                "st_nlink": 2,
            }
        }
        self.__data: dict[str, bytes] = defaultdict(bytes)
        self.__isGenerated: bool = False

    def __getTime(self, days: int = 0) -> int:
        return int((time() - (86400 * days)) * 1e9)

    def __generateFiles(self) -> None:
        if FILE_CONFIGS.get(self.__target) == None:
            self.__logger.warning("[**]: Target {} not found. Skipping...")
            return
        target = FILE_CONFIGS[self.__target]
        if not isinstance(target["files"], dict):
            self.__logger.error(
                '[!!]: Error in internal config target["files"] is not dict'
            )
            return
        for file, func in target["files"].items():
            if not isinstance(func, Callable):
                self.__logger.error(
                    '[!!]: Error in internal config target["files"]["{}"] is not a function'.format(
                        file
                    )
                )
                return
            self.__data[file] = func()
            self.__files[file] = {
                "st_mode": (stat.S_IFREG | 0o644),
                "st_nlink": 2,
                "st_size": len(self.__data[file]),
                "st_ctime": self.__getTime(randrange(200, 400)),
                "st_mtime": self.__getTime(randrange(100, 200)),
                "st_atime": self.__getTime(randrange(0, 7)),
                "st_uid": os.getuid(),
                "st_gid": os.getgid(),
            }
            self.__logger.info(
                "[ii]: Generated file and contents for {} at {}".format(
                    self.__target, file
                )
            )
        self.__isGenerated = True

    def getFiles(self) -> dict[str, dict[str, Any]]:
        if self.__isGenerated:
            return self.__files
        self.__generateFiles()
        return self.__files

    def getFileData(self) -> dict[str, bytes]:
        if self.__isGenerated:
            return self.__data
        self.__generateFiles()
        return self.__data
