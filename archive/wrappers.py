#!/usr/bin/env python3

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, Union, Any
import tarfile
import zipfile

import py7zr

import archive_types as at


class ArchiveWrapper(ABC):

    @staticmethod
    def __init__(self, archive_obj: at.ArchiveIO, path: Path) -> None:
        pass

    @abstractmethod
    def open(self, name: str) -> Union[dict[Any, Any], None]:
        pass

    @abstractmethod
    def extract_to(self, path: Path) -> bool:
        pass


class TarArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: tarfile.TarFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def open(self, name: str) -> Union[dict[Any, Any], None]:
        return {name: self.archive_obj.extractfile(name)}


class ZipArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: zipfile.ZipFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def open(self, name: str) -> Union[dict[Any, Any], None]:
        return {name: self.archive_obj.open(name)}


class SevenZArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: py7zr.SevenZipFile, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def open(self, name: str) -> Union[dict[Any, Any], None]:
        content = self.archive_obj.read(targets=[name])
        if content and len(content.keys()) == 1:
            return content


class FileUnAwareArchiveWrapper(ArchiveWrapper):

    def __init__(self, archive_obj: at.BuiltInFileUnAwareArchiveIO, path: Path) -> None:
        self.archive_obj = archive_obj
        self.path = path

    def _name(self):
        return os.path.splitext(os.path.basename(self.path))[0]
