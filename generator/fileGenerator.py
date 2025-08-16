from collections import defaultdict
from typing import Any
from time import time
import stat


class FileGenerator:
    def __init__(self) -> None:
        now: int = int(time() * 1e9)
        self.__files: dict[str, dict[str, Any]] = {
            "/": {
                "st_mode": (stat.S_IFDIR | 0o755),
                "st_ctime": now,
                "st_mtime": now,
                "st_atime": now,
                "st_nlink": 2,
            }
        }
        self.__data: dict[str, bytes] = defaultdict(bytes)
        self.__isGenerated: bool = False

    def __getTime(self) -> int:
        return int(time() * 1e9)

    def __generateFiles(self) -> None:
        now = self.__getTime()
        self.__files["/creds"] = {
            "st_mode": (stat.S_IFDIR | 0o644),
            "st_nlink": 2,
            "st_size": 20,
            "st_ctime": now,
            "st_mtime": now,
            "st_atime": now,
        }
        self.__files["/creds/pass.txt"] = {
            "st_mode": (stat.S_IFREG | 0o644),
            "st_nlink": 1,
            "st_size": 20,
            "st_ctime": now,
            "st_mtime": now,
            "st_atime": now,
        }
        self.__data["/creds/pass.txt"] = "supersecretpassword".encode()
        self.__files["/creds/user.txt"] = {
            "st_mode": (stat.S_IFREG | 0o644),
            "st_nlink": 1,
            "st_size": 13,
            "st_ctime": now,
            "st_mtime": now,
            "st_atime": now,
        }
        self.__data["/creds/user.txt"] = "notausername".encode()
        self.__files["/ssh.key"] = {
            "st_mode": (stat.S_IFREG | 0o644),
            "st_nlink": 1,
            "st_size": 8,
            "st_ctime": now,
            "st_mtime": now,
            "st_atime": now,
        }
        self.__data["/ssh.key"] = "notakey".encode()
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
