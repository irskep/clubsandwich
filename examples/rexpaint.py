"""
Demonstrate loading and displaying of REXPaint .xp files.
"""

import pathlib

from clubsandwich.geom import Point
from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.blt.rexpaint_image import REXPaintImage

examples_dir = pathlib.Path(__file__).parent

terminal.open()

# Our example .xp file does not use codepage 437 keycodes, so don't tell
# BearLibTerminal to do that mapping.
terminal.set("""
font: {}, size=10x10;
window.size=40x40;
input.filter=[keyboard, mouse];
""".format(str(examples_dir / 'assets' / 'cp437_10x10.png')))

image = REXPaintImage(str(examples_dir / 'assets' / 'xptest.xp'))
image.draw(Point(0, 0), layer=0)
image.draw(Point(0, 10), layer=1)
for i in range(image.num_layers):
  terminal.layer(i)
  image.draw(Point(15, 15), layer=i)

terminal.refresh()

while True:
  val = terminal.read()
  if val == terminal.TK_CLOSE:
    break
  elif val == terminal.TK_MOUSE_MOVE:
    print(terminal.pick(terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y)))
terminal.close()
