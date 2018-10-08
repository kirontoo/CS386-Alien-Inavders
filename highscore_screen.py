# CS-386 Alien Invaders 2
# Amy Nguyen-Dang
import pygame.font
import os
from button import Button


# noinspection PyAttributeOutsideInit
class HighScoreScreen:
    """A class to show the high score screen"""

    def __init__(self, settings, screen, stats):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.file = self.settings.hs_file

        self.text_color = (255, 255, 255)
        self.bg_color = (22, 26, 41)
        self.gray_color = (211, 211, 211)

        # Prepare the high score screen
        self.prep_title()
        self.prep_scores()
        self.prep_back_button()

    def prep_title(self):
        """Prepare the title"""

        font = pygame.font.SysFont(None, 100)
        title_str = "All-Time Highscores"
        self.title_image = font.render(title_str, True, self.text_color,
                                       self.bg_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.x = (self.settings.screen_midX - (self.title_rect.width
                             // 2))
        self.title_rect.y = self.settings.screen_padding * 2

    def prep_scores(self):
        """Prepare all top 10 scores"""
        top_ten_data = []
        self.top_scores = []
        self.top_scores_rect = []
        self.dir = os.path.dirname(__file__)
        font = pygame.font.SysFont(None, 50)
        color = (0, 255, 0)

        # Find positions
        score_x = self.screen_rect.centerx
        score_y = self.title_rect.bottom + 20

        # position all scores
        with open(os.path.join(self.dir, self.settings.hs_file), 'r') as f:
            # Read all data
            data = f.readlines()

            # create all score images
            for i in range(len(data)):
                # Only render the top ten scores
                if i == 10:
                    break

                top_ten_data.append(int(data[i]))
                score_str = "{}{:.>40}".format(str(i + 1), str(top_ten_data[i]))
                self.top_scores.append(font.render(score_str, True, color,
                                                   self.bg_color))

                self.top_scores_rect.append(self.top_scores[i].get_rect())
                self.top_scores_rect[i].centerx = score_x
                self.top_scores_rect[i].y = score_y

                # Edit score positions
                score_y = self.top_scores_rect[i].bottom + 10

    def prep_back_button(self):
        """Create a back button"""
        x = self.screen_rect.centerx
        y = self.screen_rect.bottom - self.title_rect.height - 50
        self.back_button = Button(self.screen, "Back", self.text_color, (255, 69, 0), x, y)

    def show_highscore_screen(self):
        """Draw high score screen"""
        # Fill the background color
        self.screen.fill(self.bg_color)

        # Draw the title and top ten scores
        self.screen.blit(self.title_image, self.title_rect)

        if not len(self.top_scores) == 0:
            for i in range(len(self.top_scores)):
                self.screen.blit(self.top_scores[i], self.top_scores_rect[i])

        # Draw the back button
        self.back_button.draw_button()
