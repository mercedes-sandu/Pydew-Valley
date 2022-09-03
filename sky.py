import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice


class Drop(Generic):
    def __init__(self, pos, surface, groups, z, moving):
        """Initializes a rain drop."""
        super().__init__(pos, surface, groups, z)

        # General setup
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # Moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        """Updates the rain drop."""
        # Movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        """Initializes the rain."""
        self.all_sprites = all_sprites
        self.rain_drops = import_folder("./graphics/rain/drops")
        self.rain_floor = import_folder("./graphics/rain/floor")
        self.floor_width = pygame.image.load("./graphics/world/ground.png").get_size()[0]
        self.floor_height = pygame.image.load("./graphics/world/ground.png").get_size()[1]

    def create_floor(self):
        """Creates the rain floor."""
        Drop(
            pos = (randint(0, self.floor_width), randint(0, self.floor_height)),
            surface = choice(self.rain_floor),
            groups = self.all_sprites,
            z = LAYERS['rain floor'],
            moving = False,
        )

    def create_drops(self):
        """Creates the rain drops."""
        Drop(
            pos = (randint(0, self.floor_width), randint(0, self.floor_height)),
            surface = choice(self.rain_drops),
            groups = self.all_sprites,
            z = LAYERS['rain drops'],
            moving = True,
        )

    def update(self):
        """Updates the rain drops."""
        self.create_floor()
        self.create_drops()
