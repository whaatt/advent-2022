# mypy: ignore-errors
# flake8: noqa

from functools import cache

input_value = open("input.txt", "r").read().split("\n")

values = {}
for ops in input_value:
    ops = ops.split(" ")
    ops[0] = ops[0][:-1]
    if len(ops) == 2:
        values[ops[0]] = (int(ops[1]),)
    else:
        values[ops[0]] = (ops[1], ops[2], ops[3])


@cache
def get_value(name):
    if name not in values or len(values[name]) not in (1, 3):
        raise KeyError
    # We assume that `humn` never appears as a higher-order term.
    if name == "humn":
        return (0, 1)
    if len(values[name]) == 1:
        return (values[name][0], 0)
    else:
        x = get_value(values[name][0])
        op = values[name][1] if name != "root" else "-"
        y = get_value(values[name][2])

        # Validate assumption.
        x_has_humn = x[1] != 0
        y_has_humn = y[1] != 0
        if x_has_humn and y_has_humn:
            raise AssertionError
        if y_has_humn and op == "/":
            raise AssertionError

        # Process algebraic op.
        if op == "+":
            return (x[0] + y[0], x[1] + y[1])
        elif op == "-":
            return (x[0] - y[0], x[1] - y[1])
        elif op == "*":
            if x_has_humn:
                return (x[0] * y[0], x[1] * y[0])
            elif y_has_humn:
                return (y[0] * x[0], y[1] * x[0])
            else:
                return (x[0] * y[0], 0)
        else:
            if x_has_humn:
                return (x[0] / y[0], x[1] / y[0])
            else:
                return (x[0] / y[0], 0)


(a, b) = get_value("root")
print(round(-a / b))
