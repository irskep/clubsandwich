"""
Exports a class to load ``.xp`` files and draw them to a BearLibTerminal
console.
"""

from clubsandwich.geom import Size, Rect, Point
from clubsandwich.xp_loader import load_xp_file
from clubsandwich.blt.nice_terminal import terminal as nice_terminal


TRANSPARENT_R = 255
TRANSPARENT_G = 0
TRANSPARENT_B = 255


def _read_color(cell, kr, kg, kb):
    return nice_terminal.color_from_argb(255, cell[kr], cell[kg], cell[kb])


def _read_color_transparency(cell, kr, kg, kb):
    if (cell[kr] == TRANSPARENT_R and
        cell[kg] == TRANSPARENT_G and
            cell[kb] == TRANSPARENT_B):
        return None
    else:
        return _read_color(cell, kr, kg, kb)


class REXPaintImage:
    """
    Loads REXPaint (``.xp``) images and draws them to a BearLibTerminal console.

    Note that while REXPaint lets you specify background colors for any layer,
    BearLibTerminal only supports it for layer 0. To work around this, the layer
    0 background colors are overwritten by non-transparent background colors of
    higher layers.

    :param str path: Path to a ``.xp`` file
    """

    def __init__(self, path):
        self._image = load_xp_file(path)
        self.size = Size(self._image['width'], self._image['height'])
        self.num_layers = self._image['layer_count']

        self._draw_calls_by_layer = []
        for layer_i, layer in enumerate(self._image['layer_data']):
            calls = []
            for x, col in enumerate(layer['cells']):
                for y, cell in enumerate(col):
                    fg = _read_color(cell, 'fore_r', 'fore_g', 'fore_b')
                    bg = self._read_bg_color(layer_i, x, y)
                    calls.append((Point(x, y), cell['keycode'], fg, bg))
            self._draw_calls_by_layer.append(calls)

    def _read_bg_color(self, layer_i, x, y):
        if layer_i > 0:
            return None
        c = None
        for i in range(self.num_layers):
            cell = self._image['layer_data'][i]['cells'][x][y]
            bg = _read_color_transparency(cell, 'back_r', 'back_g', 'back_b')
            c = bg or c
        return c

    def draw(self, point, layer=0, terminal=None, default_bg_color=None):
        """
        Draw the image at the given point. If *terminal* is provided, it should be
        a :py:class:`~clubsandwich.blt.context.BearLibTerminalContext`.

        :param clubsandwich.geom.Point point: origin
        :param int layer: Image layer to draw (default 0)
        :param terminal: Terminal to draw to
        """
        terminal = terminal or nice_terminal
        for call in self._draw_calls_by_layer[layer]:
            (p, value, fg, bg) = call
            terminal.color(fg)
            if bg is not None:
                terminal.bkcolor(bg)
            elif default_bg_color is not None:
                terminal.bkcolor(default_bg_color)
            terminal.put(point + p, value)
