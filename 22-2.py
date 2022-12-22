# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read().split("\n\n")
directions = input_value[1]
grid = [[char for char in line] for line in input_value[0].split("\n")]

directions = directions.replace("R", " R ")
directions = directions.replace("L", " L ")
directions = directions.split(" ")
directions = [int(x) if x not in "LR" else x for x in directions if x != " "]

# Manually filled in:
rows = 50
columns = 50

# Manually filled in:
grid_offsets = [
    (0 * rows, 1 * columns),
    (0 * rows, 2 * columns),
    (1 * rows, 1 * columns),
    (2 * rows, 0 * columns),
    (2 * rows, 1 * columns),
    (3 * rows, 0 * columns),
]

# Manually filled in:
# In theory, only twelve entries are needed in this table, but filling out all 24 is a good
# checksum on correctness. An even more intelligent approach might assign each face to a particular
# side of the cube with fixed orientation, and derive this table from that, but that's harder to
# reason about.
wrap = {
    # X low.
    (0, "X", "L"): (5, "Y", "L", False),
    (1, "X", "L"): (5, "X", "H", False),
    (2, "X", "L"): (0, "X", "H", False),
    (3, "X", "L"): (2, "Y", "L", False),
    (4, "X", "L"): (2, "X", "H", False),
    (5, "X", "L"): (3, "X", "H", False),
    # X high.
    (0, "X", "H"): (2, "X", "L", False),
    (1, "X", "H"): (2, "Y", "H", False),
    (2, "X", "H"): (4, "X", "L", False),
    (3, "X", "H"): (5, "X", "L", False),
    (4, "X", "H"): (5, "Y", "H", False),
    (5, "X", "H"): (1, "X", "L", False),
    # Y low.
    (0, "Y", "L"): (3, "Y", "L", True),
    (1, "Y", "L"): (0, "Y", "H", False),
    (2, "Y", "L"): (3, "X", "L", False),
    (3, "Y", "L"): (0, "Y", "L", True),
    (4, "Y", "L"): (3, "Y", "H", False),
    (5, "Y", "L"): (0, "X", "L", False),
    # Y high.
    (0, "Y", "H"): (1, "Y", "L", False),
    (1, "Y", "H"): (4, "Y", "H", True),
    (2, "Y", "H"): (1, "X", "H", False),
    (3, "Y", "H"): (4, "Y", "L", False),
    (4, "Y", "H"): (1, "Y", "H", True),
    (5, "Y", "H"): (4, "X", "H", False),
}

grids = [
    [
        [grid[i][j] for j in range(grid_offsets[g][1], grid_offsets[g][1] + 50)]
        for i in range(grid_offsets[g][0], grid_offsets[g][0] + 50)
    ]
    for g in range(len(grid_offsets))
]

for (side, axis, edge) in wrap:
    assert wrap[wrap[side, axis, edge][:-1]][:-1] == (side, axis, edge)
    assert wrap[side, axis, edge][-1] == wrap[wrap[side, axis, edge][:-1]][-1]

current = (0, 0, 0, 0)
for direction in directions:
    (side, x, y, facing) = current
    if type(direction) == int:
        while direction > 0:
            # Take a step.
            if facing == 0:
                axis = "Y"
                y += 1
                edge = "H" if y >= rows else None
            elif facing == 1:
                axis = "X"
                x += 1
                edge = "H" if x >= rows else None
            elif facing == 2:
                axis = "Y"
                y -= 1
                edge = "L" if y < 0 else None
            else:
                axis = "X"
                x -= 1
                edge = "L" if x < 0 else None

            # Handle cube wrapping.
            if edge is not None:
                x = x % rows
                y = y % columns
                (side, new_axis, new_edge, reverse_off_axis) = wrap[side, axis, edge]
                new_off_axis = "X" if new_axis == "Y" else "Y"
                if new_axis != axis:
                    x, y = y, x
                if new_axis == "X":
                    if new_edge == "L":
                        facing = 1
                        x = 0
                    else:
                        facing = 3
                        x = rows - 1
                    if reverse_off_axis:
                        y = (columns - 1) - y
                if new_axis == "Y":
                    if new_edge == "L":
                        facing = 0
                        y = 0
                    else:
                        facing = 2
                        y = columns - 1
                    if reverse_off_axis:
                        x = (rows - 1) - x

            # Handle walls.
            if grids[side][x][y] == "#":
                break
            current = (side, x, y, facing)
            direction -= 1
    elif direction == "R":
        facing = (facing + 1) % 4
        current = (side, x, y, facing)
    else:
        facing = (facing - 1) % 4
        current = (side, x, y, facing)

(side, x, y, facing) = current
(x_offset, y_offset) = grid_offsets[side]
print(1000 * (x + x_offset + 1) + 4 * (y + y_offset + 1) + facing)
