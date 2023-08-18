import os
import io
import unittest
import hashlib
import pathlib
import tarfile
import zipfile
import gzip
import lzma
import bz2
import py7zr
from typing import IO

from archive import archive_types

from archive.wrappers import ArchiveWrapper, TarArchiveWrapper, \
                            ZipArchiveWrapper, \
                            FileUnAwareArchiveWrapper, SevenZArchiveWrapper



SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(SCRIPT_DIR, 'fixtures')


shas = {
    'one.txt': '2c8b08da5ce60398e1f19af0e5dccc744df274b826abe585eaba68c525434806',   # noqa E501
    'three.txt': 'f6936912184481f5edd4c304ce27c5a1a827804fc7f329f43d273b8621870776'  # noqa E501
}

dirs_contents = [
    'two/',
    'one.txt',
    'two/four/',
    'two/five/',
    'two/three.txt',
    'two/five/nine/',
    'two/four/seven/',
    'two/four/six.txt',
    'two/five/eight.txt',
    'two/four/seven/.keep',
    'two/five/nine/ten.txt'
 ]


class WrapperTestCase(unittest.TestCase):

    def setUp(self):
        self.fileobj: IO[bytes]
        self.archiveobj: archive_types.ArchiveIO

    def tearDown(self):
        try:
            self.archiveobj.close()
        except Exception:
            pass
        self.fileobj.close()

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

    def _open_all_asserts(self, wrapper):
        results = wrapper.open_all()
        self.assertEqual(set(results.keys()), set(dirs_contents))

    def _list_asserts(self, wrapper):
        self.assertEqual(set(wrapper.list()), set(dirs_contents))


class TestTarArchiveWrapper(WrapperTestCase):

    def _get_tar_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = tarfile.open(fileobj=self.fileobj)
        return TarArchiveWrapper(self.archiveobj, path)

    def test_open_by_name_tar(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar')
        wrapper = self._get_tar_wrapper(path)
        self._open_asserts(wrapper)

    def test_open_by_name_tar_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.gz')
        wrapper = self._get_tar_wrapper(path)
        self._open_asserts(wrapper)

    def test_open_by_name_tar_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.bz2')
        wrapper = self._get_tar_wrapper(path)
        self._open_asserts(wrapper)

    def test_open_by_name_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        wrapper = self._get_tar_wrapper(path)
        self._open_asserts(wrapper)

    def test_open_dir_by_name_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        wrapper = self._get_tar_wrapper(path)
        result = wrapper.open_by_name('two/')
        self.assertFalse(bool(result['two/']))  # type: ignore

    def test_open_all_by_name_tar(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar')
        wrapper = self._get_tar_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_open_all_by_name_tar_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.gz')
        wrapper = self._get_tar_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_open_all_by_name_tar_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.bz2')
        wrapper = self._get_tar_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_open_all_by_name_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        wrapper = self._get_tar_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_list_tar(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar')
        wrapper = self._get_tar_wrapper(path)
        self._list_asserts(wrapper)

    def test_list_tar_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.gz')
        wrapper = self._get_tar_wrapper(path)
        self._list_asserts(wrapper)

    def test_list_tar_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.bz2')
        wrapper = self._get_tar_wrapper(path)
        self._list_asserts(wrapper)

    def test_list_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        wrapper = self._get_tar_wrapper(path)
        self._list_asserts(wrapper)


class TestZipArchiveWrapper(WrapperTestCase):

    def _get_zip_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = zipfile.ZipFile(self.fileobj)
        return ZipArchiveWrapper(self.archiveobj, path)

    def test_open_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        self._open_asserts(wrapper)

    def test_open_dir_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        result = wrapper.open_by_name('two/')
        self.assertFalse(bool(result['two/']))  # type: ignore

    def test_open_all_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_list(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        self._list_asserts(wrapper)


class TestSevenZArchiveWrapper(WrapperTestCase):

    def _get_sevenz_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = py7zr.SevenZipFile(self.fileobj)
        return SevenZArchiveWrapper(self.archiveobj, path)

    def test_open_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        self._open_asserts(wrapper)

    def test_open_dir_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        result = wrapper.open_by_name('two/')
        self.assertFalse(bool(result['two/']))  # type: ignore

    def test_open_all_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_list(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        self._list_asserts(wrapper)


class TestFileUnawareArchiveWrapper(WrapperTestCase):

    def _get_gz_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = gzip.open(self.fileobj)
        return FileUnAwareArchiveWrapper(self.archiveobj, path)

    def _get_bz2_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = bz2.open(self.fileobj)
        return FileUnAwareArchiveWrapper(self.archiveobj, path)

    def _get_xz_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = lzma.open(self.fileobj)
        return FileUnAwareArchiveWrapper(self.archiveobj, path)

    def test_open_by_name_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.gz')
        wrapper = self._get_gz_wrapper(path)
        result = wrapper.open_by_name('file.txt')
        self.assertIn('file.txt', result)  # type: ignore
        self.assertEqual(len(result.keys()), 1)  # type: ignore
        fileobj = result.get('file.txt')  # type: ignore
        self.assertEqual(b'Test text\n', fileobj.read())  # type: ignore

    def test_open_by_name_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.bz2')
        wrapper = self._get_bz2_wrapper(path)
        result = wrapper.open_by_name('file.txt')
        self.assertIn('file.txt', result)  # type: ignore
        self.assertEqual(len(result.keys()), 1)  # type: ignore
        fileobj = result.get('file.txt')  # type: ignore
        self.assertEqual(b'Test text\n', fileobj.read())  # type: ignore

    def test_open_by_name_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
        wrapper = self._get_xz_wrapper(path)
        result = wrapper.open_by_name('file.txt')
        self.assertIn('file.txt', result)  # type: ignore
        self.assertEqual(len(result.keys()), 1)  # type: ignore
        fileobj = result.get('file.txt')  # type: ignore
        self.assertEqual(b'Test text\n', fileobj.read())  # type: ignore

    def test_open_by_name_bad_name_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
        wrapper = self._get_xz_wrapper(path)
        self.assertIsNone(wrapper.open_by_name('anything'))

    def test_open_all_by_name_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
        wrapper = self._get_xz_wrapper(path)
        result = wrapper.open_all()
        self.assertIn('file.txt', result)  # type: ignore
        self.assertEqual(len(result.keys()), 1)  # type: ignore
        fileobj = result.get('file.txt')  # type: ignore
        self.assertEqual(b'Test text\n', fileobj.read())  # type: ignore

    def test_list_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.gz')
        wrapper = self._get_gz_wrapper(path)
        self.assertEqual(wrapper.list(), ['file.txt'])

    def test_list_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.bz2')
        wrapper = self._get_gz_wrapper(path)
        self.assertEqual(wrapper.list(), ['file.txt'])

    def test_list_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
        wrapper = self._get_xz_wrapper(path)
        self.assertEqual(wrapper.list(), ['file.txt'])
