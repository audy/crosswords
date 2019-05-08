import random
import sys
import time
import curses


def is_empty(grid):

    for row in grid:
        for char in row:
            if char is not None:
                return False
    return True


def draw_curses(screen, grid):
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char is not None:

                try:
                    screen.addch(j, i, char)
                except:
                    pass


def draw(grid):
    """

    Draw the current grid

    """

    for row in grid:
        for char in row:
            if char is None:
                sys.stdout.write(" ")
            else:
                sys.stdout.write(char)
        sys.stdout.write("\n")


def place_word(grid, coords, word):
    """
    Return the grid with the new word placed
    """

    for i, l in enumerate(word):
        x, y = coords[0] + i, coords[1]

        grid[y][x] = l

    return grid


def transpose(grid):

    transposed_grid = []

    width, height = len(grid), len(grid[0])

    for j in range(0, height):
        column = []
        for i in range(0, width):
            column.append(grid[i][j])
        transposed_grid.append(column)

    return transposed_grid


def can_be_placed(grid, coords, word, vertical=False):
    """


    >>> can_be_placed(grid, (1, 2), "potato", vertical=True)

    A word can be placed on the grid @ coords if it meets the following criteria

    1. is overlapping at least one existing word (not floating)
    2. does not alter the characters of the existing words

    """

    # starting at coords, iterate in direction over the grid
    # - if the location is None, it's okay
    # - if there is a letter, make sure it's the same letter as the one we're
    #   placing over it
    # - doesn't go over the edge of the grid (although we could just grow the
    #   grid in this case)
    # - need to go back over the grid and make sure any new "words" exist in
    #   some dictionary or are not generated at all
    #
    # might be useful to be able to transpose the matrix so we don't have to
    # figure out two ways to iterate over it. let's do horizontal first
    # (if we transpose the grid, we have to transpose the coordinates too)

    has_touched = is_empty(grid)

    if vertical:
        return can_be_placed(transpose(grid), (coords[1], coords[0]), word)
    else:
        for i in range(0, len(word)):

            x, y = coords[0] + i, coords[1]

            if y not in range(0, len(grid)) or x not in range(0, len(grid[0])):
                return False
            else:
                grid_contents = grid[y][x]
                current_letter = word[i]

                if grid_contents == None:
                    pass
                elif grid_contents == current_letter:
                    has_touched = True
                    pass
                else:
                    return False
        return has_touched


def crossword(grid, words):

    # idea

    # 1. create a large grid, place a word near the center either horizontally
    # or vertically

    # 2. iteratively try to place the next word, if the word cannot be placed,
    # try the next word etc etc
    # - can brute force this with random

    # 3. If a point is reached where no new words can be added, shuffle the
    # list and try again

    # some hueristics:
    # - pre-sort words so that all of them can be placed

    # make the grid much alrger than needed and then shrink it later

    width = len(grid[0])
    height = len(grid)

    for word in words:

        while True:

            if is_empty(grid):
                i, j = width // 2, height // 2
            else:
                i, j = random.randint(0, width - 1), random.randint(0, height - 1)

            if can_be_placed(grid, (i, j), word):
                return place_word(grid, (i, j), word)
            else:
                continue


def load_words(path="/usr/share/dict/words"):
    with open(path) as handle:
        return [l.strip().lower() for l in handle]


def make_grid(width, height):
    grid = []
    for j in range(0, height):
        grid.append([None] * width)

    return grid


def main(screen):

    X, Y = screen.getmaxyx()

    grid = make_grid(X, Y)

    words = load_words()

    i = 0

    while True:
        if i % 2 != 0:
            grid = transpose(grid)

        c = chr(screen.getch()).lower()
        choices = [w for w in words if w.startswith(c)]

        if len(choices) == 0:
            continue
        else:
            word = random.choice(choices)
            grid = crossword(grid, [word])
            draw_curses(screen, grid)

            i += 1
            screen.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
