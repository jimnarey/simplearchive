from typing import Union
import zipfile
import bz2
import gzip
import lzma
import tarfile

import py7zr

ArchiveIO = Union[zipfile.ZipFile, tarfile.TarFile, gzip.GzipFile,
                  bz2.BZ2File, lzma.LZMAFile, py7zr.SevenZipFile]


BuiltInFileUnAwareArchiveIO = Union[gzip.GzipFile, bz2.BZ2File, lzma.LZMAFile]
