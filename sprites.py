import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        """Initializes a generic sprite."""
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Water(Generic):
    def __init__(self, pos, frames, groups):
        """Initializes a water sprite."""
        # Animation setup
        self.frames = frames
        self.frame_index = 0

        # Sprite setup
        super().__init__(
            pos = pos, 
            surface = self.frames[self.frame_index], 
            groups = groups,
            z = LAYERS['water']
        )

    def animate(self, dt):
        """Animates the water sprites."""
        self.frame_index += 5 * dt

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        """Updates the water sprites."""
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surface, groups):
        """Initializes a wildflower sprite."""
        super().__init__(pos, surface, groups)

class Tree(Generic):
    def __init__(self, pos, surface, groups, name):
        """Initializes a tree sprite."""