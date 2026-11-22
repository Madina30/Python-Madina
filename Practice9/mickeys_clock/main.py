

import pygame
from clock import MickeyClock


# Initialize Pygame
pygame.init()

# Create window
WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

# Create clock object
clock = pygame.time.Clock()
mickey_clock = MickeyClock()

running = True

# Main game loop
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw clock
    mickey_clock.draw_clock_face(screen)
    mickey_clock.draw_time(screen)

    # Update display
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
