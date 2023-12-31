# --- Libs ---
import pygame
import sys
import os
from random import randint, choice

# --- Constants and global usages ---
pygame.init()
FPS = 50
SIZE = WIDTH, HEIGHT = (1020, 1020)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
RED = pygame.Color("red")
GREEN = pygame.Color("green")
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")


# --- Maze Board class ---
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = 20
        self.board = [[0] * self.width for i in range(self.height)]
        self.control_points = []

    def set_view(self, cell_size, left, top):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generate_labirinte()

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cl = self.cell_size
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, (cl*x, cl*y, cl, cl))

    def generate_labirinte(self):
        x = randint(1, 49)
        y = randint(1, 49)
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


# --- Main game loop ---
board = Maze(101, 101)
board.set_view(10, 0, 0)
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    board.render(screen)
    pygame.display.flip()
sys.exit(pygame.quit())



