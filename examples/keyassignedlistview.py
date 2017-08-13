from clubsandwich.director import DirectorLoop
from clubsandwich.ui import UIScene, WindowView, KeyAssignedListView, ButtonView


class BasicScene(UIScene):
  def __init__(self):
    button_generator = (ButtonView(
      text="Item {}".format(i),
      callback=lambda: print("Called Item {}".format(i)))
        for i in range(0, 100)
    )
    self.key_assign = KeyAssignedListView(
      value_controls=button_generator
    )
    super().__init__(WindowView("Scrolling Text", subviews=[self.key_assign]))


class DemoLoop(DirectorLoop):
  def get_initial_scene(self):
    return BasicScene()


if __name__ == '__main__':
  DemoLoop().run()
