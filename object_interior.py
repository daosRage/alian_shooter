import pygame
from data import *

class ObjectInterior(pygame.Rect):
    def __init__(self, x, y, weight, height, image):
        super().__init__(x, y, weight, height)
        self.IMAGE = image

class Wall(ObjectInterior):
    def __init__(self, x, y, weight, height, image):
        super().__init__(x, y, weight, height, image)

def create_wall(key_map):
    x, y = 0, 0
    
    for string in maps[key_map]:
        for element in string:
            if element == "1":
                wall_list.append(Wall(x, y, 20, 100, wall_image))
            if element == "2":
                wall_list.append(Wall(x, y, 100, 20, pygame.transform.rotate(wall_image, 90)))
            x += 20
        x = 0
        y += 20