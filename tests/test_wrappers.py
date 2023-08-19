import os
import io
import unittest
import tempfile
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
        self.assertEqual(b'one\n', results['one.txt'].read())
        self.assertEqual(b'three\n', results['two/three.txt'].read())

    def _list_asserts(self, wrapper):
        self.assertEqual(set(wrapper.list()), set(dirs_contents))

    def _extract_to_asserts(self, wrapper):
        with tempfile.TemporaryDirectory() as temp_dir:
            wrapper.extract_to(temp_dir)
            files = []
            dirs = []
            for _, _dirs, _files in os.walk(temp_dir):
                dirs.extend(_dirs)
                files.extend(_files)
            self.assertEqual(set(['two', 'five', 'four', 'nine', 'seven']), set(dirs))
            self.assertEqual(set(['one.txt', 'three.txt', 'eight.txt', 'ten.txt', 'six.txt', '.keep']), set(files))

            with open(pathlib.Path(temp_dir, 'one.txt'), 'rb') as file:
                self.assertEqual(b'one\n', file.read())
            with open(pathlib.Path(temp_dir, 'two/three.txt'), 'rb') as file:
                self.assertEqual(b'three\n', file.read())


class TestTarArchiveWrapper(WrapperTestCase):

    def _get_tar_wrapper(self, path):
        self.fileobj = open(path, 'rb')
        self.archiveobj = tarfile.open(fileobj=self.fileobj)
        return TarArchiveWrapper(self.archiveobj, path)

    # Check all variations of tarfile behave as expected
    # i.e. provide a dict with a file like object as its
    # only value and the file name as key
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

    # Check we get None in place of a file-like object
    # when 'opening' a directory
    def test_open_dir_by_name_tar_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        wrapper = self._get_tar_wrapper(path)
        result = wrapper.open_by_name('two/')
        self.assertIsNone(result['two/'])  

    # Check we get consistent results when opening all
    # files
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

    # Check we get consistent results when listing the
    # contents of variations of tarfile
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

    # Check extract_to
    def test_extract_to_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.tar.xz')
        wrapper = self._get_tar_wrapper(path)
        self._extract_to_asserts(wrapper)

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
        self.assertIsNone(result['two/'])

    def test_open_all_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_list(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        self._list_asserts(wrapper)

    def test_extract_to(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.zip')
        wrapper = self._get_zip_wrapper(path)
        self._extract_to_asserts(wrapper)


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
        self.assertIsNone(result['two/'])

    def test_open_all_by_name(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        self._open_all_asserts(wrapper)

    def test_list(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        self._list_asserts(wrapper)

    def test_extract_to(self):
        path = pathlib.Path(FIXTURES_DIR, 'dirs.7z')
        wrapper = self._get_sevenz_wrapper(path)
        self._extract_to_asserts(wrapper)


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

    def _test_open_by_name(self, wrapper):
        result = wrapper.open_by_name('file.txt')
        self.assertIn('file.txt', result)  # type: ignore
        self.assertEqual(len(result.keys()), 1)  # type: ignore
        fileobj = result.get('file.txt')  # type: ignore
        self.assertEqual(b'Test text\n', fileobj.read())  # type: ignore

    # If the file name without the gz/xz/bz2 extension is provided, 
    # the data is returned as a dict with a file-like object. Check
    # this works consistently across compression types
    def test_open_by_name_gz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.gz')
        wrapper = self._get_gz_wrapper(path)
        self._test_open_by_name(wrapper)

    def test_open_by_name_bz2(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.bz2')
        wrapper = self._get_bz2_wrapper(path)
        self._test_open_by_name(wrapper)

    def test_open_by_name_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
        wrapper = self._get_xz_wrapper(path)
        self._test_open_by_name(wrapper)

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

    # Check we get consistent results when 'listing' the contents
    # of gz, xz, bz2
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

    # Check extract_to
    def test_extract_to_xz(self):
        path = pathlib.Path(FIXTURES_DIR, 'file.txt.xz')
        wrapper = self._get_xz_wrapper(path)
        with tempfile.TemporaryDirectory() as temp_dir:
            wrapper.extract_to(temp_dir)
            self.assertEqual(set(['file.txt']), set(os.listdir(temp_dir)))
            with open(pathlib.Path(temp_dir, 'file.txt'), 'rb') as file:
                self.assertEqual(b'Test text\n', file.read())

