import os
import unittest
from zipfile import ZipFile
from tarfile import TarFile
from gzip import GzipFile
from bz2 import BZ2File
from archive import archive

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(SCRIPT_DIR, 'fixtures')


class TestArchive(unittest.TestCase):

    def test_open_as_zip_with_zip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = archive.open_as_zip(fileobj)
            self.assertIsInstance(value, ZipFile)

    def test_open_as_zip_with_non_zip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.bz2'), 'rb') as fileobj:
            value = archive.open_as_zip(fileobj)
            self.assertIsNone(value)

    def test_open_as_tar_with_tar_bz2_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.bz2'), 'rb') as fileobj:
            value = archive.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_tar_gz_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.gz'), 'rb') as fileobj:
            value = archive.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_tar_xz_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.tar.xz'), 'rb') as fileobj:
            value = archive.open_as_tar(fileobj)
            self.assertIsInstance(value, TarFile)

    def test_open_as_tar_with_non_tar_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = archive.open_as_tar(fileobj)
            self.assertIsNone(value)

    def test_open_as_bz2_with_bz2_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.bz2'), 'rb') as fileobj:
            value = archive.open_as_bz2(fileobj)
            self.assertIsInstance(value, BZ2File)

    def test_open_as_bz2_with_non_bz2_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.bak'), 'rb') as fileobj:
            value = archive.open_as_bz2(fileobj)
            self.assertIsNone(value)

    def test_open_as_gzip_with_gzip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.gz'), 'rb') as fileobj:
            value = archive.open_as_gzip(fileobj)
            self.assertIsInstance(value, GzipFile)

    def test_open_as_gzip_with_non_gzip_file(self):
        with open(os.path.join(FIXTURES_DIR, 'file.txt.zip'), 'rb') as fileobj:
            value = archive.open_as_gzip(fileobj)
            self.assertIsNone(value)

