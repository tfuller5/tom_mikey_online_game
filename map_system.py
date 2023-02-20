from shop import shop, inventory
from info import info
from output import output
import os
from player import player
import random
import simple_menu
from weapons import weapons

player.load()
weapons.select_weapon(player)





import pygame
from pygame.key import *

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("The map")
pygame.mixer.init()
test_sound=pygame.mixer.Sound("step.wav")

class whereami:
    the_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    sound_map = {1: "grass", 2: "concrete", 3: "cement"}
    x = 0
    y = 0

    @staticmethod
    def get_tile_type():
        return whereami.the_map[9-whereami.y][whereami.x]

    @staticmethod
    def set_tile_type(item, minx, maxx, miny, maxy):
        for x in range(minx - 1, maxx):
            for y in range(miny - 1, maxy):
                 whereami.the_map[9 - y][x]= item
        for l in whereami.the_map:
            print(l)

def noise():
    tile_type = whereami.get_tile_type()
    output.speak(whereami.sound_map[tile_type])
    output.speak(str(whereami.x))
    output.speak(str(whereami.y))
    player.save()

class enemy:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.dead = False

    def move(self):
        if self.x > 0:
            self.x -= 1
            output.speak(f"Enemy is at {self.x} {self.y}")
        else:
            output.speak("Enemy walked into a wall and died")
            self.dead = True

new_enemy = enemy()

def build():
    s = simple_menu.simple_menu(clicksound="menuclick.ogg", edgesound="menuedge.ogg", entersound="menuenter.ogg",
                                wrapsound="menuwrap.ogg", leftright=False, updown=True, wrapping=True, homeend=True)

    options = [1, 2, 3]
    options.remove(whereami.get_tile_type())
    for option in options:
        s.add_item(f"{option} for {whereami.sound_map[option]}", internal_name = str(option))
    choice = s.run("set a tile",True)
    minx = int(input("x min: "))
    maxx = int(input("x max: "))
    miny = int(input("y min: "))
    maxy = int(input("y max: "))

    whereami.set_tile_type(int(s.get_item_name(choice)), minx, maxx, miny, maxy)


def arrow():
    test_sound.play()

running = True
frames = 0
while running:
    frames += 1
    clock.tick(60)
    #if frames%10 == 0 and new_enemy.dead == False: new_enemy.move()

    if pygame.key.get_mods() & pygame.KMOD_CTRL:
        player.equipped.triggerhold(frames)
    else:
        player.equipped.triggerrelease()

    if not pygame.key.get_pressed()[pygame.KMOD_SHIFT]:
        if pygame.key.get_pressed()[pygame.K_LEFT] and whereami.x > 0: arrow(); whereami.x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT] and whereami.x < 9: arrow(); whereami.x += 1
        if pygame.key.get_pressed()[pygame.K_UP] and whereami.y < 9: arrow(); whereami.y += 1
        if pygame.key.get_pressed()[pygame.K_DOWN] and whereami.y > 0: arrow(); whereami.y -= 1


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: player.save(); running = False
            if event.key == pygame.K_c: noise()

            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if event.key == pygame.K_LEFT: player.turn("left")
                if event.key == pygame.K_RIGHT: player.turn("right")
                if event.key == pygame.K_UP: player.turn("up")
                if event.key == pygame.K_DOWN: player.turn("down")

            if event.key == pygame.K_l: output.speak(f"You are level {player.level}")
            if event.key == pygame.K_h: output.speak(f"You have {player.health} health.")
            if event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_SHIFT: info()
            if event.key == pygame.K_p: output.speak(f"You have {player.points} points.")
            if event.key == pygame.K_s: shop(player)
            if event.key == pygame.K_i: inventory(player.items)
            if event.key == pygame.K_g: output.speak(f"You have {player.gold} gold.")
            if event.key == pygame.K_b: build()
            if event.key == pygame.K_1: weapons.select_weapon(player)
