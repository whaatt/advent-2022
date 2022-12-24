# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque

grid = open("input.txt", "r").read().split("\n")
rows, columns = len(grid), len(grid[0])

# Populate quick lookup (O(B) for B blizzards per point) map for blizzards.
blizzards = defaultdict(list)
for r in range(len(grid)):
    for c in range(len(grid[r])):
        if grid[r][c] == "^":
            for a in range(1, rows - 1):
                # Value is (time modulo, target offset).
                blizzards[(a, c)].append((rows - 2, (r - a) % (rows - 2)))
        if grid[r][c] == "v":
            for a in range(1, rows - 1):
                blizzards[(a, c)].append((rows - 2, (a - r) % (rows - 2)))
        if grid[r][c] == ">":
            for b in range(1, columns - 1):
                blizzards[(r, b)].append((columns - 2, (b - c) % (columns - 2)))
        if grid[r][c] == "<":
            for b in range(1, columns - 1):
                blizzards[(r, b)].append((columns - 2, (c - b) % (columns - 2)))

START = (0, 1)
END = (rows - 1, columns - 2)


def solve(start, finish, start_time):
    queue = deque()
    queue.append((START, start_time))

    seen_set = set()
    while queue:
        # Track seen items.
        item = queue.popleft()
        if item in seen_set:
            continue
        seen_set.add(item)

        # Check stopping condition.
        ((r, c), t) = item
        if (r, c) == END:
            return t

        # Iterate over neighbor jumps (including a wait).
        new_t = t + 1
        for (dr, dc) in ((0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)):
            new_r = r + dr
            new_c = c + dc
            if new_r < 0 or new_r >= rows:
                continue
            if new_c < 0 or new_c >= columns:
                continue
            if grid[new_r][new_c] == "#":
                continue

            # Check blizzards for each possible neighbor jump.
            got_blizzard_hit = False
            for (modulo, offset) in blizzards[(new_r, new_c)]:
                if new_t % modulo == offset:
                    got_blizzard_hit = True
                    break
            if got_blizzard_hit:
                continue

            # Enqueue neighbor.
            queue.append(((new_r, new_c), new_t))


print(solve(START, END, solve(END, START, solve(START, END, 0))))
