import random
import os
import pygame
from pygame import draw
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, KEYDOWN

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 100)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))



def create_enemy():
    enemy_size = (40, 40)
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, 700), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2000)

enemies = []



def create_bonus():
    bonus_size = (50, 50)
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(random.randint(100, 1100), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0
    
    def append_option(self, option, callback):
        self._option_surfaces.append(FONT.render(option, True, COLOR_BLACK))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (COLOR_GREEN), option_rect)
            surf.blit(option, option_rect)



playing = True
game = True



def play():

    IMAGE_PATH = "Goose"
    PLAYER_IMAGES = os.listdir(IMAGE_PATH)

    player_size = (20, 20)
    player = pygame.image.load("player.png").convert_alpha()
    player_rect = pygame.Rect(20, 400, *player_size)

    player_move_down = [0, 4]
    player_move_right = [4, 0]
    player_move_up = [0, -4]
    player_move_left = [-4, 0]

    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move = 3

    score = 0
    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 3000)

    CHANGE_IMAGE = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMAGE, 200)

    bonuses = []

    image_index = 0
    global playing

    while playing:
        FPS.tick(200)
        print("Yes")
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False

            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())

            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())

            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0


        bg_X1 -= bg_move
        bg_X2 -= bg_move

        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()

        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))


        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)

        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)

        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)

        if keys[K_LEFT] and player_rect.right > 0:
            player_rect = player_rect.move(player_move_left)


        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                playing = False

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.pop(bonuses.index(bonus))

        main_display.blit(player, player_rect)
        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))


    pygame.display.flip()

    
    
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))



menu = Menu()
menu.append_option("PLAY", play)
# menu.append_option("EXIT", game = False)

while game:
    FPS.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                menu.switch(-1)
            elif event.key == K_DOWN:
                menu.switch(1)
            elif event.key == K_SPACE:
                menu.select()

    main_display.blit(bg, (0, 0))

    menu.draw(main_display, 600, 400, 200)

    pygame.display.flip()