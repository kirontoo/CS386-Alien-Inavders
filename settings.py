# CS-386 Alien Invaders 2
# Amy Nguyen-Dang


# noinspection PyAttributeOutsideInit
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""

        # All-time high score file
        self.hs_file = "highscore.txt"

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_midX = self.screen_width // 2
        self.screen_padding = 30
        self.bg_color = (23, 23, 79)

        # Ship Settings
        self.ship_speed_factor = 1
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 7
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 5
        self.alien_bullets_allowed = 3
        self.alien_bullet_color = (255, 38, 38)
        self.ship_bullet_color = (38, 255, 38)

        # Alien Settings
        self.alien_speed_factor = 10
        self.fleet_drop_speed = 20
        self.alien_fire_rate = 0.00000032
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Number of Bunkers
        self.bunkers_allowed = 4

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 0
        self.alien0_points = 30
        self.alien1_points = 40
        self.alien2_points = 50
        self.alien3_points = 75

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def set_alien_points(self, alien_type):
        if alien_type == 0:
            self.alien_points = self.alien0_points
        elif alien_type == 1:
            self.alien_points = self.alien1_points
        elif alien_type == 2:
            self.alien_points = self.alien2_points
        elif alien_type == 3:
            self.alien_points = self.alien3_points
