import pygame
import os
from accessible_output2.outputs.auto import Auto
output = Auto()
from player import player
from weapons import weapons
from shop import shop, inventory
from info import info
import simple_menu
from chat import chatbox

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


def youmove(x, y):
    output.speak(f"you are is at {whereami.x} {whereami.y}")
    output.speak(f"other guy is at {x} {y}")
    if os.path.exists("pop.mp3"):
        pop = pygame.mixer.Sound("pop.mp3")

        pop.play()
    else:
        step = pygame.mixer.Sound("step.wav")
        step.set_volume(1)
        step.play()

def imove(client):
    if os.path.exists("pop.mp3"):
        pop = pygame.mixer.Sound("pop.mp3")

        pop.play()
    else:
        step = pygame.mixer.Sound("step.wav")
        step.set_volume(1)
        step.play()

    client.i_just_moved(whereami.x, whereami.y)


def noise():
    tile_type = whereami.get_tile_type()
    output.speak(whereami.sound_map[tile_type])
    output.speak(str(whereami.x))
    output.speak(str(whereami.y))
    player.save()


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

def mainloop(client):
    # horrid threaded input loop
    #valid_keys = "abcdefghijklmnopqrstuvwxyz !"£$%^&*()_-+=#\

    squares_per_second= 4
    frames_per_second= 60
    frame_number =0
    my_chatbox = chatbox()
    screen = pygame.display.set_mode([50, 50])
    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()

    while True:
        frame_number += 1

        #if pygame.key.get_mods() & pygame.KMOD_CTRL:
        #    player.equipped.triggerhold(frame_number)
        #else:
        #    player.equipped.triggerrelease()

        if not my_chatbox.is_active() and not pygame.key.get_pressed()[pygame.KMOD_SHIFT]:
            if frame_number % (frames_per_second // squares_per_second) == 0:
                if pygame.key.get_pressed()[pygame.K_LEFT] and whereami.x > 0: whereami.x -= 1; imove(client)
                if pygame.key.get_pressed()[pygame.K_RIGHT] and whereami.x < 9: whereami.x += 1; imove(client)
                if pygame.key.get_pressed()[pygame.K_UP] and whereami.y < 9: whereami.y += 1; imove(client)
                if pygame.key.get_pressed()[pygame.K_DOWN] and whereami.y > 0: whereami.y -= 1; imove(client)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: player.save(); return


                if my_chatbox.is_active():
                    message = my_chatbox.send_key(event)
                    print(message)
                    if message is not None:
                        client.Chat(message)
                        #https://github.com/tfuller5/tom_mikey_online_game.git
                        #sorry about that, can you put me in the voice thingy window?
                else:
                    if event.key == pygame.K_SLASH:
                        output.speak("Enter your message")
                        my_chatbox.activate()
                    if event.key == pygame.K_i:
                        client.ListEveryone()

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

        clock.tick(frames_per_second)