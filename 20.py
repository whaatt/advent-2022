# mypy: ignore-errors
# flake8: noqa

multiplier = 811589153
input_value = open("input.txt", "r").read().split("\n")
xs = [(i, int(input_value[i]) * multiplier) for i in range(len(input_value))]


def mix(values):
    i = 0
    next_i = 0
    while next_i < len(values):
        original_i, steps = values[i]
        if original_i == next_i:
            values.pop(i)
            new_i = (i + steps) % len(values)
            if new_i == 0 and steps < 0:
                new_i = len(values)
            values.insert(new_i, (-original_i - 1, steps))
            next_i += 1
        i = (i + 1) % len(values)

    return [(-value[0] - 1, value[1]) for value in values]


for i in range(10):
    xs = mix(xs)
xs = [x[1] for x in xs]
zero_index = next(iter(i for i in range(len(xs)) if xs[i] == 0))
print(
    xs[(zero_index + 1000) % len(xs)]
    + xs[(zero_index + 2000) % len(xs)]
    + xs[(zero_index + 3000) % len(xs)]
)
