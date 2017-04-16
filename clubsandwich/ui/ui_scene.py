#!/usr/bin/env python
from bearlibterminal import terminal
from clubsandwich.blt.state import blt_state
from clubsandwich.director import Scene
from clubsandwich.geom import Size
from clubsandwich.ui import (
    FirstResponderContainerView,
)


class UIScene(Scene):
  """
  Scene that renders a :mod:`clubsandwich.ui`-based interface.

  The root view of a :class:`UIScene` is always a
  :class:`FirstResponderContainerView`. In simple terms, this means
  that buttons work.

  Log the view hierarchy by pressing the backslash key at any time.
  """

  def __init__(self, views, *args, **kwargs):
    """
    :param list|View views: One or more subviews of the root view

    See :class:`~clubsandwich.director.Scene` for the other args.
    """

    super().__init__(*args, **kwargs)

    if not isinstance(views, list):
        views = [views]

    self.view = FirstResponderContainerView(subviews=views, scene=self)
    self.add_terminal_reader(self.view)

  def terminal_read(self, val):
    super().terminal_read(val)
    if val == terminal.TK_BACKSLASH:
        self.view.debug_print()

  def terminal_update(self, is_active=False):
    self.view.frame = self.view.frame.with_size(
        Size(blt_state.width, blt_state.height))
    self.view.perform_layout()
    self.view.perform_draw()