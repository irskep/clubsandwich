from math import floor

from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.blt.state import blt_state
from clubsandwich.geom import Point, Rect, Size
from clubsandwich.draw import draw_rect
from .view import View
from .layout_options import LayoutOptions


class RectView(View):
    """
    :param str color_fg: Foreground color
    :param str color_bg: Background color (only applies on terminal layer zero)
    :param bool fill: If ``True`` (default ``False``), fill not just the border
                      but also the middle.
    :param str style: ``'single'`` or ``'double'``

    See :py:class:`View` for the rest of the init arguments.

    Draws a rectangle in its bounds using ASCII line art.

    ::

      ┌───────┐
      │       │
      │       │
      └───────┘
    """

    def __init__(
            self, color_fg='#aaaaaa', color_bg='#000000', fill=False,
            style='single', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.fill = fill
        self.style = style

    def draw(self, ctx):
        ctx.color(self.color_fg)
        ctx.bkcolor(self.color_bg)
        if self.fill or self.clear:
            ctx.clear_area(self.bounds)
        draw_rect(self.bounds, style=self.style, ctx=ctx)


class WindowView(RectView):
    """
    :param str title: Window title

    See :py:class:`RectView` for the rest of the init arguments.

    A rectangle with a centered label on the top containing the text *title*.
    All given subviews are put in an inner view that's inset by 1 cell so the
    subview don't overlap the border.

    ::

      ┌───Hello!───┐
      │            │
      │            │
      └────────────┘
    """

    def __init__(self, title=None, *args, subviews=None, **kwargs):
        super().__init__(*args, fill=True, **kwargs)
        self.title_view = LabelView(
            title, layout_options=LayoutOptions.row_top(1))
        self.content_view = View(
            subviews=subviews,
            layout_options=LayoutOptions(top=1, right=1, bottom=1, left=1))
        self.add_subviews([self.title_view, self.content_view])


class LabelView(View):
    """
    Draws the given string inside its bounds. Multi-line strings work fine.

    :param str text: Text to draw
    :param str color_fg: Foreground color
    :param str color_bg: Background color (only applies on terminal layer zero)
    :param 'center'|'left'|'right' align_horz: Horizontal alignment
    :param 'center'|'top'|'bottom' align_vert: Vertical alignment
    :param Point|None size: Override intrinsic size. Size is hard to compute; see
                            `the BearLibTerminal docs`_.
                            .. _the BearLibTerminal docs: http://foo.wyrd.name/en:bearlibterminal:reference#measure

    See :py:class:`View` for the rest of the init arguments.
    """

    def __init__(
            self, text, color_fg='#ffffff', color_bg='#000000',
            align_horz='center', align_vert='center',
            size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.align_horz = align_horz
        self.align_vert = align_vert
        self.text = text
        self.color_fg = color_fg
        self.color_bg = color_bg
        self._explicit_size = size

    @property
    def intrinsic_size(self):
        if self._explicit_size:
            return self._explicit_size
        height = 0
        width = 0
        for line in self.text.splitlines():
            height += 1
            width = max(width, len(line))
        return Size(width, height)

    def draw(self, ctx):
        ctx.color(self.color_fg)
        ctx.bkcolor(self.color_bg or '#000000')
        if self.clear:
            ctx.clear_area(self.bounds)
        x = 0
        if self.align_horz == 'center':
            x = self.bounds.width / 2 - self.intrinsic_size.width / 2
        elif self.align_horz == 'right':
            x = self.bounds.width - self.intrinsic_size.width

        y = 0
        if self.align_vert == 'center':
            y = self.bounds.height / 2 - self.intrinsic_size.height / 2
        elif self.align_vert == 'bottom':
            y = self.bounds.height - self.intrinsic_size.height

        ctx.print(Point(x, y).floored, self.text)

    @property
    def debug_string(self):
        return super().debug_string + ' ' + repr(self.text)


class ButtonView(View):
    """
    :param str text: Button title
    :param func callback: Function to call when button is activated. Takes no
                          arguments.
    :param str align_horz: Horizontal alignment. See :py:class:`LabelView`.
    :param str align_vert: Vertical alignment. See :py:class:`LabelView`.
    :param str color_fg: Foreground color of the button. When it is active,
                         this becomes the background color.
    :param str color_bg: Background color of the button. When it is active, this
                         becomes the foreground color. (Only works at terminal
                         layer 0.)
    :param Point|None size: Override intrinsic size of the label. Size is
                            hard to compute; see `the BearLibTerminal docs`_.
                            .. _the BearLibTerminal docs: http://foo.wyrd.name/en:bearlibterminal:reference#measure

    See :py:class:`View` for the rest of the init arguments.

    Contains a label. Can be first responder. When a button is the first
    responder:

    * The label is drawn black-on-white instead of white-on-black
    * Pressing the Enter key calls *callback*
    """

    def __init__(
            self, text, callback, align_horz='center', align_vert='center',
            color_fg='#ffffff', color_bg='#000000', size=None, *args, **kwargs):
        self.label_view = LabelView(
            text, align_horz=align_horz, align_vert=align_vert, size=size,
            color_fg=color_fg, color_bg=color_bg)
        super().__init__(subviews=[self.label_view], *args, **kwargs)

        self.color_fg = color_fg
        self.color_bg = color_bg
        self.callback = callback

    def set_needs_layout(self, val):
        super().set_needs_layout(val)
        self.label_view.set_needs_layout(val)

    def did_become_first_responder(self):
        self.label_view.color_fg = self.color_bg
        self.label_view.color_bg = self.color_fg

    def did_resign_first_responder(self):
        self.label_view.color_fg = self.color_fg
        self.label_view.color_bg = self.color_bg

    def draw(self, ctx):
        if self.clear:
            ctx.bkcolor(self.color_bg)
            ctx.clear_area(self.bounds)

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
    def can_become_first_responder(self):
        return True

    def terminal_read(self, val):
        if val == terminal.TK_ENTER:
            self.callback()
            return True


class IntStepperView(View):
    """
    :param int value: Initial value
    :param func callback: Called with updated values
    :param int|None min_value: Min value or ``None``
    :param int|None max_value: Max value or ``None``

    See :py:class:`View` for the rest of the init arguments.
    """

    def __init__(
            self, value, callback, min_value=None, max_value=None, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        self.label_view = LabelView(
            str(value), align_horz='left', align_vert='top',
            layout_options=LayoutOptions().with_updates(left=2, right=2))
        self.value = value
        super().__init__(subviews=[self.label_view], *args, **kwargs)
        self.callback = callback

    @property
    def can_become_first_responder(self):
        return True

    @property
    def value(self):
        return int(self.label_view.text)

    @value.setter
    def value(self, new_value):
        self.label_view.text = str(new_value)
        if self.superview:
            self.superview.set_needs_layout()

    @property
    def intrinsic_size(self):
        # add space for arrows
        return self.label_view.intrinsic_size + Size(4, 0)

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
        ctx.print(Point(0, 0), '← ')
        ctx.print(Point(self.bounds.width - 2, 0), ' →')

    def terminal_read(self, val):
        if val == terminal.TK_LEFT and (self.min_value is None or self.value > self.min_value):
            self.value -= 1
            self.callback(self.value)
            return True

        if val == terminal.TK_RIGHT and (self.max_value is None or self.value < self.max_value):
            self.value += 1
            self.callback(self.value)
            return True


class CyclingButtonView(ButtonView):
    """
    :param list options: List of options, which must be strings
    :param str initial_value: Item from *options* to display first
    :param func callback: Function taking one argument, the option that is now
                          selected

    Button which, when activated, chooses the "next" value in the given list,
    calls ``callback(new_value)``, and updates its text to the new value.

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
