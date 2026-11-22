
import pygame
import sys
from datetime import datetime

from tools import (
    draw_pencil,
    draw_line,
    draw_rectangle,
    draw_circle,
    draw_square,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    flood_fill
)

pygame.init()

WIDTH = 1100
HEIGHT = 750
TOOLBAR_HEIGHT = 125

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Paint Application")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)
PINK = (255, 105, 180)
GRAY = (210, 210, 210)
DARK_GRAY = (70, 70, 70)

colors = [
    BLACK, RED, GREEN, BLUE,
    YELLOW, ORANGE, PURPLE, PINK, WHITE
]

current_color = BLACK

brush_sizes = [2, 5, 10]
current_size = 5

tools = [
    "Pencil", "Line", "Rectangle", "Circle",
    "Square", "Right Triangle", "Equilateral Triangle",
    "Rhombus", "Eraser", "Color Picker", "Fill", "Text"
]

current_tool = "Pencil"

# Drawing canvas
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

drawing = False
start_pos = None
end_pos = None
last_pos = None

# Text settings
font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 16)

text_input = ""
text_position = None

# Tool button positions
tool_buttons = {}

for i, tool in enumerate(tools):
    x = 10 + (i % 6) * 180
    y = 10 + (i // 6) * 35
    tool_buttons[tool] = pygame.Rect(x, y, 170, 28)


def get_canvas_position(position):
    return position[0], position[1] - TOOLBAR_HEIGHT


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"

    pygame.image.save(canvas, filename)
    print(f"Canvas saved successfully: {filename}")


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Tool buttons
    for tool, button in tool_buttons.items():
        if tool == current_tool:
            button_color = BLUE
            text_color = WHITE
        else:
            button_color = WHITE
            text_color = BLACK

        pygame.draw.rect(screen, button_color, button)
        pygame.draw.rect(screen, BLACK, button, 1)

        label = small_font.render(tool, True, text_color)
        screen.blit(label, (button.x + 5, button.y + 5))

    # Color palette
    for i, color in enumerate(colors):
        x = 10 + i * 35
        y = 87

        pygame.draw.rect(screen, color, (x, y, 27, 22))
        pygame.draw.rect(screen, BLACK, (x, y, 27, 22), 1)

        if color == current_color:
            pygame.draw.rect(screen, BLUE, (x - 2, y - 2, 31, 26), 2)

    # Brush sizes
    size_label = small_font.render("Brush size:", True, BLACK)
    screen.blit(size_label, (350, 90))

    for i, size in enumerate(brush_sizes):
        x = 450 + i * 65
        button = pygame.Rect(x, 86, 55, 25)

        if size == current_size:
            button_color = BLUE
            text_color = WHITE
        else:
            button_color = WHITE
            text_color = BLACK

        pygame.draw.rect(screen, button_color, button)
        pygame.draw.rect(screen, BLACK, button, 1)

        label = small_font.render(str(size), True, text_color)
        screen.blit(label, (button.x + 20, button.y + 4))

    help_text = small_font.render(
        "Shortcuts: 1/2/3 - brush size | Ctrl+S - save | Q - quit",
        True,
        BLACK
    )
    screen.blit(help_text, (680, 90))


def draw_shape(surface, tool, start, end):
    if tool == "Line":
        draw_line(surface, start, end, current_color, current_size)

    elif tool == "Rectangle":
        draw_rectangle(surface, start, end, current_color, current_size)

    elif tool == "Circle":
        draw_circle(surface, start, end, current_color, current_size)

    elif tool == "Square":
        draw_square(surface, start, end, current_color, current_size)

    elif tool == "Right Triangle":
        draw_right_triangle(surface, start, end, current_color, current_size)

    elif tool == "Equilateral Triangle":
        draw_equilateral_triangle(surface, start, end, current_color, current_size)

    elif tool == "Rhombus":
        draw_rhombus(surface, start, end, current_color, current_size)


def draw_preview():
    if start_pos is None or end_pos is None:
        return

    preview = canvas.copy()
    draw_shape(preview, current_tool, start_pos, end_pos)
    screen.blit(preview, (0, TOOLBAR_HEIGHT))


def is_inside_canvas(position):
    x, y = position
    return (
        0 <= x < canvas.get_width()
        and 0 <= y < canvas.get_height()
    )


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                running = False

            elif event.key == pygame.K_1:
                current_size = 2

            elif event.key == pygame.K_2:
                current_size = 5

            elif event.key == pygame.K_3:
                current_size = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            # Text input
            elif current_tool == "Text" and text_position is not None:

                if event.key == pygame.K_RETURN:
                    if text_input:
                        text_surface = font.render(
                            text_input, True, current_color
                        )
                        canvas.blit(text_surface, text_position)

                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_ESCAPE:
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                elif event.unicode.isprintable():
                    text_input += event.unicode

        # Mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mouse_x, mouse_y = event.pos

            if mouse_y < TOOLBAR_HEIGHT:

                # Select tool
                for tool, button in tool_buttons.items():
                    if button.collidepoint(event.pos):
                        current_tool = tool
                        text_input = ""
                        text_position = None

                # Select color
                for i, color in enumerate(colors):
                    x = 10 + i * 35
                    if pygame.Rect(x, 87, 27, 22).collidepoint(event.pos):
                        current_color = color

                # Select brush size
                for i, size in enumerate(brush_sizes):
                    x = 450 + i * 65
                    if pygame.Rect(x, 86, 55, 25).collidepoint(event.pos):
                        current_size = size

            else:
                position = get_canvas_position(event.pos)

                if is_inside_canvas(position):

                    if current_tool == "Text":
                        text_position = position
                        text_input = ""

                    elif current_tool == "Fill":
                        flood_fill(canvas, position, current_color)

                    elif current_tool == "Color Picker":
                        current_color = canvas.get_at(position)[:3]

                    elif current_tool in ["Pencil", "Eraser"]:
                        drawing = True
                        last_pos = position

                        color = WHITE if current_tool == "Eraser" else current_color
                        size = current_size

                        pygame.draw.circle(canvas, color, position, max(1, size // 2))

                    else:
                        drawing = True
                        start_pos = position
                        end_pos = position

        # Mouse movement
        elif event.type == pygame.MOUSEMOTION and drawing:

            position = get_canvas_position(event.pos)

            if is_inside_canvas(position):

                if current_tool in ["Pencil", "Eraser"]:

                    color = WHITE if current_tool == "Eraser" else current_color

                    draw_pencil(
                        canvas,
                        last_pos,
                        position,
                        color,
                        current_size
                    )

                    last_pos = position

                else:
                    end_pos = position

        # Mouse button released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:

            position = get_canvas_position(event.pos)

            if current_tool not in ["Pencil", "Eraser"]:
                if is_inside_canvas(position):
                    end_pos = position
                    draw_shape(canvas, current_tool, start_pos, end_pos)

            drawing = False
            start_pos = None
            end_pos = None
            last_pos = None

    # Display
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and current_tool not in ["Pencil", "Eraser"]:
        draw_preview()

    draw_toolbar()

    # Text preview
    if current_tool == "Text" and text_position is not None:
        preview_text = font.render(
            text_input + "|",
            True,
            current_color
        )

        screen.blit(
            preview_text,
            (text_position[0], text_position[1] + TOOLBAR_HEIGHT)
        )

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()

