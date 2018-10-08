import pygame
import os
import game_functions as gf
from pygame.sprite import Sprite
from bullet import Bullet


class Ship(Sprite):

    def __init__(self, screen, ai_settings):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Load all ship images and get its rect
        self.images = []
        self.destroy_images = []

        self.load_ship()
        self.load_destroy_animation()

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag (continuous movement)
        self.moving_right = False
        self.moving_left = False

        self.fps_counter = 0

    def load_destroy_animation(self):
        for i in range(12):
            file = "ship_destroy" + str(i) + ".png"
            self.destroy_images.append(pygame.image.load(os.path.join("images", file)))

    def load_ship(self):
        for i in range(2):
            file = "ship" + str(i+1) + ".png"
            self.images.append(pygame.image.load(os.path.join("images", file)).convert())

    def update(self, lives):
        """Update the ship's position based on the movement flag."""

        # Destroy the ship when there are no more lives
        if lives == 0:
            self.destroy()

        # update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.image = self.images[1]
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.image = self.images[1]
            self.center -= self.ai_settings.ship_speed_factor

        if not self.moving_left and not self.moving_right:
            self.image = self.images[0]

        # update the rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def destroy(self):
        if self.fps_counter + 1 >= 60:
            self.fps_counter = 0

        self.fps_counter += 1
        self.image = self.destroy_images[self.fps_counter // 5]

    def fire_bullet(self, ai_settings, screen, bullets, sounds):
        """Fire a bullet if limit not reached yet."""
        # Create a new bullet and add it to the bullets group.
        if len(bullets) < ai_settings.bullets_allowed:
            gf.play_sound(sounds.ship_blasters, 0)
            new_bullet = Bullet(ai_settings, screen, self,
                                ai_settings.ship_bullet_color)
            bullets.add(new_bullet)
