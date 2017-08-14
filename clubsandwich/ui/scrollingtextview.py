import textwrap

from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.geom import Point, Size
from clubsandwich.ui import LabelView
from clubsandwich.ui.layout_options import LayoutOptions
from clubsandwich.ui.view import View


class ScrollingTextView(View):
  """
  :param int lines_to_display: How many lines to display at once (will not adjust the layout)
  :param int chars_per_line: Maximum amount of characters per line,  for text wrapping.

  See :py:class:`View` for the rest of the init arguments.
  """
  def __init__(self, lines_to_display, chars_per_line, *args, **kwargs):
    self.top_line_index = 0
    self.list_of_strings = []
    options = kwargs.get("layout_options")
    if not options:
        options = LayoutOptions().with_updates(left=2, right=2)
    self.label_view = LabelView(
        str(" "), align_horz='left', align_vert='top',
        layout_options=options)
    super().__init__(subviews=[self.label_view], *args, **kwargs)
    self.lines_to_display = lines_to_display
    self.chars_to_display = chars_per_line

  @property
  def can_become_first_responder(self):
    return True

  def add_lines(self, lines_string):
    unwrapped_lines = lines_string.splitlines(keepends=True)
    wrapped_lines = []
    for line in unwrapped_lines:
        wrapped_lines.extend(
            textwrap.wrap(line, width=self.chars_to_display)
        )

    self.list_of_strings.extend(wrapped_lines)
    lines_added = len(wrapped_lines)
    if self.top_line_index + self.lines_to_display <= len(self.list_of_strings) - lines_added:
        if lines_added > self.lines_to_display:
            focus_substract = lines_added
        else:
            focus_substract = self.lines_to_display - lines_added

        self.focus_on_line(len(self.list_of_strings) - focus_substract - 1)
    else:
        self._refocus()

  def focus_on_line(self, line_index):
    self.top_line_index = line_index if line_index >= 0 else 0
    self._refocus()

  def scroll_up(self):
    if self.top_line_index > 0:
        self.top_line_index -= 1
        self._refocus()

  def scroll_down(self):
    if self.top_line_index + self.lines_to_display < len(self.list_of_strings):
        self.top_line_index += 1
        self._refocus()

  def _refocus(self):
    new_view_lines = "\n".join(
        self.list_of_strings[self.top_line_index:self.top_line_index + self.lines_to_display]
    )
    self.label_view.text = new_view_lines

  @property
  def intrinsic_size(self):
    return self.label_view.intrinsic_size + Size(4, 0)  # add space for arrows

  def set_needs_layout(self, val=True):
    super().set_needs_layout(val)
    self.label_view.set_needs_layout(val)

  def did_become_first_responder(self):
    self.label_view.color_fg = '#000000'
    self.label_view.color_bg = '#ffffff'

  def did_resign_first_responder(self):
    self.label_view.color_fg = '#ffffff'
    self.label_view.color_bg = '#000000'

  def draw(self, ctx):
    color_fg = '#ffffff'
    color_bg = '#000000'
    if self.is_first_responder:
        color_fg = '#000000'
        color_bg = '#ffffff'
    ctx.color(color_fg)
    ctx.bkcolor(color_bg)
    ctx.print(Point(self.bounds.width, 2), '↑')
    ctx.print(Point(self.bounds.width, self.bounds.height), '↓')

  def terminal_read(self, val):
    if val == terminal.TK_UP:
        self.scroll_up()

    if val == terminal.TK_DOWN:
        self.scroll_down()
