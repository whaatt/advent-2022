# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("input.txt", "r").read()

monkeys = input_value.split("\n\n")

for i in range(len(monkeys)):
    monkey = monkeys[i]
    monkey = monkey.split("\n")
    items = eval("[" + monkey[1].split(": ")[1] + "]")
    op = eval("lambda old: " + monkey[2].split(" = ")[1])
    test_mod = int(monkey[3].split(" by ")[1])
    dest_true = int(monkey[4].split(" monkey ")[1])
    dest_false = int(monkey[5].split(" monkey ")[1])
    monkeys[i] = (items, op, test_mod, dest_true, dest_false)

mod_prod = 1
for monkey in monkeys:
    mod_prod *= monkey[2]

inspections = defaultdict(int)
for round in range(10000):
    for i in range(len(monkeys)):
        (items, op, test_mod, dest_true, dest_false) = monkeys[i]
        while items:
            inspections[i] += 1
            item = items.pop(0)
            item = op(item)
            if item % test_mod == 0:
                monkeys[dest_true][0].append(item % mod_prod)
            else:
                monkeys[dest_false][0].append(item % mod_prod)


top_inspections = sorted(inspections.values())
print(top_inspections[-2] * top_inspections[-1])
