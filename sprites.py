import pygame as pg
import os
from settings import *


def load_images(path, size):
    images = []
    for i in os.listdir(path):
        img = pg.transform.scale(pg.image.load(path + os.sep + i).convert_alpha(), size)
        images.append(img)
    return images


class Player(pg.sprite.Sprite):
    def __init__(self, game, images):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.images = images
        self.images_left = images
        self.images_right = [pg.transform.flip(image, True, False) for image in images]
        self.index = 0
        self.image = images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.last_update = pg.time.get_ticks()

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = pg.math.Vector2(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.images = self.images_left
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.images = self.images_right
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        now = pg.time.get_ticks()
        if now - self.last_update >= FPS:
            self.last_update = now
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
