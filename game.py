import pygame
from Grid import Grid
from Tile import Tile  # Tile now auto-assigns sprites based on type

# Settings
TILE_SIZE = 50
ROWS, COLS = 10, 10
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create the grid
grid = Grid(ROWS, COLS)

# Example: set some counters (sprites auto-assigned)
grid.set_tile_type(3, 5, "counter")
grid.set_tile_type(4, 5, "counter")
grid.set_tile_type(5, 5, "counter")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the grid
    screen.fill((0,0,0))
    for r in range(ROWS):
        for c in range(COLS):
            tile = grid.get_tile(r, c)
            tile.draw(screen, TILE_SIZE)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
