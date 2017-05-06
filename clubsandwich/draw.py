"""
Assorted functions that draw shapes to the terminal. Right now it's just lines
and rectangles.
"""
from contextlib import contextmanager

from .blt.nice_terminal import terminal
from .geom import Point
from .blt.state import blt_state


LINE_STYLES = {
  'single':  {
    'T': '─',
    'B': '─',
    'L': '│',
    'R': '│',
    'TL': '┌',
    'TR': '┐',
    'BL': '└',
    'BR': '┘',
  },
  'double':  {
    'T': '═',
    'B': '═',
    'L': '║',
    'R': '║',
    'TL': '╔',
    'TR': '╗',
    'BL': '╚',
    'BR': '╝',
  },
}


def draw_line_horz(origin, length, ctx=terminal, style='single'):
  """
  :param Point origin:
  :param int length:
  :param BearLibTerminalContext ctx:
  :param str style: Either ``'single'`` or ``'double'``

  Draw a horizontal line.
  """
  char = LINE_STYLES[style]['T']
  for i in range(length):
    ctx.put(origin + Point(i, 0), char)


def draw_line_vert(origin, length, ctx=terminal, style='single'):
  """
  :param Point origin:
  :param int length:
  :param BearLibTerminalContext ctx:
  :param str style: Either ``'single'`` or ``'double'``

  Draw a vertical line.
  """
  char = LINE_STYLES[style]['L']
  for i in range(length):
    ctx.put(origin + Point(0, i), char)


def draw_rect(rect, ctx=terminal, style='single'):
  """
  :param Rect rect:
  :param BearLibTerminalContext ctx:
  :param str style: Either ``'single'`` or ``'double'``

  Draw a rectangle.
  """
  style = LINE_STYLES[style]

  for point in rect.points_top:
    ctx.put(point, style['T'])
  for point in rect.points_bottom:
    ctx.put(point, style['B'])
  for point in rect.points_left:
    ctx.put(point, style['L'])
  for point in rect.points_right:
    ctx.put(point, style['R'])
  ctx.put(rect.origin, style['TL'])
  ctx.put(rect.point_top_right, style['TR'])
  ctx.put(rect.point_bottom_left, style['BL'])
  ctx.put(rect.point_bottom_right, style['BR'])
