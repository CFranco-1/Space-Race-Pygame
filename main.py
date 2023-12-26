import pygame
from pygame.locals import *

# fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Race')

# load background
bg = pygame.image.load("images/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))

run = True
while run:

    # limit fps to 60
    clock.tick(fps)

    # draws background
    draw_bg()

    # Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()