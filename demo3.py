from bearlibterminal import terminal
from clubsandwich.blt.loop import BearLibTerminalEventLoop

i = 0
j = 0
class MyDemo(BearLibTerminalEventLoop):
    def terminal_update(self):
        global i
        global j
        terminal.put(j, 0, str(i))
        i = (i + 1) % 10
        j = (j + 1) % 11
        return True  # this is important!

MyDemo(ctrl_c_exits=False).run()