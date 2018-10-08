# CS-386 Alien Invaders 2
# Amy Nguyen-Dang

import pygame
import os


# noinspection PyAttributeOutsideInit
class Sounds:
    dir = 'sounds'

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(10)
        self.load_sounds()

    def load_sounds(self):
        self.game_over = pygame.mixer.Sound(os.path.join(
            self.dir, 'game_over.wav'))
        self.game_music = pygame.mixer.Sound(os.path.join(
            self.dir, 'deep_space.wav'))

        # Ship sound effects
        self.ship_blasters = pygame.mixer.Sound(os.path.join(
            self.dir, '8BIT_RETRO_Fire_Blaster_Deep_Glide_mono.wav'))
        self.ship_destroyed = pygame.mixer.Sound(os.path.join(
            self.dir, '8BIT_RETRO_Explosion_Short_Bright_mono.wav'))

        # Alien sound effects
        self.alien_blasters = pygame.mixer.Sound(os.path.join(
            self.dir, '8BIT_RETRO_Movement_Effect_Bright_loop_mono.wav'))
        self.alien_destroyed = pygame.mixer.Sound(os.path.join(
            self.dir, '8BIT_RETRO_Explosion_Short_Distant_mono.wav'))

        # Bunker sound effects
        self.bunker_destroyed = pygame.mixer.Sound(os.path.join(
            self.dir, 'EXPLOSION_Medium_Bright_Impact_stereo.wav'))
