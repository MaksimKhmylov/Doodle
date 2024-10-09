import random

import pygame_menu as menu
import pygame as pg

from utils import *

pg.init()
icon = pg.image.load("img/doodle_left.png")
W, H = 480, 640
display = pg.display.set_mode((W, H))
pg.display.set_caption("Doodle Jump")
pg.display.set_icon(icon)

GRAVITY = 1
JUMP = -30
PLATFORM_WIDTH = 105
MIN_GAP = 90
MAX_GAP = 180


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    display.blit(img, (x, y))


class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.dead = False

    def update(self):
        super().update()

    def draw(self):
        display.blit(self.image, self.rect)

    def kill(self):
        self.dead = True
        super().kill()


class PLayer(Sprite):
    def __init__(self):
        super().__init__(W // 2, H // 2, 'img/doodle_left.png')
        self.image_left = self.image
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.speed = 0

    def draw(self):
        if self.rect.y > H:
            self.die()
        else:
            display.blit(self.image, self.rect)

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rect.x -= 5
            self.image = self.image_left
        if key[pg.K_RIGHT]:
            self.rect.x += 5
            self.image = self.image_right

        if self.rect.right < 0:
            self.rect.left = W
        if self.rect.left > W:
            self.rect.right = 0

        self.speed += GRAVITY
        self.rect.y += self.speed

    def die(self):
        draw_text("GAME OVER", pg.font.Font(None, 50), 'red', W//4, H//2)
        self.kill()


class BaseBonus(Sprite):
    def __init__(self, image_path: str, plat: 'BasePlatform'):
        img = pg.image.load(image_path)
        w = img.get_width()
        h = img.get_height()
        rect = plat.rect
        x = random.randint(rect.left + w // 2, rect.right - w // 2)
        y = rect.top - h // 2
        super().__init__(x, y, image_path)
        self.platform = plat
        self.dx = self.rect.x - self.platform.rect.x

    def on_collision(self, player):
        self.kill()

    def update(self):
        self.rect.x = self.platform.rect.x + self.dx
        if self.platform.dead:
            self.kill()


class Spring(BaseBonus):
    def __init__(self, plat):
        super().__init__('img/spring.png', plat)

    def on_collision(self, player):
        player.speed = -50
        self.image = pg.image.load('img/spring_1.png')


class BasePlatform(Sprite):
    def on_collision(self, player):
        player.speed = JUMP

    def update(self):
        if self.rect.top > H:
            self.kill()

    def attach_bonus(self, platforms):
        if random.randint(0, 100) > 90:
            bonus = random.choice([Spring])
            obj = bonus(self)
            platforms.add(obj)


class NormalPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/green.png")


class JumpingPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/purple.png")

    def on_collision(self, player):
        player.speed = JUMP * 2


class MovingPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/blue.png")
        self.direction = random.choice((-10, 10))

    def update(self):
        self.rect.x += self.direction
        if self.rect.x < 0 or self.rect.right > H - 100:
            self.direction = self.direction * -1
        if self.rect.top > H:
            self.kill()


class BreakablePlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/red.png")

    def on_collision(self, player):
        self.image = pg.image.load("img/red_broken.png")

    def attach_bonus(self, platforms):
        pass


class BaseEnemy(Sprite):
    def update(self):
        if self.rect.top > H:
            self.kill()

    def on_collision(self, player):
        player.kill()


class Hole(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "img/enemy_hole.png")


class LeftRightEnemy(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "img/enemy_u_d.png")
        self.direction = random.choice((-10, 10))

    def update(self):
        self.rect.x += self.direction
        if self.rect.x < 0 or self.rect.right > H - 100:
            self.direction = self.direction * -1
        if self.rect.top > H:
            self.kill()


class UpDownEnemy(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "img/enemy_l_r.png")

    def update(self):
        self.rect.y += 10
        if self.rect.y > H:
            self.kill()


class Game:
    def __init__(self):
        self.points = 0
        self.points_text = "0"

    def main(self):
        self.points = 0
        doodle = PLayer()
        platforms = pg.sprite.Group()
        platform = NormalPlatform(W // 2 - PLATFORM_WIDTH // 2, H - 50)
        platforms.add(platform)
        enemies = pg.sprite.Group()
        passed_time = 0
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return
            doodle.update()
            platforms.update()
            enemies.update()
            pg.sprite.spritecollide(doodle, platforms, False, collided=is_top_collision)
            hit_enemy = pg.sprite.spritecollide(doodle, enemies, False)
            if doodle.speed > 0:
                self.points += doodle.speed*GRAVITY
            if hit_enemy or doodle.dead:
                self.show_end_screen()
            if len(platforms) < 25:
                spawn_platform(platforms)
            if doodle.speed < 0 and doodle.rect.bottom < H / 2:
                doodle.rect.y -= doodle.speed
                for platform in platforms:
                    platform.rect.y -= doodle.speed
                for enemy in enemies:
                    enemy.rect.y -= doodle.speed
            passed_time = spawn_enemy(passed_time, enemies)
            display.fill('white')
            platforms.draw(display)
            enemies.draw(display)
            doodle.draw()
            pg.display.update()
            passed_time += pg.time.delay(1000 // 60)
            self.points_text = self.points

    def show_end_screen(self):
        end_menu = menu.Menu('Игра окончена', W, H,
                             theme=menu.themes.THEME_BLUE)
        end_menu.add.label(f"Очки:{self.points_text} ")
        save_to_db("No name", self.points_text)
        end_menu.add.button('Заново', self.main)
        end_menu.add.button('Меню', self.show_start_screen)
        end_menu.add.button('Выйти', menu.events.EXIT)
        end_menu.mainloop(display)

    def show_start_screen(self):
        start_screen = menu.Menu('Doodle Jump', W, H, theme=menu.themes.THEME_BLUE)
        start_screen.add.button('Начать', self.main)
        start_screen.add.button('Выйти', menu.events.EXIT)
        start_screen.add.button('Лидеры', self.leader_board)
        start_screen.mainloop(display)

    def leader_board(self):
        leader_screen = menu.Menu("Лидеры:", W, H, theme=menu.themes.THEME_BLUE)
        leaders = get_high_score()
        leader_screen.add.label(f'1 место - {leaders[0]}')
        leader_screen.add.label(f'2 место - {leaders[1]}')
        leader_screen.add.label(f'3 место - {leaders[2]}')
        leader_screen.add.button('Меню', self.show_start_screen)
        leader_screen.mainloop(display)


def spawn_enemy(delay, enemies):
    if delay > 2000:
        delay = 0
        enemy = random.choice([Hole, LeftRightEnemy, UpDownEnemy])
        x = random.randint(0, W - 80)
        e = enemy(x, -H)
        enemies.add(e)
    return delay


def is_top_collision(player: PLayer, platform: BasePlatform):
    if player.rect.colliderect(platform.rect):
        if player.speed > 0:
            if player.rect.bottom < platform.rect.bottom:
                platform.on_collision(player)


def spawn_platform(platforms):
    platform = platforms.sprites()[-1]
    y = platform.rect.y - random.randint(MIN_GAP, MAX_GAP)
    x = random.randint(0, W - PLATFORM_WIDTH)
    types = [NormalPlatform,
             NormalPlatform,
             NormalPlatform,
             JumpingPlatform,
             BreakablePlatform,
             MovingPlatform]
    plat = random.choice(types)
    platform = plat(x, y)
    platform.attach_bonus(platforms)
    platforms.add(platform)


if __name__ == '__main__':
    game = Game()
    game.show_start_screen()
