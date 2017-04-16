import weakref

from bearlibterminal import terminal

from clubsandwich.blt.loop import BearLibTerminalEventLoop


class DirectorLoop(BearLibTerminalEventLoop):
    def __init__(self):
        super().__init__()
        self.should_exit = False
        self.scene_stack = []

    @property
    def active_scene(self):
        return self.scene_stack[-1]

    def replace_scene(self, new_value):
        self.pop_scene(may_exit=False)
        self.push_scene(new_value)

    def push_scene(self, new_value):
        self.scene_stack.append(new_value)
        new_value.director = self
        new_value.enter()

    def pop_scene(self, may_exit=True):
        if self.scene_stack:
            last_scene = self.scene_stack.pop()
            last_scene.exit()
            last_scene.director = None
        if may_exit and not self.scene_stack:
            self.should_exit = True

    def quit(self):
        while self.scene_stack:
            self.pop_scene()

    def get_initial_scene(self):
        raise NotImplementedError()

    def terminal_init(self):
        super().terminal_init()
        self.replace_scene(self.get_initial_scene())

    def terminal_update(self):
        terminal.clear()
        for scene in self.scene_stack:
            scene.terminal_update(scene == self.scene_stack[-1])
        return not self.should_exit

    def terminal_read(self, char):
        if self.scene_stack:
            return self.active_scene.terminal_read(char)


class Scene():
    def __init__(self):
        super().__init__()
        self.terminal_readers = []
        self.covers_screen = True
        self._director_weakref = lambda: None

    @property
    def director(self):
        return self._director_weakref()

    @director.setter
    def director(self, new_value):
        if new_value:
            self._director_weakref = weakref.ref(new_value)
        else:
            self._director_weakref = lambda: None

    def add_terminal_reader(self, reader):
        if not getattr(reader, 'terminal_read'):
            raise ValueError("Invalid reader")
        self.terminal_readers.append(reader)

    def remove_terminal_reader(self, reader):
        self.terminal_readers.remove(reader)

    def enter(self):
        pass

    def exit(self):
        pass

    def terminal_update(self, is_active=False):
        return True

    def terminal_read(self, char):
        for reader in self.terminal_readers:
            reader.terminal_read(char)
        return True
