import pygame
from settings import *
from player import Player
from overlay import Overlay

class Level:
    def __init__(self):
        """Initializes a level."""
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        """Sets up the player."""
        self.player = Player((640, 370), self.all_sprites)

    def run(self, dt):
        """Runs/updates the level."""
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.overlay.display()