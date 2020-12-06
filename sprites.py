import pygame as pg
import os
from settings import *


def load_images(path, size):
    images = []
    for i in os.listdir(path):
        img = pg.transform.scale(pg.image.load(path + os.sep + i).convert_alpha(), size)
        images.append(img)
    return images

#
# class Sprites:
#     def __init__(self, filename):
#         self.sprites = pg.image.load(filename).convert_alpha()
#
#     def get_image(self, x, y, width, height):
#         image = pg.Surface((width, height))
#         image.blit(self.sprites, (0, 0), (x, y, width, height))
#         image = pg.transform.scale(image, (144, 144))
#         return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, images):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.pal_stay = images
        self.images_left = images
        self.images_right = [pg.transform.flip(image, True, False) for image in images]
        self.current_frame = 0
        self.image = images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.last_update = pg.time.get_ticks()

    def load_images(self):
        pass

    def update(self, pal_run):
        self.acc = pg.math.Vector2(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # self.pal_stay = self.images_left
            self.pal_stay = pal_run
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # self.pal_stay = self.images_right
            self.pal_stay = pal_run
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE]:
            self.rect.x += 1
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 1
            if hits:
                self.vel.y = -PLAYER_JUMP

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        now = pg.time.get_ticks()
        if now - self.last_update >= FPS:
            self.last_update = now
            self.current_frame += 1
        if self.current_frame >= len(self.pal_stay):
            self.current_frame = 0
        self.image = self.pal_stay[self.current_frame]


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
