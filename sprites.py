from asyncio import current_task
import pygame
from settings import *
from timer import Timer
from random import randint, choice

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z=LAYERS['main']):
        """Initializes a generic sprite."""
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width *
                                               0.2, -self.rect.height * 0.75)


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        """Initializes an interactable sprite."""
        surface = pygame.Surface(size)
        super().__init__(pos, surface, groups)
        self.name = name


class Water(Generic):
    def __init__(self, pos, frames, groups):
        """Initializes a water sprite."""
        # Animation setup
        self.frames = frames
        self.frame_index = 0

        # Sprite setup
        super().__init__(
            pos=pos,
            surface=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water']
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
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Particle(Generic):
    def __init__(self, pos, surface, groups, z, duration=200):
        """Initializes a particle sprite."""
        super().__init__(pos, surface, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # White surface
        mask_surface = pygame.mask.from_surface(self.image)
        new_surface = mask_surface.to_surface()
        new_surface.set_colorkey((0, 0, 0))
        self.image = new_surface

    def update(self, dt):
        """Updates the particle sprites."""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surface, groups, name, player_add):
        """Initializes a tree sprite and its apples."""
        super().__init__(pos, surface, groups)

        # Tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'./graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surface = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # Apples
        self.apple_surface = pygame.image.load('./graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def create_fruit(self):
        """Creates a fruit object."""
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos=(x, y),
                    surface=self.apple_surface,
                    groups=[self.apple_sprites, self.groups()[0]],
                    z=LAYERS['fruit']
                )

    def damage(self):
        """Takes health away from the tree."""
        # Damage the tree
        self.health -= 1

        # Remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft, random_apple.image,
                     self.groups()[0], LAYERS['fruit'])
            self.player_add('apple')
            random_apple.kill()

    def check_death(self):
        """Checks whether the tree is alive and changes its state if dead."""
        if self.health <= 0:
            Particle(self.rect.topleft, self.image,
                     self.groups()[0], LAYERS['fruit'], 300)
            self.image = self.stump_surface
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood')

    def update(self, dt):
        """Updates the tree object."""
        if self.alive:
            self.check_death()