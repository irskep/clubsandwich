from .view import View
from contextlib import contextmanager
from math import floor

from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.blt.state import blt_state
from clubsandwich.geom import Point, Rect, Size
from .view import View
from .layout_options import LayoutOptions


@contextmanager
def temporary_color(fg, bg):
  old_fg = blt_state.color
  old_bg = blt_state.bkcolor
  if fg:
    terminal.color(fg)
  if bg:
    terminal.bkcolor(bg)
  yield
  terminal.color(old_fg)
  terminal.bkcolor(old_bg)


class RectView(View):
  def __init__(self, color_fg='#aaaaaa', color_bg='#000000', *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.color_fg = color_fg
    self.color_bg = color_bg

  def draw(self, ctx):
    with temporary_color(self.color_fg, self.color_bg):
      ctx.clear_area(self.bounds)
      for point in self.bounds.points_top:
        ctx.put(point, '─')
      for point in self.bounds.points_bottom:
        ctx.put(point, '─')
      for point in self.bounds.points_left:
        ctx.put(point, '│')
      for point in self.bounds.points_right:
        ctx.put(point, '│')
      ctx.put(self.bounds.origin, '┌')
      ctx.put(self.bounds.point_top_right, '┐')
      ctx.put(self.bounds.point_bottom_left, '└')
      ctx.put(self.bounds.point_bottom_right, '┘')


class WindowView(RectView):
  def __init__(self, title=None, *args, subviews=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.title_view = LabelView(title, layout_options=LayoutOptions.row_top(1))
    self.content_view = View(
      subviews=subviews,
      layout_options=LayoutOptions(top=1, right=1, bottom=1, left=1))
    self.add_subviews([self.title_view, self.content_view])


class LabelView(View):
  def __init__(
      self, text, color_fg='#ffffff', color_bg=None,
      align_horz='center', align_vert='center',
      *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.align_horz = align_horz
    self.align_vert = align_vert
    self.text = text
    self.color_fg = color_fg
    self.color_bg = color_bg

  @property
  def intrinsic_size(self):
    height = 0
    width = 0
    for line in self.text.splitlines():
      height += 1
      width = max(width, len(line))
    return Size(width, height)

  def draw(self, ctx):
    with temporary_color(self.color_fg, self.color_bg):
      x = 0
      if self.align_horz == 'center':
        x = self.bounds.width / 2 - self.intrinsic_size.width / 2
      elif self.align_horz == 'right':
        x = self.bounds.width - self.intrinsic_size.width

      y = 0
      if self.align_vert == 'center':
        y = self.bounds.height / 2 - self.intrinsic_size.height / 2
      elif self.align_vert == 'right':
        y = self.bounds.height - self.intrinsic_size.height

      ctx.print(Point(x, y).floored, self.text)

  def debug_string(self):
    return super().debug_string() + ' ' + repr(self.text)


class ButtonView(View):
  def __init__(
      self, text, callback, align_horz='center', align_vert='center',
      *args, **kwargs):
    self.label_view = LabelView(text, align_horz=align_horz, align_vert=align_vert)
    super().__init__(subviews=[self.label_view], *args, **kwargs)
    self.callback = callback

  def set_needs_layout(self, val):
    super().set_needs_layout(val)
    self.label_view.set_needs_layout(val)

  def did_become_first_responder(self):
      self.label_view.color_fg = '#000000'
      self.label_view.color_bg = '#ffffff'

  def did_resign_first_responder(self):
      self.label_view.color_fg = '#ffffff'
      self.label_view.color_bg = '#000000'

  @property
  def text(self):
    return self.label_view.text

  @text.setter
  def text(self, new_value):
    self.label_view.text = new_value

  @property
  def intrinsic_size(self):
    return self.label_view.intrinsic_size

  def layout_subviews(self):
    super().layout_subviews()
    self.label_view.frame = self.bounds

  @property
  def can_did_become_first_responder(self):
    return True

  def terminal_read(self, val):
    if val == terminal.TK_ENTER:
      self.callback()
      return True


class CyclingButtonView(ButtonView):
  """
  Button which, when activated, chooses the "next" value in the given list,
  calls its ``callback`` function with it (``callback(new_value)``), and
  updates its text to the new value.

  All values must be strings. If this bothers you, pull requests are welcome.
  """
  def __init__(self, options, initial_value, callback, *args, **kwargs):
    self.options = options
    self._inner_callback = callback
    super().__init__(initial_value, self._call_inner_callback, *args, **kwargs)

  def _call_inner_callback(self):
    i = self.options.index(self.text)
    new_value = self.options[(i + 1) % len(self.options)]
    self.text = new_value
    self._inner_callback(new_value)