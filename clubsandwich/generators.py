from math import floor
from random import randrange, choice

from .blt.nice_terminal import terminal
from .geom import Point, Rect, Size
from .draw import draw_rect


class BSPNode:
  def __init__(self, rect, is_horz=True, value=None, level=0):
    self.rect = rect
    self.level = level
    self.is_horz = is_horz
    self.value = value
    self.child_a = None
    self.child_b = None
    self.data = {}  # put whatever you want in here

  def get_size_coord(self, size):
    if self.is_horz:
      return size.width
    else:
      return size.height

  def get_next_rect(self, is_a):
    if self.is_horz:
      if is_a:
        return Rect(self.rect.origin, Size(self.value, self.rect.height))
      else:
        return Rect(
          self.rect.origin + Point(self.value + 1, 0),
          Size(self.rect.width - self.value - 1, self.rect.height))
    else:
      if is_a:
        return Rect(self.rect.origin, Size(self.rect.width, self.value))
      else:
        return Rect(
          self.rect.origin + Point(0, self.value + 1),
          Size(self.rect.width , self.rect.height - self.value - 1))

  def __repr__(self):
    return 'BSPNode(is_horz={}, value={})'.format(self.is_horz, self.value)

  @property
  def leaves(self):
    if self.child_a and self.child_b:
      yield from self.child_a.leaves
      yield from self.child_b.leaves
    else:
      yield self

  @property
  def sibling_pairs(self):
    if not self.child_a or not self.child_b:
      return
    yield from self.child_a.sibling_pairs
    yield from self.child_b.sibling_pairs
    yield (self.child_a, self.child_b)

  @property
  def leftmost_leaf(self):
    if self.child_a:
      return self.child_a.leftmost_leaf
    else:
      return self

  @property
  def rightmost_leaf(self):
    if self.child_b:
      return self.child_b.leftmost_leaf
    else:
      return self

  @property
  def random_leaf(self):
    if self.child_a or self.child_b:
      return choice((self.child_a, self.child_b)).random_leaf
    else:
      return self


DEFAULT_RANDRANGE_FUNC = lambda _, a, b: randrange(a, b)
class RandomBSPTree:
  def __init__(self, size, min_leaf_size, randrange_func=DEFAULT_RANDRANGE_FUNC):
    self.randrange_func = randrange_func
    self.min_leaf_size = min_leaf_size
    self.root = BSPNode(Rect(Point(0, 0), size))
    self.subdivide(self.root)

  def subdivide(self, node, iterations_left=8):
    if iterations_left < 1:
      return
    if self.add_children(node):
      self.subdivide(node.child_a, iterations_left=iterations_left - 1)
      self.subdivide(node.child_b, iterations_left=iterations_left - 1)

  def add_children(self, node):
    a = self.min_leaf_size
    b = node.get_size_coord(node.rect.size) - self.min_leaf_size * 2 - 1
    if b - a < 1:
      return False
    node.value = self.randrange_func(node.level, a, b)
    node.child_a = BSPNode(node.get_next_rect(True), not node.is_horz, level=node.level+1)
    node.child_b = BSPNode(node.get_next_rect(False), not node.is_horz, level=node.level+1)
    return True

  def draw(self, n=None, color_so_far='#f'):
    if n is None:
      n = self.root
    if n.child_a or n.child_b:
      if n.child_a:
        self.draw(n.child_a, color_so_far + 'f')
      if n.child_b:
        self.draw(n.child_b, color_so_far + '0')
      return
    color = color_so_far + '0' * (7 - len(color_so_far))
    terminal.color(color)
    draw_rect(n.rect)
    terminal.print(n.rect.origin, color)
    terminal.bkcolor('#000000')
