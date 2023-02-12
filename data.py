import os
import pygame
from create_json import *

setting_win = read_json("setting_win.json")

maps = read_json("maps.json")

wall_list = list()

test_speed = list()

bots_list = list()

abs_path = os.path.abspath(__file__ + "/..") + "\\image\\"

image_hero = list()
name_move = ["hero_stay.png", "hero_stay_with_gun.png", "hero_stay_with_gun_shot.png", "hero_move_1.png", "hero_move_2.png",
            "hero_move_with_gun_1.png", "hero_move_with_gun_2.png", "hero_move_with_gun_shot_1.png", "hero_move_with_gun_shot_2.png"]
for name in name_move:
    image_hero.append(pygame.image.load(abs_path + "\\hero\\" + name))

move_empty = [image_hero[3], image_hero[0], image_hero[4], image_hero[0]]
move_with_gun = [image_hero[5], image_hero[1], image_hero[6], image_hero[1]]
move_with_gun_shot = [image_hero[7], image_hero[2], image_hero[8], image_hero[2]]
tp_image = [
    pygame.image.load(abs_path + "\\tp\\tp_1.png"),
    pygame.image.load(abs_path + "\\tp\\tp_2.png"),
    pygame.image.load(abs_path + "\\tp\\tp_3.png"),
    pygame.image.load(abs_path + "\\tp\\tp_2.png"),
]

wall_image = pygame.image.load(abs_path + "wall.png")
alian_eazy_move_1_image = pygame.image.load(abs_path + "\\monster\\" + "alian_eazy_move_1.png")
alian_eazy_move_2_image = pygame.image.load(abs_path + "\\monster\\" + "alian_eazy_move_2.png")
alian_eazy_stay_image = pygame.image.load(abs_path + "\\monster\\" + "alian_eazy_stay.png")
bullet_image = pygame.image.load(abs_path + "bullet.png")
key_image = pygame.image.load(abs_path + "key.png")