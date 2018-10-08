# CS-386 Alien Invaders 2
# Amy Nguyen-Dang

import sys
import pygame
import random
from alien import Alien
from time import sleep
from bunker import Bunker


def check_events(ai_settings, screen, stats, sb, start_screen, ship, aliens,
                 ship_bullets, sounds, bunkers, hs_screen):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # check all buttons
            check_button(ai_settings, screen, stats, sb,
                         start_screen.play_button, ship, aliens,
                         ship_bullets, mouse_x, mouse_y, sounds, bunkers)
            check_button(ai_settings, screen, stats, sb,
                         start_screen.highscore_button, ship, aliens,
                         ship_bullets, mouse_x, mouse_y, sounds, bunkers)
            check_button(ai_settings, screen, stats, sb,
                         hs_screen.back_button, ship, aliens,
                         ship_bullets, mouse_x, mouse_y, sounds, bunkers)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship,
                                 ship_bullets, sounds)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship,
                         ship_bullets, sounds):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        ship.fire_bullet(ai_settings, screen, ship_bullets, sounds)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, ship_bullets,
                  alien_bullets, start_screen, bunkers, hs_screen):
    """Update images on the screen and flip to the new screen."""

    # If the game is inactive, show the start screen.
    if not stats.game_active:
        # show high score screen when highscores button pressed
        if stats.hs_active:
            hs_screen.show_highscore_screen()
        else:
            start_screen.show_start_screen()
    else:
        # Redraw the screen during each pass through the loop.
        screen.fill(ai_settings.bg_color)

        # Redraw all bullets behind ship and aliens
        for bullet in ship_bullets.sprites():
            bullet.draw_bullet()

        for bullet in alien_bullets.sprites():
            bullet.draw_bullet()

        ship.blitme()
        bunkers.draw(screen)
        aliens.draw(screen)

        # Draw the score information.
        sb.show_score()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bunkers, ship_bullets,
                   alien_bullets, sounds):
    """Update position of ship_bullets and get rid of old ship_bullets."""
    # Update bullet positions
    ship_bullets.update()
    alien_bullets.update()

    # get rid of bullets that have disappeared
    for bullet in ship_bullets.copy():
        if bullet.rect.bottom <= 0:
            ship_bullets.remove(bullet)

    for bullet in alien_bullets.copy():
        if bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(bullet)

    # Check for collisions
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  ship_bullets, sounds)
    check_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                 ship_bullets, alien_bullets, sounds)
    check_bunker_bullet_collisions(ship_bullets, alien_bullets,
                                   bunkers, sounds)


def check_bunker_bullet_collisions(ship_bullets, alien_bullets, bunkers, sounds):
    """Respond to bullet-bunker collisions"""
    ship_collisions = pygame.sprite.groupcollide(ship_bullets, bunkers, True, False)
    alien_collisions = pygame.sprite.groupcollide(alien_bullets, bunkers, True, False)

    if ship_collisions:
        for bunkers in ship_collisions.values():
            for bunker in bunkers:
                play_sound(sounds.bunker_destroyed, 0)
                bunker.damage()

    if alien_collisions:
        for bunkers in alien_collisions.values():
            for bunker in bunkers:
                play_sound(sounds.bunker_destroyed, 0)
                bunker.damage()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  ship_bullets, sounds):
    """Respond to bullet-alien collisions."""
    # Remove any ship_bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(ship_bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            # Play a collision sound
            play_sound(sounds.alien_destroyed, 0)

            for alien in aliens:
                a_type = alien.alien_type
                ai_settings.set_alien_points(a_type)
                stats.score += ai_settings.alien_points

            sb.prep_score()

        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        ship_bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                 ship_bullets, alien_bullets, sounds):
    """Respond to bullet-ship collisions."""
    collisions = pygame.sprite.spritecollide(ship, alien_bullets, True)

    if collisions:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens,
                 ship_bullets, alien_bullets, sounds)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_objects_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_bunker_row(ai_settings, screen, ship, bunkers):
    """Create a row of bunkers"""
    for bunker_num in range(ai_settings.bunkers_allowed):
        create_bunker(ai_settings, screen, ship, bunkers, bunker_num)


def create_bunker(ai_settings, screen, ship, bunkers, bunker_num):
    """Create a bunker and place it in the row."""
    bunker = Bunker(ai_settings, screen, ship)
    bunker_width = bunker.rect.width
    x = bunker_width + 1.8 * bunker_width * bunker_num
    # Set its position
    bunker.set_width(x)
    bunkers.add(bunker)


def get_number_objects_x(ai_settings, width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * width
    number_objects_x = int(available_space_x / (2 * width))
    return number_objects_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_sprite_by_position(index, group):
    """Return a specific sprite in a group"""
    try:
        return group.sprites()[index]
    except IndexError:
        pass


def get_rand_number(num):
    try:
        return random.randrange(num)
    except ValueError:
        return 0


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, ship_bullets,
                  alien_bullets, sounds):
    """Check if the fleet is at an edge,
        and then update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # A random alien fires a bullet when needed
    tick = pygame.time.get_ticks()
    rand_time = random.uniform(0, 1)
    rate = tick * ai_settings.alien_fire_rate
    num_of_aliens = len(aliens)
    rand_alien = get_rand_number(num_of_aliens)
    alien = get_sprite_by_position(rand_alien, aliens)

    if alien and (rand_time < rate):
        alien.fire_bullet(ai_settings, screen, alien_bullets, sounds)

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets, sounds)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets, sounds)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets, sounds):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets, sounds)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets, sounds):
    """Respond to ship being hit by alien."""
    play_sound(sounds.ship_destroyed, 0)
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update ship lives left on scoreboard
        sb.prep_ships()

        # Empty the list of aliens and ship_bullets
        aliens.empty()
        ship_bullets.empty()
        alien_bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        reset_game(stats, sb, sounds)


def reset_game(stats, sb, sounds):
    """Reset game,play game over music and save high score"""
    # Stop game play music and play game over music
    pygame.mixer.stop()
    play_sound(sounds.game_over, 0)

    # Save new scores
    if stats.score > 0:
        sb.save_data()

    sleep(7)
    stats.game_active = False
    pygame.mouse.set_visible(True)


def check_button(ai_settings, screen, stats, sb, button, ship,
                 aliens, ship_bullets, mouse_x, mouse_y, sounds,
                 bunkers):
    """Start a new game when the player clicks Play."""
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        if button.msg == "Highscores":
            stats.hs_active = True

        elif button.msg == "Back":
            stats.hs_active = False

        elif button.msg == "Play":
            # Play game play music
            play_sound(sounds.game_music, -1)

            # Reset the game settings.
            ai_settings.initialize_dynamic_settings()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True

            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            ship_bullets.empty()
            bunkers.empty()

            # Create a new fleet and center the ship.
            create_fleet(ai_settings, screen, ship, aliens)
            create_bunker_row(ai_settings, screen, ship, bunkers)
            ship.center_ship()


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def play_sound(sound_effect, loop):
    channel = pygame.mixer.find_channel()
    if channel:
        channel.play(sound_effect, loop)
