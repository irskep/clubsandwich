"""
Tilemap data structures for 2D grids
"""
from .geom import Point, Rect


class CellOutOfBoundsError(Exception):
  """You have tried to access a cell at a coordinates outside of the tilemap"""
  pass


class Cell:
  """
  One cell at a point in 2D space. You'll probably want to subclass this to add
  your own data.

  .. py:attribute:: point

    :py:class:`clubsandwich.geom.Point`

  .. py:attribute:: terrain

    Arbitrary value representing the type of terrain in this cell, if any

  .. py:attribute:: feature

    Arbitrary value representing the "feature" (exit, furniture...) on this
    cell, if any

  .. py:attribute:: items

    List of arbitrary values representing any items on this cell.

  .. py:attribute:: annotations

    Set of arbitrary values. Original use was to let a level generator give a
    hint to the draw function. For example if the generator places a
    rectangular room, it can mark cells as 'corner-top-left', 'wall-vert',
    etc.

  .. py:attribute:: debug_character

    Another slot for arbitrary debugging data. Intended use is to visually mark
    cells in a map.
  """
  def __init__(self, point):
    """
    :param clubsandwich.geom.Point point:
    """
    self.point = point
    self.terrain = 0
    self.feature = None
    self.items = []
    self.annotations = set()
    self.debug_character = None


class TileMap:
  """
  A collection of cells within a rectangular 2D area, with various convenience
  methods. You'll probably want to subclass this to add your own.

  .. py:attribute:: size

    :py:class:`clubsandwich.geom.Size`

  .. py:attribute:: points_of_interest

    Dict of arbitrary data. Intended use is for the level generator to pass
    data to game logic, for example to define mob positions.
  """
  def __init__(self, size, cell_class=Cell):
    """
    :param Size size:
    :param class cell_class: Class to use for cells. Instantiated with a single
                             argument, the point: ``cell_class(Point(x, y))``
    """
    self.size = size
    self.points_of_interest = {}
    self._cells = [
      [cell_class(Point(x, y)) for y in range(size.height)] for x in range(size.width)]

  def contains_point(self, point):
    """
    :param clubsandwich.geom.Point point:

    Returns ``True`` iff *point* is within this tilemap's bounds, otherwise
    ``False``.
    """
    return point.x >= 0 and point.y >= 0 and point.x < self.size.width and point.y < self.size.height

  def cell(self, point):
    """
    :param clubsandwich.geom.Point point:

    Returns the cell at the given point, or raises
    :py:class:`CellOutOfBoundsError`.

    As a shortcut, you can use indexing syntax instead of calling this method::

      cell = tilemap[Point(x, y)]
    """
    try:
      return self._cells[point.x][point.y]
    except IndexError:
      raise CellOutOfBoundsError("Cell index out of range: {!r}".format(point))

  @property
  def cells(self):
    """Iterator of all cells in this tilemap"""
    for point in Rect(Point(0, 0), self.size).points:
      yield self.cell(point)

  def __getitem__(self, k):
    if isinstance(k, Point):
      return self.cell(k)
    return self.cells[k]