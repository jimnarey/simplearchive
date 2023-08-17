#!/usr/bin/env python3

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
