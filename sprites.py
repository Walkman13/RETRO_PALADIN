import pygame as pg
from settings import *


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (144, 144))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.fliping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames_l[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)

    def load_images(self):
        self.standing_frames_l = [self.game.spritesheet.get_image(0, 0, 48, 48),
                                  self.game.spritesheet.get_image(48, 0, 48, 48),
                                  self.game.spritesheet.get_image(96, 0, 48, 48),
                                  self.game.spritesheet.get_image(144, 0, 48, 48)]
        self.standing_frames_r = []
        for frame in self.standing_frames_l:
            frame.set_colorkey(BLACK)
            self.standing_frames_r.append(pg.transform.flip(frame, True, False))

        self.walk_frames_l = [self.game.spritesheet.get_image(0, 48, 48, 48),
                            self.game.spritesheet.get_image(48, 48, 48, 48),
                            self.game.spritesheet.get_image(96, 48, 48, 48),
                            self.game.spritesheet.get_image(144, 48, 48, 48)]
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
            self.walk_frames_r.append(pg.transform.flip(frame, True, False))

        self.jump_frames_l = [self.game.spritesheet.get_image(0, 96, 48, 48),
                              self.game.spritesheet.get_image(48, 96, 48, 48)]
        self.jump_frames_r = []
        for frame in self.jump_frames_l:
            frame.set_colorkey(BLACK)
            self.jump_frames_r.append(pg.transform.flip(frame, True, False))

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = pg.math.Vector2(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.fliping = False
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.fliping = True
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 120:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # OMG!! Refactor this!!
        if self.jumping:
            bottom = self.rect.bottom
            if not self.fliping:
                if self.vel.y < 0:
                    self.current_frame = 0
                    self.image = self.jump_frames_l[self.current_frame]
                else:
                    self.current_frame = 1
                    self.image = self.jump_frames_l[self.current_frame]
            else:
                if self.vel.y < 0:
                    self.current_frame = 0
                    self.image = self.jump_frames_r[self.current_frame]
                else:
                    self.current_frame = 1
                    self.image = self.jump_frames_r[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_l)
                bottom = self.rect.bottom
                if not self.fliping:
                    self.image = self.standing_frames_l[self.current_frame]
                else:
                    self.image = self.standing_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
