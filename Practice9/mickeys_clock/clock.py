

import pygame
import math
import time


class MickeyClock:

    def __init__(self):
        self.width = 600
        self.height = 600

        self.center_x = 300
        self.center_y = 275
        self.radius = 210

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Create Mickey-style glove hands
        self.hand = self.create_hand()

    def create_hand(self):
        # Transparent surface for the hand
        surface = pygame.Surface((400, 400), pygame.SRCALPHA)

        # Draw the wrist and arm
        pygame.draw.line(
            surface, self.black,
            (200, 200), (200, 130), 35
        )
        pygame.draw.line(
            surface, self.white,
            (200, 200), (200, 130), 27
        )

        # Draw cartoon glove
        glove_points = [
            (190, 135),
            (180, 65),
            (185, 35),
            (200, 25),
            (214, 35),
            (220, 100),
            (235, 75),
            (251, 80),
            (253, 112),
            (265, 95),
            (280, 105),
            (272, 140),
            (258, 155),
            (245, 170),
            (215, 175),
            (190, 160),
            (175, 145)
        ]

        pygame.draw.polygon(
            surface, self.black, glove_points
        )
        pygame.draw.polygon(
            surface, self.white, glove_points, 7
        )

        # Draw glove details
        pygame.draw.line(
            surface, self.black,
            (195, 120), (215, 140), 5
        )
        pygame.draw.line(
            surface, self.black,
            (220, 125), (238, 145), 5
        )
        pygame.draw.line(
            surface, self.black,
            (245, 125), (255, 140), 5
        )

        return surface

    def draw_clock_face(self, screen):

        screen.fill(self.white)

        # Draw clock circle
        pygame.draw.circle(
            screen,
            self.black,
            (self.center_x, self.center_y),
            self.radius,
            5
        )

        # Draw clock marks
        for i in range(60):

            angle = math.radians(i * 6 - 90)

            if i % 5 == 0:
                length = 15
                width = 4
            else:
                length = 7
                width = 2

            x1 = self.center_x + math.cos(angle) * (
                self.radius - length
            )
            y1 = self.center_y + math.sin(angle) * (
                self.radius - length
            )

            x2 = self.center_x + math.cos(angle) * self.radius
            y2 = self.center_y + math.sin(angle) * self.radius

            pygame.draw.line(
                screen,
                self.black,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                width
            )

    def draw_hand(self, screen, angle, scale):

        # Resize the hand
        size = int(400 * scale)

        hand = pygame.transform.smoothscale(
            self.hand,
            (size, size)
        )

        # Rotate the hand
        rotated_hand = pygame.transform.rotate(
            hand, -angle
        )

        # Keep the hand center at the clock center
        rect = rotated_hand.get_rect(
            center=(self.center_x, self.center_y)
        )

        screen.blit(rotated_hand, rect)

    def draw_time(self, screen):

        # Get current system time
        current_time = time.localtime()

        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # Calculate rotation angles
        minute_angle = minutes * 6
        second_angle = seconds * 6

        # Right hand = minutes
        self.draw_hand(
            screen,
            minute_angle,
            0.85
        )

        # Left hand = seconds
        self.draw_hand(
            screen,
            second_angle,
            1.0
        )

        # Draw center circle
        pygame.draw.circle(
            screen,
            self.black,
            (self.center_x, self.center_y),
            13
        )

        # Display digital time
        font = pygame.font.SysFont(
            "Arial", 38, bold=True
        )

        digital_time = time.strftime("%M:%S")

        text = font.render(
            digital_time,
            True,
            self.black
        )

        screen.blit(
            text,
            (
                self.center_x - text.get_width() // 2,
                510
            )
        )
