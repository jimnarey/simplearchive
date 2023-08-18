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

    def _open_tests(self, wrapper):

        result = wrapper.open('one.txt')
        self.assertIsInstance(result, dict)
        self.assertIn('one.txt', result)
        fileobj = result.get('one.txt')
        self.assertEqual(b'one\n', fileobj.read())

        result = wrapper.open('two/three.txt')
        self.assertIsInstance(result, dict)
        self.assertIn('two/three.txt', result)
        fileobj = result.get('two/three.txt')
        self.assertEqual(b'three\n', fileobj.read())


class TestTarArchiveWrapper(WrapperTestCase):

    def setUp(self):
        pass

    def _test_open(self, path):
        with open(path, 'rb') as fileobj:
            tar = tarfile.open(fileobj=fileobj)
            tar_wrapper = TarArchiveWrapper(tar, path)
            self._open_tests(tar_wrapper)

    def test_open_tar(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar')
        self._test_open(path)

    def test_open_tar_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.gz')
        self._test_open(path)

    def test_open_tar_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.bz2')
        self._test_open(path)

    def test_open_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        self._test_open(path)


class TestZipArchiveWrapper(WrapperTestCase):

    def test_open(self):
        pass


class TestSevenZArchiveWrapper(WrapperTestCase):

    def test_open(self):
        pass


class TestFileUnawareArchiveWrapper(WrapperTestCase):

    def test_open(self):
        pass
