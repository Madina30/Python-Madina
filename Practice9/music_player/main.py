

import pygame
from player import MusicPlayer


# Initialize Pygame
pygame.init()

# Window settings
WIDTH = 700
HEIGHT = 450

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Madina's Music Player")

# Colors
BLACK = (25, 25, 35)
WHITE = (255, 255, 255)
PURPLE = (150, 100, 220)
GRAY = (180, 180, 190)
GREEN = (80, 200, 120)

# Fonts
title_font = pygame.font.SysFont("Arial", 38, bold=True)
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

# Create music player
player = MusicPlayer()

# Main loop
running = True
clock = pygame.time.Clock()

while running:

    # Handle keyboard events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.previous_track()

            elif event.key == pygame.K_q:
                running = False

    # Check if current song has finished
    player.update()

    # Background
    screen.fill(BLACK)

    # Title
    title = title_font.render(
        "MUSIC PLAYER",
        True,
        PURPLE
    )
    screen.blit(title, (220, 35))

    # Current track
    track_name = player.get_current_track()

    track_text = font.render(
        "Track: " + track_name,
        True,
        WHITE
    )

    screen.blit(
        track_text,
        (50, 130)
    )

    # Track number
    if player.playlist:
        track_number = (
            f"Track {player.current_index + 1} "
            f"of {len(player.playlist)}"
        )
    else:
        track_number = "Playlist is empty"

    number_text = small_font.render(
        track_number,
        True,
        GRAY
    )

    screen.blit(number_text, (50, 175))

    # Playback position
    position = player.get_position()

    minutes = position // 60
    seconds = position % 60

    position_text = font.render(
        f"Playback position: {minutes:02d}:{seconds:02d}",
        True,
        GREEN
    )

    screen.blit(position_text, (50, 220))

    # Playback status
    if player.is_playing:
        status = "Status: PLAYING"
        status_color = GREEN
    else:
        status = "Status: STOPPED"

        status_color = GRAY

    status_text = font.render(
        status,
        True,
        status_color
    )

    screen.blit(status_text, (50, 270))

    # Keyboard instructions
    controls = [
        "P - Play",
        "S - Stop",
        "N - Next track",
        "B - Previous track",
        "Q - Quit"
    ]

    y = 320

    for control in controls:
        text = small_font.render(
            control,
            True,
            WHITE
        )

        screen.blit(text, (50, y))
        y += 25

    # Update display
    pygame.display.flip()

    clock.tick(30)

# Close music player
player.quit()
pygame.quit()
