import pygame as pg

GRAVITY = 1
JUMP = -30
PLATFORM_WIDTH = 105
MIN_GAP = 90
MAX_GAP = 180

pg.init()
W, H = 480, 640
display = pg.display.set_mode((W, H))

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pg.image.load('img/doodle_left.png')
        self.image = self.image_left
        self.image_right = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(W // 2, H // 2))
        self.speed = 0

    def draw(self):
        if self.rect.y > H:
            self.rect.y = H // 2
        else:
            display.blit(self.image, self.rect)


    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= 5
        self.image = self.image_left
        if keys[pg.K_RIGHT]:
            self.rect.x += 5
        self.image = self.image_right
        if self.rect.left > W:
            self.rect.left = 0
        if self.rect.right < 0:
            self.rect.right = W

        self.speed += GRAVITY
        self.rect.y += self.speed


class Game:
    def gui(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                quit()

    def main(self):
        doodle = Player()
        while True:
            doodle.update()
            doodle.draw()
            self.gui()
            display.fill('white')
            pg.display.update()
            pg.time.delay(1000 // 60)


if __name__ == '__main__':
    game = Game()
    game.main()