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
platforms = pg.sprite.Group()


class PLayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pg.image.load('img/doodle_left.png')
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect(center=(W//2, H//2))
        self.power = 1
        self.speed = 0

    def draw(self):
        if self.rect.y > H:
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

    def jump(self):
        self.speed = JUMP*self.power
        self.power = 1


class BasePlatform(pg.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pg.image.load(sprite)
        self.rect = self.image.get_rect(topleft=(x, y))

    def on_collision(self, player):
        player.power = 1
        doodle.jump()

    def update(self, doodle):
        if pg.sprite.spritecollide(doodle, platforms, False) and doodle.speed > 0:
            self.on_collision(doodle)
        if self.rect.top > H:
            self.kill()


class NormalPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/green.png")


class JumpingPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/purple.png")

    def on_collision(self, player):
        player.power = 1.5
        doodle.jump()


class MovingPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/blue.png")
        self.direction = 10

    def update(self, doodle):
        self.rect.x += self.direction
        if pg.sprite.spritecollide(doodle, platforms, False) and doodle.speed > 0:
            self.on_collision(doodle)
        if self.rect.top > H:
            self.kill()
        if self.rect.x < 0 or self.rect.right > H-100:
            self.direction = self.direction * -1

class BreakablePlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/red.png")

    def on_collision(self, player):
        player.power = 0
        self.image = pg.image.load("img/red_broken.png")

def spawn_platform():
    platform = platforms.sprites()[-1]
    y = platform.rect.y - random.randint(MIN_GAP, MAX_GAP)
    x = random.randint(0, W - PLATFORM_WIDTH)
    types = [NormalPlatform, NormalPlatform, JumpingPlatform, MovingPlatform, BreakablePlatform]
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
        platforms.update(doodle)
        if len(platforms) < 25:
            spawn_platform()
        if doodle.speed < 0 and doodle.rect.bottom < H / 2:
            doodle.rect.y -= doodle.speed
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
