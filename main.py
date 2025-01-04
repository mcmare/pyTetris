import pygame
import random

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),     # Cyan
    (0, 0, 255),     # Blue
    (255, 127, 0),   # Orange
    (255, 255, 0),     # Yellow
    (0, 255, 0),     # Green
    (128, 0, 128),   # Purple
    (255, 0, 0)       # Red
]
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 0], [1, 1, 1]],
]

# Game Functions
def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def get_random_shape():
    return random.choice(SHAPES), random.randint(0, len(COLORS)-1)


def rotate_shape(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


def is_valid_position(grid, shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                grid_x = x + col_idx
                grid_y = y + row_idx
                if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT or (grid_y >= 0 and grid[grid_y][grid_x]):
                    return False
    return True


def place_shape_on_grid(grid, shape, x, y, color_idx):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                grid[y + row_idx][x + col_idx] = color_idx + 1


def clear_full_lines(grid):
    full_lines = []
    for row_idx, row in enumerate(grid):
        if all(row):
            full_lines.append(row_idx)
    if full_lines:
         for idx in full_lines:
              del grid[idx]
              grid.insert(0, [0] * GRID_WIDTH)
         return len(full_lines)
    return 0


def game_over_check(grid):
     return not all(x==0 for x in grid[0])
# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pyTetris")
clock = pygame.time.Clock()

# Game variables
grid = create_grid()
current_shape, current_color_idx = get_random_shape()
shape_x, shape_y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0
fall_speed = 400  # ms
last_fall_time = pygame.time.get_ticks()
score = 0
game_over = False
font = pygame.font.Font(None, 36)

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                if is_valid_position(grid, current_shape, shape_x - 1, shape_y):
                    shape_x -= 1
            elif event.key == pygame.K_RIGHT:
                if is_valid_position(grid, current_shape, shape_x + 1, shape_y):
                    shape_x += 1
            elif event.key == pygame.K_DOWN:
                if is_valid_position(grid, current_shape, shape_x, shape_y + 1):
                    shape_y += 1
            elif event.key == pygame.K_UP:
                rotated_shape = rotate_shape(current_shape)
                if is_valid_position(grid, rotated_shape, shape_x, shape_y):
                    current_shape = rotated_shape

    if not game_over:
        if pygame.time.get_ticks() - last_fall_time > fall_speed:
            if is_valid_position(grid, current_shape, shape_x, shape_y + 1):
                shape_y += 1
            else:
                place_shape_on_grid(grid, current_shape, shape_x, shape_y, current_color_idx)
                cleared_lines = clear_full_lines(grid)
                if cleared_lines:
                    score += cleared_lines ** 2 * 100
                if game_over_check(grid):
                    game_over = True
                else:
                    current_shape, current_color_idx = get_random_shape()
                    shape_x, shape_y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0

            last_fall_time = pygame.time.get_ticks()
    # Drawing
    screen.fill(BLACK)
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[cell - 1],
                                 (col_idx * CELL_SIZE, row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, WHITE, (col_idx * CELL_SIZE, row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    if not game_over:
        for row_idx, row in enumerate(current_shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[current_color_idx], (
                    (shape_x + col_idx) * CELL_SIZE, (shape_y + row_idx) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, WHITE, (
                    (shape_x + col_idx) * CELL_SIZE, (shape_y + row_idx) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()