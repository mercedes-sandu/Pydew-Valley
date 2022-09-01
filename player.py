import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        """Initializes the player."""
        super().__init__(group)

        # Animation/sprite setup
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # General setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Timers
        self.timers = {
            'tool use': Timer(350, self.use_tool)
        }

        # Tools
        self.selected_tool = 'axe'

    def use_tool(self):
        """Allows the player to use its selected tool."""
        print(self.selected_tool)

    def import_assets(self):
        """Imports all of the assets for the player."""
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_hoe': [],
            'left_hoe': [],
            'up_hoe': [],
            'down_hoe': [],
            'right_axe': [],
            'left_axe': [],
            'up_axe': [],
            'down_axe': [],
            'right_water': [],
            'left_water': [],
            'up_water': [],
            'down_water': []
        }

        for animation in self.animations.keys():
            full_path = './graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        """Animates the player sprite."""
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        """Processes input for the player."""
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
            # Directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else: 
                self.direction.y = 0
            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def get_status(self):
        """Sets status of the player appropriately."""
        # Idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # Tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' +  self.selected_tool

    def update_timers(self):
        """Updates the player's timers."""
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        """Moves the player's pos."""
        # Normalize vectors for diagonal speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        
        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        """Updates the player."""
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)