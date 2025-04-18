from pygame import *
from random import randint

window = display.set_mode((700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, sizeX = 85, sizeY = 85):
        super().__init__()
        self.image = transform.scale(image.load(filename), (sizeX, sizeY))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 600:
            self.rect.x += self.speed
    def fire(self):
        global countFire
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and countFire > 10:
            bullets.add(Bullet('bullet2.png', self.rect.x, self.rect.y, 5, 90, 40))
            countFire = 0
        countFire += 1

class Player2(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >= 10:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x <= 600:
            self.rect.x += self.speed
    def fire(self):
        global countFire
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and countFire > 30:
            bullets.add(Bullet('bullet2.png', self.rect.x, self.rect.y, 5, 90, 40))
            countFire = 0
        countFire += 1

lost = 0
score = 0
life = 4

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0 , 600)
            self.speed = randint(1 , 3)
            lost = lost + 1

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0 , 600)
            self.speed = randint(1 , 3)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 100:
            self.kill

background = transform.scale(image.load('monkey.jpg'), (700,500))

clock = time.Clock()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

shoot = mixer.Sound('fire.ogg')

hero = Player('mm.png', 20, 420, 10)
hero2 = Player2('biger.png', 400, 420, 10)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 5):
    monsters.add(Enemy('cat.png', 260, 30, 3))
asteroids = sprite.Group()
for i in range(1, 3):
    asteroids.add(Enemy2('asteroid.png', 160, 10, 3))
finish = False
game = True

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)


countFire = 0

while game:
    #text_life = font1.render('Жизни:' + str(life), (255, 255, 255)) 
    text_score = font1.render('Счет:' + str(score), 1, (255, 255, 255))
    text_lose = font1.render('Пропущено:' + str(lost), 1 , (255, 255, 255))
    win = font2.render("YOU WIN", True, (0, 255, 0))
    lose = font2.render("YOU LOSE!", True, (0, 206, 209))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:

        window.blit(background,(0,0))
        window.blit(text_lose, (0, 35))
        window.blit(text_score, (0, 5))
        #window.blit(text_life, (0, 500))
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        hero2.update()
        hero.update()
        monsters.update()
        asteroids.update()
        hero.reset()
        hero2.reset()
        hero.fire()
        hero2.fire()
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('cat.png', randint(80, 620), - 40, randint(1, 3), 85, 85)
            monsters.add(monster)
            if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero2, monsters, False):
                sprite.spritecollide(hero, monsters, True) or sprite.spritecollide(hero2, monsters, True)
                life = life - 1

        if lost >= 10 or life <= 0:
            finish = True
            window.blit(lose, (200, 200))
            
        if score == 20:
            finish = True
            window.blit(win, (200, 200))
    clock.tick(60)
    display.update()