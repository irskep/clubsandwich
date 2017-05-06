from contextlib import contextmanager

from bearlibterminal import terminal as _terminal

from .nice_terminal import NiceTerminal
from .state import blt_state
from clubsandwich.geom import Point

class BearLibTerminalContext(NiceTerminal):
  """
  A class that acts like :py:attr:`clubsandwich.blt.nice_terminal.terminal`
  (you can use :py:class:`Point` and :py:class:`Rect` instead of separate
  ints), except:

    * It's a class, so you have to instantiate it
    * It includes a context manager, :py:meth:`translate`, that offsets all
      position-related calls.

  Example::

      from clubsandwich.blt.context import BearLibTerminalContext
      from clubsandwich.geom import Point

      ctx = BearLibTerminalContext()
      ctx.open()

      a = Point(10, 10)
      with ctx.translate(a):
        terminal.put(Point(0, 0), 'a')
        terminal.put(Point(1, 1), 'b')
      terminal.refresh()
      terminal.read()
      terminal.close()
  """

  def __init__(self):
    super().__init__()
    self.offset = Point(0, 0)
    self._crop_rect = None
    self._fg = blt_state.color
    self._bg = blt_state.bkcolor

  @contextmanager
  def translate(self, offset_delta):
    old_offset = self.offset
    self.offset = self.offset + offset_delta
    yield
    self.offset = old_offset

  @contextmanager
  def crop_before_send(self, crop_rect):
    old_rect = self._crop_rect
    self._crop_rect = crop_rect.moved_by(self.offset * -1)
    yield
    self._crop_rect = old_rect

  def color(self, c):
    self._fg = c
    return _terminal.color(c)

  def bkcolor(self, c):
    self._bg = c
    return _terminal.bkcolor(c)

  def clear_area(self, rect, *args):
    computed_rect = rect.moved_by(self.offset)
    if self._crop_rect and not self._crop_rect.intersects(computed_rect):
      return
    return super().clear_area(computed_rect, *args)

  def crop(self, rect, *args):
    computed_rect = rect.moved_by(self.offset)
    if self._crop_rect and not self._crop_rect.intersects(rect):
      return
    return super().crop(computed_rect, *args)

  def print(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().print(computed_point, *args)

  def printf(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().printf(computed_point, *args)

  def put(self, point, char):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().put(computed_point, char)

  def pick(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().pick(computed_point, *args)

  def pick_color(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().pick_color(computed_point, *args)

  def pick_bkcolor(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().pick_bkcolor(computed_point, *args)

  def put_ext(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().put_ext(computed_point, *args)

  def read_str(self, point, *args):
    computed_point = point + self.offset
    if self._crop_rect and not self._crop_rect.contains(computed_point):
      return
    return super().read_str(computed_point, *args)
  