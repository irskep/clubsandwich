#!/usr/bin/env python3
"""
This program is added to your ``$PATH`` when you install clubsandwich.
It repeatedly runs a command until you ctrl+c the ``babysit`` process.

Imagine you're working on a flame effect for your main screen. It takes
a lot of tweaking. Every time you make a change, you go to run your game::

  python flamegame.py

This is annoying. With ``babysit``, you can make it continuously relaunch
every time you quit, so as soon as you exit you see the latest code running
in seconds::

  babysit python flamegame.py

It will keep relaunching until you ctrl+c the ``babysit`` process.

Relaunches are never more often than 5 seconds, in case you've got a
crash-on-launch bug.
"""
import sys
import subprocess
import time
from math import floor

cmd = sys.argv[1:]

message = '< NEW BABYSIT SESSION (Ctrl+C to stop) >'
left_padding = floor((78 - len(message)) / 2)
right_padding = 78 - len(message) - left_padding


def cli():
    if len(sys.argv) == 1 or len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__.strip())
        return

    cont = True
    last_time = time.time()
    while cont:
        print('-' * left_padding + message +
              '-' * right_padding, file=sys.stderr)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            p.wait()
            time.sleep(max(0, 5 - (time.time() - last_time)))
            last_time = time.time()
        except KeyboardInterrupt:
            cont = False
