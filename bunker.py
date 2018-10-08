import pygame
import os
from pygame.sprite import Sprite


class Bunker(Sprite):
    """A class to represent a single bunker"""

    def __init__(self, ai_settings, screen, ship):
        """Initialize the bunker and set its starting position."""
        super(Bunker, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.images = []
        self.rect_images = []

        # set damaged counter
        self.damaged = 0

        # Load the bunker images and set its rect attribute
        for i in range(3):
            image_file = "bunker_" + str(i) + ".png"
            self.images.append(pygame.image.load(os.path.join("images", image_file)))
            self.rect_images.append(self.images[i].get_rect())

            # Start each new bunker near the bottom left of the screen
            self.rect_images[i].x = self.rect_images[i].width
            self.rect_images[i].bottom = ship.rect.top - (self.rect_images[i].height // 2)

        self.image = self.images[0]
        self.rect = self.rect_images[0]

    def set_width(self, x):
        """Set width for all bunker images"""
        for i in range(3):
            self.rect_images[i].x = x

    def damage(self):
        """Damage the bunker"""
        if self.damaged >= 2:
            self.kill()
        else:
            self.damaged += 1

    def blitme(self):
        """Draw the bunker at tis current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.image = self.images[self.damaged]
