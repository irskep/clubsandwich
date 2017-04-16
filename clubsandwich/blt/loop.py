#!/usr/bin/env python
import asyncio
from bearlibterminal import terminal
from .state import blt_state


class BearLibTerminalEventLoop:
    """
    Simple wrapper around BearLibTerminal and asyncio.

    Subclass terminal_init(), terminal_read(), and terminal_update().
    Instantiate your class and call its run() method.
    """

    def __init__(self, fps=72):
        super().__init__()
        self.fps = fps

    def terminal_init(self):
        """
        Terminal has just been opened. You should configure it with 
        terminal.set().
        """
        pass

    def terminal_read(self, char):
        """
        Handle input here
        """
        pass

    def terminal_update(self):
        """
        Update the view. Fires once per frame regardless of whether there
        was any input.
        """
        return True

    def run(self):
        terminal.open()
        self.terminal_init()
        terminal.refresh()

        try:
            asyncio_loop = asyncio.get_event_loop()
            asyncio_loop.run_until_complete(self.loop_until_terminal_exits())
        except KeyboardInterrupt:
            pass
        finally:
            terminal.close()

    async def loop_until_terminal_exits(self):
        try:
            while self.run_loop_iteration():
                await asyncio.sleep(1/80)
        except KeyboardInterrupt:
            pass

    def run_loop_iteration(self):
        while terminal.has_input():
            char = terminal.read()
            if char == terminal.TK_CLOSE:
                return False
            if char == terminal.TK_C and blt_state.control:
                return False
            self.terminal_read(char)
        should_continue = self.terminal_update()
        terminal.refresh()
        return should_continue