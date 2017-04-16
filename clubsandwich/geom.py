from math import floor

class Point:
  __slots__ = ('x', 'y')

  def __init__(self, x=0, y=0):
    super().__init__()
    self.x = x
    self.y = y

  def __eq__(self, other):
    if not isinstance(other, Point):
        return False
    return self.x == other.x and self.y == other.y

  def __repr__(self):
    return 'Point({}, {})'.format(self.x, self.y)

  @property
  def floored(self):
    return self.__class__(floor(self.x), floor(self.y))

  def __add__(self, other):
    return self.__class__(self.x + other.x, self.y + other.y)

  def __mul__(self, other):
    if isinstance(other, Point):
      return self.__class__(self.x * other.x, self.y * other.y)
    else:
      return self.__class__(self.x * other, self.y * other)

  def __sub__(self, other):
    return self + (other * -1)

  def __truediv__(self, other):
    if isinstance(other, Point):
      return self.__class__(self.x / other.x, self.y / other.y)
    else:
      return self.__class__(self.x / other, self.y / other)


class Size(Point):
  def __init__(self, width=0, height=0):
    super().__init__(x=width, y=height)

  @property
  def point(self):
    return Point(self.width, self.height)

  @property
  def width(self):
    return self.x

  @width.setter
  def width(self, value):
    self.x = value

  @property
  def height(self):
    return self.y

  @height.setter
  def height(self, value):
    self.y = value

  def __repr__(self):
    return 'Size({}, {})'.format(self.width, self.height)


class Rect:
  __slots__ = ('origin', 'size')

  def __init__(self, origin=None, size=None):
    super().__init__()
    self.origin = origin or Point()
    self.size = size or Size()

  def __eq__(self, other):
    if not isinstance(other, Rect):
      return False
    return self.origin == other.origin and self.size == other.size

  def __repr__(self):
    return 'Rect({!r}, {!r})'.format(self.origin, self.size)

  @property
  def x(self):
    return self.origin.x

  @x.setter
  def x(self, new_value):
    self.origin = Point(new_value, self.y)

  @property
  def y(self):
    return self.origin.y

  @y.setter
  def y(self, new_value):
    self.origin = Point(self.x, new_value)

  @property
  def width(self):
    return self.size.width

  @width.setter
  def width(self, new_value):
    self.size = Size(new_value, self.height)

  @property
  def height(self):
    return self.size.height

  @height.setter
  def height(self, new_value):
    self.size = Size(self.width, new_value)

  @property  # no setter; it's not clear if it would change origin or size
  def x2(self):
    return self.origin.x + self.size.width - 1

  @property  # no setter; it's not clear if it would change origin or sizey
  def y2(self):
    return self.origin.y + self.size.height - 1

  ### handy iterators ###

  @property
  def points(self):
    for x in range(self.origin.x, self.origin.x + self.size.width):
      for y in range(self.origin.y, self.origin.y + self.size.height):
        yield Point(x, y)

  @property
  def points_top(self, corners=False):
    start = self.origin.x if corners else self.origin.x + 1
    end = self.origin.x + self.size.width if corners else self.origin.x + self.size.width - 1
    for x in range(start, end):
      yield Point(x, self.origin.y)

  @property
  def points_bottom(self, corners=False):
    start = self.origin.x if corners else self.origin.x + 1
    end = self.origin.x + self.size.width if corners else self.origin.x + self.size.width - 1
    for x in range(start, end):
      yield Point(x, self.origin.y + self.size.height - 1)

  @property
  def points_left(self, corners=False):
    start = self.origin.y if corners else self.origin.y + 1
    end = self.origin.y + self.size.height if corners else self.origin.y + self.size.height - 1
    for y in range(start, end):
      yield Point(self.origin.x, y)

  @property
  def points_right(self, corners=False):
    start = self.origin.y if corners else self.origin.y + 1
    end = self.origin.y + self.size.height if corners else self.origin.y + self.size.height - 1
    for y in range(start, end):
      yield Point(self.origin.x + self.size.width - 1, y)

  @property
  def points_corners(self):
    yield self.origin
    yield self.point_top_right
    yield self.point_bottom_right
    yield self.point_bottom_left

  ### individual points ###

  @property
  def center(self):
    return self.origin + self.size / 2

  @property
  def point_top_right(self):
    return Point(self.origin.x + self.size.width - 1, self.origin.y)
  
  @property
  def point_bottom_left(self):
    return Point(self.origin.x, self.origin.y + self.size.height - 1)

  @property
  def point_bottom_right(self):
    return self.origin + self.size - Point(1, 1)

  ### copying transforms ###

  @property
  def floored(self):
    return Rect(self.origin.floored, self.size.floored)

  def moved_by(self, delta):
    return Rect(self.origin + delta, self.size)

  def with_origin(self, new_origin):
    return Rect(new_origin, self.size)

  def with_size(self, new_size):
    return Rect(self.origin, new_size)

  def with_inset(self, inset):
    return Rect(self.origin + inset, self.size - inset * 2)
