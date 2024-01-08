from random import randint, choice

def generate_maze(width, height):
    board = [[0] * width for i in range(height)]
    control_points = []
    x = randint(1, 49)
    y = randint(1, 49)
    board[y][x] = 1
    control_points.append((x, y))
    while len(control_points) != 0:
        size = choice(control_points)
        cells = [(size[0] + 2, size[1]), (size[0] - 2, size[1]), (size[0], size[1] - 2), (size[0], size[1] + 2)]
        cells_2 = []
        for i in range(4):
            x, y = cells[i]
            if (0 < y < height - 1) and (0 < x < width - 1) and board[y][x] == 0:
                if i + 1 % 2 == 0:
                    if i > 2:
                        if board[y + 1][x] == 0:
                            cells_2.append(cells[i])
                    else:
                        if board[y][x + 1] == 0:
                            cells_2.append(cells[i])
                else:
                    if i > 2:
                        if board[y - 1][x] == 0:
                            cells_2.append(cells[i])
                    else:
                        if board[y][x - 1] == 0:
                            cells_2.append(cells[i])
        if len(cells_2) == 0:
            control_points.remove(size)
        else:
            x, y = choice(cells_2)
            board[y][x] = 1
            control_points.append((x, y))
            if x == size[0]:
                if y > size[1]:
                    board[y - 1][x] = 1
                elif y < size[1]:
                    board[y + 1][x] = 1
            elif y == size[1]:
                if x > size[0]:
                    board[y][x - 1] = 1
                elif x < size[0]:
                    board[y][x + 1] = 1
    return board
