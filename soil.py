import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        """Initializes a soil tile."""
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS["soil"]

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        """Initializes a watered soil tile."""
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS["soil water"]

class SoilLayer:
    def __init__(self, all_sprites):
        """Initializes the soil layer."""
        # Sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surfaces = import_folder_dict("./graphics/soil")
        self.water_surfaces = import_folder("./graphics/soil_water")

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        """Creates the grid of farmable soil."""
        ground = pygame.image.load("./graphics/world/ground.png")
        horizontal_tiles = ground.get_width() // TILE_SIZE
        vertical_tiles = ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(horizontal_tiles)] for row in range(vertical_tiles)]
        for x, y, _ in load_pygame("./data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append("F")

    def create_hit_rects(self):
        """Creates the farmable soil rects that can be hit."""
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "F" in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        """Hits the soil at the point."""
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if "F" in self.grid[y][x]:
                    self.grid[y][x].append("X")
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        """Waters the soil at the target position."""
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append("W")
                WaterTile(soil_sprite.rect.topleft, choice(self.water_surfaces), [self.all_sprites, self.water_sprites])

    def water_all(self):
        """Waters all the soil tiles if it rains."""
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "X" in cell and "W" not in cell:
                    cell.append("W")
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    WaterTile((x, y), choice(self.water_surfaces), [self.all_sprites, self.water_sprites])

    def remove_water(self):
        """Destroys all water sprites and updates the grid."""
        # Destroys water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # Updates the grid
        for row in self.grid:
            for cell in row:
                if "W" in cell:
                    cell.remove("W")

    def create_soil_tiles(self):
        """Creates soil tiles."""
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "X" in cell:
                    # Tile options
                    t = "X" in self.grid[index_row - 1][index_col]
                    b = "X" in self.grid[index_row + 1][index_col]
                    r = "X" in row[index_col + 1]
                    l = "X" in row[index_col - 1]

                    tile_type = "o"

                    # All sides
                    if all((t, b, r, l)):
                        tile_type = "x"

                    # Horizontal tiles only
                    if l and not any((t, b, r)):
                        tile_type = "r"
                    if r and not any((t, b, l)):
                        tile_type = "l"
                    if l and r and not any((t, b)):
                        tile_type = "lr"

                    # Vertical tiles only
                    if t and not any((b, r, l)):
                        tile_type = "b"
                    if b and not any((t, r, l)):
                        tile_type = "t"
                    if t and b and not any((r, l)):
                        tile_type = "tb"

                    # Corners
                    if l and b and not any((t, r)):
                        tile_type = "tr"
                    if r and b and not any((t, l)):
                        tile_type = "tl"
                    if l and t and not any((b, r)):
                        tile_type = "br"
                    if r and t and not any((b, l)):
                        tile_type = "bl"

                    # T shapes
                    if all((t, b, r)) and not l:
                        tile_type = "tbr"
                    if all((t, b, l)) and not r:
                        tile_type = "tbl"
                    if all((l, r, t)) and not b:
                        tile_type = "lrb"
                    if all((l, r, b)) and not t:
                        tile_type = "lrt"

                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE), self.soil_surfaces[tile_type], [self.all_sprites, self.soil_sprites])