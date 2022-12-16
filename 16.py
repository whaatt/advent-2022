# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict
from functools import cache

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")


def parse_line(line):
    start = line.split(" ")[1]
    destinations = (
        set(line.split("valves ")[1].split(", "))
        if "valves" in line
        else {line.split("valve ")[1]}
    )
    flow = int(line.split("=")[1].split(";")[0])
    return (start, flow, destinations)


valves = {}
sources = defaultdict(set)
for line in lines:
    (start, flow, destinations) = parse_line(line)
    valves[start] = (flow, destinations)

non_zero_valves = sorted([valve for valve in valves.keys() if valves[valve][0] > 0])
non_zero_valve_count = len(non_zero_valves)
non_zero_valve_bit = {non_zero_valves[i]: i for i in range(len(non_zero_valves))}

considered = 0


@cache
def solve(minute, position, el_position, on_set):
    if minute <= 0:
        return 0
    if on_set == 2**non_zero_valve_count - 1:
        return 0

    global considered
    considered += 1
    # if considered % 1000000 == 0:
    #     print(considered)

    best = 0
    (flow, destinations) = valves[position]
    (el_flow, el_destinations) = valves[el_position]

    can_open = False
    if flow > 0:
        position_bit = non_zero_valve_bit[position]
        can_open = not (on_set & (1 << position_bit))

    el_can_open = False
    if el_flow > 0:
        el_position_bit = non_zero_valve_bit[el_position]
        el_can_open = not (on_set & (1 << el_position_bit))

    # Move; Move
    for destination in destinations:
        for el_destination in el_destinations:
            best = max(
                best,
                solve(
                    minute - 1,
                    min(destination, el_destination),
                    max(destination, el_destination),
                    on_set,
                ),
            )

    # Open; Move
    if can_open:
        new_on_set = on_set | (1 << position_bit)
        for el_destination in el_destinations:
            best = max(
                best,
                flow * (minute - 1)
                + solve(
                    minute - 1,
                    min(position, el_destination),
                    max(position, el_destination),
                    new_on_set,
                ),
            )

    # Move; Open
    if el_can_open:
        new_on_set = on_set | (1 << el_position_bit)
        for destination in destinations:
            best = max(
                best,
                el_flow * (minute - 1)
                + solve(
                    minute - 1,
                    min(destination, el_position),
                    max(destination, el_position),
                    new_on_set,
                ),
            )

    # Open; Open
    if can_open and el_can_open and position != el_position:
        new_on_set = on_set | (1 << position_bit) | (1 << el_position_bit)
        best = max(
            best,
            (flow + el_flow) * (minute - 1)
            + solve(
                minute - 1,
                position,
                el_position,
                new_on_set,
            ),
        )

    return best


print(solve(26, "AA", "AA", 0))
