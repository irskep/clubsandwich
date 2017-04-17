"""
The :py:mod:`~clubsandwich.director` module deals with state management.

Most games have at least two screens: a main menu that prompts you to play,
and the actual game. The :py:class:`~DirectorLoop` class keeps track of
the screen (scene) that the player is seeing and interacting with, and
lets you switch to another one.

Scenes are stored in a stack. To go back to the previous scene, you pop
off the top of the stack. If there are no more scenes, the loop exits.

Here's a simple example::

    from bearlibterminal import terminal
    from clubsandwich.director import DirectorLoop, Scene

    class BasicLoop2(DirectorLoop):
        def get_initial_scene(self):
            return MainMenuScene()

    class MainMenuScene(Scene):
        def terminal_update(self):
            print(0, 0, "Press Enter to begin game, Esc to quit")

        def terminal_read(self, val):
            if val == terminal.TK_ENTER:
                self.director.push_scene(GameScene())
            elif val == terminal.TK_ESCAPE:
                self.director.pop_scene()

    class GameScene(Scene):
        def terminal_update(self):
            print(
                0, 0,
                "You are playing the game, it is so fun!" +
                " Press Esc to stop.")

        def terminal_read(self, val):
            if val == terminal.TK_ESCAPE:
                self.director.pop_scene()

    if __name__ == '__main__':
        BasicLoop2().run()
"""
import weakref

from bearlibterminal import terminal

from clubsandwich.blt.loop import BearLibTerminalEventLoop


class DirectorLoop(BearLibTerminalEventLoop):
    """
    An event loop that manages a stack of scenes. Forwards all input events to
    the topmost scene. Draws all scenes each frame, starting with the topmost
    scene a ``True`` value for :py:attr:`Scene.covers_screen`.

    **You use this class by subclassing it.** Override
    :py:meth:`~DirectorLoop.get_initial_scene` to return the initial scene.
    Override :py:meth:`~DirectorLoop.terminal_init` to do any initial setup.

    This is a subclass of :py:class:`BearLibTerminalEventLoop`, so after
    subclassing it, instantiate it and call ``.run()`` to run your game.

    .. py:attribute:: scene_stack

        List of scenes. Topmost is active.

    .. py:attribute: should_exit

        If truthy, the loop will exit at the end of the frame.
    """

    def __init__(self):
        super().__init__()
        self.should_exit = False
        self.scene_stack = []

    @property
    def active_scene(self):
        """The scene on top of the stack which is receiving keyboard events."""
        return self.scene_stack[-1]

    def replace_scene(self, new_value):
        """
        :param Scene new_value:

        Replace the topmost scene on the stack with a new value. If popping a
        scene results in an empty stack, the loop **does not** exit.
        """
        self.pop_scene(may_exit=False)
        self.push_scene(new_value)

    def push_scene(self, new_value):
        """
        :param Scene new_value:

        Push a scene onto the stack and make it active.
        """
        self.scene_stack.append(new_value)
        new_value.director = self
        new_value.enter()

    def pop_scene(self, may_exit=True):
        """
        :param boolean may_exit: If ``False``, the loop will not exit if there
                                 are no more scenes in the stack.

        Pop a scene off the stack and make the next topmost one active.
        """
        if self.scene_stack:
            last_scene = self.scene_stack.pop()
            last_scene.exit()
            last_scene.director = None
        if may_exit and not self.scene_stack:
            self.should_exit = True

    def quit(self):
        """
        Pop all scenes off the stack and exit the loop.
        """
        while self.scene_stack:
            self.pop_scene()

    def get_initial_scene(self):
        """
        :return: :py:class:`Scene`

        .. note::

            **You must override this in your subclass.**
        """
        raise NotImplementedError()

    def terminal_init(self):
        """
        Called immedialy after the terminal has been opened, but before the
        first ``terminal.refresh()`` call.

        If you subclass, you probably want to call ``super().terminal_init()``
        *after* you do your setup, because this method implementation adds the
        first scene to the stack.
        """
        super().terminal_init()
        self.replace_scene(self.get_initial_scene())

    def terminal_update(self):
        """
        :py:class:`DirectorLoop`'s implementation of
        :py:meth:`BearLibTerminalEventLoop.terminal_update`. Updates the
        active scene and any visible behind it.

        You don't need to call or subclass this method.
        """
        terminal.clear()
        i = 0
        for j, scene in enumerate(self.scene_stack):
            if scene.covers_screen:
                i = j
        for scene in self.scene_stack[i:]:
            scene.terminal_update(scene == self.scene_stack[-1])
        return not self.should_exit

    def terminal_read(self, char):
        """
        :py:class:`DirectorLoop`'s implementation of
        :py:meth:`BearLibTerminalEventLoop.terminal_read`. Forwards events to
        the active scene.

        You don't need to call or subclass this method.
        """
        if self.scene_stack:
            return self.active_scene.terminal_read(char)


class Scene():
    """
    Handle logic for one screen.

    .. py:attribute:: covers_screen

        If ``True``, no scenes under this one in the stack will be drawn by
        :py:class:`DirectorLoop`. You'll probably want to set this to
        ``True`` in most cases, unless you really want the lower scenes to
        show through (e.g. popups).
    """

    def __init__(self):
        super().__init__()
        self._terminal_readers = []
        self.covers_screen = True
        self._director_weakref = lambda: None

    @property
    def director(self):
        """
        Weak reference to the director this scene is managed by. Becomes
        ``None`` if the director is garbage collected, or if this scene is
        removed from the director's stack.
        """
        return self._director_weakref()

    @director.setter
    def director(self, new_value):
        if new_value:
            self._director_weakref = weakref.ref(new_value)
        else:
            self._director_weakref = lambda: None

    def add_terminal_reader(self, reader):
        """
        :param Object reader: An object that has a method ``terminal_read(val)``

        Add an object to be called when terminal input is sent to this scene.
        All input is sent to all readers.

        You may never need to worry about this. :py:class:`UIScene` takes care
        of the details for :py:mod:`clubsandwich.ui`.
        """
        if not getattr(reader, 'terminal_read'):
            raise ValueError("Invalid reader")
        self._terminal_readers.append(reader)

    def remove_terminal_reader(self, reader):
        """
        :param Object reader: An object in the list of terminal readers

        Stop calling ``reader.terminal_read(val)`` when this scene receives
        events.
        """
        self._terminal_readers.remove(reader)

    def enter(self):
        """
        Called by :py:class:`DirectorLoop` when added to the stack.
        """

    def exit(self):
        """
        Called by :py:class:`DirectorLoop` when removed from the stack.
        """

    def terminal_update(self, is_active=False):
        """
        :param boolean is_active: :py:class:`DirectorLoop` will pass ``True``
                                  iff this scene is topmost in the stack.

        Called by :py:class:`DirectorLoop` each frame iff no scenes above
        it in the stack have set ``covers_screen == True``.
        """
        return True

    def terminal_read(self, char):
        """
        :param str char: Return value of ``BearLibTerminal.terminal.read()``.

        Called by :py:class:`DirectorLoop` if there is input to be processed.
        """
        for reader in self._terminal_readers:
            reader.terminal_read(char)
        return True
