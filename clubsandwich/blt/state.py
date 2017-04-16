"""
Provides a ``blt_state`` object containing properties for all BearLibTerminal
state keys. When you access a property, ``terminal_state(THE_CONST)`` is
called and its value is returned.

For example, ``blt_state.shift`` returns ``True`` iff the Shift key is down.
"""
from bearlibterminal import terminal


class _TerminalState:
    pass

for constant_key in (c for c in dir(terminal) if c.startswith('TK_')):
    def getter(k):
        constant_value = getattr(terminal, k)
        def get(self):
            return terminal.state(constant_value)
        return get
    setattr(
        _TerminalState,
        constant_key[3:].lower(),
        property(getter(constant_key)))

blt_state = _TerminalState()