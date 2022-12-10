# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
input_value = input_value.split("\n")

x = 1
cycle = 1

xs = []
# signal_strengths = []
for line in input_value:
    if line == "noop":
        xs.append(x)
        cycle += 1
    else:
        xs.append(x)
        cycle += 1
        xs.append(x)
        cycle += 1
        add = int(line.split(" ")[1])
        x += add

for i in range(6):
    for j in range(40):
        index = 40 * i + j
        if j - 1 <= xs[index] <= j + 1:
            print("#", end="")
        else:
            print(".", end="")
    print("\n", end="")
