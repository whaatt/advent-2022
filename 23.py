# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

grid = open("input.txt", "r").read().split("\n")

elves = set()
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == "#":
            # (X, Y) from bottom-left.
            elves.add((j, (len(grid) - 1) - i))


def propose_north(elves, elf, props):
    (x, y) = elf
    if all((x + dx, y + 1) not in elves for dx in range(-1, 2)):
        props[(x, y + 1)].add((x, y))
        return True
    return False


def propose_south(elves, elf, props):
    (x, y) = elf
    if all((x + dx, y - 1) not in elves for dx in range(-1, 2)):
        props[(x, y - 1)].add((x, y))
        return True
    return False


def propose_west(elves, elf, props):
    (x, y) = elf
    if all((x - 1, y + dy) not in elves for dy in range(-1, 2)):
        props[(x - 1, y)].add((x, y))
        return True
    return False


def propose_east(elves, elf, props):
    (x, y) = elf
    if all((x + 1, y + dy) not in elves for dy in range(-1, 2)):
        props[(x + 1, y)].add((x, y))
        return True
    return False


def print_elves(elves):
    min_x = min(elf[0] for elf in elves)
    max_x = max(elf[0] for elf in elves)
    min_y = min(elf[1] for elf in elves)
    max_y = max(elf[1] for elf in elves)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")


# Probably a less repetitive way to do this...
start_offset = 0
prop_fns = [propose_north, propose_south, propose_west, propose_east]

rounds = 0
elf_moved = True
# for _ in range(rounds):
while elf_moved:
    rounds += 1
    props = defaultdict(set)
    for elf in elves:
        for i in range(start_offset, start_offset + len(prop_fns)):
            (x, y) = elf
            if all(
                (x + dx, y + dy) not in elves
                for dy in range(-1, 2)
                for dx in range(-1, 2)
                if dx != 0 or dy != 0
            ):
                continue
            if prop_fns[i % len(prop_fns)](elves, elf, props):
                break
    elf_moved = False
    for destination, proposers in props.items():
        if len(proposers) != 1:
            continue
        proposer = next(iter(proposers))
        elves.remove(proposer)
        elves.add(destination)
        elf_moved = True
    start_offset += 1
    # print_elves(elves)
    # print()

# box_width = max(elf[0] for elf in elves) + 1 - min(elf[0] for elf in elves)
# box_height = max(elf[1] for elf in elves) + 1 - min(elf[1] for elf in elves)
# box_size = box_height * box_width
# print(box_size - len(elves))
print(rounds)
