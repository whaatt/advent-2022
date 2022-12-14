# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

rock_points = set()
for line in lines:
    points = line.split(" -> ")
    last_point = None
    for point_str in points:
        point = tuple(int(i) for i in point_str.split(","))
        if last_point is None:
            last_point = point
            continue
        if last_point[0] == point[0]:
            smaller = min(last_point[1], point[1])
            bigger = max(last_point[1], point[1])
            for y in range(smaller, bigger + 1):
                rock_points.add((point[0], y))
        else:
            smaller = min(last_point[0], point[0])
            bigger = max(last_point[0], point[0])
            for x in range(smaller, bigger + 1):
                rock_points.add((x, point[1]))
        last_point = point

max_y = max(point[1] for point in rock_points)

units = 0
while True:
    sand_point = (500, 0)
    while sand_point[1] <= max_y:
        if (sand_point[0], sand_point[1] + 1) not in rock_points:
            sand_point = (sand_point[0], sand_point[1] + 1)
        elif (sand_point[0] - 1, sand_point[1] + 1) not in rock_points:
            sand_point = (sand_point[0] - 1, sand_point[1] + 1)
        elif (sand_point[0] + 1, sand_point[1] + 1) not in rock_points:
            sand_point = (sand_point[0] + 1, sand_point[1] + 1)
        else:
            break
    units += 1
    if sand_point == (500, 0):
        break
    rock_points.add(sand_point)

print(units)
