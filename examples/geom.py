"""
Demonstrates the ``nice_terminal`` and ``geom`` modules.
"""

from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.geom import Point

terminal.open()

a = Point(10, 10)
b = a + Point(1, 1)
terminal.put(a, 'a')
terminal.put(b, 'b')
terminal.refresh()
terminal.read()
terminal.close()