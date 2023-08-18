import os
import unittest
import hashlib
import pathlib
import tarfile
import zipfile
import gzip
import lzma
import bz2
import py7zr

from archive.wrappers import TarArchiveWrapper, ZipArchiveWrapper, \
                             FileUnAwareArchiveWrapper, SevenZArchiveWrapper



SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(SCRIPT_DIR, 'fixtures')


shas = {
    'one.txt': '2c8b08da5ce60398e1f19af0e5dccc744df274b826abe585eaba68c525434806',   # noqa E501
    'three.txt': 'f6936912184481f5edd4c304ce27c5a1a827804fc7f329f43d273b8621870776'  # noqa E501
}


class WrapperTestCase(unittest.TestCase):

    def _open_asserts(self, wrapper):

        result = wrapper.open_by_name('one.txt')
        self.assertIsInstance(result, dict)
        self.assertIn('one.txt', result)
        fileobj = result.get('one.txt')
        self.assertEqual(b'one\n', fileobj.read())

        result = wrapper.open_by_name('two/three.txt')
        self.assertIsInstance(result, dict)
        self.assertIn('two/three.txt', result)
        fileobj = result.get('two/three.txt')
        self.assertEqual(b'three\n', fileobj.read())

        result = wrapper.open_by_name('notafile')
        self.assertIsNone(result)


class TestTarArchiveWrapper(WrapperTestCase):

    def _test_open_by_name(self, path):
        with open(path, 'rb') as fileobj:
            tar = tarfile.open(fileobj=fileobj)
            tar_wrapper = TarArchiveWrapper(tar, path)
            self._open_asserts(tar_wrapper)

    def test_open_by_name_tar(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar')
        self._test_open_by_name(path)

    def test_open_by_name_tar_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.gz')
        self._test_open_by_name(path)

    def test_open_by_name_tar_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.bz2')
        self._test_open_by_name(path)

    def test_open_by_name_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        self._test_open_by_name(path)


class TestZipArchiveWrapper(WrapperTestCase):

    def _test_open_by_name(self, path):
        with open(path, 'rb') as fileobj:
            zip = zipfile.ZipFile(fileobj)
            zip_wrapper = ZipArchiveWrapper(zip, path)
            self._open_asserts(zip_wrapper)

    def test_open_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        self._test_open_by_name(path)


class TestSevenZArchiveWrapper(WrapperTestCase):

    def _test_open_by_name(self, path):
        with open(path, 'rb') as fileobj:
            sevenZ = py7zr.SevenZipFile(fileobj)
            sZ_wrapper = SevenZArchiveWrapper(sevenZ, path)
            self._open_asserts(sZ_wrapper)

    def test_open_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        self._test_open_by_name(path)


class TestFileUnawareArchiveWrapper(WrapperTestCase):

    @staticmethod
    def _get_wrapper(path):
        fileobj = open(path, 'rb')
        sevenZ = py7zr.SevenZipFile(fileobj)
        return SevenZArchiveWrapper(sevenZ, path)

    # def test_open_by_name_gz(self):
    #     path = pathlib.Path(FIXTURES_DIR, 'file.txt.gz')
    #     wrapper = self._get_wrapper(path)
    #     self.assertIsInstance(wrapper.open_by_name(),  )

    # def test_open_by_name_bz2(self):
    #     path = pathlib.Path(FIXTURES_DIR, 'file.txt.bz2')
    #     wrapper = self._get_wrapper(path)

    # def test_open_by_name_xz(self):
    #     path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
    #     wrapper = self._get_wrapper(path)
