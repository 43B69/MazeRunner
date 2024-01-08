# --- Libs ---
import pygame
import sys
import os
from random import randint, choice
from MazeGenerator import generate_maze


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# --- Constants and global usages ---
pygame.init()
FPS = 50
SIZE = WIDTH, HEIGHT = (1020, 1020)
screen = pygame.display.set_mode(SIZE)
CameraSurface = pygame.Surface(SIZE)
clock = pygame.time.Clock()
RED = pygame.Color("red")
GREEN = pygame.Color(1, 50, 32)
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_image = load_image('Player.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(0, 0)
        self.speed = 1

    def update(self, *args, **kwargs):
        if args:
            if args[0] == pygame.K_UP:
                self.rect = self.rect.move(0, -self.speed)
            if args[0] == pygame.K_DOWN:
                self.rect = self.rect.move(0, self.speed)
            if args[0] == pygame.K_LEFT:
                self.rect = self.rect.move(-self.speed, 0)
            if args[0] == pygame.K_RIGHT:
                self.rect = self.rect.move(self.speed, 0)
        '''if pygame.sprite.spritecollide(self, box_group, False):
            if args[0] == pygame.K_UP:
                self.rect = self.rect.move(0, +50)
            if args[0] == pygame.K_DOWN:
                self.rect = self.rect.move(0, -50)
            if args[0] == pygame.K_LEFT:
                self.rect = self.rect.move(+50, 0)
            if args[0] == pygame.K_RIGHT:
                self.rect = self.rect.move(-50, 0)'''


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


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
        self.board = generate_maze(self.width, self.height)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cl = self.cell_size
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, GREEN, (cl*x, cl*y, cl, cl))


# --- Main game loop ---
# board = Maze(101, 101)
# board.set_view(50, 0, 0)
player = Player(10, 10)

camera = Camera()


running = True

while running:
    clock.tick(120)
    screen.fill(BLACK)
    KEYS = pygame.key.get_pressed()
    if any(KEYS):
        if KEYS[pygame.K_UP]:
            player.update(pygame.K_UP)
        if KEYS[pygame.K_DOWN]:
            player.update(pygame.K_DOWN)
        if KEYS[pygame.K_LEFT]:
            player.update(pygame.K_LEFT)
        if KEYS[pygame.K_RIGHT]:
            player.update(pygame.K_RIGHT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # board.render(screen)
    all_sprites.draw(screen)
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    pygame.display.flip()
sys.exit(pygame.quit())



