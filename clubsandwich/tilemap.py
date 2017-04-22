from .geom import Point, Rect


class Cell:
  def __init__(self, point):
    self.point = point
    self.terrain = 0
    self.feature = None
    self.items = []
    self.annotations = set()


class TileMap:
  def __init__(self, size):
    self.size = size
    self._cells = [
      [Cell(Point(x, y)) for y in range(size.height)] for x in range(size.width)]

  def cell(self, point):
    return self._cells[point.x][point.y]

  @property
  def cells(self):
    for point in Rect(Point(0, 0), self.size).points:
      yield self.cell(point)

  def __get__(self, k):
    if isinstance(k, Point):
      return self.cell(k)
    return self.cells[k]