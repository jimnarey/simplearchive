#!/usr/bin/env python3

import os
import pathlib
import shutil
import zipfile
import tarfile
import gzip
import bz2
import lzma
from typing import IO, Optional

import py7zr

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(SCRIPT_DIR, '../tests/fixtures')
OUT = os.path.join(SCRIPT_DIR, '../out')
OUT_FILE = os.path.join(OUT, 'file.txt')


def print_file(path):
    with open(path, 'r') as file:
        print(file.read())


def all_files(path: str) -> list[pathlib.Path]:
    root_dir = pathlib.Path(path)
    return [item for item in root_dir.rglob('*') if item.is_file()]


archives = all_files(FIXTURES)


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

# for archive in archives:
#     with open(archive, 'rb') as arch_file:
#         open_as_tar(arch_file)


SUPPORTED_TARS = ['file.tar.bz2', 'file.tar.gz', 'file.tar.xz']

for tarname in SUPPORTED_TARS:
    with tarfile.open(os.path.join(FIXTURES, tarname)) as tarf:
        tarf.extractall(path=OUT)
    # print_file(OUT_FILE)
    # os.remove(OUT_FILE)

with open(os.path.join(OUT, 'file.txt'), 'wb') as out_file:
    with gzip.open(os.path.join(FIXTURES, 'file.txt.gz')) as gzf:
        shutil.copyfileobj(gzf, out_file)
# print_file(OUT_FILE)
# os.remove(OUT_FILE)

with open(os.path.join(OUT, 'file.txt'), 'wb') as out_file:
    with bz2.open(os.path.join(FIXTURES, 'file.txt.bz2')) as bzf:
        shutil.copyfileobj(bzf, out_file)
# print_file(OUT_FILE)
# os.remove(OUT_FILE)

with open(os.path.join(OUT, 'file.txt'), 'wb') as out_file:
    with lzma.open(os.path.join(FIXTURES, 'file.txt.xz')) as bzf:
        shutil.copyfileobj(bzf, out_file)
# print_file(OUT_FILE)
# os.remove(OUT_FILE)

with zipfile.ZipFile(os.path.join(FIXTURES, 'file.txt.zip'), 'r') as zipf:
    zipf.extractall(OUT)
# print_file(OUT_FILE)
# os.remove(OUT_FILE)

with py7zr.SevenZipFile(os.path.join(FIXTURES, 'file.txt.7z'), 'r') as szf:
    szf.extractall(path=OUT)
# print_file(OUT_FILE)
# os.remove(OUT_FILE)

with py7zr.SevenZipFile(os.path.join(FIXTURES, 'file.tar.7z'), 'r') as sztarf:
    contents = sztarf.readall()
    with tarfile.open(fileobj=contents['file.tar']) as tarf:
        tarf.extractall(path=OUT)
# print_file(OUT_FILE)
# os.remove(OUT_FILE)
