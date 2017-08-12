from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.geom import Point, Size
from clubsandwich.ui.layout_options import LayoutOptions
from clubsandwich.ui.view import View
from clubsandwich.ui import LabelView
import os


class ScrollingTextView(View):
    """
    :param int value: Initial value
    :param func callback: Called with updated values
    :param int|None min_value: Min value or ``None``
    :param int|None max_value: Max value or ``None``

    See :py:class:`View` for the rest of the init arguments.
    """

    def __init__(self, *args, **kwargs):
        self.top_line_index = 0
        self.list_of_strings = []
        options = kwargs.get("layout_options")
        if not options:
            options = LayoutOptions().with_updates(left=2, right=2)
        self.label_view = LabelView(
            str("Wat"), align_horz='left', align_vert='top',
            layout_options=options)
        super().__init__(subviews=[self.label_view], *args, **kwargs)
        self.height = self.label_view.intrinsic_size.height + 1

    @property
    def can_become_first_responder(self):
        return True

    def add_lines(self, lines_string):
        lines = lines_string.split("\n")
        self.list_of_strings.extend(lines)
        lines_added = len(lines)
        if self.top_line_index + self.height < self.top_line_index + lines_added:
            self.focus_on_line(self.height - lines_added)
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
        if self.top_line_index + self.height < len(self.list_of_strings):
            self.top_line_index += 1
            self._refocus()

    def _refocus(self):
        lines_we_should_show = self.height
        new_view_lines = "\n".join(self.list_of_strings[self.top_line_index:self.top_line_index + lines_we_should_show])
        print("Focused on lines {} to {}".format(self.top_line_index, self.top_line_index + lines_we_should_show))
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
        ctx.print(Point(self.bounds.width - 2, 0), '↑ ')
        ctx.print(Point(self.bounds.width - 2, self.bounds.height - 4), ' ↓')

    def terminal_read(self, val):
        if val == terminal.TK_UP:
            self.scroll_up()

        if val == terminal.TK_DOWN:
            self.scroll_down()
