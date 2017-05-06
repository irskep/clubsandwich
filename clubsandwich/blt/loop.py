"""
If you're using the state management features of clubsandwich, you might want
to look at :py:class:`DirectorLoop` instead. This is its superclass.
"""
import sys
import time
from bearlibterminal import terminal
from .state import blt_state


class BearLibTerminalEventLoop:
    """
    :param Real fps: After each loop iteration,
                     :py:class:`BearLibTerminalEventLoop` waits ``1/fps``
                     seconds before checking for input and updating again.

    Simple wrapper around BearLibTerminal and ``asyncio``.

    Subclass :py:meth:`terminal_init`, :py:meth:`terminal_read`, and
    :py:meth:`terminal_update`. Instantiate your class and call its
    :py:meth:`run` method.

    Example::

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

        MyDemo().run()
    """

    def __init__(self, fps=72):
        super().__init__()
        self.fps = fps

    def terminal_init(self):
        """
        Terminal has just been opened. You should configure it with 
        ``terminal.set()``.
        """
        pass

    def terminal_read(self, char):
        """
        :param str char: Return value of ``BearLibTerminal.terminal.read()``

        Called whenever new input is available.
        """
        pass

    def terminal_update(self):
        """
        :return: ``True`` if another loop should be run, ``False`` if the loop
                 should exit

        Update the view. Fires once per frame regardless of whether there
        was any input. **Make sure you return True to continue each loop
        iteration!** (If you are using :py:class:`DirectorLoop`, this is
        already taken care of.)
        """
        return True

    def run(self):
        """
        Start the event loop.
        """
        terminal.open()
        self.terminal_init()
        terminal.refresh()

        try:
            self.loop_until_terminal_exits()
        except KeyboardInterrupt:
            pass
        finally:
            terminal.close()

    def loop_until_terminal_exits(self):
        try:
            has_run_one_loop = False
            while self.run_loop_iteration():
                has_run_one_loop = True
                time.sleep(1/80)
            if not has_run_one_loop:
                print(
                    "Exited after only one loop iteration. Did you forget to" +
                    " return True from terminal_update()?",
                    file=sys.stderr)
        except KeyboardInterrupt:
            pass

    def run_loop_iteration(self):
        while terminal.has_input():
            char = terminal.read()
            self.terminal_read(char)
        should_continue = self.terminal_update()
        terminal.refresh()
        return should_continue