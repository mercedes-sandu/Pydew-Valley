from asyncio import current_task
import pygame

class Timer:
    def __init__(self, duration, func = None):
        """Initializes a timer with the specified duration and function."""
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        """Activates/starts the timer."""
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        """Deactivates/stops the timer."""
        self.active = False
        self.start_time = 0

    def update(self):
        """Updates the timer, called continuously."""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()