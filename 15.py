# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("input.txt", "r").read()
# Input was manually modified to look like `((x, y), (a, b))`.
sensor_beacons = [eval(line) for line in input_value.split("\n")]


def manhattan(pair):
    return abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])


def range_and(range, value, greater):
    if range is None:
        return None
    if greater:
        lower = max(range[0], value)
        range = (lower, range[1])
    else:
        higher = min(range[1], value)
        range = (range[0], higher)
    if range[0] > range[1]:
        return None
    return range


min_distances = [manhattan(pair) for pair in sensor_beacons]

x_max = 4000000
y_max = 4000000

# manhattan((a, b), (x, y)) > min_distance[(a, b)]
# Case 1: (x - a) > min_distance[(a, b)] - abs(y - b)
# OR
# Case 2: (x - a) < abs(y - b) - min_distance[(a, b)]

valid_columns_for_row = defaultdict(list)
for row in range(y_max + 1):
    # if row % 100000 == 0:
    #     print(row)
    valid_ranges = [(0, x_max)]
    # +1 to minimum distances because of `_eq`.
    x_must_be_above_eq = [
        (min_distances[i] + 1)
        - abs(row - sensor_beacons[i][0][1])
        + sensor_beacons[i][0][0]
        for i in range(len(sensor_beacons))
    ]
    x_must_be_below_eq = [
        abs(row - sensor_beacons[i][0][1])
        - (min_distances[i] + 1)
        + sensor_beacons[i][0][0]
        for i in range(len(sensor_beacons))
    ]
    for i in range(len(x_must_be_above_eq)):
        if x_must_be_below_eq[i] < x_must_be_above_eq[i]:
            new_valid_ranges = []
            for valid_range in valid_ranges:
                if x_must_be_below_eq[i] < x_must_be_above_eq[i]:
                    valid_range_a = range_and(valid_range, x_must_be_above_eq[i], True)
                    valid_range_b = range_and(valid_range, x_must_be_below_eq[i], False)
                    valid_range_combined = range_and(
                        valid_range_a, x_must_be_below_eq[i], False
                    )
                    if valid_range_combined is not None:
                        new_valid_ranges.append(valid_range_combined)
                    else:
                        if valid_range_a is not None:
                            new_valid_ranges.append(valid_range_a)
                        if valid_range_b is not None:
                            new_valid_ranges.append(valid_range_b)
            valid_ranges = new_valid_ranges

    for valid_range in valid_ranges:
        valid_columns_for_row[row].append(range(valid_range[0], valid_range[1] + 1))

# manhattan((a, b), (x, y)) > min_distance[(a, b)]
# Case 1: (y - b) > min_distance[(a, b)] - abs(x - a)
# OR
# Case 2: (y - b) < abs(x - a) - min_distance[(a, b)]

for column_ranges in valid_columns_for_row.values():
    for column_range in column_ranges:
        for column in column_range:
            valid_ranges = [(0, y_max)]
            y_must_be_above_eq = [
                (min_distances[i] + 1)
                - abs(column - sensor_beacons[i][0][0])
                + sensor_beacons[i][0][1]
                for i in range(len(sensor_beacons))
            ]
            y_must_be_below_eq = [
                abs(column - sensor_beacons[i][0][0])
                - (min_distances[i] + 1)
                + sensor_beacons[i][0][1]
                for i in range(len(sensor_beacons))
            ]
            for i in range(len(y_must_be_above_eq)):
                if y_must_be_below_eq[i] < y_must_be_above_eq[i]:
                    new_valid_ranges = []
                    for valid_range in valid_ranges:
                        if y_must_be_below_eq[i] < y_must_be_above_eq[i]:
                            valid_range_a = range_and(
                                valid_range, y_must_be_above_eq[i], True
                            )
                            valid_range_b = range_and(
                                valid_range, y_must_be_below_eq[i], False
                            )
                            valid_range_combined = range_and(
                                valid_range_a, y_must_be_below_eq[i], False
                            )
                            if valid_range_combined is not None:
                                new_valid_ranges.append(valid_range_combined)
                            else:
                                if valid_range_a is not None:
                                    new_valid_ranges.append(valid_range_a)
                                if valid_range_b is not None:
                                    new_valid_ranges.append(valid_range_b)
                    valid_ranges = new_valid_ranges

            row_set = set()
            for valid_range in valid_ranges:
                row_set.update(set(range(valid_range[0], valid_range[1] + 1)))
            for row in row_set:
                for column_range in valid_columns_for_row[row]:
                    if column in column_range:
                        print(column * x_max + row)
                        exit(0)
