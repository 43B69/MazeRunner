import sys
import pygame
from random import choice, randint
from copy import deepcopy
import os
pygame.init()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        #массив лабиринта
        self.board = [[0] * self.width for i in range(self.height)]
        #контрольные точки для создания лабиринта
        self.control_points = []
        self.list_polidrom = [(0, 0, width-1, height-1)]
        self.list_polidrom_2 = deepcopy(self.list_polidrom)

        self.list_room = []

    def set_view(self, cell_size_0):
        self.cell_size = cell_size_0
        self.generate_labirinte()
        self.generate_room(0)
        self.union()
        for y in range(self.height):
            self.board[y].insert(0, 0)
            self.board[y].append(0)
        self.board.append([0] * (self.width+2))
        self.board.insert(0, [0] * (self.width+2))

    def generate_labirinte(self):
        x = randint(1, 18)
        y = randint(1, 13)
        self.board[y][x] = 1
        self.control_points.append((x, y))
        while len(self.control_points) != 0:
            size = choice(self.control_points)
            cells = [(size[0] + 2, size[1]), (size[0] - 2, size[1]), (size[0], size[1] - 2), (size[0], size[1] + 2)]
            cells_2 = []
            for i in range(4):
                x, y = cells[i]
                if (0 < y < self.height-1) and (0 < x < self.width-1) and self.board[y][x] == 0:
                    if i + 1 % 2 == 0:
                        if i > 2:
                            if self.board[y + 1][x] == 0:
                                cells_2.append(cells[i])
                        else:
                            if self.board[y][x + 1] == 0:
                                cells_2.append(cells[i])
                    else:
                        if i > 2:
                            if self.board[y - 1][x] == 0:
                                cells_2.append(cells[i])
                        else:
                            if self.board[y][x - 1] == 0:
                                cells_2.append(cells[i])
            if len(cells_2) == 0:
                self.control_points.remove(size)
            else:
                x, y = choice(cells_2)
                self.board[y][x] = 1
                self.control_points.append((x, y))
                if x == size[0]:
                    if y > size[1]:
                        self.board[y-1][x] = 1
                    elif y < size[1]:
                        self.board[y+1][x] = 1
                elif y == size[1]:
                    if x > size[0]:
                        self.board[y][x-1] = 1
                    elif x < size[0]:
                        self.board[y][x + 1] = 1

    def generate_room(self, count):
        if count == 7:
            return 1
        for i in self.list_polidrom:
            variant = choice(['h', 'w'])
            if variant == 'h':
                start = i[1] + 3
                end = i[3] - 3
                if start <= end:
                    s = randint(start, end)
                    self.list_polidrom_2.remove(i)
                    self.list_polidrom_2.append((i[0], i[1], i[2], s - 1))
                    self.list_polidrom_2.append((i[0], s + 1, i[2], i[3]))
                else:
                    start = i[0] + 3
                    end = i[2] - 3
                    if start <= end:
                        s = randint(start, end)
                        self.list_polidrom_2.remove(i)
                        self.list_polidrom_2.append((i[0], i[1], s - 1, i[3]))
                        self.list_polidrom_2.append((s + 1, i[1], i[2], i[3]))
            elif variant == 'w':
                start = i[0] + 3
                end = i[2] - 3
                if start <= end:
                    s = randint(start, end)
                    self.list_polidrom_2.remove(i)
                    self.list_polidrom_2.append((i[0], i[1], s - 1, i[3]))
                    self.list_polidrom_2.append((s + 1, i[1], i[2], i[3]))
                else:
                    start = i[1] + 3
                    end = i[3] - 3
                    if start <= end:
                        s = randint(start, end)
                        self.list_polidrom_2.remove(i)
                        self.list_polidrom_2.append((i[0], i[1], i[2], s - 1))
                        self.list_polidrom_2.append((i[0], s + 1, i[2], i[3]))
        self.list_polidrom = deepcopy(self.list_polidrom_2)
        return self.generate_room(count + 1)

    def union(self):
        for i in self.list_polidrom:
            x1, y1, x2, y2 = i
            x_pol_1 = randint(x1, x2 - 2)
            y_pol_1 = randint(y1, y2 - 2)
            x_pol_2 = randint(x_pol_1 + 1, x2)
            y_pol_2 = randint(y_pol_1 + 1, y2)
            self.list_room.append((x_pol_1, y_pol_1, x_pol_2, y_pol_2))
            for y in range(y_pol_1, y_pol_2 + 1):
                for x in range(x_pol_1, x_pol_2 + 1):
                    self.board[y][x] = 1

    def print_laberinte(self):
        return self.board
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()
floor_sprite = pygame.sprite.Group()
wall_sprite = pygame.sprite.Group()
stone_sprite = pygame.sprite.Group()
class FloorBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, floor_sprite)
        self.image = load_image('пол2.jpg')
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)


class WallBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, wall_sprite)
        self.image = load_image('стена.jpg')
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)

class StoneBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, stone_sprite)
        self.image = load_image('камень2.png')
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)
def generate_level(laberinte):
    for y in range(HEIGHT+2):
        for x in range(WIDTH+2):
            if laberinte[y][x] == 0:
                cells = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                cells_bools = []
                for cell in cells:
                    x_0, y_0 = cell
                    if (0 <= x_0 < (WIDTH+2)) and (0 <= y_0 < HEIGHT+2):
                        if laberinte[y_0][x_0] == 1:
                            cells_bools.append(True)
                        else:
                            cells_bools.append(False)
                    else:
                        cells_bools.append(False)
                if all(cells_bools):
                    FloorBlock(x, y)
                    StoneBlock(x, y)
                else:
                    WallBlock(x, y)
            if laberinte[y][x] == 1:
                FloorBlock(x, y)

SIZE = W, H = (1200, 900)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
RED = pygame.Color("red")
GREEN = pygame.Color("green")
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
#размер кнопки
cell_size = 50
WIDTH = 20
HEIGHT = 15
board = Board(20, 15)
board.set_view(50)
laberinte = board.print_laberinte()
generate_level(laberinte)
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    pygame.display.flip()
sys.exit(pygame.quit())