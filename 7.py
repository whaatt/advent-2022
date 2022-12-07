# mypy: ignore-errors
# flake8: noqa

x = open("input.txt", "r").read()
x = x.split("\n")

root = (None, {})
current = root
for line in x:
    (parent, children) = current
    command = line[:4]
    if command == "$ ls":
        continue
    elif command == "$ cd":
        arg = line[5:]
        if arg == "..":
            current = parent
        elif arg == "/":
            current = root
        else:
            current = children[arg]
    else:
        item_type, name = line.split(" ")
        if item_type == "dir":
            if name not in children:
                children[name] = (current, {})
        else:
            if name not in children:
                children[name] = (current, int(item_type))

large_dir_sum = 0


def traverse(path, tree):
    global large_dir_sum
    size_here = 0
    for name, item in tree[1].items():
        if type(item[1]) == int:
            size_here += item[1]
        else:
            size_here += traverse(path + name + "/", item)
    if size_here <= 100000:
        large_dir_sum += size_here
    return size_here


to_free = 30000000 - (70000000 - traverse("/", root))
min_above_to_free = float("inf")


def traverse2(path, tree):
    global min_above_to_free
    size_here = 0
    for name, item in tree[1].items():
        if type(item[1]) == int:
            size_here += item[1]
        else:
            size_here += traverse2(path + name + "/", item)
    if size_here >= to_free:
        min_above_to_free = min(min_above_to_free, size_here)
    return size_here


traverse2("/", root)
print(min_above_to_free)
