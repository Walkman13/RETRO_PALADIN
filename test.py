import pygame as pg
import os

pg.init()

SIZE = WIDTH, HEIGHT = (1280, 720)
FPS = 120
SPEED = 6
ANIM_COUNT = 0
PAL_X_POS = 900
PAL_Y_POS = 485

# flags = pygame.SCALED | pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pg.display.set_mode(SIZE)
clock = pg.time.Clock()


def load_images(path, size):
    images = []
    for i in os.listdir(path):
        img = pg.transform.scale(pg.image.load(path + os.sep + i).convert_alpha(), size)
        images.append(img)
    return images


class Player(pg.sprite.Sprite):
    def __init__(self, position, images):
        super(Player, self).__init__()
        self.size = (144, 144)
        self.rect = pg.Rect(position, self.size)
        self.images = images
        self.images_right = images
        self.images_left = [pg.transform.flip(image, True, False) for image in images]
        self.index = 0
        self.image = images[self.index]
        self.velocity = pg.math.Vector2(0, 0)
        self.last_update = pg.time.get_ticks()

    def move(self):
        pass

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update >= FPS:
            self.last_update = now
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


background = pg.transform.scale(pg.image.load('assets/img/background.png').convert(), SIZE)

pal_stay = load_images(path='assets/img/pal/stay', size=(144, 144))
player = Player(position=(PAL_X_POS, PAL_Y_POS), images=pal_stay)
all_sprites = pg.sprite.Group(player)

GAME_IS_DONE = False

while not GAME_IS_DONE:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_IS_DONE = True

    all_sprites.update()

    screen.blit(background, (background.get_rect()))
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
