"""
Simple data structures for working with points, sizes, and rects.
"""
from math import floor
from random import randint

class Point:
  """
  :param Real x:
  :param Real y:

  Represents a point in 2D space. Supports arithmetic operations with other
  points, and supports multiplication and division with numbers.

  BearLibTerminal requires ints for all coordinate values, so
  :py:attr:`~Point.floored` is your friend.

  .. py:attribute:: x

    X axis coordinate; may be any number

  .. py:attribute:: y

    Y coordinate; may be any number
  """
  __slots__ = ('x', 'y')

  def __init__(self, x=0, y=0):
    super().__init__()
    self.x = x
    self.y = y

  def __hash__(self):
    return hash(repr(self))

  def __repr__(self):
    return 'Point({}, {})'.format(self.x, self.y)

  @property
  def floored(self):
    """A copy of this point with ``math.floor()`` called on each coordinate."""
    return self.__class__(floor(self.x), floor(self.y))

  def path_L_to(self, target):
    p = self
    while p.x < target.x:
      p = p + Point(1, 0)
      yield p
    while p.x > target.x:
      p = p - Point(1, 0)
      yield p
    while p.y < target.y:
      p = p + Point(0, 1)
      yield p
    while p.y > target.y:
      p = p - Point(0, 1)
      yield p

  def manhattan_distance_to(self, target):
    return abs(self.x - target.x) + abs(self.y - target.y)

  @property
  def neighbors(self):
    yield self - Point(-1, 0)
    yield self - Point(0, -1)
    yield self - Point(1, 0)
    yield self - Point(0, 1)

  ### operators ###

  def __eq__(self, other):
    if not isinstance(other, Point):
        return False
    return self.x == other.x and self.y == other.y

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
  """
  :param Real width:
  :param Real height:

  Thin wrapper over :py:class:`Point` that forwards :py:attr:`~Point.x` to
  :py:attr:`width` and :py:attr:`~Point.y` to :py:attr:`height`.

  .. py:attribute:: width

    alias for :py:attr:`~Point.x`

  .. py:attribute:: height

    alias for :py:attr:`~Point.y`
  """

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
  """
  :param Point origin:
  :param Size size:

  Represents an rectangle in 2D space.

  BearLibTerminal requires ints for all coordinate values, so
  :py:attr:`~Rect.floored` is your friend.

  .. py:attribute:: origin

    Origin of the rectangle

  .. py:attribute:: size

    Size of the rectangle
  """
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
    """Forwarded from ``self.origin.x``"""
    return self.origin.x

  @x.setter
  def x(self, new_value):
    self.origin = Point(new_value, self.y)

  @property
  def y(self):
    """Forwarded from ``self.origin.y``"""
    return self.origin.y

  @y.setter
  def y(self, new_value):
    self.origin = Point(self.x, new_value)

  @property
  def width(self):
    """Forwarded from ``self.size.width``"""
    return self.size.width

  @width.setter
  def width(self, new_value):
    self.size = Size(new_value, self.height)

  @property
  def height(self):
    """Forwarded from ``self.size.height``"""
    return self.size.height

  @height.setter
  def height(self, new_value):
    self.size = Size(self.width, new_value)

  @property  # no setter; it's not clear if it would change origin or size
  def x2(self):
    """Max X value of this rect. Read-only."""
    return self.origin.x + self.size.width - 1

  @property  # no setter; it's not clear if it would change origin or sizey
  def y2(self):
    """Max Y value of this rect. Read-only."""
    return self.origin.y + self.size.height - 1

  ### handy iterators ###

  @property
  def points(self):
    """Iterator of all points in this rect"""
    for x in range(self.origin.x, self.origin.x + self.size.width):
      for y in range(self.origin.y, self.origin.y + self.size.height):
        yield Point(x, y)

  @property
  def points_top(self):
    """Iterator of all points along the top edge of this rect"""
    start = self.origin.x + 1
    end = self.origin.x + self.size.width - 1
    for x in range(start, end):
      yield Point(x, self.origin.y)

  @property
  def points_bottom(self):
    """Iterator of all points along the bottom edge of this rect"""
    start = self.origin.x + 1
    end = self.origin.x + self.size.width - 1
    for x in range(start, end):
      yield Point(x, self.origin.y + self.size.height - 1)

  @property
  def points_left(self):
    """Iterator of all points along the left edge of this rect"""
    start = self.origin.y + 1
    end = self.origin.y + self.size.height - 1
    for y in range(start, end):
      yield Point(self.origin.x, y)

  @property
  def points_right(self):
    """Iterator of all points along the right edge of this rect"""
    start = self.origin.y + 1
    end = self.origin.y + self.size.height - 1
    for y in range(start, end):
      yield Point(self.origin.x + self.size.width - 1, y)

  @property
  def points_corners(self):
    """Iterator of all four points in this rect's corners"""
    yield self.origin
    yield self.point_top_right
    yield self.point_bottom_right
    yield self.point_bottom_left

  ### individual points ###

  @property
  def center(self):
    """Point at the center of this rect"""
    return self.origin + self.size / 2

  @property
  def point_top_right(self):
    """Point at the top right corner of this rect"""
    return Point(self.origin.x + self.size.width - 1, self.origin.y)
  
  @property
  def point_bottom_left(self):
    """Point at the bottom left corner of this rect"""
    return Point(self.origin.x, self.origin.y + self.size.height - 1)

  @property
  def point_bottom_right(self):
    """Point at the bottom right corner of this rect"""
    return self.origin + self.size - Point(1, 1)

  ### copying transforms ###

  @property
  def floored(self):
    """A copy of this rect with the :py:attr:`Point.floored` origin/size
    copies"""
    return Rect(self.origin.floored, self.size.floored)

  def moved_by(self, delta):
    """
    :param Point delta:

    A copy of this rect with the origin moved by **delta**
    """
    return Rect(self.origin + delta, self.size)

  def with_origin(self, new_origin):
    """
    :param Point new_origin:

    A copy of this rect with the given origin
    """
    return Rect(new_origin, self.size)

  def with_size(self, new_size):
    """
    :param Point new_size:

    A copy of this rect with the given size
    """
    return Rect(self.origin, new_size)

  def with_inset(self, inset):
    """
    :param Point|Real inset:

    A copy of this rect inset by the given amount. If you pass a number, all
    sides will be inset by the same amount. If you pass a :py:class:`Point`
    or a :py:class:`Size`, the X and Y axes will be inset by the respective
    amounts specified in each coordinate.
    """
    if not isinstance(inset, Point):
      inset = Point(inset, inset)
    return Rect(self.origin + inset, self.size - inset * 2)

  ### random stuff ###

  def get_random_point(self):
    return Point(
      randint(self.origin.x, self.origin.x + self.size.width),
      randint(self.origin.y, self.origin.y + self.size.height))

  def get_random_rect(self, min_size=Size(1, 1)):
    if self.width <= min_size.width:
      return self
    if self.height <= min_size.height:
      return self
    width = randint(min_size.width, self.width)
    height = randint(min_size.height, self.height)
    x = self.origin.x + randint(0, self.size.width - width)
    y = self.origin.y + randint(0, self.size.height - height)
    if width == 0 or height == 0:
      raise ValueError((x, y, width, height, self))
    return Rect(Point(x, y), Size(width, height))
