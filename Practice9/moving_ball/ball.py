
import pygame


class Ball:

    def __init__(self, x, y):
        # Ball radius and movement speed
        self.radius = 25
        self.speed = 20

        # Initial position of the ball
        self.x = x
        self.y = y

        # Ball color
        self.color = (255, 0, 0)

    def move(self, direction, screen_width, screen_height):
        # Move the ball up
        if direction == pygame.K_UP:
            if self.y - self.speed - self.radius >= 0:
                self.y -= self.speed

        # Move the ball down
        elif direction == pygame.K_DOWN:
            if self.y + self.speed + self.radius <= screen_height:
                self.y += self.speed

        # Move the ball left
        elif direction == pygame.K_LEFT:
            if self.x - self.speed - self.radius >= 0:
                self.x -= self.speed

        # Move the ball right
        elif direction == pygame.K_RIGHT:
            if self.x + self.speed + self.radius <= screen_width:
                self.x += self.speed

    def draw(self, screen):
        # Draw the red ball
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.radius
        )
