import os
import pathlib
import shutil
import zipfile
import tarfile
import gzip
import bz2
import lzma
from typing import IO, Optional, Union, Callable

import py7zr
import rarfile
import lhafile

from custom_types.io import ArchiveIO, CompressionIO


def open_as_zip(fileobj: IO[bytes]) -> Optional[zipfile.ZipFile]:
    try:
        zipf = zipfile.ZipFile(fileobj)
    except zipfile.BadZipFile:
        return None
    return zipf


def open_as_tar(fileobj: IO[bytes]) -> Optional[tarfile.TarFile]:
    try:
        tarf = tarfile.open(fileobj=fileobj)
    except tarfile.ReadError:
        return None
    return tarf


def open_as_gzip(fileobj: IO[bytes]) -> Optional[gzip.GzipFile]:
    try:
        gzipf = gzip.open(fileobj)
        gzipf.peek(32)
    except gzip.BadGzipFile:
        return None
    return gzipf


def open_as_bz2(fileobj: IO[bytes]) -> Optional[bz2.BZ2File]:
    try:
        bz2f = bz2.open(fileobj)
        bz2f.peek(32)  # type: ignore
    except OSError:
        return None
    return bz2f


def open_as_lzma(fileobj: IO[bytes]) -> Optional[lzma.LZMAFile]:
    try:
        lzmaf = lzma.open(fileobj)
        lzmaf.peek(32)
    except lzma.LZMAError:
        return None
    return lzmaf


def open_as_tar_7z(fileobj: IO[bytes]) -> Optional[tarfile.TarFile]:
    try:
        szf = py7zr.SevenZipFile(fileobj)  # type: ignore
    except py7zr.Bad7zFile:
        return None
    if len(szf.files) == 1:
        if fileobjs := szf.read(targets=[szf.files[0].filename]):
            sz_tar_fobj = tuple(fileobjs.values())[0]
            return open_as_tar(sz_tar_fobj)
    return None


def open_as_7z(fileobj: IO[bytes]) -> Optional[py7zr.SevenZipFile]:
    try:
        szf = py7zr.SevenZipFile(fileobj)  # type: ignore
    except py7zr.Bad7zFile:
        return None
    return szf


def open_as_rar(fileobj: IO[bytes]) -> Optional[rarfile.RarFile]:
    try:
        rarf = rarfile.RarFile(fileobj)
    except rarfile.NotRarFile:
        return None
    return rarf


def open_as_lha(fileobj: IO[bytes]) -> Optional[lhafile.LhaFile]:
    try:
        lhaf = lhafile.LhaFile(fileobj)
    except lhafile.BadLhafile:
        return None
    return lhaf


OPEN_FUNCS = [
    open_as_tar_7z,
    open_as_tar,
    open_as_zip,
    open_as_7z,
    open_as_gzip,
    open_as_lzma,
    open_as_bz2,
    open_as_rar
]

# TODO - handle rar, handle lzma
EXTENSIONS = {
    '.tar.7z': open_as_tar_7z,
    '.tar.xz': open_as_tar,
    '.tar.gz': open_as_tar,
    '.tar.bz2': open_as_tar,
    '.tar': open_as_tar,
    '.zip': open_as_zip,
    '.gz': open_as_gzip,
    '.xz': open_as_lzma,
    '.bz2': open_as_bz2,
    '.7z': open_as_7z,
    '.rar': open_as_rar
}


def get_open_func_by_ext(path: pathlib.Path) -> Optional[Callable]:
    for ext, openfunc in EXTENSIONS.items():
        if str(path).endswith(ext):
            return openfunc
    return None


def open_archive(path: pathlib.Path) -> Optional[ArchiveIO]:
    open_funcs = OPEN_FUNCS
    with open(path, 'rb') as fileobj:
        ext_open_func = get_open_func_by_ext(path)
        if ext_open_func:
            archive_obj = ext_open_func(fileobj)
            if archive_obj:
                return archive_obj
            open_funcs = [func for func in OPEN_FUNCS if func
                          is not ext_open_func]
        for open_func in open_funcs:
            archive_obj = open_func(fileobj)
            if archive_obj:
                return archive_obj
    return None
