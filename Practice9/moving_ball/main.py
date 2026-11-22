
import pygame
from ball import Ball


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Colors
WHITE = (255, 255, 255)

# Create ball in the center of the screen
ball = Ball(WIDTH // 2, HEIGHT // 2)

# Game clock
clock = pygame.time.Clock()

# Main game loop
running = True

while running:

    # Handle events
    for event in pygame.event.get():

        # Close the game
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard input
        elif event.type == pygame.KEYDOWN:

            if event.key in (
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT
            ):
                ball.move(
                    event.key,
                    WIDTH,
                    HEIGHT
                )

    # Fill background with white
    screen.fill(WHITE)

    # Draw ball
    ball.draw(screen)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
