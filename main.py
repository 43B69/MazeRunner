import sys
import pygame
from random import choice, randint
from copy import deepcopy
import os
from functools import partial
from pygame.math import Vector2
from math import *
import time
from pprint import pprint
import threading
from MainRoom import *
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
        point_player = (randint(2, self.width-2), 0)
        self.board[point_player[1]][point_player[0]] = 2
        down = 1
        cells = [self.board[point_player[1] + down][point_player[0]], self.board[point_player[1]][point_player[0] + 1],
                 self.board[point_player[1]][point_player[0]-1]]
        while cells[0] == 0 and cells[1] == 0 and cells[2] == 0:
            self.board[point_player[1] + down][point_player[0]] = 1
            cells = [self.board[point_player[1] + down][point_player[0]],
                     self.board[point_player[1]][point_player[0] + 1], self.board[point_player[1]][point_player[0] - 1]]
            down += 1
        point_exit = (randint(2, self.width-2), self.height+1)
        self.board[point_exit[1]][point_exit[0]] = 1
        up = -1
        cells = [self.board[point_exit[1] + up][point_exit[0]], self.board[point_exit[1]][point_exit[0] + 1],
                 self.board[point_exit[1]][point_exit[0] - 1]]
        while cells[0] == 0 and cells[1] == 0 and cells[2] == 0:
            self.board[point_player[1] + up][point_player[0]] = 1
            cells = [self.board[point_exit[1] + up][point_exit[0]], self.board[point_exit[1]][point_exit[0] + 1],
                     self.board[point_exit[1]][point_exit[0] - 1]]
            up += -1
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
effects_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
patrons_group = pygame.sprite.Group()

class FloorBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, floor_sprite)
        self.image = load_image('images.jpg')
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos_x
        self.y = pos_y


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
    def __init__(self, pos_x, pos_y, user_groups, walls_groups):
        super().__init__(player_group, user_groups, all_sprites)
        self.alpha = 0
        self.image = pygame.transform.rotate(load_image('player2C.png'), self.alpha)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)
        self.speed = 5
        self.max_hp = 10
        self.hp = 10
        self._walls_groups = walls_groups
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
        if pygame.sprite.spritecollide(self, self._walls_groups, False):
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
        self.alpha = -angle
        self.image = pygame.transform.rotate(self.orig, self.alpha)
        self.rect = self.image.get_rect(center=self.rect.center)

    def render(self):
        x, y = self.rect.center
        len_line_hp = (150*self.hp)/self.max_hp
        pygame.draw.line(screen, RED, (x-75, y-80), (x-75+len_line_hp, y-80), 10)
# class OrdinaryZombie(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         pygame.sprite.Sprite.__init__(self, zombie_group, all_sprites)
#         self.image = load_image('zombie-transformed.png')
#         self.rect = self.image.get_rect().move(pos[0]+100, pos[1] + 100)
#         self.hp = 10
#         self.damage = 2
#         self.orig = self.image
#         self.speed = 4
#
#     def rotate(self, pos):
#         x, y, w, h = self.rect
#         direction = pos - Vector2(x + w // 2, y + h // 2)
#         radius, angle = direction.as_polar()
#         self.image = pygame.transform.rotate(self.orig, -angle-90)
#         self.rect = self.image.get_rect(center=self.rect.center)
#
#     def run(self, pos):
#         x, y, w, h = self.rect
#         delta_x = pos[0] - x
#         delta_y = pos[1] - y
#         if delta_x < 0:
#             if abs(delta_x) >= self.speed:
#                 self.rect = self.rect.move(-self.speed, 0)
#                 if pygame.sprite.spritecollide(self, wall_sprite, False):
#                     self.rect = self.rect.move(self.speed, 0)
#             else:
#                 self.rect = self.rect.move(-(self.speed-abs(delta_x)), 0)
#         if delta_x > 0:
#             if abs(delta_x) >= self.speed:
#                 self.rect = self.rect.move(self.speed, 0)
#                 if pygame.sprite.spritecollide(self, wall_sprite, False):
#                     self.rect = self.rect.move(-self.speed, 0)
#             else:
#                 self.rect = self.rect.move(self.speed-abs(delta_x), 0)
#         if delta_y < 0:
#             if abs(delta_y) >= self.speed:
#                 self.rect = self.rect.move(0, -self.speed)
#                 if pygame.sprite.spritecollide(self, wall_sprite, False):
#                     self.rect = self.rect.move(0, self.speed)
#             else:
#                 self.rect = self.rect.move(0, -(self.speed-abs(delta_x)))
#
#         if delta_y > 0:
#             if abs(delta_y) >= self.speed:
#                 self.rect = self.rect.move(0, self.speed)
#                 if pygame.sprite.spritecollide(self, wall_sprite, False):
#                     self.rect = self.rect.move(0, -self.speed)
#             else:
#                 self.rect = self.rect.move(0, (self.speed-abs(delta_x)))


class OrdinaryZombie2(pygame.sprite.Sprite):
    def __init__(self, image, pos_mouse):
        super().__init__(zombie_group, all_sprites)
        self.image = load_image(image)
        self.orig = self.image
        self.timer_att = threading.Thread(target=self.time_effect)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_mouse[0], pos_mouse[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.width = 0
        self.height = 0
        self.number_wave = 3
        self.destination = ()
        self.flag_algoritm = False
        self.go_flag = True
        self.hp = 10
        self.max_hp = 10
        self.speed = 5
        self.x2 = 0
        self.y2 = 0
        self.center = ()
        self.count = 0
        self.damage = 1
        self.board = [[0] * self.width for i in range(self.height)]
        self.wave_board = [[0] * self.width for i in range(self.height)]
        self.cortage_wave_board = [[0] * self.width for i in range(self.height)]
        self.my_way = [[0] * self.width for i in range(self.height)]
        self.zom_pos = ()

    def set_view(self, width, height, lab, pos):
        player_pos = pos
        self.width = width + 2
        self.height = height + 2
        self.board = lab
        self.wave_board = deepcopy(self.board)
        self.cortage_wave_board = [[0] * self.width for i in range(self.height)]
        self.my_way = [[0] * self.width for i in range(self.height)]
        for sprite1 in floor_sprite.sprites():
            if pygame.sprite.collide_mask(self, sprite1):
                self.zom_pos = (sprite1.x, sprite1.y)
                break
        result = self.has_path(self.zom_pos[0], self.zom_pos[1], player_pos[0], player_pos[1])
        if result == "Нашелся путь!":
            self.way(self.zom_pos[0], self.zom_pos[1], player_pos[0], player_pos[1], 0)
            self.my_way[player_pos[1]][player_pos[0]] = 1
            self.flag_algoritm = True
            for sprite1 in floor_sprite.sprites():
                x, y = sprite1.x, sprite1.y
                if x == self.destination[0] and y == self.destination[1]:
                    self.center = sprite1.rect.center
            self.number_wave = 3
    def has_path(self, x1, y1, x2, y2):
        if self.number_wave == 3:
            cells = [(x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1)]
            for i in cells:
                mx, my = i
                if 0 <= my < len(self.wave_board) and 0 <= mx < len(self.wave_board[0]):
                    if self.wave_board[my][mx] != 0 and self.wave_board[my][mx] == 1:
                        self.wave_board[my][mx] = self.number_wave
                        if self.cortage_wave_board[y1][x1] == 0:
                            self.cortage_wave_board[y1][x1] = []
                        self.cortage_wave_board[y1][x1].append((mx, my))
                        if my == y2 and x2 == mx:
                            return "Нашелся путь!"
        else:
            count = 0
            for y_0 in range(len(self.wave_board)):
                if not (self.number_wave - 1 in self.wave_board[y_0]):
                    count += 1
                    if count == len(self.wave_board):
                        return "Путь не найден"
                for x_0 in range(len(self.wave_board[0])):
                    if self.wave_board[y_0][x_0] == self.number_wave - 1:
                        cells = [(x_0 + 1, y_0), (x_0 - 1, y_0), (x_0, y_0 + 1), (x_0, y_0 - 1)]
                        for i in cells:
                            mx, my = i
                            if 0 <= my < len(self.wave_board) and 0 <= mx < len(self.wave_board[0]):
                                if self.wave_board[my][mx] != 0 and self.wave_board[my][mx] == 1:
                                    self.wave_board[my][mx] = self.number_wave
                                    if self.cortage_wave_board[y_0][x_0] == 0:
                                        self.cortage_wave_board[y_0][x_0] = []
                                    self.cortage_wave_board[y_0][x_0].append((mx, my))
                                    if my == y2 and x2 == mx:
                                        return "Нашелся путь!"
        self.number_wave += 1
        return self.has_path(x1, y1, x2, y2)

    def way(self, x1, y1, x2, y2, ct):
        px, py = x2, y2
        flag = True
        ct += 1
        for y in range(len(self.wave_board)):
            for x in range(len(self.wave_board[0])):
                if self.cortage_wave_board[y][x] != 0:
                    if (x2, y2) in self.cortage_wave_board[y][x]:
                        if ct == self.number_wave-3:
                            self.my_way[y][x] = 8
                            self.destination = (x, y)
                        else:
                            self.my_way[y][x] = 1
                        px, py = x, y
                        if x == x1 and y == y1:
                            return self.my_way
                        flag = False
                        break
            if not flag:
                break
        return self.way(x1, y1, px, py, ct)

    def run(self, pos_player):
        if self.go_flag:
            x, y = self.rect.center
            px, py = pos_player
            delta_x = (px - x) / 15
            delta_y = (py - y) / 15
            direction = (x, y) - Vector2(px, py)
            radius, angle = direction.as_polar()
            flag = True
            for j in range(15):
                for sprite1 in wall_sprite.sprites():
                    sx, sy, w, h = sprite1.rect
                    if sx + w > (x + j * delta_x) > sx and sy < (y + j * delta_y) < sy + h:
                        flag = False
                        break
                if not flag:
                    break
            delta_f_x = 80
            if flag:
                for i in range(4):
                    for j in range(15):
                        for sprite1 in wall_sprite.sprites():
                            sx, sy, w, h = sprite1.rect
                            if sx + w > (x + delta_f_x + j * delta_x) > sx and sy < (y + j * delta_y) < sy + h:
                                flag = False
                                break
                        if not flag:
                            break
                    if not flag:
                        break
                    delta_f_x -= 40
                    if delta_f_x == 0:
                        delta_f_x -= 40

            if flag:
                x2 = -cos(radians(-angle)) * (self.speed + 1)
                y2 = sin(radians(-angle)) * (self.speed + 1)
                self.rect = self.rect.move(x2, y2)
                self.rotate(x2, y2)
                self.flag_algoritm = False
            else:
                if self.flag_algoritm:
                    for sprite1 in floor_sprite.sprites():
                        if pygame.sprite.collide_mask(self, sprite1):
                            self.zom_pos = (sprite1.x, sprite1.y)
                            break
                    zx, zy = self.zom_pos
                    cx, cy = self.destination
                    if zx < cx:
                        self.x2 = self.speed
                        self.rect = self.rect.move(self.x2, self.y2)
                        self.rotate(self.x2, self.y2)
                    elif zx > cx:
                        self.x2 = -self.speed
                        self.rect = self.rect.move(self.x2, self.y2)
                        self.rotate(self.x2, self.y2)
                        self.count = 0
                    elif zy > cy:
                        self.y2 = -self.speed
                        self.rect = self.rect.move(self.x2, self.y2)
                        self.rotate(self.x2, self.y2)
                        self.count = 0
                    elif zy < cy:
                        self.y2 = self.speed
                        self.rect = self.rect.move(self.x2, self.y2)
                        self.rotate(self.x2, self.y2)
                        self.count = 0
                    else:
                        self.count += 1
                        self.rect = self.rect.move(self.x2, self.y2)
                        if self.count == 25:
                            self.x2 = 0
                            self.y2 = 0
                            self.flag_algoritm = False
                            self.count = 0
            if pygame.sprite.spritecollide(self, player_group, False):
                self.go_flag = False
                self.timer_att.start()


    def rotate(self, x, y):
        x_0, y_0 = self.rect.center
        direction = (x_0, y_0) - Vector2(x + x_0, y + y_0)
        radius, angle = direction.as_polar()
        self.image = pygame.transform.rotate(self.orig, -angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)

    def render(self):
        # ПИЗДЕЦ, ЧТО ЗА ХУЙНЯ?
        if self.hp <= 0:
            self.kill()
        else:
            x, y = self.rect.center
            len_line_hp = (150*self.hp)/self.max_hp
            pygame.draw.line(screen, RED, (x-75, y-80), (x-75+len_line_hp, y-80), 10)

    def time_effect(self):
        time.sleep(0.5)
        if pygame.sprite.spritecollide(self, player_group, False):
            player_group.sprites()[0].hp -= self.damage
        self.go_flag = True
        self.timer_att = threading.Thread(target=self.time_effect)


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(patrons_group, effects_group)
        self.image = load_image('стрела.png')
        self.rect = self.image.get_rect()
        self.flag = True
        self.damage = 5
        self.alpha = 90
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, self.alpha)
        self.timer = threading.Thread(target=self.time_effect)

    def set_view(self, pos_x, pos_y, alpha):
        self.alpha = alpha
        self.image = pygame.transform.rotate(self.image, self.alpha)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(pos_x+5, pos_y))

    def run(self):
        if self.flag:
            x2 = cos(radians(self.alpha)) * 7
            y2 = -sin(radians(self.alpha)) * 7
            self.rect = self.rect.move(x2, y2)
            if pygame.sprite.spritecollide(self, wall_sprite, False):
                self.timer.start()
                self.flag = False
            else:
                for sprite2 in zombie_group.sprites():
                    if pygame.sprite.collide_mask(self, sprite2):
                        sprite2.hp -= self.damage
                        self.timer.start()
                        self.flag = False
                        break




    def time_effect(self):
        ct = 0
        while True:
            ct += 1
            if ct == 2:
                self.kill()
                break
            time.sleep(1)


class WeaponIcon:
    def __init__(self):
        self.image = ''
        self.flag_image = False
        self.allinventory_coordinate = [0, 0, 0, 0, 0]

    def mousebuttondown(self, mouse_pos):
        if self.flag_image:
            self.rect = self.image.get_rect(center=mouse_pos)

    def mousebuttonup(self, pos_x, pos_y, left, top, cs):
        self.kill()
        inventory_group.add(self)
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

    def purpose_basic_inventory(self, pos_x, pos_y, left, top, cs):
        basic_inventory_group.add(self)
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
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image)
        self.orig = self.image
        self.count = 1



class OnionIcon(WeaponIcon, pygame.sprite.Sprite):
    def __init__(self, image):
        WeaponIcon.__init__(self)
        pygame.sprite.Sprite.__init__(self, inventory_group)
        self.image = load_image(image)
        self.orig = self.image


class SwordIcon(WeaponIcon, pygame.sprite.Sprite):
    def __init__(self, image):
        WeaponIcon.__init__(self)
        pygame.sprite.Sprite.__init__(self, inventory_group)
        self.image = load_image(image)
        self.orig = self.image


class Sword(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(effects_group)
        self.radius = 120
        self.damage = 2
        self.image = load_image('effect_sword1.png')
        self.rect = self.image.get_rect()
        self.timer = threading.Thread(target=self.time_effect)
        self.x = 0
        self.y = 0
        self.alpha = 0
        self.betta = 60
        self.posx = 0
        self.posy = 0
        self.flag = True

    def set_view(self, posx, posy, alpha):
        self.alpha = alpha
        self.x = posx + self.radius * cos(radians(alpha))
        self.y = posy + -self.radius * sin(radians(alpha))
        self.posx = posx
        self.posy = posy

    def run(self):
        if self.flag:
            self.image = pygame.transform.rotate(self.image, self.alpha + 135)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            for sprite1 in zombie_group.sprites():
                x, y = sprite1.rect.center
                radius, angle = self.rotate(self.posx, self.posy, x, y)
                if radius > self.radius:
                    pass
                else:
                    new_alpha_1 = self.alpha + self.betta
                    new_alpha_2 = self.alpha - self.betta
                    if new_alpha_1 < 0 and new_alpha_2 < 0 and (-angle > 0):
                        angle = -angle
                    if min(new_alpha_1, new_alpha_2) <= -angle <= max(new_alpha_2, new_alpha_1):
                        sprite1.hp -= self.damage
            self.timer.start()
            self.flag = False

    def rotate(self, x1, y1, x2, y2):
        direction = (x2, y2) - Vector2(x1, y1)
        radius, angle = direction.as_polar()
        return radius, angle

    def time_effect(self):
        ct = 0
        while True:
            ct += 1
            time.sleep(1)
            if ct == 1:
                self.kill()
                break



class AllInventory:
    def __init__(self):
        self.flag = False
        self.width = 5
        self.height = 5
        self.cell_size = 150
        self.top = 125
        self.left = 375
        self.inventory = [[0] * self.width for i in range(self.height)]

    def append(self):
        self.inventory[0][1] = ArrowIcon('стрела_icon.png')
        self.inventory[0][1].add_allinventory(1, 0, self.left, self.top, self.cell_size)
        self.inventory[1][1] = SwordIcon('sword.png')
        self.inventory[1][1].add_allinventory(1, 1, self.left, self.top, self.cell_size)
        self.inventory[1][2] = OnionIcon('лук_icon.png')
        self.inventory[1][2].add_allinventory(2, 1, self.left, self.top, self.cell_size)
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


    def get_obj(self, player, *args):
        if args[0] == pygame.K_e:
            free_places = []
            for y in range(self.height):
                for x in range(self.width):
                    if self.inventory[y][x] == 0:
                        free_places.append((x, y))
            if len(free_places) != 0:
                sprites = []
                old_weapon_map = weapon_on_map.sprites()
                if pygame.sprite.spritecollide(player, weapon_on_map, True):
                    for sprite in old_weapon_map:
                        if not sprite in weapon_on_map.sprites():
                            sprites.append(sprite)
                    if len(sprites) != 0:
                        for i in free_places:
                            if len(sprites) == 0:
                                break
                            x, y = i
                            obj = choice(sprites)
                            self.inventory[y][x] = obj
                            obj.add_allinventory(x, y, self.left, self.top, self.cell_size)
                            sprites.remove(obj)
                        for i in sprites:
                            i.add(all_sprites)
                            i.add(weapon_on_map)

    def all_mousebuttondown(self, mouse_pos):
        for y in range(self.height):
            for x in range(self.width):
                if self.inventory[y][x] != 0:
                    self.inventory[y][x].mousebuttondown(mouse_pos)


class BasicInventory(AllInventory):
    def __init__(self):
        super().__init__()
        self.basic_inventory = self.inventory[self.height-1]
        self.top = 850
        self.binding = {pygame.K_1: 0,
                        pygame.K_2: 1,
                        pygame.K_3: 2,
                        pygame.K_4: 3,
                        pygame.K_5: 4}
        self.cursor = 0
        self.keys = []
        for key in self.binding.keys():
            self.keys.append(key)
    def render(self):
        for x in range(self.width):
            pygame.draw.rect(screen, GREY_3, (
                    x * self.cell_size + self.left, 0 * self.cell_size + self.top, self.cell_size,
                    self.cell_size))
            pygame.draw.rect(screen, GREY_1, (
                x * self.cell_size + self.left, 0 * self.cell_size + self.top, self.cell_size, self.cell_size), 10)
            if self.basic_inventory[x] != 0:
                self.basic_inventory[x].purpose_basic_inventory(x, 0, self.left, self.top, self.cell_size)

    def update(self, inventor):
        self.basic_inventory = inventor[4]

    def treatment(self, *args):
        if args[0] in self.keys:
            self.cursor = self.binding[args[0]]

    def attacked_obj(self):
        a = str(self.basic_inventory[self.cursor]).split()
        a = a[0][1:] + a[1][:6]
        if a == 'OnionIconSprite':
            patron = Arrow()
            patron.set_view(player.rect.center[0], player.rect.center[1], player.alpha)
        if a == 'SwordIconSprite':
            patron = Sword()
            patron.set_view(player.rect.center[0], player.rect.center[1], player.alpha)
            b = ''
            # if a in connect_obj.keys():
            #     if isinstance(connect_obj[a], dict):
            #         for j in connect_obj[a].keys():
            #             b = j
            #         for y in range(self.height):
            #             for x in range(self.width):
            #                 if self.inventory[y][x] != 0:
            #                     cl = str(self.inventory[y][x]).split()
            #                     cl = cl[0][1:] + cl[1][:6]
            #                     if cl == b:
            #                         patron = connect_obj[a][b]
            #                         patron.set_view(player.rect.center[0], player.rect.center[1], player.alpha)





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
                WallBlock(x, y)
            if laberinte[y][x] == 1:
                FloorBlock(x, y)
            if laberinte[y][x] == 2:
                FloorBlock(x, y)
                px, py = x, y
    new_player = Player(px, py, all_sprites, wall_sprite)
    laberinte[py][px] = 1
    return new_player

def generate_zombie():
    ct = 0
    while True:
        ct += 1
        if ct % 5 == 0:
            pos_zombie = (randint(0, WIDTH-1), randint(0, HEIGHT-1))
            while laberinte[pos_zombie[1]][pos_zombie[0]] != 1:
                pos_zombie = (randint(0, WIDTH - 1), randint(0, HEIGHT - 1))
            for sprite in floor_sprite.sprites():
                if (sprite.x, sprite.y) == pos_zombie:
                    OrdinaryZombie2('zombie_UP.png', sprite.rect.center)
                    break
        time.sleep(1)
def generate_ghost():
    # ct = 0
    # while True:
    #     ct += 1
    #     if ct % 15 == 0:
    #         OrdinaryZombie2('zombie_UP.png')
    pass


SIZE = W, H = (1500, 1000)
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
spawn_zombie = threading.Thread(target=generate_zombie)
spawn_qhost = threading.Thread(target=generate_ghost)
#размер кнопки
cell_size = 300
WIDTH = 20
HEIGHT = 15
board = Board(20, 15)
board.set_view(50)
camera = Camera()
inventory = AllInventory()
inventory.append()
basic_inventory = BasicInventory()
MAIN_ROOM = MainRoom()
MAIN_ROOM.load_sprites()
laberinte = board.print_laberinte()
player = generate_level(laberinte)
MAIN_ROOM_PLAYER = Player(0, 0, MAIN_ROOM_ALL_SPRITES, MAIN_ROOM_COLLIDE_SPRITES)
connect_obj = {'SwordIconSprite': partial(Sword),
               'OnionIconSprite': {'ArrowIconSprite': partial(Arrow)}}
IN_MAIN_MENU = True
IN_GAME = False
TRANSFORM = False
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)
    if IN_MAIN_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                inventory.open_inventory(event.key)
                inventory.get_obj(MAIN_ROOM_PLAYER, event.key)
            if inventory.flag:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    inventory.get_click(pygame.mouse.get_pos(), 'MOUSEBUTTONDOWN', MAIN_ROOM_PLAYER.rect)
                if event.type == pygame.MOUSEBUTTONUP:
                    inventory.get_click(pygame.mouse.get_pos(), 'MOUSEBUTTONUP', MAIN_ROOM_PLAYER.rect)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in MAIN_ROOM_DOOR_SPRITES:
                        mx, my = pygame.mouse.get_pos()
                        if i.rect[0] <= mx <= i.rect[0] + 160 and i.rect[1] <= my <= i.rect[1] + 50:
                            TRANSFORM = True
                            IN_MAIN_MENU = False
        if not inventory.flag:
            MAIN_ROOM_PLAYER.rotate()
            MAIN_ROOM_PLAYER.update(pygame.key.get_pressed())
        camera.update(MAIN_ROOM_PLAYER)
        # обновляем положение всех спрайтов
        for sprite in MAIN_ROOM_ALL_SPRITES:
            camera.apply(sprite)
        MAIN_ROOM_PLAYER.kill()
        MAIN_ROOM_ALL_SPRITES.add(MAIN_ROOM_PLAYER)
        MAIN_ROOM_ALL_SPRITES.draw(screen)
        if inventory.flag:
            inventory.render()
            inventory.all_mousebuttondown(pygame.mouse.get_pos())
            inventory_group.draw(screen)

    if TRANSFORM:
        TRANSFORM = False
        screen.fill("BLACK")
        IN_GAME = True
        spawn_zombie.start()
    if IN_GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                inventory.open_inventory(event.key)
                inventory.get_obj(player, event.key)
            if inventory.flag:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    inventory.get_click(pygame.mouse.get_pos(), 'MOUSEBUTTONDOWN', player.rect)
                if event.type == pygame.MOUSEBUTTONUP:
                    inventory.get_click(pygame.mouse.get_pos(), 'MOUSEBUTTONUP', player.rect)
            else:
                if event.type == pygame.KEYDOWN:
                    basic_inventory.treatment(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # s = Sword()
                    # s.run(player.alpha, player.rect.center)
                    # s.timer.start()
                    # k = Arrow('стрела.png')
                    # k.set_view(player.rect.center[0], player.rect.center[1], player.alpha)
                    # k.flag = True
                    basic_inventory.attacked_obj()
        if not inventory.flag:
            player.rotate()
            player.update(pygame.key.get_pressed())
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        player.kill()
        player_group.add(player)
        all_sprites.add(player)
        all_sprites.draw(screen)
        for sprite in effects_group:
            camera.apply(sprite)
        effects_group.draw(screen)
        basic_inventory.update(inventory.inventory)
        basic_inventory.render()
        basic_inventory_group.draw(screen)
        if inventory.flag:
            inventory.render()
            inventory.all_mousebuttondown(pygame.mouse.get_pos())
            inventory_group.draw(screen)
        # draw_ray(player.alpha, player.rect.center, 125)
        for sprite in patrons_group:
            camera.apply(sprite)
            sprite.run()
        patrons_group.draw(screen)
        for sprite1 in zombie_group.sprites():
            sprite1.render()
            if not sprite1.flag_algoritm:
                pos = ()
                for sprite in floor_sprite.sprites():
                    if pygame.sprite.collide_mask(sprite, player):
                        pos = (sprite.x, sprite.y)
                        break

                sprite1.set_view(20, 15, laberinte, pos)
                sprite1.flag_algoritm = True
            sprite1.run(player.rect.center)
        zombie_group.draw(screen)
        player.render()
        for sprite1 in effects_group.sprites():
            sprite1.run()
    pygame.display.flip()

sys.exit(pygame.quit())