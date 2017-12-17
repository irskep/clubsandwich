"""
Demonstrates BearLibTerminalContext (more convenient rendering) and blt_state
"""
from clubsandwich.blt.state import blt_state
from clubsandwich.blt.context import BearLibTerminalContext
from clubsandwich.geom import Rect, Size, Point

terminal = BearLibTerminalContext()

terminal.open()
terminal.bkcolor('#ff0000')
# move frame of reference to middle of screen
with terminal.translate((Point(blt_state.width, blt_state.height) / 2).floored):
    terminal.clear_area(Rect(Point(-1, -1), Size(3, 2)))
terminal.refresh()
# less verbose than terminal.state(terminal.TK_ESCAPE)!
while not blt_state.escape:
    terminal.read()
terminal.close()
