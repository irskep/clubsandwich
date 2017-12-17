from bearlibterminal import terminal
from clubsandwich.blt.loop import BearLibTerminalEventLoop

i = 0
j = 0


class MyDemo(BearLibTerminalEventLoop):
    def __init__(self):
        super().__init__()
        self.should_exit = False

    def terminal_init(self):
        terminal.print(0, 1, "Cmd+Q/Alt+F4/whatever to quit")

    def terminal_read(self, val):
        self.should_exit = val == terminal.TK_CLOSE

    def terminal_update(self):
        global i
        global j
        terminal.put(j, 0, str(i))
        i = (i + 1) % 10
        j = (j + 1) % 11
        return not self.should_exit


MyDemo().run()
