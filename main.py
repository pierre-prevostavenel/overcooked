import pygame
from pygame.sprite import LayeredUpdates, Sprite
from MySprite import MySprite
from Player import Player

pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
player = Player()

all_sprites = LayeredUpdates()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # On inverse la valeur de manual_control
                player.manual_control = not player.manual_control

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)  # Order is based on layer
    pygame.display.flip()
    player.update()
    clock.tick(60)

pygame.quit()
