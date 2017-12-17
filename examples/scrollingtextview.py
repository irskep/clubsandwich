from clubsandwich.director import DirectorLoop
from clubsandwich.ui import UIScene, ScrollingTextView, LayoutOptions, WindowView
from bearlibterminal import terminal


class BasicScene(UIScene):
    def __init__(self):
        self.lets_scroll = ScrollingTextView(
            lines_to_display=4, chars_per_line=60,
            layout_options=LayoutOptions(left=0.05, width=0.85, height=0.3, right=None, bottom=0.1, top=None))
        super().__init__(WindowView(
            "Scrolling Text", subviews=[self.lets_scroll]))
        self.lets_scroll.add_lines("Sometimes this scrolling view can come quite handy right?\n"
                                   "I mean often we need to scroll through logs of action\n"
                                   "to make sure we get everything visible and nice to read things.\n"
                                   "\n"
                                   "Maybe you should stop reading all this and\n"
                                   "Use the scrolling text view into your own game?\n"
                                   "Just making sure this is nicely wrapped.\n"
                                   "This, however\n"
                                   "Needs to break up\n"
                                   "as expected.")

    def terminal_read(self, val):
        super().terminal_read(val)
        if val == terminal.TK_ENTER:
            self.lets_scroll.add_lines("Adding a new line.\n")


class DemoLoop(DirectorLoop):
    def get_initial_scene(self):
        return BasicScene()


if __name__ == '__main__':
    DemoLoop().run()
