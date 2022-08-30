import pygame
from settings import *

class Level:
    def __init__(self):
        """Initializes a level."""
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()

    def run(self, dt):
        """Runs/updates the level."""
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()