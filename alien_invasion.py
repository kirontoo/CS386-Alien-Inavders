# CS-386 Alien Invaders 2
# Amy Nguyen-Dang

import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from sounds import Sounds
from start_screen import StartScreen
from highscore_screen import HighScoreScreen


def run_game():
    # Initialize pygame, settings, screen object, music channel
    pygame.init()
    sounds = Sounds()

    # Limit FPS
    clock = pygame.time.Clock()

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )

    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Create the start and highscore screen
    start_screen = StartScreen(ai_settings, screen)
    hs_screen = HighScoreScreen(ai_settings, screen, stats)

    # Make a ship, a group of ship_bullets, and a group of aliens
    ship = Ship(screen, ai_settings)
    ship_bullets = Group()
    aliens = Group()
    alien_bullets = Group()
    bunkers = Group()

    # Create the fleet of aliens and row of bunkers
    gf.create_fleet(ai_settings, screen, ship, aliens)
    gf.create_bunker_row(ai_settings, screen, ship, bunkers)

    # Start the main loop for the game
    while True:

        # Limit FPS
        clock.tick(60)

        # Watch for keyboard/mouse events
        gf.check_events(ai_settings, screen, stats, sb,
                        start_screen, ship, aliens,
                        ship_bullets, sounds, bunkers, hs_screen)

        if stats.game_active:
            ship.update(stats.ships_left)
            ship_bullets.update()
            alien_bullets.update()
            bunkers.update()

            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bunkers,
                              ship_bullets, alien_bullets, sounds)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             ship_bullets, alien_bullets, sounds)

        # Redraw the screen during each pass through the loop.
        # Make the most recently drawn screen visible
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         ship_bullets, alien_bullets, start_screen,
                         bunkers, hs_screen)


run_game()
