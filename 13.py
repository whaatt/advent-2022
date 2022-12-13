# mypy: ignore-errors
# flake8: noqa

import functools

input_value = open("input.txt", "r").read()
pairs = input_value.split("\n\n")

all_packets = []
for i in range(len(pairs)):
    pairs[i] = [eval(packet) for packet in pairs[i].split("\n")]
    for pair in pairs[i]:
        all_packets.append(pair)

all_packets.append([[2]])
all_packets.append([[6]])


def right_order(pair):
    [x, y] = pair
    if type(x) == int and type(y) == int:
        return None if x == y else x < y
    elif type(x) == int and type(y) == list:
        return right_order([[x], y])
    elif type(x) == list and type(y) == int:
        return right_order([x, [y]])
    else:
        for i in range(len(x)):
            if i >= len(y):
                return False
            right = right_order([x[i], y[i]])
            if right is not None:
                return right
        if len(x) < len(y):
            return True
        return None


def sort_key(x, y):
    right = right_order([x, y])
    if right == True:
        return -1
    elif right == False:
        return 1
    else:
        return 0


all_packets = sorted(all_packets, key=functools.cmp_to_key(sort_key))

product = 1
for i in range(len(all_packets)):
    if all_packets[i] == [[2]] or all_packets[i] == [[6]]:
        product *= i + 1

print(product)
