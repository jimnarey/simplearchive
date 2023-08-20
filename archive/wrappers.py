#!/usr/bin/env python3

# from io import RawIOBase
import os
import io
from functools import cached_property
from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, Union, Any
import tarfile
import zipfile

import py7zr
import rarfile

import archive.archive_types as at


class ArchiveWrapper(ABC):

    @abstractmethod
    def __init__(self, archive_obj: at.ArchiveIO, path: Path) -> None:
        pass

    @abstractmethod
    def list(self) -> list[str]:
        pass

    @abstractmethod
    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        pass

    @abstractmethod
    def extract_to(self, path: Path) -> bool:
        pass

    def _name(self) -> str:
        return os.path.splitext(os.path.basename(self.path))[0]
    
    def _num_root_items(self):
        root_items = set([item.split('/')[0] for item in self.list()])
        return len(root_items)

    def _get_extract_path(self, path):
        if self._num_root_items() < 2:
            return path
        return Path(path, self._name())

    def open_all(self):
        all_items = {}
        for name in self.list():
            item = self.open_by_name(name)
            if item:
                all_items.update(item)
        return all_items


class TarArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: tarfile.TarFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def _name(self):
        name = super()._name()
        if name.endswith('.tar'):
            return name[:-4]
        return name
    
    def list(self) -> list[str]:
        members = self.archive_obj.getmembers()
        names = []
        for member in members:
            if member.isdir():
                names.append('{}/'.format(member.name))
            else:
                names.append(member.name)
        return names

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        try:
            return {name: self.archive_obj.extractfile(name)}
        except KeyError:
            pass
        return None

    def extract_to(self, path: Path) -> None:
        path_ = self._get_extract_path(path)
        # breakpoint()
        self.archive_obj.extractall(path_)


class ZipArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: zipfile.ZipFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def list(self) -> list[str]:
        return self.archive_obj.namelist()

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        try:
            item: dict[str, Any] = {name: self.archive_obj.open(name)}
            if name.endswith('/'):
                item[name] = None
        except KeyError:
            return None
        return item

    def extract_to(self, path: Path) -> None:
        path = self._get_extract_path(path)
        self.archive_obj.extractall(path)


class SevenZArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: py7zr.SevenZipFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def list(self) -> list[str]:
        names = []
        for member in self.archive_obj.list():
            if member.is_directory:
                names.append('{}/'.format(member.filename))
            else:
                names.append(member.filename)
        return names

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        self.archive_obj.reset()
        item = self.archive_obj.read(targets=[name])
        if item:
            return item
        if name in self.list():
            return {name: None}
        return None

    def extract_to(self, path: Path) -> None:
        path = self._get_extract_path(path)
        self.archive_obj.extractall(path)


# class RarFileObjWrapper(io.BufferedReader):

#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__( *args, **kwargs)

#     def read(self, *args, **kwargs) -> bytes:
#         self.seek(0)
#         return super().read(*args, **kwargs)

class RarArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: rarfile.RarFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path
        self.rar_file_path = archive_obj.filename

    def _refresh(self):
        """
        Workaround this issue: https://github.com/markokr/rarfile/issues/73
        """
        self.archive_obj.close()
        self.archive_obj = rarfile.RarFile(self.rar_file_path)

    def list(self) -> list[str]:
        return self.archive_obj.namelist()

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        self._refresh()
        try:
            item = {name: self.archive_obj.open(name)}
        except io.UnsupportedOperation:
            item = {name: None}
        except rarfile.NoRarEntry:
            item = None
        return item

    def extract_to(self, path: Path) -> None:
        path = self._get_extract_path(path)
        self.archive_obj.extractall(path)


class FileUnAwareArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: at.BuiltInFileUnAwareArchiveIO, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def list(self) -> list[str]:
        return [self._name()]

    # TODO - return file object if name is given
    def open_by_name(self, name: str):
        if name == self._name():
            return {name: self.archive_obj}
        return None

    def extract_to(self, path: Path) -> None:
        path = self._get_extract_path(path)
        file_path = Path(path, self._name())
        with open(file_path, 'wb') as targetfobj:
            targetfobj.write(self.archive_obj.read())
