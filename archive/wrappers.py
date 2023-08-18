#!/usr/bin/env python3

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, Union, Any
import tarfile
import zipfile

import py7zr

import archive.archive_types as at


class ArchiveWrapper(ABC):

    @abstractmethod
    def __init__(self, archive_obj: at.ArchiveIO, path: Path) -> None:
        pass

    @abstractmethod
    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        pass

    @abstractmethod
    def extract_to(self, path: Path) -> bool:
        pass


class TarArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: tarfile.TarFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        try:
            return {name: self.archive_obj.extractfile(name)}
        except KeyError:
            pass
        return None

    def extract_to(self, path: Path) -> bool:
        return True


class ZipArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: zipfile.ZipFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        try:
            item = {name: self.archive_obj.open(name)}
        except KeyError:
            return None
        return item

    def extract_to(self, path: Path) -> bool:
        return True


class SevenZArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: py7zr.SevenZipFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def open_by_name(self, name: str) -> Union[dict[Any, Any], None]:
        self.archive_obj.reset()
        item = self.archive_obj.read(targets=[name])
        if item and len(item.keys()) == 1:
            return item
        return None

    def extract_to(self, path: Path) -> bool:
        return True


class FileUnAwareArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: at.BuiltInFileUnAwareArchiveIO, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def _name(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    def open_by_name(self, name: str):
        return {self._name(): self.archive_obj}

    def extract_to(self, path: Path) -> bool:
        return True
