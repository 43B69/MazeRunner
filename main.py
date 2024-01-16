import sys
import pygame
from random import choice, randint
from copy import deepcopy
import os
from pygame.math import Vector2
pygame.init()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 300
        #массив лабиринта
        self.board = [[0] * self.width for i in range(self.height)]
        #контрольные точки для создания лабиринта
        self.control_points = []
        self.list_polidrom = [(0, 0, width-1, height-1)]
        self.list_polidrom_2 = deepcopy(self.list_polidrom)

        self.list_room = []

    def render(self):
        for y in range(self.height):
            for x in range(self.height):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, SANDY, (x*cell_size, y*cell_size, cell_size, cell_size))
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
        point_player = (randint(1, self.width-1), randint(1, self.height-1))
        if self.board[point_player[1]][point_player[0]] != 1:
            while self.board[point_player[1]][point_player[0]] != 1:
                point_player = (randint(1, self.width - 1), randint(1, self.height - 1))
        self.board[point_player[1]][point_player[0]] = 2
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
player_group = pygame.sprite.Group()
inventory_group = pygame.sprite.Group()
basic_inventory_group = pygame.sprite.Group()
weapon_on_map = pygame.sprite.Group()


class FloorBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, floor_sprite)
        self.image = load_image('images.jpg')
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)


class WallBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, wall_sprite)
        self.image = load_image('стена.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)


class StoneBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, stone_sprite)
        self.image = load_image('камень3.png')
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.alpha = 180
        self.image = pygame.transform.rotate(load_image('player.png'), self.alpha)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)
        self.speed = 5
        self.orig = self.image

    def update(self, *args, **kwargs):
        if args[0][pygame.K_w]:
            self.rect = self.rect.move(0, -self.speed)
        if args[0][pygame.K_s]:
            self.rect = self.rect.move(0, self.speed)
        if args[0][pygame.K_a]:
            self.rect = self.rect.move(-self.speed, 0)
        if args[0][pygame.K_d]:
            self.rect = self.rect.move(self.speed, 0)
        if pygame.sprite.spritecollide(self, wall_sprite, False):
            if args[0][pygame.K_w]:
                self.rect = self.rect.move(0, self.speed)
            if args[0][pygame.K_s]:
                self.rect = self.rect.move(0, -self.speed)
            if args[0][pygame.K_a]:
                self.rect = self.rect.move(self.speed, 0)
            if args[0][pygame.K_d]:
                self.rect = self.rect.move(-self.speed, 0)


    def rotate(self):
        x, y, w, h = self.rect
        direction = pygame.mouse.get_pos() - Vector2(x + w//2, y + h // 2)
        radius, angle = direction.as_polar()
        self.alpha = -angle-90
        self.image = pygame.transform.rotate(self.orig, self.alpha)
        self.rect = self.image.get_rect(center=self.rect.center)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, alpha, dx, dy):
        super().__init__(all_sprites)


class WeaponIcon:
    def __init__(self):
        self.image = ''
        self.flag_image = False
        self.allinventory_coordinate = [0, 0, 0, 0, 0]

    def mousebuttondown(self, mouse_pos):
        if self.flag_image:
            self.rect = self.image.get_rect(center=mouse_pos)

    def mousebuttonup(self, pos_x, pos_y, left, top, cs):
        self.rect = self.image.get_rect().move(pos_x * cs + left + 20, pos_y * cs + top)
        self.allinventory_coordinate[0], self.allinventory_coordinate[1] = pos_x, pos_y

    def return_old_pos_inventory(self):
        return self.allinventory_coordinate[0], self.allinventory_coordinate[1]

    def add_allinventory(self, pos_x, pos_y, left, top, cs):
        self.kill()
        inventory_group.add(self)
        self.allinventory_coordinate = [pos_x, pos_y, left, top, cs]

    def purpose_allinventory(self):
        pos_x, pos_y, left, top, cs = self.allinventory_coordinate
        self.image = self.orig
        self.rect = self.image.get_rect().move(pos_x * cs + left + 20, pos_y * cs + top)


    def purpose_weapon_on_map_coordinate(self, mouse_pos):
        self.kill()
        weapon_on_map.add(self)
        all_sprites.add(self)
        self.rect = self.image.get_rect().move(mouse_pos[0], mouse_pos[1])
        self.flag_image = False


class ArrowIcon(WeaponIcon, pygame.sprite.Sprite):
    def __init__(self, image):
        WeaponIcon.__init__(self)
        pygame.sprite.Sprite.__init__(self, inventory_group)
        self.image = load_image(image)
        self.orig = self.image


class OnionIcon(WeaponIcon, pygame.sprite.Sprite):
    def __init__(self, image):
        WeaponIcon.__init__(self)
        pygame.sprite.Sprite.__init__(self, inventory_group)
        self.image = load_image(image)
        self.orig = self.image


class AllInventory:
    def __init__(self):
        self.flag = False
        self.width = 5
        self.height = 5
        self.cell_size = 150
        self.top = 125
        self.left = 375
        self.inventory = [[0] * self.width for i in range(self.height)]
        self.inventory[0][0] = ArrowIcon('стрела_icon.png')
        self.inventory[0][0].add_allinventory(0, 0, self.left, self.top, self.cell_size)
        self.inventory[0][1] = OnionIcon('лук_icon.png')
        self.inventory[0][1].add_allinventory(1, 0, self.left, self.top, self.cell_size)

    def render(self):
        if self.flag:
            surf = pygame.Surface((W, H))
            surf.fill(GREY_2)
            surf.set_alpha(200)
            screen.blit(surf, (0, 0))
            for y in range(self.height):
                for x in range(self.width):
                    if y != self.height - 1:
                        pygame.draw.rect(screen, GREY_2, (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                    else:
                        pygame.draw.rect(screen, GREY_3, (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))
                    pygame.draw.rect(screen, GREY_1, (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 10)
                    if self.inventory[y][x] != 0:
                        self.inventory[y][x].purpose_allinventory()

        else:
            screen.fill((0, 0, 0))

    def get_cell(self, mouse_pos):
        mx = (mouse_pos[0] - self.left) // self.cell_size
        my = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= mx < self.width and 0 <= my < self.height:
            return mx, my

    def get_click(self, mouse_pos, treatment, player_rect):
        cell = self.get_cell(mouse_pos)
        if cell:
            x, y = cell
            if treatment == 'MOUSEBUTTONDOWN':
                if self.inventory[y][x] != 0:
                    self.inventory[y][x].flag_image = True
                    self.inventory[y][x].kill()
                    inventory_group.add(self.inventory[y][x])
            elif treatment == 'MOUSEBUTTONUP':
                for y_0 in range(self.height):
                    for x_0 in range(self.width):
                        if self.inventory[y_0][x_0] != 0:
                            if self.inventory[y_0][x_0].flag_image:
                                self.inventory[y_0][x_0].flag_image = False
                                dx, dy = self.inventory[y_0][x_0].return_old_pos_inventory()
                                if not self.inventory[y][x]:
                                    self.inventory[y_0][x_0].mousebuttonup(x, y, self.left, self.top, self.cell_size)
                                    self.inventory[y][x] = self.inventory[dy][dx]
                                    self.inventory[dy][dx] = 0
                                else:
                                    self.inventory[y_0][x_0].mousebuttonup(dx, dy, self.left, self.top, self.cell_size)
        else:
            if treatment == 'MOUSEBUTTONUP':
                for y_0 in range(self.height):
                    for x_0 in range(self.width):
                        if self.inventory[y_0][x_0] != 0:
                            if self.inventory[y_0][x_0].flag_image:
                                self.inventory[y_0][x_0].purpose_weapon_on_map_coordinate(player_rect)
                                self.inventory[y_0][x_0] = 0



    def open_inventory(self, *args):
        if args[0] == pygame.K_TAB:
            if self.flag:
                self.flag = False
            else:
                self.flag = True

    def all_mousebuttondown(self, mouse_pos):
        for y in range(self.height):
            for x in range(self.width):
                if self.inventory[y][x] != 0:
                    self.inventory[y][x].mousebuttondown(mouse_pos)


class BasicInventory(AllInventory):
    def __init__(self):
        super().__init__()


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
        self.dx = -(target.rect.x + target.rect.w // 2 - W // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - H // 2)
def generate_level(laberinte):
    px, py = None, None
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
            if laberinte[y][x] == 2:
                FloorBlock(x, y)
                px, py = x, y
    new_player = Player(px, py)
    return new_player


SIZE = W, H = (700, 700)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
RED = pygame.Color("red")
GREEN = pygame.Color("green")
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
SANDY = pygame.Color("#D39353")
GREY_1 = pygame.Color("#808080")
GREY_2 = pygame.Color("#C0C0C0")
GREY_3 = pygame.Color("#C6C3B5")
#размер кнопки
cell_size = 300
WIDTH = 20
HEIGHT = 15
board = Board(20, 15)
board.set_view(50)
camera = Camera()
inventory = AllInventory()
laberinte = board.print_laberinte()
player = generate_level(laberinte)
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            inventory.open_inventory(event.key)
        if inventory.flag:
            if event.type == pygame.MOUSEBUTTONDOWN:
                inventory.get_click(pygame.mouse.get_pos(), 'MOUSEBUTTONDOWN', player.rect)
            if event.type == pygame.MOUSEBUTTONUP:
                inventory.get_click(pygame.mouse.get_pos(), 'MOUSEBUTTONUP', player.rect)
    if not inventory.flag:
        player.rotate()
        player.update(pygame.key.get_pressed())
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    player.kill()
    all_sprites.add(player)
    all_sprites.draw(screen)
    if inventory.flag:
        inventory.render()
        inventory.all_mousebuttondown(pygame.mouse.get_pos())
        inventory_group.draw(screen)
    pygame.display.flip()
sys.exit(pygame.quit())