import pygame
from pygame.locals import *
from pygame.sprite import Group
import random
pygame.init()

# fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Race')

# fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# define game variables
rows = 5
cols = 5
alien_cooldown = 1000 # MS
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

# define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# load background
bg = pygame.image.load("images/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))

# create text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# create superman class
class Superman(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/superman.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # movement speed
        speed = 8

        # cooldown
        cooldown = 500 # MS
        game_over = 0

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # update mask
            self.mask = pygame.mask.from_surface(self.image)

        # record time
        time_now = pygame.time.get_ticks()

        # shooting
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser = Lasers(self.rect.centerx, self.rect.top)
            laser_group.add(laser)
            self.last_shot = time_now
        
        # draw hp bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            self.kill()
            game_over = -1
        return game_over

# create laser class
class Lasers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()

# create alien class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        
# create alien laser class
class Alien_Lasers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien_laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, superman_group, False, pygame.sprite.collide_mask):
            self.kill()
            # Superman HP damaged
            superman.health_remaining -= 1

# sprite groups
superman_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_laser_group = pygame.sprite.Group()

# spawn aliens
def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()

# player
superman = Superman(int(screen_width / 2), screen_height - 100, 3)
superman_group.add(superman)

run = True
while run:

    # limit fps to 60
    clock.tick(fps)

    # draws background
    draw_bg()

    if countdown == 0:
        # random alien lasers
        time_now = pygame.time.get_ticks()
        if time_now - last_alien_shot > alien_cooldown and len(alien_laser_group) < 5 and len(alien_group) > 0:
            hostile_alien = random.choice(alien_group.sprites())
            alien_laser = Alien_Lasers(hostile_alien.rect.centerx, hostile_alien.rect.bottom)
            alien_laser_group.add(alien_laser)
            last_alien_shot = time_now

        # check if all aliens are killed
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:

            # update superman
            game_over = superman.update()

            # update sprite 
            laser_group.update()
            alien_group.update()
            alien_laser_group.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text('WINNER!!!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

    
    if countdown > 0:
        draw_text('STARTING IN', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer


    # draw sprites
    superman_group.draw(screen)
    laser_group.draw(screen)
    alien_group.draw(screen)
    alien_laser_group.draw(screen)

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()