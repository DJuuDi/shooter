from random import choice, randint
from typing import Any
from pygame import *

init()
font.init()
font1 = font.SysFont("Impact", 100)
game_over_text = font1.render("GAME OVER", True, (150, 100, 0))
mixer.init()
mixer.music.load('space.ogg')
# mixer.music.play()
mixer.music.set_volume(0.2)
bullet_sound = mixer.Sound("fire.ogg")
bullet_sound.set_volume(0.5)


screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

window = display.set_mode((WIDTH,HEIGHT), flags=FULLSCREEN)
FPS = 90
clock = time.Clock()

bg = image.load('infinite_starts.jpg')
bg = transform.scale(bg,(WIDTH,HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT

player_img = image.load("spaceship.png")
bullet_img = image.load("lazer.png")
enemy_img = image.load("alien.png")
all_sprites = sprite.Group()

class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 5
        self.bg_speed = 2
        self.max_speed = 30

    def shoot(self):
        new_bullet = Bullet(bullet_img, 10, 20, self.rect.left, self.rect.top)
        new_bullet = Bullet(bullet_img, 10, 20, self.rect.right -10, self.rect.top)
        bullet_sound.play()
        
    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_w] and self.rect.y > 200:
            self.rect.y -= self.speed
            if self.bg_speed < self.max_speed:
                self.bg_speed += 0.1
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        enemy_collide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100

bullets = sprite.Group()
class Bullet(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.rect.centerx = x
        self.rect.bottom = y
        self.damage = 100
        self.speed = 10  
        enemys.add(self) 

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(Sprite):
    def __init__(self, sprite_img, width, height):
        rand_x = randint(0, WIDTH-width)
        super().__init__(sprite_img, width, height, rand_x, -200)
        self.damage = 100
        self.speed = 4    
        enemys.add(self) 

    def update(self):
        self.rect.y += player.bg_speed +2
        if self.rect.y > HEIGHT:
            self.kill()

player = Player(player_img, 100, 70, 300, 300)
enemys = sprite.Group()
enemy1 = Enemy(enemy_img, 80, 60)
start_time = time.get_ticks()
enemy_spawn_time = time.get_ticks()
spawn_interval = randint(1,100)
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
            if e.key == K_SPACE:
                player.shoot()

    window.blit(bg,(0,bg_y1))
    window.blit(bg,(0,bg_y2))
    bg_y1 += player.bg_speed
    bg_y2 += player.bg_speed

    if bg_y1 > HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 > HEIGHT:
        bg_y2 = -HEIGHT

    if player.hp <= 0:
        finish = True

    now = time.get_ticks()
    if now - enemy_spawn_time > spawn_interval:
        enemy1 = Enemy(enemy_img, 80, 60)
        enemy_spawn_time = time.get_ticks()
        spawn_interval = randint(500,5000)

    collide_list = sprite.spritecollide(player, enemys, True, sprite.collide_mask)
    if len(collide_list) > 0:
        finish = True

    all_sprites.draw(window)
    if not finish:
        all_sprites.update()
    if finish:
        window.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
    display.update()
    clock.tick(FPS)