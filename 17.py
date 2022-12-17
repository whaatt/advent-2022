# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

directions = open("input.txt", "r").read()

# Vertical direction reversed.
pieces = [
    [
        "####",
    ],
    [
        ".#.",
        "###",
        ".#.",
    ],
    [
        "###",
        "..#",
        "..#",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]


def height(filled_value):
    # (Y, X)
    return max(y for (y, _) in filled_value) + 1


width = 7
filled = set()
for i in range(width):
    # (Y, X)
    filled.add((-1, i))


def check_obstruction(filled_value, piece, new_bl):
    if new_bl[1] < 0 or new_bl[1] + len(piece[0]) - 1 >= width:
        return True
    for y in range(new_bl[0], new_bl[0] + len(piece)):
        y_offset = y - new_bl[0]
        for x in range(new_bl[1], new_bl[1] + len(piece[y_offset])):
            # (Y, X)
            y_offset = y - new_bl[0]
            x_offset = x - new_bl[1]
            if piece[y_offset][x_offset] == "#" and (y, x) in filled_value:
                return True
    return False


rocks = 1000000000000
directions_offset = 3373
period_piece_offset = 1
repetition_offset = 566
repetition_offset_height = 868
repetition_period = 1720
repetition_period_height = 2626

directions_i = directions_offset
for rock in range((rocks - repetition_offset) % repetition_period):
    piece = pieces[(rock + period_piece_offset) % len(pieces)]
    bl = (height(filled) + 3, 2)
    while True:
        # Horizontal movement:
        dx = 1 if directions[directions_i] == ">" else -1
        directions_i = (directions_i + 1) % len(directions)

        # (Y, X)
        new_bl = (bl[0], bl[1] + dx)
        if not check_obstruction(filled, piece, new_bl):
            bl = new_bl

        # Vertical movement:
        dy = -1

        # (Y, X)
        new_bl = (bl[0] + dy, bl[1])
        if not check_obstruction(filled, piece, new_bl):
            bl = new_bl
        else:
            for y_offset in range(len(piece)):
                for x_offset in range(len(piece[y_offset])):
                    # (Y, X)
                    if piece[y_offset][x_offset] == "#":
                        filled.add((bl[0] + y_offset, bl[1] + x_offset))
            break

    current_height = height(filled)
    if all((current_height - 1, x) in filled for x in range(width)):
        # 566 rocks = 868 height with one as the next piece.
        # Cycle thereafter is 1720 rocks = 2626 height.
        print(
            rock + 1,
            current_height,
            ((rock + period_piece_offset + 1) % len(pieces)),
            directions_i,
        )

        for y in range(height(filled) - 1, height(filled) - 10, -1):
            print("".join("#" if (y, x) in filled else "." for x in range(width)))
        print()


print(
    height(filled)
    + ((rocks - repetition_offset) // repetition_period) * repetition_period_height
    + repetition_offset_height
)
