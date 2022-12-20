# mypy: ignore-errors
# flake8: noqa

from functools import cache
from math import ceil

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

blueprints = []
lines = [line.split(" ") for line in lines]
for i in range(len(lines)):
    blueprints.append([])
    for word in lines[i]:
        word = word.strip(":")
        try:
            blueprints[i].append(int(word))
        except ValueError:
            pass
    blueprints[i] = tuple(blueprints[i])


def score_blueprint_quality(blueprint, minutes_start):
    id = blueprint[0]
    ore_for_robot_ore = blueprint[1]
    ore_for_robot_clay = blueprint[2]
    ore_for_robot_obsidian = blueprint[3]
    clay_for_robot_obsidian = blueprint[4]
    ore_for_robot_geode = blueprint[5]
    obsidian_for_robot_geode = blueprint[6]

    @cache
    def max_geodes(
        minutes,
        ore,
        clay,
        obsidian,
        robots_ore,
        robots_clay,
        robots_obsidian,
        robots_geode,
    ):
        if minutes == 0:
            return 0

        best = 0
        # Next: Ore Robot
        if robots_ore > 0:
            minutes_until = ceil(max(0, (ore_for_robot_ore - ore)) / robots_ore) + 1
            if minutes - minutes_until >= 0:
                best = max(
                    best,
                    (robots_geode * minutes_until)
                    + max_geodes(
                        minutes - minutes_until,
                        ore + robots_ore * minutes_until - ore_for_robot_ore,
                        clay + robots_clay * minutes_until,
                        obsidian + robots_obsidian * minutes_until,
                        robots_ore + 1,
                        robots_clay,
                        robots_obsidian,
                        robots_geode,
                    ),
                )

        # Next: Clay Robot
        if robots_ore > 0:
            minutes_until = ceil(max(0, (ore_for_robot_clay - ore)) / robots_ore) + 1
            if minutes - minutes_until >= 0:
                best = max(
                    best,
                    (robots_geode * minutes_until)
                    + max_geodes(
                        minutes - minutes_until,
                        ore + robots_ore * minutes_until - ore_for_robot_clay,
                        clay + robots_clay * minutes_until,
                        obsidian + robots_obsidian * minutes_until,
                        robots_ore,
                        robots_clay + 1,
                        robots_obsidian,
                        robots_geode,
                    ),
                )

        # Next: Obsidian Robot
        if robots_ore > 0 and robots_clay > 0:
            minutes_until = (
                max(
                    ceil(max(0, (ore_for_robot_obsidian - ore)) / robots_ore),
                    ceil(max(0, (clay_for_robot_obsidian - clay)) / robots_clay),
                )
                + 1
            )
            if minutes - minutes_until >= 0:
                best = max(
                    best,
                    (robots_geode * minutes_until)
                    + max_geodes(
                        minutes - minutes_until,
                        ore + robots_ore * minutes_until - ore_for_robot_obsidian,
                        clay + robots_clay * minutes_until - clay_for_robot_obsidian,
                        obsidian + robots_obsidian * minutes_until,
                        robots_ore,
                        robots_clay,
                        robots_obsidian + 1,
                        robots_geode,
                    ),
                )

        # Next: Geode Robot
        if robots_ore > 0 and robots_obsidian > 0:
            minutes_until = (
                max(
                    ceil(max(0, (ore_for_robot_geode - ore)) / robots_ore),
                    ceil(
                        max(0, (obsidian_for_robot_geode - obsidian)) / robots_obsidian
                    ),
                )
                + 1
            )
            if minutes - minutes_until >= 0:
                best = max(
                    best,
                    (robots_geode * minutes_until)
                    + max_geodes(
                        minutes - minutes_until,
                        ore + robots_ore * minutes_until - ore_for_robot_geode,
                        clay + robots_clay * minutes_until,
                        obsidian
                        + robots_obsidian * minutes_until
                        - obsidian_for_robot_geode,
                        robots_ore,
                        robots_clay,
                        robots_obsidian,
                        robots_geode + 1,
                    ),
                )

        # Next: No Robot Possible
        best = max(best, robots_geode * minutes)
        return best

    # return id * max_geodes(minutes_start, 0, 0, 0, 1, 0, 0, 0)
    return max_geodes(minutes_start, 0, 0, 0, 1, 0, 0, 0)


# total = 0
product = 1
# for i in range(len(blueprints)):
for i in range(3):
    print(i)
    # total += score_blueprint_quality(blueprints[i], 24)
    product *= score_blueprint_quality(blueprints[i], 32)

print(product)
