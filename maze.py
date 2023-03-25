#создай игру "Лабиринт"!
import pygame
pygame.init()

pygame.font.init()
font1 = pygame.font.SysFont("Arial", 70)
Win = font1.render("БИТКОИН СПАСЕН", True, (0, 255, 100))
Lose = font1.render("БИТКОИН УМЕР", True, (255, 0, 100))





pygame.mixer.init()
pygame.mixer.music.load('Rick.ogg')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)

money = pygame.mixer.Sound('money.ogg')
kick = pygame.mixer.Sound('kick.ogg')
secretSound = pygame.mixer.Sound('secret.ogg')



win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("ЛАБИРИНТ")
background = pygame.transform.scale(pygame.image.load('background.jpg'), (700, 500))
clock = pygame.time.Clock()
FPS = 60
game = True



secretik = False


class MySprite(pygame.sprite.Sprite):
    def __init__(self, picture, x, y, width, height, side='right', speed=5):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.side = side
        self.speed = speed
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def go(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x <= 625:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y >=0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y <= 425:
            self.rect.y += self.speed

        if keys[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x <= 625:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y >=0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y <= 425:
            self.rect.y += self.speed


class Enemy(MySprite):
    def update(self):
        if self.rect.x >= 625:
            self.side = 'left'
        if self.rect.x <= 525:
            self.side = 'right'

        if self.side == 'right':
            self.rect.x += 1
        if self.side == 'left':
            self.rect.x -= 1
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = wall_width
        self.height = wall_height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

hero = MySprite(picture = 'hero.png', x=70, y=70, width=60, height=60)
cyborg = Enemy(picture = 'cyborg.png', x=600, y=300, width=70, height=70)
treasure = MySprite(picture = 'bitcoin.png', x = 600, y = 400, width=80, height=80)

secret = MySprite(picture = 'secret.png', x=407, y=377, width=60, height=60)


w1 = Wall(255, 205, 50, 50, 50, 10, 400)
w2 = Wall(255, 205, 50, 50, 50, 475, 10)
w3 = Wall(255, 205, 50, 50, 450, 475, 10)

w4 = Wall(255, 205, 50, 525, 160, 10, 300)

w5 = Wall(255, 205, 50, 175, 50, 10, 300)

w6 = Wall(255, 205, 50, 350, 160, 10, 300)

secretWall = Wall(255, 50, 50, 525, 50, 10, 120)

finish = False

while game:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print('x', x)
            print('y', y)

    if finish != True:
        win.blit(background, (0, 0))
        hero.reset()
        cyborg.reset()
        treasure.reset()


        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        
        if secretik != True:
            secretWall.draw_wall()
            secret.reset()
            
            if pygame.sprite.collide_rect(hero, secretWall):
                hero.rect.x = 70
                hero.rect.y = 70

            if pygame.sprite.collide_rect(hero, secret):
                secretik = True
                secretSound.play()
                hero.rect.x = 70
                hero.rect.y = 70

        hero.go()
        cyborg.update()
        
        if pygame.sprite.collide_rect(hero, treasure):
            money.play()
            finish = True
            win.blit(Win, (30, 200))
        
        if pygame.sprite.collide_rect(hero, cyborg): 
            kick.play()
            finish = True
            win.blit(Lose, (30, 200))

        if pygame.sprite.collide_rect(hero, w1) or pygame.sprite.collide_rect(hero, w2) or pygame.sprite.collide_rect(hero, w3) or pygame.sprite.collide_rect(hero, w4) or pygame.sprite.collide_rect(hero, w5) or pygame.sprite.collide_rect(hero, w6):
            hero.rect.x = 70
            hero.rect.y = 70


        

    clock.tick(FPS)
    pygame.display.update()