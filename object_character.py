import pygame
from data import *
import math

#загальний клас для бота та героя
class ObjectCharacter(pygame.Rect):
    def __init__(self, x, y, width, height, image, step):
        super().__init__(x, y, width, height)
        self.X = x
        self.Y = y
        self.IMAGE = image      #основна картинка яка має бути в момент
        self.IMAGE_NOW = self.IMAGE #зображення яке демонструється на екран
        self.IMAGE_MOVE = 0     #змінна для зміни зображень(симуляція хотьби)
        self.STEP = step        #довжина кроку

#клас бота
class Bot(ObjectCharacter):
    def __init__(self, x, y, width, height, image, step):
        super().__init__(x, y, width, height, image, step)
        self.FOOD = False
    
    def angle(self, enemy):
        x = self.x - enemy.x
        d = (((abs(self.x - enemy.x) ** 2) + (abs(self.y - enemy.y) ** 2)) ** 0.5)
        #print(f"катет = {x}, гіпотенуза = {d}")
        if d == 0:
            d = 0.01
        sin = abs(x) / d
        degree = math.asin(sin) / 3.1415 * 180
        triang_x = enemy.x - self.x
        triang_y = enemy.y - self.y

        #визначеня кута для повороту зображення та повернення кута в напрямку героя
        if triang_x < 0 and triang_y <= 0:     #4 четверті
            self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 270 + degree)
            return 180 + degree
        elif triang_x >= 0 and triang_y < 0:         #3 четверті
            self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 270 - degree)
            return 180 - (90 + degree) + 90
        elif triang_x > 0 and triang_y >= 0:        #2 четверті
            self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 90 + degree)
            return degree
        elif triang_x <= 0 and triang_y > 0:   #1 четверті
            self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 90 - degree)
            return 360 - (270 + degree) + 270
        return degree

    #метод для руху
    def step(self, enemy):
        #в залежності від кута повороту бота, далі ми визначаємо дистанцію проходу по х та по у
        degree = self.angle(enemy)
        y = math.cos(math.radians(degree)) * self.STEP
        x = math.cos(math.radians(90 - degree)) * self.STEP
        #x = ((self.STEP ** 2 - y ** 2) ** 0.5)
        self.X += x
        self.Y += y
        self.x = self.X
        self.y = self.Y
        if self.collidelist(wall_list) != -1:
            self.X -= x
            self.Y -= y
            self.x = self.X
            self.y = self.Y

            if True:
                pass
        #print(x, y, degree)


#клас героя
class Hero(ObjectCharacter):
    def __init__(self, x, y, width, height, image, step):
        super().__init__(x, y, width, height, image, step)
        self.MOVE = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}     #словник для визначення напрямку руху
        #об'єкт ректа для постійного підтримання основи при поворотах, щоб не переходити скрізь стінку
        self.RECT = pygame.Rect(self.x, self.y + self.height // 2 - self.width // 2, self.width, self.width)
        self.TEST = [False, False, False, False]
        self.WHO_MOVE = 2
        self.SHOT = False
        self.BULLET = []
    
    #def imageRotate(self, test, test_list, agle):
    #    if not test:
    #        self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, agle)
    #        self.TEST = test_list

    def imageStayRotate(self, image):
        if self.TEST[0]:
            self.IMAGE_NOW = pygame.transform.rotate(image, 90)
            self.TEST[0] = False
        elif self.TEST[1]:
            self.IMAGE_NOW = pygame.transform.rotate(image, 270)
            self.TEST[1] = False
        elif self.TEST[2]:
            self.IMAGE_NOW = pygame.transform.rotate(image, 180)
            self.TEST[2] = False
        elif self.TEST[3]:
            self.IMAGE_NOW = pygame.transform.rotate(image, 0)
            self.TEST[3] = False

    def move(self):
        if self.WHO_MOVE == 0:
            if not self.MOVE["UP"] and not self.MOVE["DOWN"] and not self.MOVE["LEFT"] and not self.MOVE["RIGHT"]:
                self.imageStayRotate(image_hero[0])
                self.IMAGE_MOVE = 0
            else:
                self.IMAGE = move_empty[int(self.IMAGE_MOVE // 10)]
                #print(int(self.IMAGE_MOVE // 10), self.IMAGE)
        elif self.WHO_MOVE == 1:
            if not self.MOVE["UP"] and not self.MOVE["DOWN"] and not self.MOVE["LEFT"] and not self.MOVE["RIGHT"]:
                self.imageStayRotate(image_hero[1])
                self.IMAGE_MOVE = 0
            else:
                self.IMAGE = move_with_gun[int(self.IMAGE_MOVE // 10)]
        elif self.WHO_MOVE == 2:
            if not self.MOVE["UP"] and not self.MOVE["DOWN"] and not self.MOVE["LEFT"] and not self.MOVE["RIGHT"]:
                self.imageStayRotate(image_hero[2])
                self.IMAGE_MOVE = 0
            else:
                self.IMAGE = move_with_gun_shot[int(self.IMAGE_MOVE // 10)]
        if self.MOVE["UP"] and self.y > 0:
            self.RECT.y -= self.STEP
            if self.RECT.collidelist(wall_list) == -1:          #якщо герой не зіткнувся з перешкодою то
                self.y -= self.STEP         # то ми робимо реальний крок героєм
                # перевіряємо чи герой вже повертав в потрібну сторону, але є проблема при зміні картинки ми сюди не заходимо
                if not self.TEST[0]:         
                    self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 90)    # і якщо не повертав, то повертаємо
                    self.TEST = [True, False, False, False]
                self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 90)
                self.IMAGE_MOVE += 1
                #self.imageRotate(self.TEST[0], [True, False, False, False], 90)
            else:
                self.RECT.y += self.STEP
        elif self.MOVE["DOWN"] and self.y < setting_win["HEIGHT"] - self.height:
            self.RECT.y += self.STEP
            if self.RECT.collidelist(wall_list) == -1:
                self.y += self.STEP
                if not self.TEST[1]:
                    self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 270)
                    self.TEST = [False, True, False, False]
                self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 270)
                self.IMAGE_MOVE += 1
                #self.imageRotate(self.TEST[1], [False, True, False, False], 270)
            else:
                self.RECT.y -= self.STEP
        elif self.MOVE["LEFT"] and self.x > 0:
            self.RECT.x -= self.STEP
            if self.RECT.collidelist(wall_list) == -1:
                self.x -= self.STEP
                if not self.TEST[2]:
                    self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 180)
                    self.TEST = [False, False, True, False]
                self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 180)
                self.IMAGE_MOVE += 1
                #self.imageRotate(self.TEST[2], [False, False, True, False], 180)
            else:
                self.RECT.x += self.STEP
        elif self.MOVE["RIGHT"] and self.x < setting_win["WIDTH"] - self.width:
            self.RECT.x += self.STEP
            if self.RECT.collidelist(wall_list) == -1:
                self.x += self.STEP
                if not self.TEST[3]:
                    self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 0)
                    self.TEST = [False, False, False, True]
                self.IMAGE_NOW = pygame.transform.rotate(self.IMAGE, 0)
                self.IMAGE_MOVE += 1
                #self.imageRotate(self.TEST[3], [False, False, False, True], 0)
            else:
                self.RECT.x -= self.STEP
        if self.IMAGE_MOVE == 40:
            self.IMAGE_MOVE = 0
        
class Shot(pygame.Rect):
    def __init__(self):
        pass
#створення класа пули
class Bullet(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.IMAGE = bullet_image
        self.X = 0
        self.Y = 0
        self.STEP = 8

    #розрахунок кута повороту пулі при пострілі
    def make_angle(self, x, y, heroX, heroY):
        leg = abs(x - heroX)
        hypotenuse = (leg ** 2 + abs(y - heroY) ** 2) ** 0.5
        if hypotenuse == 0:
            hypotenuse = 0.01
        sin = leg / hypotenuse
        degree = math.asin(sin) / 3.1415 * 180
        triang_x = heroX - x
        triang_y = heroY - y
        if triang_x < 0 and triang_y <= 0:     #4 четверті
            self.X = math.cos(math.radians(180 - 90-degree)) * self.STEP
            self.Y = math.cos(math.radians(degree)) * self.STEP
            degree = 270 + degree
            
        elif triang_x >= 0 and triang_y < 0:         #3 четверті
            self.X = math.cos(math.radians(180 - 90-degree)) * self.STEP * -1
            self.Y = math.cos(math.radians(degree)) * self.STEP
            degree = 180 + (90 - degree)

        elif triang_x > 0 and triang_y >= 0:        #2 четверті
            self.X = math.cos(math.radians(180 - 90-degree)) * self.STEP * -1
            self.Y = math.cos(math.radians(degree)) * self.STEP * -1
            degree = 90 + degree

        elif triang_x <= 0 and triang_y > 0:   #1 четверті
            self.X = math.cos(math.radians(180 - 90-degree)) * self.STEP
            self.Y = math.cos(math.radians(degree)) * self.STEP * -1
            degree = 90 - degree

        #print(f"Bullet X: {self.X}, Y: {self.Y}", abs(self.X) + abs(self.Y))
        #print(f"HERO X: {heroX}, Y: {heroY}")
        #print(f"click X: {x}, Y: {y}")
        #
        #print(degree)
        self.IMAGE =  pygame.transform.rotate(self.IMAGE, degree)

class Tp(pygame.Rect):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height)
        self.IMAGE_LIST = image
        self.IMAGE = self.IMAGE_LIST[0]
        self.IMAGE_MOVE = 0
    #рух телепорта
    def move(self):
        if self.IMAGE_MOVE % 10 == 0:
            if self.IMAGE_MOVE == 40:
                self.IMAGE_MOVE = 0
            self.IMAGE = self.IMAGE_LIST[self.IMAGE_MOVE // 10]
        self.IMAGE_MOVE += 1
