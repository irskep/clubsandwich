"""
Functions related to line of sight calculations
"""
from clubsandwich.geom import Point

MULT = [
  [1,  0,  0, -1, -1,  0,  0,  1],
  [0,  1, -1,  0,  0, -1,  1,  0],
  [0,  1,  1,  0,  0, -1, -1,  0],
  [1,  0,  0,  1, -1,  0,  0, -1],
]
def get_visible_points(vantage_point, get_allows_light, max_distance=30):
  """
  :param :py:class:`clubsandwich.geom.Point` vantage_point:
  :param function get_allows_light: ``get_allows_light(point) -> bool``
  :param int max_distance:

  Returns a set of all points visible from the given vantage point.

  Adapted from `this RogueBasin article <http://www.roguebasin.com/index.php?title=Python_shadowcasting_implementation>`_.
  """
  los_cache = set()
  for region in range(8):
    _cast_light(
      los_cache, get_allows_light,
      vantage_point.x, vantage_point.y, 1, 1.0, 0.0, max_distance,
      MULT[0][region], MULT[1][region],
      MULT[2][region], MULT[3][region])
  return los_cache


def _cast_light(los_cache, get_allows_light, cx, cy, row, start, end, radius, xx, xy, yx, yy):
  if start < end:
    return

  radius_squared = radius*radius

  for j in range(row, radius+1):
    dx, dy = -j-1, -j
    blocked = False
    while dx <= 0:
      dx += 1
      # Translate the dx, dy coordinates into map coordinates:
      X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
      point = Point(X, Y)
      # l_slope and r_slope store the slopes of the left and right
      # extremities of the square we're considering:
      l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
      if start < r_slope:
        continue
      elif end > l_slope:
        break
      else:
        # Our light beam is touching this square; light it:
        if dx*dx + dy*dy < radius_squared:
          los_cache.add(point)
        if blocked:
          # we're scanning a row of blocked squares:
          if not get_allows_light(point):
            new_start = r_slope
            continue
          else:
            blocked = False
            start = new_start
        else:
          if not get_allows_light(point) and j < radius:
            # This is a blocking square, start a child scan:
            blocked = True
            _cast_light(
              los_cache, get_allows_light,
              cx, cy, j+1, start, l_slope,
              radius, xx, xy, yx, yy)
            new_start = r_slope
    # Row is scanned; do next row unless last square was blocked:
    if blocked:
        break
