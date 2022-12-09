# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
input_value = input_value.split("\n")
input_value = [line.split(" ") for line in input_value]
input_value = [(line[0], int(line[1])) for line in input_value]

knots = [(0, 0) for _ in range(10)]


def neighbors(point):
    (x, y) = point
    return {
        (x + i, y + j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    }


def edge_neighbors(point):
    (x, y) = point
    return {
        (x + i, y + j) for i in range(-1, 2) for j in range(-1, 2) if abs(i + j) == 1
    }


def diagonal_neighbors(point):
    (x, y) = point
    return {
        (x + i, y + j)
        for i in range(-1, 2)
        for j in range(-1, 2)
        if abs(i) == 1 and abs(j) == 1
    }


seen_set = {knots[9]}
for (direction, steps) in input_value:
    for _ in range(steps):
        for i in range(len(knots) - 1):
            head, tail = knots[i], knots[i + 1]
            if i == 0:
                if direction == "U":
                    head = (head[0], head[1] + 1)
                elif direction == "L":
                    head = (head[0] - 1, head[1])
                elif direction == "R":
                    head = (head[0] + 1, head[1])
                else:
                    head = (head[0], head[1] - 1)
                knots[i] = head

            if head == tail or head in neighbors(tail):
                continue

            edge_overlap = edge_neighbors(tail) & edge_neighbors(head)
            if edge_overlap:
                tail = next(iter(edge_overlap))
                if i + 1 == len(knots) - 1:
                    seen_set.add(tail)
                knots[i + 1] = tail
                continue

            tail = next(iter(neighbors(head) & diagonal_neighbors(tail)))
            if i + 1 == len(knots) - 1:
                seen_set.add(tail)
            knots[i + 1] = tail

print(len(seen_set))
