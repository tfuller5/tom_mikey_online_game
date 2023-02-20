import pygame
import os
from output import output

class chatbox:
    def __init__(self):
        self.activated = False
        self.message = []
        self.cursor = 0
        self.bad_keys = {pygame.KMOD_SHIFT, pygame.K_LSHIFT, pygame.K_RSHIFT}

    def is_active(self):
        return self.activated

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def reset(self):
        self.message = []

    def send_key(self, event):
        print(self.message)
        if event.key == pygame.K_RETURN:
            self.deactivate()
            self.reset()
            return "".join(self.message)

        elif event.key == pygame.K_LEFT:
            if self.cursor != 0:
                self.cursor = self.cursor - 1
            output.speak(self.message[self.cursor])

        elif event.key == pygame.K_RIGHT:
            if self.cursor < len(self.message) - 1:
                self.cursor = self.cursor + 1
            output.speak(self.message[self.cursor])

        elif event.key == pygame.K_BACKSPACE:
            if self.message != []:
                self.message.pop()
        elif event.key not in self.bad_keys:
            self.message.insert(self.cursor, event.unicode)
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
                    message = my_chatbox.send_key(event)
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

        if not my_chatbox.is_active() and not pygame.key.get_pressed()[pygame.KMOD_SHIFT]:
            if pygame.key.get_pressed()[pygame.K_LEFT] and whereami.x > 0: whereami.x -= 1; imove(client)
            if pygame.key.get_pressed()[pygame.K_RIGHT] and whereami.x < 9: whereami.x += 1; imove(client)
            if pygame.key.get_pressed()[pygame.K_UP] and whereami.y < 9: whereami.y += 1; imove(client)
            if pygame.key.get_pressed()[pygame.K_DOWN] and whereami.y > 0: whereami.y -= 1; imove(client)

        clock.tick(60)