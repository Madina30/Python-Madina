
import pygame
from collections import deque


def draw_pencil(surface, start_pos, end_pos, color, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def draw_line(surface, start_pos, end_pos, color, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def draw_rectangle(surface, start_pos, end_pos, color, size):
    rect = pygame.Rect(start_pos, end_pos)
    rect.normalize()

    if rect.width > 0 and rect.height > 0:
        pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, start_pos, end_pos, color, size):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    radius = int((dx ** 2 + dy ** 2) ** 0.5)

    if radius > 0:
        pygame.draw.circle(surface, color, start_pos, radius, size)


def draw_square(surface, start_pos, end_pos, color, size):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    side = min(abs(dx), abs(dy))

    x = start_pos[0] + (side if dx < 0 else 0)
    y = start_pos[1] + (side if dy < 0 else 0)

    if side > 0:
        pygame.draw.rect(surface, color, (x, y, side, side), size)


def draw_right_triangle(surface, start_pos, end_pos, color, size):
    points = [
        start_pos,
        (start_pos[0], end_pos[1]),
        end_pos
    ]
    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, start_pos, end_pos, color, size):
    width = end_pos[0] - start_pos[0]
    height = abs(width) * (3 ** 0.5) / 2
    direction = -1 if end_pos[1] < start_pos[1] else 1

    points = [
        start_pos,
        end_pos,
        (start_pos[0] + width / 2,
         start_pos[1] + direction * height)
    ]

    pygame.draw.polygon(surface, color, points, size)


def draw_rhombus(surface, start_pos, end_pos, color, size):
    center_x = (start_pos[0] + end_pos[0]) // 2
    center_y = (start_pos[1] + end_pos[1]) // 2

    points = [
        (center_x, start_pos[1]),
        (end_pos[0], center_y),
        (center_x, end_pos[1]),
        (start_pos[0], center_y)
    ]

    pygame.draw.polygon(surface, color, points, size)


def flood_fill(surface, position, new_color):
    width, height = surface.get_size()
    x, y = position

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))

    if target_color[:3] == new_color[:3]:
        return

    pixels = deque([(x, y)])

    while pixels:
        x, y = pixels.popleft()

        if not (0 <= x < width and 0 <= y < height):
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), new_color)

        pixels.append((x + 1, y))
        pixels.append((x - 1, y))
        pixels.append((x, y + 1))
        pixels.append((x, y - 1))
