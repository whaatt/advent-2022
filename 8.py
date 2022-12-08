# mypy: ignore-errors
# flake8: noqa

grid = open("input.txt", "r").read()
grid = grid.split("\n")
grid = [[int(c) for c in line] for line in grid]

max_scenic_score = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        x_low = 0
        for x in range(i - 1, -1, -1):
            x_low += 1
            if grid[x][j] >= grid[i][j]:
                break

        x_high = 0
        for x in range(i + 1, len(grid)):
            x_high += 1
            if grid[x][j] >= grid[i][j]:
                break

        y_low = 0
        for y in range(j - 1, -1, -1):
            y_low += 1
            if grid[i][y] >= grid[i][j]:
                break

        y_high = 0
        for y in range(j + 1, len(grid[i])):
            y_high += 1
            if grid[i][y] >= grid[i][j]:
                break

        max_scenic_score = max(max_scenic_score, x_low * x_high * y_low * y_high)

print(max_scenic_score)
