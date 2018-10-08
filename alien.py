import pygame
import os
import random
import game_functions as gf
from pygame.sprite import Sprite
from bullet import Bullet


# noinspection PyAttributeOutsideInit
class Alien(Sprite):
    """A class to represent a single alien in the flee."""

    def __init__(self, ai_settings, screen, alien_type=None, x=0, y=0):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.fps_counter = 0

        # Load a random alien image and set its rect attribute.
        if alien_type is None:
            self.alien_type = random.randrange(4)
        else:
            self.alien_type = alien_type

        self.images = []

        # Load all images for a type of alien
        for i in range(2):
            image_file = "alien" + str(self.alien_type) + "_" + str(i+1) + ".png"
            self.images.append(pygame.image.load(os.path.join("images", image_file)))

        # Store the alien's exact position
        self.rect = self.images[0].get_rect()

        if alien_type is None:
            # Start each new alien near the top left of the screen
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height
        else:
            self.rect.x = x
            self.rect.y = y

        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left."""
        if self.fps_counter + 1 >= 60:
            self.fps_counter = 0

        self.fps_counter += 1
        self.image = self.images[self.fps_counter // 30]

        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def fire_bullet(self, ai_settings, screen, bullets, sounds):
        """Fire a bullet if limit not reached yet."""
        # Create a new bullet and add it to the alien_bullets group.
        if len(bullets) < ai_settings.alien_bullets_allowed:
            gf.play_sound(sounds.alien_blasters, 0)
            new_bullet = Bullet(ai_settings, screen, self, ai_settings.alien_bullet_color)
            new_bullet.speed_factor = -new_bullet.speed_factor
            bullets.add(new_bullet)
