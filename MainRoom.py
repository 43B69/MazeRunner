import os
import sys
import pygame

# Путь к файлу с текстурами
MAIN_ROOM_TEXTURE_FILE_NAME = "data/MAIN_ROOM_TEXTURES_UP_10.png"
# Здесь чисто риторическая проверка
if not os.path.isfile(MAIN_ROOM_TEXTURE_FILE_NAME):
    print(f"Отсутствует data-файл: {MAIN_ROOM_TEXTURE_FILE_NAME}")
    sys.exit()
# А это плоскость с нашей текстурой
MAIN_ROOM_TEXTURE_IMAGE = pygame.image.load(MAIN_ROOM_TEXTURE_FILE_NAME)
# В теории, у нас создаётся всего одна копия главного меню, поэтому
# подобную историю я мог разместить в классе, запихав туда и
# спрайты и прочее. Но так как я возможно добавлю изменение
# окружение комнаты ГГ, то пусть они лежат в global.
# P.S. Это самый простой метод грузить их в главной программе
# - Это все спрайты
MAIN_ROOM_ALL_SPRITES = pygame.sprite.Group()
# - Спрайты для разных объектов
MAIN_ROOM_AMBIENT_SPRITES = pygame.sprite.Group()
# - Спрайты для стен
MAIN_ROOM_WALLS_SPRITES = pygame.sprite.Group()
# - Спрайты пола
MAIN_ROOM_FLOOR_SPRITES = pygame.sprite.Group()
# - Группа с которой игрок будет сталкиваться
MAIN_ROOM_DOOR_SPRITES = pygame.sprite.Group()
# - Группа спрайтов с дверями
MAIN_ROOM_BED_SPRITES = pygame.sprite.Group()
# - Группа спрайтов с которыми сталкиваемся
MAIN_ROOM_COLLIDE_SPRITES = pygame.sprite.Group()
# - Это спрайт коробки
MAIN_ROOM_BOX_SPRITES = pygame.sprite.Group()


# Класс отвечающий за окружающие игрока предметы (вообще все)
class Ambient(pygame.sprite.Sprite):
    # pos_x и pos_y - позиции по x и y
    # sprite_size - размер спрайта
    # coordinates_in_texture - координаты по которым вырезаем
    # sprite_group - ссылка на группу спрайтов
    # support_sprite_group - только в тех случаях, если необходимо собственное назначение
    def __init__(self, pos_x, pos_y, coordinates_in_texture, sprite_group, support_sprite_group=MAIN_ROOM_ALL_SPRITES):
        if support_sprite_group != MAIN_ROOM_ALL_SPRITES:
            super().__init__(MAIN_ROOM_ALL_SPRITES, sprite_group, support_sprite_group)
        else:
            super().__init__(MAIN_ROOM_ALL_SPRITES, sprite_group)
        global MAIN_ROOM_TEXTURE_IMAGE
        # производим вырез нужного блока
        self.image = MAIN_ROOM_TEXTURE_IMAGE.subsurface(coordinates_in_texture)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


# Это главная комната (по совместительству и главное меню)
class MainRoom:
    def __init__(self):
        # Коэффициент изменения (С этой штукой мы просто меняем размер спрайтов исходя из названия картинки)
        self.ss = int(MAIN_ROOM_TEXTURE_FILE_NAME.split(".")[0].split("_")[-1])
        # Карта комнаты с планировкой:
        # H - стена горизонтальная;     1 - левый верх;     3 - левый низ
        # V - стена вертикальная;   2 - правый верх;        4 - правый низ
        # B - кровать;  . - пол;    D - дверь;    T - стол;   W - окно
        # X - коробка;    S - оружейный стол
        self.map = [
            "1HWWWH2",
            "VB..T.V",
            "V.....V",
            "V.....V",
            "VX...SV",
            "V.....V",
            "3HHDHH4"
        ]
        # Здесь хранятся трафареты для всех спрайтов в
        self.room_main = {
            "1": [(5 * self.ss, 5 * self.ss), (144 * self.ss, 10 * self.ss, 5 * self.ss, 5 * self.ss)],
            "2": [(5 * self.ss, 5 * self.ss), (152 * self.ss, 10 * self.ss, 5 * self.ss, 5 * self.ss)],
            "3": [(5 * self.ss, 5 * self.ss), (144 * self.ss, 18 * self.ss, 5 * self.ss, 5 * self.ss)],
            "4": [(5 * self.ss, 5 * self.ss), (152 * self.ss, 18 * self.ss, 5 * self.ss, 5 * self.ss)],
            "H": [(16 * self.ss, 5 * self.ss), (136 * self.ss, 2 * self.ss, 16 * self.ss, 5 * self.ss)],
            "V": [(5 * self.ss, 16 * self.ss), (136 * self.ss, 10 * self.ss, 5 * self.ss, 16 * self.ss)],
            ".": [(16 * self.ss, 16 * self.ss), (3 * self.ss, 2 * self.ss, 16 * self.ss, 16 * self.ss)],
            "W": [(16 * self.ss, 5 * self.ss), (136 * self.ss, 28 * self.ss, 16 * self.ss, 5 * self.ss)],
            "D": [(16 * self.ss, 5 * self.ss), (136 * self.ss, 35 * self.ss, 16 * self.ss, 5 * self.ss)],
        }
        # Словарь с различными объектами комнаты (или проще - мебелью)
        self.room_ambient = {
            "B": [(30 * self.ss, 50 * self.ss), (160 * self.ss, 2 * self.ss, 30 * self.ss, 50 * self.ss)],
            "P": [(16 * self.ss, 16 * self.ss), (3 * self.ss, 2 * self.ss, 16 * self.ss, 16 * self.ss)],
            "T": [(32 * self.ss, 30 * self.ss), (101 * self.ss, 3 * self.ss, 32 * self.ss, 30 * self.ss)],
            "X": [(35 * self.ss, 32 * self.ss), (53 * self.ss, 2 * self.ss, 35 * self.ss, 32 * self.ss)],
            "S": [(16 * self.ss, 32 * self.ss), (30 * self.ss, 2 * self.ss, 16 * self.ss, 32 * self.ss)],
        }

    # Функция для зрузкипрайтов
    def load_sprites(self):
        start_x, start_y = -470, -400
        # Делим эту функцию на два этапа:
        # 1 этап - отрисовка самой комнаты

        # Задаём актуальные координаты
        act_x, act_y = start_x, start_y
        # Начинаем идти по данным
        for i in self.map:
            for j in i:
                # Защита, в случае если словим объект из AMBIENT
                buff = self.room_main["."]
                if j in self.room_main:
                    if j == ".":
                        Ambient(act_x, act_y, buff[1], MAIN_ROOM_FLOOR_SPRITES)
                    else:
                        buff = self.room_main[j]
                        if j == "D":
                            Ambient(act_x, act_y, buff[1], MAIN_ROOM_COLLIDE_SPRITES, MAIN_ROOM_DOOR_SPRITES)
                        else:
                            Ambient(act_x, act_y, buff[1], MAIN_ROOM_COLLIDE_SPRITES)
                else:
                    Ambient(act_x, act_y, buff[1], MAIN_ROOM_FLOOR_SPRITES)
                # прибавляем координаты для сдвига рисования
                act_x += buff[0][0]
            # Возвращаем обратно
            act_x = start_x
            # Прибавляем максимальный размер
            act_y += max([self.room_main[j][1][3] for j in i if j in self.room_main])

        # Этап 2 - добавляем в комнату разные элементы
        act_x, act_y = start_x, start_y
        for i in self.map:
            for j in i:
                if j in self.room_main:
                    # Просто прибавим размеры объекты по X
                    act_x += self.room_main[j][0][0]
                else:
                    # А вот теперь делаем загрузку в память данных из словаря
                    buff = self.room_ambient[j]
                    if j == "X":
                        Ambient(act_x, act_y, buff[1], MAIN_ROOM_COLLIDE_SPRITES, MAIN_ROOM_BOX_SPRITES)
                    elif j == "B":
                        Ambient(act_x, act_y, buff[1], MAIN_ROOM_COLLIDE_SPRITES, MAIN_ROOM_BED_SPRITES)
                    else:
                        Ambient(act_x, act_y, buff[1], MAIN_ROOM_COLLIDE_SPRITES)
                    act_x += 16 * self.ss
            act_x = start_x
            # Вот здесь в массив пойдут все, но я не нашёл варианта поиска сразу в обоих
            act_y += min([self.room_ambient[j][1][3] if j in self.room_ambient else self.room_main[j][1][3] for j in i])

'''
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
from MainRoom import *
import threading
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, user_groups, walls_groups):
        super().__init__(player_group, user_groups)
        self.alpha = 0
        self.image = pygame.transform.rotate(load_image('player2C.png'), self.alpha)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            cell_size * pos_x, cell_size * pos_y)
        self.speed = 20
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
#размер кнопки
cell_size = 300
WIDTH = 20
k = Arrow('стрела.png')
HEIGHT = 15
board = Board(20, 15)
board.set_view(50)
camera = Camera()
inventory = AllInventory()
inventory.append()
basic_inventory = BasicInventory()
laberinte = board.print_laberinte()
player = generate_level(laberinte)
MAIN_ROOM = MainRoom()
MAIN_ROOM.load_sprites()
MAIN_ROOM_PLAYER = Player(0, 0, MAIN_ROOM_ALL_SPRITES, MAIN_ROOM_COLLIDE_SPRITES)
connect_obj = {'SwordIconSprite': partial(Sword)}

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
        laberinte = board.print_laberinte()
        player = generate_level(laberinte)
        IN_GAME = True

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
                    s = Sword()
                    s.run(player.alpha, player.rect.center)
                    s.timer.start()
                    k = Arrow('стрела.png')
                    k.set_view(player.rect.center[0], player.rect.center[1], player.alpha)
                    k.flag = True
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
        k.run()
        for sprite in patrons_group:
            camera.apply(sprite)
            sprite.run()
        patrons_group.draw(screen)
        zombie_group.draw(screen)
    pygame.display.flip()
sys.exit(pygame.quit())
'''