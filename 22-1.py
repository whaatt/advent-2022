# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read().split("\n\n")
directions = input_value[1]
grid = [[char for char in line] for line in input_value[0].split("\n")]
rows = len(grid)
columns = max(len(line) for line in grid)

for i in range(len(grid)):
    if len(grid[i]) < columns:
        grid[i] += [" "] * (columns - len(grid[i]))

directions = directions.replace("R", " R ")
directions = directions.replace("L", " L ")
directions = directions.split(" ")
directions = [int(x) if x not in "LR" else x for x in directions if x != " "]

row_to_start_column = {}
row_to_end_column = {}
column_to_start_row = {}
column_to_end_row = {}
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if not grid[i][j] in ".#":
            continue
        if i not in row_to_start_column:
            row_to_start_column[i] = j
        row_to_end_column[i] = j
        if j not in column_to_start_row:
            column_to_start_row[j] = i
        column_to_end_row[j] = i

current = (0, row_to_start_column[0], 0)
# (x, y, facing) = current
# grid[x][y] = (">v<^")[facing]
for direction in directions:
    (x, y, facing) = current
    if type(direction) == int:
        # Take a step.
        while direction > 0:
            if facing == 0:
                y = (y + 1) % columns
                if grid[x][y] == " ":
                    y = row_to_start_column[x]
            elif facing == 1:
                x = (x + 1) % rows
                if grid[x][y] == " ":
                    x = column_to_start_row[y]
            elif facing == 2:
                y = (y - 1) % columns
                if grid[x][y] == " ":
                    y = row_to_end_column[x]
            else:
                x = (x - 1) % rows
                if grid[x][y] == " ":
                    x = column_to_end_row[y]

            # Handle walls.
            if grid[x][y] == "#":
                break
            current = (x, y, facing)
            # grid[x][y] = (">v<^")[facing]
            direction -= 1
    elif direction == "R":
        current = (x, y, (facing + 1) % 4)
        # grid[x][y] = (">v<^")[facing]
    else:
        current = (x, y, (facing - 1) % 4)
        # grid[x][y] = (">v<^")[facing]

# grid[x][y] = (">v<^")[facing]
(x, y, facing) = current
print(1000 * (x + 1) + 4 * (y + 1) + facing)
# print("\n".join("".join(line) for line in grid))
