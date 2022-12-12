# mypy: ignore-errors
# flake8: noqa

from collections import deque

input_value = open("input.txt", "r").read()
input_value = input_value.split("\n")
input_value = [[char for char in line] for line in input_value]

queue = deque()
end = None
grid = {}

for i in range(len(input_value)):
    for j in range(len(input_value[i])):
        if input_value[i][j] == "S":
            queue.append(((i, j), 0))
            grid[i, j] = 0
        elif input_value[i][j] == "E":
            end = (i, j)
            grid[i, j] = 25
        else:
            # Comment out for Part 1:
            if input_value[i][j] == "a":
                queue.append(((i, j), 0))
            grid[i, j] = ord(input_value[i][j]) - ord("a")

seen = set(point for (point, _) in queue)
while queue:
    ((x, y), steps) = queue.popleft()
    if (x, y) == end:
        print(steps)
        break
    else:
        for (i, j) in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
            if (
                (i, j) not in seen
                and (i, j) in grid
                and grid[(i, j)] <= grid[(x, y)] + 1
            ):
                seen.add((i, j))
                queue.append(((i, j), steps + 1))
