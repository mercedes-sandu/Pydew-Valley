import pygame
from settings import *
from timer import Timer

class Merchant:
    def __init__(self, player, toggle_menu):
        """Initializes the merchant's shop menu."""
        # General setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('./font/LycheeSoda.ttf', 30)

        # Options
        self.width = 400
        self.space = 10
        self.padding = 8

        # Menu entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # Movement
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        """Displays the player's money in the merchant's shop menu."""
        text_surface = self.font.render(f'${self.player.money}', False, 'black')
        text_rect = text_surface.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surface, text_rect)

    def setup(self):
        """Sets up the merchant's shop menu."""
        # Create the text surfaces
        self.text_surfaces = []
        self.total_height = 0
        for item in self.options:
            text_surface = self.font.render(item, False, 'black')
            self.text_surfaces.append(text_surface)
            self.total_height += text_surface.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfaces) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

        # Buy/sell text surface
        self.buy_text = self.font.render('buy', False, 'black')
        self.sell_text = self.font.render('sell', False, 'black')

    def input(self):
        """Processes input for the merchant's shop menu."""
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()
        
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # Get item
                current_item = self.options[self.index]

                if self.index <= self.sell_border: # sell
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
                else: # buy
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]

        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surface, amount, top, selected):
        """Displays an entry in the merchant's shop menu."""
        # Background
        background_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surface.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'white', background_rect, 0, 4)

        # Text
        text_rect = text_surface.get_rect(midleft = (self.main_rect.left + 20, background_rect.centery))
        self.display_surface.blit(text_surface, text_rect)

        # Amount
        amount_surface = self.font.render(str(amount), False, 'black')
        amount_rect = amount_surface.get_rect(midright = (self.main_rect.right - 20, background_rect.centery))
        self.display_surface.blit(amount_surface, amount_rect)

        if selected:
            pygame.draw.rect(self.display_surface, 'black', background_rect, 4, 4)
            if self.index <= self.sell_border: # sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, background_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else: # buy
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150, background_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        """Updates the merchant's shop menu."""
        self.input()
        self.display_money()
        for text_index, text_surface in enumerate(self.text_surfaces):
            top = self.main_rect.top + text_index * (text_surface.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surface, amount, top, self.index == text_index)