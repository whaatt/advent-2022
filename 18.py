# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

cubes = set(tuple(int(i) for i in line.split(",")) for line in lines)

min_x = float("inf")
min_y = float("inf")
min_z = float("inf")
max_x = float("-inf")
max_y = float("-inf")
max_z = float("-inf")
for (x, y, z) in cubes:
    min_x = min(x, min_x)
    min_y = min(y, min_y)
    min_y = min(y, min_y)
    max_x = max(x, max_x)
    max_y = max(y, max_y)
    max_z = max(z, max_z)


def is_external(point):
    if point in cubes:
        return False
    seen_set = {point}
    queue = deque({point})
    while queue:
        (x, y, z) = queue.popleft()
        if (
            x == min_x
            or x == max_x
            or y == min_y
            or y == max_y
            or z == min_z
            or z == max_z
        ):
            return True
        for dx in [-1, 1]:
            new_point = (x + dx, y, z)
            if new_point not in seen_set and new_point not in cubes:
                seen_set.add(new_point)
                queue.append(new_point)
        for dy in [-1, 1]:
            new_point = (x, y + dy, z)
            if new_point not in seen_set and new_point not in cubes:
                seen_set.add(new_point)
                queue.append(new_point)
        for dz in [-1, 1]:
            new_point = (x, y, z + dz)
            if new_point not in seen_set and new_point not in cubes:
                seen_set.add(new_point)
                queue.append(new_point)
    return False


sides = 0
for (x, y, z) in cubes:
    for dx in [-1, 1]:
        if is_external((x + dx, y, z)):
            sides += 1
    for dy in [-1, 1]:
        if is_external((x, y + dy, z)):
            sides += 1
    for dz in [-1, 1]:
        if is_external((x, y, z + dz)):
            sides += 1

print(sides)
