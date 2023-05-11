import pygame
from accessible_output2.outputs.auto import Auto
output = Auto()

class buffer_manager:
    def __init__(self):
        self.buffers = []
        self.buffer_index = 0

    def key_down_event(self, event):
        if event.key == pygame.K_COMMA:
            self.read_and_go_previous()
        elif event.key == pygame.K_PERIOD:
            self.read_and_go_next()

    def is_empty(self):
        return self.buffers == []

    def read_and_go_previous(self):
        if self.buffer_index > 0:
            self.buffer_index -= 1
        if not self.is_empty():
            output.speak(self.buffers[self.buffer_index])

    def read_and_go_next(self):
        if self.buffer_index < len(self.buffers) - 1:
            self.buffer_index += 1
        if not self.is_empty():
            output.speak(self.buffers[self.buffer_index])

    def add_message(self, message):
        self.buffers.append(message)
        self.buffer_index = len(self.buffers) - 1