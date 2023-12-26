import pygame
from pygame.locals import *
from pygame.sprite import Group

# fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Race')

# define colors
red = (255, 0, 0)
green = (0, 255, 0)

# load background
bg = pygame.image.load("images/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))

# create superman class
class Superman(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/superman.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health

    def update(self):
        # movement speed
        speed = 8

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
        
        # draw hp bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))


# sprite groups
superman_group = pygame.sprite.Group()

# player
superman = Superman(int(screen_width / 2), screen_height - 100, 3)
superman_group.add(superman)

run = True
while run:

    # limit fps to 60
    clock.tick(fps)

    # draws background
    draw_bg()

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update superman
    superman.update()

    # draw sprites
    superman_group.draw(screen)

    pygame.display.update()


pygame.quit()