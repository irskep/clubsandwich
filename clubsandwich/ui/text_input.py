from time import time

from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.blt.state import blt_state
from clubsandwich.geom import Size, Point
from .view import View


class SingleLineTextInputView(View):
  """
  :param func callback: ``callback(text)``. Called when focus changes.
  :param string color_unselected_fg:
  :param string color_unselected_bg:
  :param string color_selected_fg:
  :param string color_selected_bg:

  See :py:class:`View` for the rest of the constructor args.

  Simple text input.
  """
  def __init__(
      self,
      callback, initial_value="",
      color_unselected_fg='#ffffff',
      color_unselected_bg=None,
      color_selected_fg='#ffff00',
      color_selected_bg=None,
      *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.text = initial_value
    self.callback = callback
    self.color_unselected_fg = color_unselected_fg
    self.color_unselected_bg = color_unselected_bg
    self.color_selected_fg = color_selected_fg
    self.color_selected_bg = color_selected_bg

  @property
  def intrinsic_size(self):
    return Size(len(self.text) + 1, 1)

  def draw(self, ctx):
    color_fg = self.color_selected_fg if self.is_first_responder else self.color_unselected_fg
    color_bg = self.color_selected_bg if self.is_first_responder else self.color_unselected_bg
    ctx.color(self.color_fg)
    ctx.bkcolor(self.color_bg)
    ctx.print(Point(0, 0), self.text)

    text_len = len(self.text)
    if self.bounds.width > text_len:
      ctx.print(Point(text_len, 0), '_' * (self.bounds.width - text_len))

    if self.is_first_responder and int(time() * 1.2) % 2 == 0:
      ctx.put(Point(text_len, 0), '▒')

  def debug_string(self):
    return super().debug_string() + ' ' + repr(self.text)

  def did_resign_first_responder(self):
    super().did_resign_first_responder()
    self.set_needs_layout()

  @property
  def can_become_first_responder(self):
    return True

  def _update_text(self, val):
    self.text = val
    self.superview.set_needs_layout()

  def terminal_read(self, val):
    if val == terminal.TK_ENTER:
      self.callback(self.text)
      self.first_responder_container_view.find_next_responder()
      return True
    if val == terminal.TK_TAB:
      self.callback(self.text)
      return False
    elif val == terminal.TK_BACKSPACE:
      if self.text:
        self._update_text(self.text[:-1])
        return True
    elif terminal.check(terminal.TK_WCHAR):
      self._update_text(self.text + chr(blt_state.wchar))
      return True
      