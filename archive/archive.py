#!/usr/bin/env python3

import os
import zipfile
import tarfile
import gzip
import bz2
import lzma

import py7zr

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(SCRIPT_DIR, '../tests/fixtures')
OUT =  os.path.join(SCRIPT_DIR, '../out')

with zipfile.ZipFile(os.path.join(FIXTURES, 'file.zip'), 'r') as zipf:
    # Extract all contents to the specified folder
    zipf.extractall(OUT)

TARS = ['file.tar.bz2', 'file.tar.gz', 'file.tar.xz']

for tarname in TARS:
    with tarfile.open(os.path.join(FIXTURES, tarname)) as tarf:
        tarf.extractall(path=OUT)





