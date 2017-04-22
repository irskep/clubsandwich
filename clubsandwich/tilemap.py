from .geom import Point


class Cell:
  def __init__(self):
    self.terrain = 0
    self.feature = None
    self.items = []


class TileMap:
  def __init__(self, size):
    self.size = size
    self.cells = [
      [Cell() for _ in range(size.height)] for _ in range(size.width)]

  def cell(self, point):
    return self.cells[point.x][point.y]

  def __get__(self, k):
    if isinstance(k, Point):
      return self.cell(k)
    return self.cells[k]