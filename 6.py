# mypy: ignore-errors
# flake8: noqa

x = open("input.txt", "r").read()
for i in range(len(x)):
    if len(set(x[i : i + 14])) == 14:
        print(i + 14)
        break
