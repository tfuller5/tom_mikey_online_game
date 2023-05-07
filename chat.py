import pygame
from accessible_output2.outputs.auto import Auto
output = Auto()

class chatbox:
    def __init__(self, prompt = "Enter your message"):
        self.prompt = prompt
        self.activated = False
        self.message = []
        self.actual = ""
        self.upto = ""
        self.cursor = -1
        self.updated()

    def updated(self):
        if self.message != []:
            if self.cursor != -1:
                output.speak(self.message[self.cursor])

    def is_active(self):
        return self.activated

    def activate(self):
        output.speak(self.prompt)
        self.activated = True

    def deactivate(self):
        self.activated = False

    def reset(self):
        self.cursor = -1
        self.message = []

    def send_key(self, event):
        print(self.message)
        if event.key == pygame.K_RETURN:
            final_message = "".join(self.message)
            self.deactivate()
            self.reset()
            self.updated()
            if final_message != "":
                return final_message

        elif event.key == pygame.K_LEFT:
            print("left")
            print(self.cursor)
            if self.cursor >= 0:
                self.cursor = self.cursor - 1
            self.updated()

        elif event.key == pygame.K_RIGHT:
            if self.cursor < len(self.message) - 1:
                self.cursor = self.cursor + 1
            self.updated()

        elif event.key == pygame.K_BACKSPACE:
            if self.message != [] and self.cursor != -1:
                self.message.pop(self.cursor)
                self.cursor -= 1
                self.updated()
        elif event.unicode != "":
            self.cursor = self.cursor + 1
            self.message.insert(self.cursor, event.unicode)
            self.updated()