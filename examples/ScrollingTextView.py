from clubsandwich.director import DirectorLoop
from clubsandwich.ui import UIScene, ScrollingTextView, LayoutOptions, WindowView


class BasicScene(UIScene):
    def __init__(self):
        self.lets_scroll = ScrollingTextView(
            lines_to_display=5, chars_per_line=70,
            layout_options=LayoutOptions(left=0, width=0.9, height=0.3, right=None, bottom=0.1, top=None))
        super().__init__(WindowView("Scrolling Text", subviews=[self.lets_scroll]))
        self.lets_scroll.add_lines("Sometimes this scrolling view\ncan come quite handy right?\n"
                                   "I mean often we need to scroll through logs of action\n"
                                   "to make sure we get everything visible and nice to read things.\n"
                                   "Maybe you should stop reading all this and\n"
                                   "\n"
                                   "\n"
                                   "Use the scrolling text view into your own game?")


class DemoLoop(DirectorLoop):
    def get_initial_scene(self):
        return BasicScene()


if __name__ == '__main__':
    DemoLoop().run()
