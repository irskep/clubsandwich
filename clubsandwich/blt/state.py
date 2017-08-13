"""
.. py:attribute:: state

    Object with attributes that map to all BearLibTerminal
    `event and state constants <http://foo.wyrd.name/en:bearlibterminal:reference:input>`_.

    For example, ``blt_state.shift`` returns ``True`` iff the Shift key is
    down. This is forwarded to
    ``bearlibterminal.terminal.state(terminal.TK_SHIFT)``.

    Numbers are prefixed with ``num_``. So ``blt_state.num_1`` is true iff the
    "1" key is being pressed.
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


    constant_name = constant_key[3:].lower()
    attr_name = 'num_{}'.format(constant_name) if constant_name[0].isdigit() else constant_name
    setattr(
        _TerminalState,
        attr_name,
        property(getter(constant_key)))

blt_state = _TerminalState()
