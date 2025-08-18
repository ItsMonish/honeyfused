from typing import Any, Iterable, Optional, List
from generator import fileGenerator
from time import time
import ctypes
import errno
import mfusepy as fuse
import stat
import struct


class HoneyFileSystem(fuse.LoggingMixIn, fuse.Operations):
    use_ns = True

    def __init__(self) -> None:
        super().__init__()
        fGen = fileGenerator.FileGenerator()
        self.__files: dict[str, dict[str, Any]] = fGen.getFiles()
        self.__data: dict[str, bytes] = fGen.getFileData()

    def __getTime(self) -> int:
        return int(time() * 1e9)

    def __getParentPath(self, path: str) -> str:
        if path[-1] == "/":
            parent = "/".join(path[:-1].split("/")[:-1])
        else:
            parent = "/".join(path.split("/")[:-1])
        return "/" if parent == "" else parent

    @fuse.overrides(fuse.Operations)
    def chmod(self, path: str, mode: int) -> int:
        self.__files[path]["st_mode"] &= 0o770000
        self.__files[path]["st_mode"] |= mode
        return 0

    @fuse.overrides(fuse.Operations)
    def chown(self, path: str, uid: int, gid: int) -> int:
        self.__files[path]["st_uid"] = uid
        self.__files[path]["st_gid"] = gid
        return 0

    @fuse.overrides(fuse.Operations)
    def create(self, path: str, mode: int, fi=None) -> int:
        print("Called {}".format(path))
        now = self.__getTime()
        self.__files[path] = {
            "st_mode": (stat.S_IFREG | mode),
            "st_nlink": 1,
            "st_size": 0,
            "st_ctime": now,
            "st_mtime": now,
            "st_atime": now,
        }
        return 0

    @fuse.overrides(fuse.Operations)
    def getattr(self, path: str, fh=None) -> dict[str, Any]:
        if path not in self.__files:
            # return {path: {"st_mode": 0o00000, "st_nlink": 2}}
            raise fuse.FuseOSError(errno.ENOENT)
        return self.__files[path]

    @fuse.overrides(fuse.Operations)
    def getxattr(self, path: str, name: str, position=0) -> bytes:
        attrs: dict[str, bytes] = self.__files[path].get("attrs", {})
        try:
            return attrs[name]
        except KeyError:
            return b""

    @fuse.overrides(fuse.Operations)
    def listxattr(self, path: str) -> Iterable[str]:
        attrs = self.__files[path].get("attrs", {})
        return attrs.keys()

    @fuse.overrides(fuse.Operations)
    def mkdir(self, path: str, mode: int) -> int:
        now = self.__getTime()
        self.__files[path] = {
            "st_mode": (stat.S_IFDIR | mode),
            "st_nlink": 2,
            "st_size": 0,
            "st_ctime": now,
            "st_mtime": now,
            "st_atime": now,
        }
        parent = self.__getParentPath(path)
        self.__files[parent]["st_nlink"] += 1
        return 0

    @fuse.overrides(fuse.Operations)
    def read(self, path: str, size: int, offset: int, fh: int) -> bytes:
        return self.__data[path][offset : offset + size]

    @fuse.overrides(fuse.Operations)
    def readdir(self, path: str, fh: int) -> List[str]:
        dir = {".", ".."}
        for x in self.__files:
            if x.startswith(path) and len(x) > len(path):
                x = x.removeprefix(path)
                file = x.split("/")[0]
                file = x.split("/")[1] if file == "" else file
                dir.add(file)
        return list(dir)

    @fuse.overrides(fuse.Operations)
    def readlink(self, path: str) -> str:
        return self.__data[path].decode()

    @fuse.overrides(fuse.Operations)
    def removexattr(self, path: str, name: str) -> int:
        attrs: dict[str, bytes] = self.__files[path].get("attrs", {})
        try:
            del attrs[name]
        except KeyError:
            pass
        return 0

    @fuse.overrides(fuse.Operations)
    def rename(self, old: str, new: str) -> int:
        if old in self.__data:
            self.__data[new] = self.__data.pop(old)
        if old in self.__files:
            self.__files[new] = self.__files.pop(old)
        else:
            raise fuse.FuseOSError(errno.ENOENT)
        return 0

    @fuse.overrides(fuse.Operations)
    def rmdir(self, path: str) -> int:
        self.__files.pop(path)
        parent = self.__getParentPath(path)
        self.__files[parent]["st_nlink"] -= 1
        return 0

    @fuse.overrides(fuse.Operations)
    def setxattr(
        self, path: str, name: str, value, options: int, position: int = 0
    ) -> int:
        attrs: dict[str, bytes] = self.__files[path].setdefault("attrs", {})
        attrs[name] = value
        return 0

    @fuse.overrides(fuse.Operations)
    def statfs(self, path: str) -> dict[str, int]:
        return {"f_bsize": 512, "f_blocks": 4096, "f_bavail": 2048}

    @fuse.overrides(fuse.Operations)
    def symlink(self, target: str, source: str) -> int:
        self.__files[target] = {
            "st_mode": (stat.S_IFLNK | 0o777),
            "st_nlink": 1,
            "st_size": len(source),
        }
        self.__data[target] = source.encode()
        return 0

    @fuse.overrides(fuse.Operations)
    def truncate(self, path: str, length: int, fh=None) -> int:
        self.__data[path] = self.__data[path][:length].ljust(
            length, "\x00".encode("ascii")
        )
        self.__files[path]["st_size"] = length
        return 0

    @fuse.overrides(fuse.Operations)
    def unlink(self, path: str) -> int:
        try:
            self.__data.pop(path)
        except KeyError:
            pass
        self.__files.pop(path)
        return 0

    @fuse.overrides(fuse.Operations)
    def utimens(self, path: str, times: Optional[tuple[int, int]] = None) -> int:
        now = self.__getTime()
        atime, mtime = times or (now, now)
        self.__files[path]["st_atime"] = atime
        self.__files[path]["st_mtime"] = mtime
        return 0

    @fuse.overrides(fuse.Operations)
    def write(self, path: str, data, offset: int, fh: int) -> int:
        self.__data[path] = (
            self.__data[path][:offset].ljust(offset, "\x00".encode("ascii"))
            + data
            + self.__data[path][offset + len(data) :]
        )
        self.__files[path]["st_size"] = len(self.__data[path])
        return len(data)

    @fuse.overrides(fuse.Operations)
    def ioctl(self, path: str, cmd: int, arg, fh: int, flags: int, data) -> int:
        from ioctl_opt import IOWR

        iowr_m = IOWR(ord("M"), 1, ctypes.c_uint32)
        if cmd == iowr_m:
            inbuf = ctypes.create_string_buffer(4)
            ctypes.memmove(inbuf, data, 4)
            data_in = struct.unpack("<I", inbuf)[0]
            data_out = data_in + 1
            outbuf = struct.pack("<I", data_out)
            ctypes.memmove(data, outbuf, 4)
        else:
            raise fuse.FuseOSError(errno.ENOTTY)
        return 0
