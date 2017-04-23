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
  char = LINE_STYLES[style]['T']
  for i in range(length):
    ctx.put(origin + Point(i, 0), char)


def draw_line_vert(origin, length, ctx=terminal, style='single'):
  char = LINE_STYLES[style]['L']
  for i in range(length):
    ctx.put(origin + Point(0, i), char)


def draw_rect(rect, style='single', ctx=terminal):
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
