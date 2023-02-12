import pygame
from data import *
from object_character import *
from object_interior import *
import time

pygame.init()

window = pygame.display.set_mode((setting_win["WIDTH"], setting_win["HEIGHT"]))


def run():
    game = True
    health = 3
    respawn = 1
    respawn1 = 1
    respawn2 = 1
    amount= 0
    amount1= 0
    amount2= 0
    alian_show_key = False
    alian_show_key1 = False
    alian_show_key2 = False
    key_lvl = 0
    hero = Hero(100, 100, 25, 50, image_hero[1], 5)
    tp = Tp(800, 150, 100, 150, tp_image)
    clock = pygame.time.Clock()

    #надписи у грі
    font_health = pygame.font.SysFont("Arial", 20)
    render_health = font_health.render("Життя", True, (255, 87, 88))
    render_health_value = font_health.render(str(health), True, (255, 87, 88))
    font_win_loose = pygame.font.SysFont("Arial", 50)
    render_win = font_win_loose.render("Перемога", True, (13, 251, 103))
    render_loose = font_win_loose.render("Програш", True, (214, 35, 0))
    
    start_create_bots_1 = pygame.Rect(380, 340, 200, 15)
    start_create_bots_2 = pygame.Rect(280, 560, 200, 15)

    key1 = pygame.Rect(280, 10, 40, 19)
    key2 = pygame.Rect(940, 560, 40, 19)
    
    create_wall("MAP1")

    while game:
        window.fill((0,0,0))
        window.blit(render_health, (setting_win["WIDTH"] - 90, 10))
        window.blit(render_health_value, (setting_win["WIDTH"] - 20, 10))
        window.blit(key_image, (key1.x, key1.y))
        window.blit(key_image, (key2.x, key2.y))

        window.blit(tp.IMAGE, (tp.x, tp.y))
        tp.move()

        for wall in wall_list:
            window.blit(wall.IMAGE, (wall.x, wall.y))

        window.blit(hero.IMAGE_NOW, (hero.x, hero.y))
        for bot in bots_list:
            window.blit(bot.IMAGE_NOW, (bot.x, bot.y))
            bot.step(hero)
            if bot.colliderect(hero) and not bot.FOOD:
                bot.FOOD = True
                health -= 1
                render_health_value = font_health.render(str(health), True, (255, 87, 88))
            elif not bot.colliderect(hero) and bot.FOOD:
                bot.FOOD = False
                
        time1 = time.time()
        hero.move()
        time2 = time.time()
        
        test_speed.append(float(time2 - time1))
        #політ пулі
        if hero.SHOT == True:
            for bullet in hero.BULLET:
                bullet.x += bullet.X
                bullet.y += bullet.Y
                window.blit(bullet.IMAGE, (bullet.x, bullet.y))
                for bot in bots_list:
                    if bot.colliderect(bullet):
                        hero.BULLET.remove(bullet)
                        bots_list.remove(bot)
                        hero.SHOT = False
                        break
                if bullet.x > setting_win["WIDTH"] or bullet.y > setting_win["HEIGHT"] or bullet.x < 0 or bullet.y < 0 or bullet.collidelist(wall_list) != -1:
                    hero.BULLET.remove(bullet)
                    hero.SHOT = False
        period_respawn = time.time()
        #якщо ми переходимо якісь координати, то запускається алгоритм для появи ботів
        if hero.y > 200 and amount != 10 or alian_show_key and amount != 10:
            alian_show_key = True
            if period_respawn - respawn > 1 or period_respawn // respawn == int(period_respawn):
                bots_list.append(Bot(100, 600, 40, 40, alian_eazy_stay_image, 1))
                respawn = time.time()
                amount += 1
        period_respawn = time.time()
        if (hero.colliderect(start_create_bots_1) or alian_show_key1) and amount1 != 10:
            alian_show_key1 = True
            if period_respawn - respawn1 > 1 or period_respawn // respawn1 == int(period_respawn):
                bots_list.append(Bot(380, 10, 40, 40, alian_eazy_stay_image, 1))
                respawn1 = time.time()
                amount1 += 1
        period_respawn = time.time()
        if (hero.colliderect(start_create_bots_2) or alian_show_key2) and amount2 != 10:
            alian_show_key2 = True
            if period_respawn - respawn2 > 1 or period_respawn // respawn2 == int(period_respawn):
                bots_list.append(Bot(950, 650, 40, 40, alian_eazy_stay_image, 1))
                respawn2 = time.time()
                amount2 += 1
        #ключі
        if key_lvl == 0 and hero.colliderect(key1):
            key_lvl = 1
            key1.x = -100
        elif key_lvl == 1 and hero.colliderect(key2):
            key_lvl = 2
            key2.x = -100
        elif key_lvl == 2 and hero.colliderect(tp):
            key_lvl = 3
        elif key_lvl == 3:
            window.blit(render_win, (setting_win["WIDTH"] // 2 - 100, setting_win["HEIGHT"] // 2 - 30))

        #якщо хп менше ніж 0 то ми програли
        if health <= 0:
            window.blit(render_loose, (setting_win["WIDTH"] // 2 - 100, setting_win["HEIGHT"] // 2 - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = True
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = True
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = True
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = False
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = False
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = False
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not hero.SHOT:
                hero.SHOT = True
                hero.BULLET.append(Bullet(hero.x, hero.y, 20, 10))
                x,y = event.pos
                hero.BULLET[-1].make_angle(x, y, hero.x, hero.y)
               # print(":::::::", hero.X, hero.Y, hero.x, hero.y)


        
        clock.tick(60)
        pygame.display.flip()

run()

#print(test_speed)
d = 0
for i in test_speed:
    d += i
#print(d / len(test_speed),d, len(test_speed), len(wall_list))
