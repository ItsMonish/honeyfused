from collections import defaultdict
from .fileConfigs import FILE_CONFIGS
from random import randrange
from typing import Any, Callable
from time import time
import stat


class FileGenerator:
    def __init__(self, target: str) -> None:
        self.__target = target
        self.__files: dict[str, dict[str, Any]] = {
            "/": {
                "st_mode": (stat.S_IFDIR | 0o755),
                "st_ctime": self.__getTime(randrange(365, 730)),
                "st_mtime": self.__getTime(randrange(1, 3)),
                "st_atime": self.__getTime(randrange(1, 3)),
                "st_nlink": 2,
            }
        }
        self.__data: dict[str, bytes] = defaultdict(bytes)
        self.__isGenerated: bool = False

    def __getTime(self, days: int = 0) -> int:
        return int((time() - (86400 * days)) * 1e9)

    def __generateFiles(self) -> None:
        if FILE_CONFIGS.get(self.__target) == None:
            print("[!!]: Target {} not found. Skipping...")
            return
        target = FILE_CONFIGS[self.__target]
        if not isinstance(target["files"], dict):
            print('[!!]: Error in internal config target["files"] is not dict')
            return
        for file, func in target["files"].items():
            if not isinstance(func, Callable):
                print(
                    '[!!]: Error in internal config target["files"]["{}"] is not a function'.format(
                        file
                    )
                )
                return
            self.__data[file] = func()
            self.__files[file] = {
                "st_mode": (stat.S_IFDIR | 0o644),
                "st_nlink": 2,
                "st_size": 20,
                "st_ctime": self.__getTime(randrange(200, 400)),
                "st_mtime": self.__getTime(randrange(100, 200)),
                "st_atime": self.__getTime(randrange(0, 7)),
            }
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
