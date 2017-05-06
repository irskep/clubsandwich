"""
Level generator utilities.
"""

import weakref
from math import floor
from random import randrange, choice

from .blt.nice_terminal import terminal
from .geom import Point, Rect, Size
from .draw import draw_rect


class BSPNode:
  """
  Node in a binary space partitioning tree

  .. py:attribute:: rect

    :py:class:`Rect` represented by this node

  .. py:attribute:: is_horz

    ``True`` iff this node is divided down its Y axis; ``False`` otherwise

  .. py:attribute:: value

    Int representing split point between the two children of this node. So
    if this is a horizontal node and the width is 10, the value could be 6,
    with the left node taking up 6 cells and the right taking up 4.

  .. py:attribute:: child_a

    :py:class:`BSPNode` either on the left (horizontal) or on top (vertical).

  .. py:attribute:: child_b

    :py:class:`BSPNode` either on the right (horizontal) or on bottom (vertical).

  .. py:attribute:: level

    How many levels of parents does this node have?

  .. py:attribute:: data

    Dict of arbitrary data for your game's use.
  """

  def __init__(self, rect, is_horz=True, value=None, level=0):
    """
    :param Rect rect:
    :param bool is_horz:
    :param int|None value:
    :param int level:
    """
    self.parent_weakref = lambda: None
    self.rect = rect
    self.level = level
    self.is_horz = is_horz
    self.value = value
    self.child_a = None
    self.child_b = None
    self.data = {}  # put whatever you want in here

  @property
  def max_value(self):
    """Max value of :py:attr:`BSPNode.value`"""
    if self.is_horz:
      return self.rect.size.width - 1
    else:
      return self.rect.size.height - 1

  def _get_next_rect(self, is_a):
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

  @property
  def rect_a(self):
    """Assuming :py:attr:`BSPNode.value` has already been set, return the
    :py:class:`Rect` of child A"""
    return self._get_next_rect(True)

  @property
  def rect_b(self):
    """Assuming :py:attr:`BSPNode.value` has already been set, return the
    :py:class:`Rect` of child B"""
    return self._get_next_rect(False)

  def get_node_at_path(self, spec=''):
    """
    Given a string containing only the characters ``'a'`` and ``'b'``, return
    the node matching the given branches. For example, in a tree with 4
    leaves, ``root.get_node_at_path('aa')`` would return the left/top-most
    leaf.
    """
    if spec:
      if spec[0] == 'a':
        return self.child_a.get_node_at_path(spec[1:])
      elif spec[0] == 'b':
        return self.child_b.get_node_at_path(spec[1:])
      else:
        raise ValueError("Invalid character: {}".format(spec[0]))
    else:
      return self

  def __repr__(self):
    return 'BSPNode(is_horz={}, value={})'.format(self.is_horz, self.value)

  @property
  def leaves(self):
    """Iterator of all leaves, left/top-to-right/bottom"""
    if self.child_a and self.child_b:
      yield from self.child_a.leaves
      yield from self.child_b.leaves
    else:
      yield self

  @property
  def sibling_pairs(self):
    """Iterator of all pairs of siblings"""
    if not self.child_a or not self.child_b:
      return
    yield from self.child_a.sibling_pairs
    yield from self.child_b.sibling_pairs
    yield (self.child_a, self.child_b)

  @property
  def leftmost_leaf(self):
    """The left/top-most leaf in the tree"""
    if self.child_a:
      return self.child_a.leftmost_leaf
    else:
      return self

  @property
  def rightmost_leaf(self):
    """The right/bottom-most leaf in the tree"""
    if self.child_b:
      return self.child_b.leftmost_leaf
    else:
      return self

  def random_leaf(self):
    """Returns a random leaf"""
    if self.child_a or self.child_b:
      return choice((self.child_a, self.child_b)).random_leaf
    else:
      return self

  @property
  def ancestors(self):
    """Iterator of ``self`` and all parents, starting with first parent"""
    yield self
    parent = self.parent_weakref()
    if parent:
      yield from parent.ancestors


DEFAULT_RANDRANGE_FUNC = lambda _, a, b: randrange(a, b)
class RandomBSPTree:
  """
  A randomly generated BSP tree. Pass a dungeon size and minimum leaf size.
  After initialization, the root's leaves represent non-overlapping rectangles
  that completely fill the space.

  .. py:attribute:: root

    :py:class:`BSPNode` root of all children
  """

  def __init__(self, size, min_leaf_size, randrange_func=DEFAULT_RANDRANGE_FUNC):
    """
    :param Size size:
    :param int min_leaf_size: Minimum size of leaf nodes on both axes
    :param function randrange_func: A function ``fn(level, min_size, max_size)``
                                    that returns the ``value`` (see
                                    :py:class:`BSPnode`) of the node at the
                                    given level of recursion. Defaults to
                                    ``randrange()``, but you can use this to
                                    de-randomize specific splits.
    """
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
    b = node.max_value - self.min_leaf_size * 2
    if b - a < 1:
      return False
    node.value = self.randrange_func(node.level, a, b)
    node.child_a = BSPNode(node.rect_a, not node.is_horz, level=node.level+1)
    node.child_a.parent_weakref = weakref.ref(node)
    node.child_b = BSPNode(node.rect_b, not node.is_horz, level=node.level+1)
    node.child_b.parent_weakref = weakref.ref(node)
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
