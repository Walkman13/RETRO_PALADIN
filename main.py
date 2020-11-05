import pygame


pygame.mixer.init()
pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 120
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

rend = pygame.transform.scale(pygame.image.load('assets/img/rend.png').convert_alpha(), (WIDTH, HEIGHT))
bg_surface = pygame.transform.scale(pygame.image.load('assets/img/background.png').convert(), (WIDTH, HEIGHT))
# paladin = pygame.transform.scale(pygame.image.load('assets/img/pal/stay/pal_0.png').convert_alpha(), (336, 192))

pal_anim_stay = []
for i in range(4):
    filename = f'pal_{i}.png'
    img = pygame.transform.scale(pygame.image.load(f'assets/img/pal/stay/{filename}').convert_alpha(), (288, 144))
    pal_anim_stay.append(img)

pal_anim_run = []
for i in range(4):
    filename = f'pal_run_{i}.png'
    img = pygame.transform.scale(pygame.image.load(f'assets/img/pal/run/{filename}').convert_alpha(), (288, 144))
    pal_anim_run.append(img)

speed = 2
bg_x_pos = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((288, 144))
        self.image = pal_anim_stay[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 160)
        self.frame = 0
        self.frame_rate = 30
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        self.last_update = now
        self.frame += 1


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

GAME_IS_DONE = False

while not GAME_IS_DONE:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_IS_DONE = True

    # Отрисовка фона с цикличной прокруткой влево и вправо
    # Текущая позиция по Х
    x_current = bg_x_pos % WIDTH

    if x_current > 0:
        x_additional = x_current - WIDTH
    else:
        x_additional = x_current + WIDTH

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bg_x_pos += speed
    if keys[pygame.K_RIGHT]:
        bg_x_pos -= speed

    screen.blit(bg_surface, (x_current, 0))
    screen.blit(bg_surface, (x_additional, 0))

    all_sprites.update()
    all_sprites.draw(screen)

    screen.blit(rend, (0, 0))

    pygame.display.flip()

pygame.quit()
