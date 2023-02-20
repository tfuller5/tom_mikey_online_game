import pygame
import os
from output import output

class chatbox:
    def __init__(self):
        self.activated = False
        self.message = []
        self.cursor = 0

    def is_active(self):
        return self.activated

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def send_key(self, key):
        if key == pygame.K_LEFT:
            if self.cursor != 0:
                self.cursor = self.cursor - 1
            output.speak(self.message[self.cursor])

        if key == pygame.K_RIGHT:
            if self.cursor < len(self.message) - 1:
                self.cursor = self.cursor + 1
            output.speak(self.message[self.cursor])

        if key == pygame.K_RETURN:
            self.deactivate()
            return "".join(self.message)

        elif key == pygame.K_BACKSPACE:
            if self.message != "":
                self.message = self.message[:-1]
        else:
            print(key)
            char = "@"
            if key < 255:
                if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
                    if 49 <= key <= 57:
                        char = chr(key - 16)
                    else:
                        char = chr(key - 32)
                else:
                    char = chr(key)
            self.message.insert(self.cursor, char)
            self.cursor = self.cursor + 1

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


def mainloop(client):
    # horrid threaded input loop
    #valid_keys = "abcdefghijklmnopqrstuvwxyz !"£$%^&*()_-+=#\

    my_chatbox = chatbox()
    screen = pygame.display.set_mode([50, 50])
    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


                if my_chatbox.is_active():
                    message = my_chatbox.send_key(event.key)
                    if message is not None:
                        client.Chat(message)

                else:
                    if event.key == pygame.K_SLASH:
                        output.speak("Enter your message")
                        my_chatbox.activate()
                    if event.key == pygame.K_i:
                        client.ListEveryone()

        if not my_chatbox.is_active() and not pygame.key.get_pressed()[pygame.KMOD_SHIFT]:
            if pygame.key.get_pressed()[pygame.K_LEFT] and whereami.x > 0: whereami.x -= 1; imove(client)
            if pygame.key.get_pressed()[pygame.K_RIGHT] and whereami.x < 9: whereami.x += 1; imove(client)
            if pygame.key.get_pressed()[pygame.K_UP] and whereami.y < 9: whereami.y += 1; imove(client)
            if pygame.key.get_pressed()[pygame.K_DOWN] and whereami.y > 0: whereami.y -= 1; imove(client)

        clock.tick(60)