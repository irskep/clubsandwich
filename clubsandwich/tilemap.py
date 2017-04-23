from .geom import Point, Rect


class CellOutOfBoundsError(Exception):
  pass


class Cell:
  def __init__(self, point):
    self.point = point
    self.terrain = 0
    self.feature = None
    self.items = []
    self.annotations = set()
    self.debug_character = None


class TileMap:
  def __init__(self, size, cell_class=Cell):
    self.size = size
    self.points_of_interest = {}
    self._cells = [
      [cell_class(Point(x, y)) for y in range(size.height)] for x in range(size.width)]

  def contains_point(self, point):
    return point.x >= 0 and point.y >= 0 and point.x < self.size.width and point.y < self.size.height

  def cell(self, point):
    try:
      return self._cells[point.x][point.y]
    except IndexError:
      raise CellOutOfBoundsError("Cell index out of range: {!r}".format(point))

  @property
  def cells(self):
    for point in Rect(Point(0, 0), self.size).points:
      yield self.cell(point)

  def __get__(self, k):
    if isinstance(k, Point):
      return self.cell(k)
    return self.cells[k]