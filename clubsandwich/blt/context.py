from contextlib import contextmanager
from .nice_terminal import NiceTerminal
from clubsandwich.geom import Point

class BearLibTerminalContext(NiceTerminal):
  """
  Like ``NiceTerminal``, but you can use ``translate()`` to offset all
  calls that take a position or rect.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.offset = Point(0, 0)

  @contextmanager
  def translate(self, offset_delta):
    old_offset = self.offset
    self.offset = self.offset + offset_delta
    yield
    self.offset = old_offset

  def clear_area(self, rect, *args):
    return super().clear_area(rect.moved_by(self.offset), *args)

  def crop(self, rect, *args):
    return super().crop(rect.moved_by(self.offset), *args)

  def print(self, point, *args):
    return super().print(point + self.offset, *args)

  def printf(self, point, *args):
    return super().printf(point + self.offset, *args)

  def put(self, point, *args):
    return super().put(point + self.offset, *args)

  def pick(self, point, *args):
    return super().pick(point + self.offset, *args)

  def pick_color(self, point, *args):
    return super().pick_color(point + self.offset, *args)

  def pick_bkcolor(self, point, *args):
    return super().pick_bkcolor(point + self.offset, *args)

  def put_ext(self, point, *args):
    return super().put_ext(point + self.offset, *args)

  def read_str(self, point, *args):
    return super().read_str(point + self.offset, *args)
  