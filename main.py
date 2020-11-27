import pygame
import random
from PIL import Image
import time

pacman = Image.open('x-wing.jpg')
pacman.resize((70, 70)).save('x-wing2.png')
fruit = Image.open('C3PO.jpg')
fruit.resize((30,30)).save('C3PO-2.png')
space = Image.open('space.jpg')
space.resize((1000, 800)).save('background.png')

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

screen_width = 1000
screen_height = 800

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super(Pacman, self).__init__()
        self.surf = pygame.Surface((70, 70))
        self.surf = pygame.image.load('x-wing2.png')
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 7)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(7, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class fruit(pygame.sprite.Sprite):
    def __init__(self):
        super(fruit, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf = pygame.image.load('C3PO-2.png').convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = (random.randint(30,screen_width - 30), random.randint(30,screen_height-30)))
        self.speed = random.randint(5,7)

    def update(self):
        self.kill()

class rocket(pygame.sprite.Sprite):
    def __init__(self):
        super(rocket,self).__init__()
        self.surf = pygame.image.load('rocket1.png').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(center = (random.randint(screen_width + 20,screen_width +100), random.randint(0,screen_height)))
        self.speed = random.randint(5,15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
fontx = screen_width/2 - 30
fonty = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (77, 0, 77))
    screen.blit(score, (x,y))

output = pygame.font.Font('freesansbold.ttf', 100)
outputx = screen_width/2 - 150
outputy = screen_height/2 - 50

def show_victory(x, y):
    win = output.render("Victory", True, (230, 230, 0))
    screen.blit(win, (x, y))

output2 = pygame.font.Font('freesansbold.ttf', 100)
output2x = screen_width/2 - 150
output2y = screen_height/2 - 50

def show_defeat(x, y):
    lose = output2.render("Defeat", True, (51, 0, 0))
    screen.blit(lose, (x, y))

AddEnemy = pygame.USEREVENT + 1
pygame.time.set_timer(AddEnemy, 500)

AddFruit = pygame.USEREVENT + 2
pygame.time.set_timer(AddFruit, 500)

hero = Pacman()
clock = pygame.time.Clock()

rockets = pygame.sprite.Group()
fruits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(hero)

screen = pygame.display.set_mode((screen_width, screen_height))

color_light = (0,0,60)

color_dark = (0,0,20)

width = screen.get_width()

height = screen.get_height()

playfont = pygame.font.Font('freesansbold.ttf', 35)

text = playfont.render('PLAY', True, (139,0,0))

mesoutput = pygame.font.Font('freesansbold.ttf', 30)
mesx = screen_width/2 - 300
mesy = 40

def show_message(x, y):
    message = mesoutput.render("Welcome to Collision!" + " " + "Collect 15 C3POS to win!", True, (139,0,0))
    screen.blit(message, (x, y))

background = pygame.image.load('background.png').convert()

play = True

while play:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if width/2 <= mouse[0] <= width/2 + 140 and height/2 <= mouse[1] <= height/2 + 40:
                play = False

    pressed_keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    show_message(mesx, mesy)

    if width/2 <= mouse[0] <= width/2 + 140 and height/2 <= mouse[1] <= height/2 + 40:
        pygame.draw.rect(screen, color_light, [width/2, height/2, 140, 40])

    else:
        pygame.draw.rect(screen, color_dark, [width/2, height/2, 140, 40])

    screen.blit(text, (width/2 + 26, height/2 + 4))

    pygame.display.update()

time.sleep(1/2)

running = True

while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == AddEnemy:
            new_enemy = rocket()
            rockets.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == AddFruit and len(fruits) == 0:
            new_fruit = fruit()
            fruits.add(new_fruit)
            all_sprites.add(new_fruit)

    pressed_keys = pygame.key.get_pressed()

    hero.update(pressed_keys)

    rockets.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(hero, fruits):
        score_value += 1
        fruits.update()

    show_score(fontx, fonty)

    if score_value == 15:
        output_screen = pygame.display.set_mode((screen_width, screen_height))
        output_screen.fill((0,0,0))
        output_screen.blit(background, (0, 0))
        running = False
        show_victory(outputx, outputy)
        show_score(fontx, fonty)
    elif pygame.sprite.spritecollideany(hero, rockets):
        hero.kill()
        output_screen = pygame.display.set_mode((screen_width, screen_height))
        output_screen.fill((0, 0, 0))
        output_screen.blit(background, (0, 0))
        running = False
        show_defeat(output2x, output2y)
        show_score(fontx, fonty)


    pygame.display.flip()

    clock.tick(60)

time.sleep(2)

f = open('high score.txt', 'w')
f.write('0')
f.close()

fl = open('high score.txt', 'r')
current_score = fl.read()
fl.close()

fl2 = open('high score.txt', 'w')
if score_value > int(current_score):
    fl2.write(str(score_value))
fl2.close()


hscore = pygame.font.Font('freesansbold.ttf', 40)
hscore_x = screen_width/2 - 100
hscore_y = screen_height/2

fl3 = open('high score.txt', 'r')
highest_score = fl3.read()
fl3.close()


def show_high_score(x, y):
    hscore_text = hscore.render('High Score: ' + highest_score, True, (139,0,0))
    screen.blit(hscore_text, (x, y))


last_page = True

while last_page:

    screen.fill((0,0,0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.QUIT:
            pygame.quit()

    show_high_score(hscore_x, hscore_y)

    pygame.display.flip()

    last_page = False

time.sleep(2)