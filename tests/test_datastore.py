import pathlib
import unittest
from collections import namedtuple

from clubsandwich.datastore import (
  DataStore,
  Source,
  CSVReader,
)

root = pathlib.Path(__file__).parent.parent

StringyRow = namedtuple('StringyRow', ('f1', 'f2', 'f3', 'f4'))
ALPHABET_VALUE = [
  ['a', 'b', 'c', 'd'],
  ['e', 'f', 'g', 'h'],
  ['i', 'j', 'k', 'l'],
]


class FakeReader:
  def __init__(self, initial_values):
    self._values = initial_values
    self.identifier = 'FAKE'
  
  def read(self):
    return self._values

  def replace_values(self, new_values):
    self._values = new_values


class CSVReaderTestCase(unittest.TestCase):
  def test_reads_alphabet_default(self):
    r = CSVReader(
      str(root / 'tests' / 'fixtures' / 'alphabet.csv'))
    self.assertListEqual(list(r.read()), ALPHABET_VALUE[1:])

  def test_reads_alphabet_skip(self):
    r = CSVReader(
      str(root / 'tests' / 'fixtures' / 'alphabet.csv'),
      skip_first_line=True)
    self.assertListEqual(list(r.read()), ALPHABET_VALUE[1:])

  def test_reads_alphabet_noskip(self):
    r = CSVReader(
      str(root / 'tests' / 'fixtures' / 'alphabet.csv'),
      skip_first_line=False)
    self.assertListEqual(list(r.read()), ALPHABET_VALUE)


class SourceTestCase(unittest.TestCase):
  def _source(self, r):
    return Source(r, StringyRow, (
      ('f1', str),
      ('f2', str),
      ('f3', str),
      ('f4', str),
    ))

  def test_basically_works(self):
    r = CSVReader(
      str(root / 'tests' / 'fixtures' / 'alphabet.csv'),
      skip_first_line=False)
    source = self._source(r)
    source.reload()
    self.assertListEqual(list(source.keys()), ['a', 'e', 'i'])
    self.assertEqual(source['a'], StringyRow('a', 'b', 'c', 'd'))
    self.assertIn('a', source)

  def test_Dicts(self):
    r = FakeReader([{'f1': 'a', 'f2': 'b', 'f3': 'c', 'f4': 'd'}])
    source = self._source(r)
    source.reload()
    self.assertEqual(source['a'], StringyRow('a', 'b', 'c', 'd'))
    self.assertIn('a', source)

  def test_reload(self):
    r = FakeReader([['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h']])
    source = self._source(r)
    source.reload()
    self.assertListEqual(list(source.keys()), ['a', 'e'])
    r.replace_values(ALPHABET_VALUE)
    source.reload()
    self.assertListEqual(list(source.keys()), ['a', 'e', 'i'])
    self.assertIn('i', source)

  def test_dislikes_duplicate_keys(self):
    r = FakeReader([['a', 'b', 'c', 'd'], ['a', 'f', 'g', 'h']])
    source = self._source(r)
    self.assertRaises(ValueError, source.reload)


class DataStoreTestCase(unittest.TestCase):
  def _datastore(self):
    return DataStore('Row', (
      ('f1', str),
      ('f2', str),
      ('f3', str),
      ('f4', str),
    ))

  def test_multiple_sources(self):
    ds = self._datastore();
    ds.add_sources_with_glob(
      str(root / 'tests' / 'fixtures' / '*.csv'),
      lambda path: CSVReader(path))
    self.assertListEqual(list(ds.keys()), ['e', 'i', '5', '9'])
    self.assertEqual(ds['e'], ds.row_class('e', 'f', 'g', 'h'))
    self.assertEqual(ds.e, ds.row_class('e', 'f', 'g', 'h'))
    self.assertEqual(ds['5'], ds.row_class('5', '6', '7', '8'))
    self.assertEqual(ds.r_5, ds.row_class('5', '6', '7', '8'))
    self.assertRaises(KeyError, lambda: ds['x'])

  def test_dislikes_duplicate_keys(self):
    ds = self._datastore()
    ds.add_sources_with_glob(
      str(root / 'tests' / 'fixtures' / '*.csv'),
      lambda path: CSVReader(path))

    def _add_duplicates():
      ds.add_source(FakeReader([['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h']]))
    self.assertRaises(ValueError, _add_duplicates)
