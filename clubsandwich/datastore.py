"""
Convenient access to spreadsheet-style game data files. CSV is the only
included implementation, but writing new readers is trivial.

Here's a simple example::

  def f_char(val):
    "Ensure *val* is a one-character string"
    if isinstance(val, str) and len(val) == 1:
      return val
    else:
      raise ValueError("Bad character value: {!r}".format(val))

  # Imagine you have a directory of CSVs with monster definitions.
  # One of them, gnomes.csv, might look like this:
  #  ID,            Strength,   Color,    Char
  #  gnome_easy,    1,          #ff0000,  g
  #  gnome_medium,  2,          #ffff00,  g
  #  gnome_hard,    3,          #ff00ff,  g
  #  gnome_huge,    4,          #880000,  G

  # To read them, create a :py:class:`DataStore`, passing a class name
  # for items and an ordered mapping of field name to value:
  monster_types = DataStore('MonsterType', (
    ('id', str),
    ('strength', int), # int('5') = 5
    ('color', str),
    ('char', f_char),  # see helper at top of example
  ))

  # You can load all the CSVs at once, like this:
  monster_types.add_sources_with_glob('data/monsters/*.csv', CSVReader)

  # Now you can access any monster type easily:
  print(monster_types.gnome_easy)
  # > MonsterType(id='gnome_easy', strength=1, color='#ff0000', char='g')
  print(monster_types['gnome_easy'])
  # > same thing

  # And if you edit your data files, you can reload them at runtime to
  # immediately pick up changes:

  monster_types.reload()

Limitations and details:

* The first field in the mapping must be a unique identifier, unique across all
  readers.
* Identifiers may overlap built-in Python method names or start with numbers.
  To access these values by attribute, prefix them with ``r_``. So a value with
  id ``5`` could be accessed by ``data_store.r_5``. Or you could just use
  dict-style lookup, like ``data_store['5']``. To avoid these issues, use
  Python-identifier-legal uppercase string identifiers.
* You may pass default values to the :py:class:`DataStore`. These only matter
  if your data may be missing keys (i.e. if your reader emits ``dict``s), so
  you can just pass ``None`` if you want.
"""

import csv
import glob
from collections import namedtuple
from uuid import uuid4


class ValidationException(Exception):
    """
    Thrown when a row does not match the mapping in your :py:class:`DataStore`
    instance
    """
    pass


class Reader:
    """
    Abstract base class for a reader. You can subclass this for your own readers
    if you want, but duck typing is probably less verbose.

    .. py:attribute:: identifier

      String identifier for this reader. Only used to provide helpful
      exception messages.
    """

    def read(self):
        """
        Iterator of sequences or dicts from the file or data structure. Like
        ``('a', 'b', 'c')`` or ``{'f1': 'a', 'f2': 'b', 'f3': 'c'}``.
        """


class CSVReader:
    """
    Returns the lines from a single CSV file. If your first line is just column
    labels, you can skip it (this is the default behavior).

    .. py:attribute:: path

      Path to the file

    .. py:attribute:: identifier

      See :py:attr:`Reader.identifier`

    .. py:attribute:: skip_first_line

      If ``True`` (default), always skip the first line of the file.
    """

    def __init__(self, path, skip_first_line=True):
        """
        """
        self.path = path
        self.skip_first_line = skip_first_line
        self.identifier = path

    def read(self):
        """Iterator of CSV values. Values are lists."""
        with open(self.path) as f:
            reader = csv.reader(f)
            skip_next_line = self.skip_first_line
            for line in reader:
                if skip_next_line:
                    skip_next_line = False
                    continue
                yield line


def _read_row(row_class, fields, defaults, values):
    if isinstance(values, dict):
        kwargs = {}
        for k, v in fields:
            if k in values:
                kwargs[k] = v(values[k])
            else:
                kwargs[k] = defaults[k]
        return row_class(**kwargs)
    else:
        return row_class(**{
            k: fn(v) for (k, fn), v in zip(fields, values)})


class Source:
    """
    Stores and indexes values from a reader. You shouldn't need to worry about
    this class much; it's created automatically for you, and sources are accessed
    in aggregate via a :py:class:`DataStore`.

    .. py:attribute:: reader

      Some :py:class:`Reader` subclass or duck-typed class.

    .. py:attribute:: row_class

      Class to instantiate for each row

    .. py:attribute:: fields

      Sequence of pairs mapping field name to value factory

    .. py:attribute::  defaults

      Default values for the fields, or ``None`` if you're quite sure all values
      will be specified

    .. py:attribute:: items

      List of items read from the source
    """

    def __init__(self, reader, row_class, fields, defaults=None):
        self.reader = reader
        self.row_class = row_class
        self.fields = fields
        self.defaults = defaults
        self._items_by_key = {}
        self.items = []

    def reload(self):
        """Run the reader again; replace all stored items"""
        self._items_by_key = {}
        self.items = []
        for values in self.reader.read():
            try:
                item = _read_row(self.row_class, self.fields,
                                 self.defaults, values)
            except:
                raise ValidationException(
                    "Validation error in reader {} for class {}: row does not match schema: {!r}".format(
                        self.reader.identifier, self.row_class.__name__, values))
            self.items.append(item)
            if item[0] in self._items_by_key:
                raise ValueError(
                    "Duplicate key {!r} in {}".format(item[0], self.reader.identifier))
            self._items_by_key[item[0]] = item

    def keys(self):
        """Iterator of all keys in this source"""
        # strong assumption: first field is unique id
        return [i[0] for i in self.items]

    def __contains__(self, k):
        return k in self._items_by_key

    def __getitem__(self, k):
        return self._items_by_key[k]


class DataStore:
    """
    Collection of data sources for convenient access. See example in module docs
    for a basic guide.
    """

    def __init__(self, type_name, fields, defaults=None):
        """
        :param str type_name: Name of the class to create for values
        :param [(name, factory), ...] fields: Sequence mapping field name to a
                                              function that converts a string to
                                              the field's value
        :param dict|None defaults: Default values for fields, or ``None`` if
                                   irrelevant.

        The class creation stuff merits some explanation. The idea is that you'll
        have one data store per type, and having to separately specify the class
        would add unnecessary boilerplate.

        So what you do instead is to pass a class name and a field mapping. This
        is turned into a ``namedtuple``, and each field is run through the mapping
        function when the data is parsed from a file.
        """
        self.row_class = namedtuple(type_name, [f[0] for f in fields])
        self.fields = fields
        self.defaults = defaults
        self.sources = []

    def _add_source(self, reader):
        source = Source(reader, self.row_class, self.fields, self.defaults)
        self.sources.append(source)
        source.reload()

    def add_source(self, reader):
        """
        :param Reader reader:

        Add a source that reads from the given reader.
        """
        self._add_source(reader)
        self.validate()

    def add_sources_with_glob(self, pattern, reader_factory):
        """
        :param str pattern: Glob pattern (`docs <https://docs.python.org/3/library/glob.html>`_)
        :param function reader_factory: ``reader_factory(path) -> Reader``

        Add multiple sources for paths that match the given pattern (glob).
        For example, if you wanted to read all CSV files in your "monsters"
        directory, you'd do this::

          data_store.add_sources_with_glob('data/monsters/*.csv', CSVReader)
        """
        for path in glob.glob(pattern, recursive=True):
            self._add_source(reader_factory(path))
        self.validate()

    def validate(self):
        for key in self.keys():
            sources = [source for source in self.sources if key in source]
            if len(sources) > 1:
                raise ValueError("Duplicate key {!r} in ".format(
                    key, [s.reader.identifier for s in sources]))

    def reload(self):
        """
        Reload all sources. Does not pick up new files if you used a glob. To
        handle that case, call :py:meth:`unload` and then re-add all your sources.
        """
        for source in self.sources:
            source.reload()

    def unload(self):
        """
        Remove all sources.
        """
        self.sources = []

    def keys(self):
        """Iterator of all item identifiers"""
        for source in self.sources:
            yield from source.keys()

    @property
    def items(self):
        """Iterator of all items"""
        for source in self.sources:
            yield from source.items

    def __contains__(self, k):
        return any(k in source for source in self.sources)

    def __getitem__(self, k):
        for source in self.sources:
            if k in source:
                return source[k]
        raise KeyError(k)

    def __getattr__(self, k):
        try:
            object.__getattr__(self, k)
        except AttributeError:
            if k.startswith('r_'):
                return self[k[2:]]
            else:
                return self[k]
