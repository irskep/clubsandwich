from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.blt.state import blt_state
from clubsandwich.tilemap import TileMap, CellOutOfBoundsError
from clubsandwich.geom import Point, Rect, Size
from clubsandwich.line_of_sight import get_visible_points

dungeon = ["###########################################################",
           "#...........#.............................................#",
           "#...........#........#....................................#",
           "#.....................#...................................#",
           "#....####..............#..................................#",
           "#.......#.......................#####################.....#",
           "#.......#...........................................#.....#",
           "#.......#...........##..............................#.....#",
           "#####........#......##.....@....##################..#.....#",
           "#...#...........................#................#..#.....#",
           "#...#............#..............#................#..#.....#",
           "#...............................#..###############..#.....#",
           "#...............................#...................#.....#",
           "#...............................#...................#.....#",
           "#...............................#####################.....#",
           "#.........................................................#",
           "#.........................................................#",
           "###########################################################"]


def _get_allows_light(tilemap, point):
    try:
        return tilemap[point].terrain == 0
    except CellOutOfBoundsError:
        return False


def draw(tilemap, player_pos):
    los_cache = get_visible_points(player_pos, lambda p: _get_allows_light(tilemap, p))

    for cell in tilemap.cells:
        if cell.point not in los_cache: continue
        if cell.terrain == 0:
            terminal.put(cell.point, '.')
        elif cell.terrain == 1:
            terminal.put(cell.point, '#')
    terminal.put(player_pos, '@')


def main():
    terminal.open()
    tilemap = TileMap(Size(80, 24))

    player_pos = Point(0, 0)
    for y, row in enumerate(dungeon):
        for x, char in enumerate(row):
            cell = tilemap[Point(x, y)]
            if char == '.':
                cell.terrain = 0
            elif char == '#':
                cell.terrain = 1
            elif char == '@':
                player_pos = Point(x, y)
            else:
                raise ValueError(char)

    terminal.refresh()
    terminal.clear()
    draw(tilemap, player_pos)
    try:
        while True:
            terminal.clear()
            draw(tilemap, player_pos)
            terminal.refresh()
            if terminal.has_input():
                char = terminal.read()
                if char == terminal.TK_Q:
                    break
                if char == terminal.TK_UP:
                    player_pos = player_pos + Point(0, -1)
                if char == terminal.TK_DOWN:
                    player_pos = player_pos + Point(0, 1)
                if char == terminal.TK_LEFT:
                    player_pos = player_pos + Point(-1, 0)
                if char == terminal.TK_RIGHT:
                    player_pos = player_pos + Point(1, 0)
    except KeyboardInterrupt:
        pass
    finally:
        terminal.close()


main()
