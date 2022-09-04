import pygame
from settings import *

class Transition:
    def __init__(self, reset, player):
        """Initializes a transition."""
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # Overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play(self):
        """Plays the transition."""
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)

# # New: Task #001
# class Start_Transition:
#     def __init__(self, level):
#         """Initializes a transition upon starting the game."""
#         self.level = level
#         self.display_surface = pygame.display.get_surface()
#         self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
#         self.color = 0
#         self.speed = 2

#     def play(self):
#         """Plays the start transition at the beginning of the level."""
#         self.color += self.speed
#         if self.color > 255:
#             self.color = 255
#             self.level.starting = False
        
#         print(self.color)
#         self.image.fill((self.color, self.color, self.color))
#         self.display_surface.blit(self.image, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)