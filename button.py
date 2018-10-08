import pygame.font


class Button:

    def __init__(self, screen, msg, text_color, bg_color, x, y):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg = msg

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x
        self.rect.y = y

        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    # noinspection PyAttributeOutsideInit
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button"""
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
