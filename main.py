import random

import pygame as pg

pg.init()
W, H = 480, 640
display = pg.display.set_mode((W, H))

GRAVITY = 1
JUMP = -30
PLATFORM_WIDTH = 105
MIN_GAP = 90
MAX_GAP = 180

score = 0

class PLayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pg.image.load('img/doodle_left.png')
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect(center=(W//2, H//2))
        self.speed = 0

    def draw(self):
        if self.rect.y > H:
            # ТУТ ПОТОМ СДЕЛАЕМ ГЕЙМ ОВЕР (но пока респавн для теста)
            self.rect.y = H//2
        else:
            display.blit(self.image, self.rect)

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rect.x -= 10
            self.image = self.image_left
        if key[pg.K_RIGHT]:
            self.rect.x += 10
            self.image = self.image_right

        if self.rect.right < 0:
            self.rect.left = W
        if self.rect.left > W:
            self.rect.right = 0

        self.speed += GRAVITY
        self.rect.y += self.speed

class BasePlatform(pg.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pg.image.load(sprite)
        self.rect = self.image.get_rect(topleft=(x, y))

    def on_collision(self, player):
        player.speed = JUMP

    def update(self):
        if self.rect.top > H:
            self.kill()

class NormalPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/green.png")

class JumpingPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/green.png")
        self.image.set_colorkey("purple")

    def on_collision(self, player):
        player.speed = JUMP + 100

platforms = pg.sprite.Group()

def spawn_platform():
    platform = platforms.sprites()[-1]
    y = platform.rect.y - random.randint(MIN_GAP, MAX_GAP)
    x = random.randint(0, W - PLATFORM_WIDTH)
    types = [NormalPlatform, JumpingPlatform]
    Plat = random.choice(types)
    platform = Plat(x, y)
    platforms.add(platform)

doodle = PLayer()

platform = NormalPlatform(W//2 - PLATFORM_WIDTH//2, H - 50)
platforms.add(platform)

def main():
    while True:
        #1
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        #2
        doodle.update()
        platforms.update()
        if pg.sprite.spritecollide(doodle, platforms, False) and doodle.speed > 0:
            doodle.speed = JUMP
        if len(platforms) < 25:
            spawn_platform()
        if doodle.speed < 0 and doodle.rect.bottom < H / 2:
            doodle.rect.y -= doodle.speed
            global score
            score += 1
            for platform in platforms:
                platform.rect.y -= doodle.speed
        #3
        display.fill('white')
        platforms.draw(display)
        doodle.draw()
        pg.display.update()
        pg.time.delay(1000 // 60)

if __name__ == '__main__':
    main()