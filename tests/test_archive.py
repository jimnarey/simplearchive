import os
import pathlib
import unittest
from zipfile import ZipFile
from tarfile import TarFile
from gzip import GzipFile
from bz2 import BZ2File
from lzma import LZMAFile

from py7zr import SevenZipFile

from archive import opener

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(SCRIPT_DIR, 'fixtures')


class TestopenerArchiveSpecificFuncs(unittest.TestCase):

    # zip
    def test_open_as_zip_with_zip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = opener.open_as_zip(fileobj)
            self.assertIsInstance(value, ZipFile)

    def test_open_as_zip_with_non_zip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.bz2'), 'rb') as fileobj:
            value = opener.open_as_zip(fileobj)
            self.assertIsNone(value)

    # tarfile variations
    def test_open_as_tar_with_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.tar'), 'rb') as fileobj:
            value = opener.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_tar_bz2_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.bz2'), 'rb') as fileobj:
            value = opener.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_tar_gz_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.gz'), 'rb') as fileobj:
            value = opener.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_tar_xz_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.xz'), 'rb') as fileobj:
            value = opener.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_non_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = opener.open_as_tar(fileobj)
            self.assertIsNone(value)

    # tar.7z
    def test_open_as_tar_7z_with_tar_7z_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.7z'), 'rb') as fileobj:
            value = opener.open_as_tar_7z(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_7z_with_7z_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.7z'), 'rb') as fileobj:
            value = opener.open_as_tar_7z(fileobj)
            self.assertIsNone(value)

    def test_open_as_tar_7z_with_non_7z_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = opener.open_as_tar_7z(fileobj)
            self.assertIsNone(value)

    # bz2
    def test_open_as_bz2_with_bz2_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.bz2'), 'rb') as fileobj:
            value = opener.open_as_bz2(fileobj)
            self.assertIsInstance(value, BZ2File)

    def test_open_as_bz2_with_bz2_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.bz2'), 'rb') as fileobj:
            value = opener.open_as_bz2(fileobj)
            self.assertIsInstance(value, BZ2File)

    def test_open_as_bz2_with_non_bz2_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.7z'), 'rb') as fileobj:
            value = opener.open_as_bz2(fileobj)
            self.assertIsNone(value)

    # gz
    def test_open_as_gzip_with_gzip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.gz'), 'rb') as fileobj:
            value = opener.open_as_gzip(fileobj)
            self.assertIsInstance(value, GzipFile)

    def test_open_as_gzip_with_gzip_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.gz'), 'rb') as fileobj:
            value = opener.open_as_gzip(fileobj)
            self.assertIsInstance(value, GzipFile)

    def test_open_as_gzip_with_non_gzip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = opener.open_as_gzip(fileobj)
            self.assertIsNone(value)

    # xz
    def test_open_as_lzma_with_lzma_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.xz'), 'rb') as fileobj:
            value = opener.open_as_lzma(fileobj)
            self.assertIsInstance(value, LZMAFile)

    def test_open_as_lzma_with_lzma_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.xz'), 'rb') as fileobj:
            value = opener.open_as_lzma(fileobj)
            self.assertIsInstance(value, LZMAFile)

    def test_open_as_lzma_with_non_lzma_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = opener.open_as_lzma(fileobj)
            self.assertIsNone(value)

    # 7z
    def test_open_as_7z_with_7z_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.7z'), 'rb') as fileobj:
            value = opener.open_as_7z(fileobj)
            self.assertIsInstance(value, SevenZipFile)

    def test_open_as_7z_with_7z_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.7z'), 'rb') as fileobj:
            value = opener.open_as_7z(fileobj)
            self.assertIsInstance(value, SevenZipFile)

    def test_open_as_7z_with_non_7z_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = opener.open_as_7z(fileobj)
            self.assertIsNone(value)


class TestopenerGeneralFuncs(unittest.TestCase):

    def test_open_with_zip_file(self):
        path = pathlib.Path(os.path.join(FIXTURES_DIR, 'file.txt.zip'))
        self.assertIsInstance(opener.open_archive(path), ZipFile)
