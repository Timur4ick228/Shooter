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

def init_game():
    global lost, score, countFire, hero, hero2, bullets, monsters, asteroids, current_level_index, finish
    lost = 0
    score = 0
    countFire = 0
    current_level_index = 0
    finish = False
    hero = Player('pngegg.png', 20, 420, 10)
    hero2 = Player('jan.png', 400, 420, 10, 5, 2)
    bullets = sprite.Group()
    monsters = sprite.Group()
    level_data = levels[current_level_index]
    for i in range(level_data["enemy_count"]//2):
        monsters.add(Enemy('cati.png', randint(0, 500), 0, randint(1,4)))
    asteroids = sprite.Group()
    for i in range(level_data["enemy_count"]//2):
        asteroids.add(Enemy2('asteroid.png', randint(0, 500), 0, randint(1,4)))

levels = [
    {"enemy_count": 10},
    {"enemy_count": 20},
    {"enemy_count": 30}
]

def load_level(level_index):
    global monsters, score
    monsters.empty()
    asteroids.empty()
    score = 0

    level_data = levels[level_index]
    for _ in range(level_data["enemy_count"]//2):
        monsters.add(Enemy('cati.png', randint(100, 500), 0, randint(1,4)))
    for _ in range(level_data["enemy_count"]//2):
        monsters.add(Enemy2('asteroid.png', randint(100, 500), 0, randint(1,4)))

def check_level_complete(level_index):
    if level_index > len(levels)-1:
        global finish
        finish = True
        window.blit(font2.render("YOU WIN", True, (0, 255, 0)),(200,200))
        return True
    level_data = levels[level_index]
    return score == level_data["enemy_count"]



class Player(GameSprite):
    def __init__(self, filename, x, y, speed, life=5, type_=1, sizeX=85, sizeY=85):
        super().__init__(filename, x, y, speed, sizeX, sizeY)
        self.life = life
        self.type = type_
    def update(self):
        keys_pressed = key.get_pressed()
        if self.type == 1:
            if keys_pressed[K_a] and self.rect.x >= 10:
                self.rect.x -= self.speed
            if keys_pressed[K_d] and self.rect.x <= 600:
                self.rect.x += self.speed 
        else:
            if keys_pressed[K_LEFT] and self.rect.x >= 10:
                self.rect.x -= self.speed
            if keys_pressed[K_RIGHT] and self.rect.x <= 600:
                self.rect.x += self.speed
    def fire(self):
        global countFire
        keys_pressed = key.get_pressed()
        if self.type == 1:
            if keys_pressed[K_SPACE] and countFire > 10:
                bullets.add(Bullet('bullet.png', self.rect.x, self.rect.y, 5, 30, 40))
                countFire = 0
            countFire += 1
        else:
            if keys_pressed[K_UP] and countFire > 30:
                bullets.add(Bullet('bullet.png', self.rect.x, self.rect.y, 5, 30, 40))
                countFire = 0
            countFire += 1

# class Player2(GameSprite):
#     def update(self):
#         keys_pressed = key.get_pressed()
#         if keys_pressed[K_LEFT] and self.rect.x >= 10:
#             self.rect.x -= self.speed
#         if keys_pressed[K_RIGHT] and self.rect.x <= 600:
#             self.rect.x += self.speed
#     def fire(self):
#         global countFire
#         keys_pressed = key.get_pressed()
#         if keys_pressed[K_UP] and countFire > 30:
#             bullets.add(Bullet('bullet2.png', self.rect.x, self.rect.y, 5, 90, 40))
#             countFire = 0
#         countFire += 1

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

finish = False
game = True

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
init_game()
load_level(current_level_index)
while game:

    text_score = font1.render('Счет:' + str(score), 1, (255, 255, 255))
    text_lose = font1.render('Пропущено:' + str(lost), 1 , (255, 255, 255))
    win = font2.render("YOU WIN", True, (0, 255, 0))
    lose = font2.render("YOU LOSE!", True, (0, 206, 209))
    if check_level_complete(current_level_index):
        current_level_index += 1

        if current_level_index < len(levels):
            load_level(current_level_index)
            
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN:
            if e.key == K_r:
                init_game() 
    if not finish:

        window.blit(background,(0,0))
        window.blit(text_lose, (0, 35))
        window.blit(text_score, (0, 5))
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
            monster = Enemy('cati.png', randint(80, 620), - 40, randint(1, 3), 120, 100)
            monsters.add(monster)
            if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero2, monsters, False):
                sprite.spritecollide(hero, monsters, True) or sprite.spritecollide(hero2, monsters, True)
                

        if lost >= 20 or hero.life <= 0:
            finish = True
            window.blit(lose, (200, 200))
            
        if score == levels:
            finish = True
            window.blit(win, (200, 200))
    clock.tick(60)
    display.update()