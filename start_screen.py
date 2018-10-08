# CS-386 Alien Invaders 2
# Amy Nguyen-Dang

import pygame
from button import Button
from alien import Alien


# noinspection PyAttributeOutsideInit,PyTypeChecker
class StartScreen:
    """A class to show the start screen"""

    def __init__(self, settings, screen):
        """Initialize all start screen attributes"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = (22, 26, 41)
        self.text_color = (255, 255, 255)
        self.gray_color = (211, 211, 211)
        self.orange_color = (255, 69, 0)
        self.subtitle_color = self.settings.ship_bullet_color

        # Prepare start screen
        self.prep_title()
        self.prep_subtitle()
        self.prep_alien_types()

        # Create all buttons
        self.create_all_buttons()

    def prep_title(self):
        """Prepare the title"""
        font = pygame.font.SysFont(None, 120)
        title_str = "ALIEN"

        # Create and position the Title
        self.title_image = font.render(title_str, True, self.text_color,
                                       self.bg_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.x = (self.settings.screen_midX - (self.title_rect.width
                             // 2))
        self.title_rect.y = self.settings.screen_padding * 2

    def prep_subtitle(self):
        """Prepare the subtitle"""
        font = pygame.font.SysFont(None, 80)
        subtitle_str = "INVADERS"

        # Create and position the Title
        self.subtitle_image = font.render(subtitle_str, True,
                                          self.subtitle_color, self.bg_color)
        self.subtitle_rect = self.subtitle_image.get_rect()
        self.subtitle_rect.x = (self.settings.screen_midX -
                                (self.subtitle_rect.width // 2))
        self.subtitle_rect.top = self.title_rect.bottom

    def prep_alien_types(self):
        """Prepare all alien types"""
        alien_x = self.screen_rect.centerx - 155
        alien_y = self.subtitle_rect.bottom + self.settings.screen_padding * 2

        # Create all alien types
        self.aliens = [None] * 4
        for i in range(4):
            self.aliens[i] = Alien(self.settings, self.screen, i,
                                   alien_x, alien_y)
            alien_y += self.aliens[0].rect.width + self.settings.screen_padding

        self.prep_alien_scores()

    def prep_alien_scores(self):
        """Prepare all alien scores"""
        eq_str = "= "
        pt_str = " PTS"
        font = pygame.font.SysFont(None, 80)
        score_str = [None] * 4
        self.alien_scores = [None] * 4
        self.alien_scores_rect = [None] * 4

        # Create the score point text
        score_str[0] = eq_str + str(self.settings.alien0_points) + pt_str
        score_str[1] = eq_str + str(self.settings.alien1_points) + pt_str
        score_str[2] = eq_str + str(self.settings.alien2_points) + pt_str
        score_str[3] = eq_str + str(self.settings.alien3_points) + pt_str

        for i in range(4):
            self.alien_scores[i] = font.render(score_str[i], True,
                                               self.gray_color, self.bg_color)

            # Position the alien score points
            score_x = (self.aliens[i].rect.x + self.aliens[i].rect.width
                       + self.settings.screen_padding)
            score_y = self.aliens[i].rect.y

            self.alien_scores_rect[i] = self.alien_scores[i].get_rect()
            self.alien_scores_rect[i].x = score_x
            self.alien_scores_rect[i].top = score_y

    def create_all_buttons(self):
        """Create the play and highscore button"""

        # Create the play button
        button_y = (self.aliens[3].rect.bottom + self.settings.screen_padding)
        self.play_button = Button(self.screen, "Play", self.subtitle_color, self.bg_color,
                                  self.screen_rect.centerx, button_y)

        # Create the highscore button
        button_y = self.play_button.rect.bottom + self.settings.screen_padding
        self.highscore_button = Button(self.screen, "Highscores", self.orange_color,
                                       self.bg_color, self.screen_rect.centerx, button_y)

    def show_start_screen(self):
        """Draw start screen"""
        # fill the background color
        self.screen.fill(self.bg_color)

        # Draw the title and subtitle
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.subtitle_image, self.subtitle_rect)

        # Draw Alien Types
        for i in range(4):
            self.screen.blit(self.aliens[i].images[0], self.aliens[i].rect)
            self.screen.blit(self.alien_scores[i],
                             self.alien_scores_rect[i])

        # Draw all button
        self.play_button.draw_button()
        self.highscore_button.draw_button()
