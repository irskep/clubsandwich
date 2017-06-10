from clubsandwich.director import DirectorLoop
from clubsandwich.ui import (
  UIScene,
  ButtonView,
)
class MainMenuScene(UIScene):
    def __init__(self, *args, **kwargs):
        views = [ButtonView(text="Quit", callback=self.quit)]
        super().__init__(views, *args, **kwargs)

    def quit(self):
        self.director.pop_scene()

class GameLoop(DirectorLoop):
    def get_initial_scene(self):
        return MainMenuScene()

GameLoop().run()