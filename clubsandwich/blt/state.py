"""
.. py:attribute:: state

    Object with attributes that map to all BearLibTerminal
    `event and state constants <http://foo.wyrd.name/en:bearlibterminal:reference:input>`_.

    For example, ``blt_state.shift`` returns ``True`` iff the Shift key is
    down. This is forwarded to
    ``bearlibterminal.terminal.state(terminal.TK_SHIFT)``.
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