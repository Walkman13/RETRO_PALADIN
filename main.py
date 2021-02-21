from sprites import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.flags = pg.FULLSCREEN | pg.DOUBLEBUF
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(SIZE, vsync=1)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'assets/img')
        self.background = pg.transform.scale(pg.image.load('assets/img/background.png').convert(), (WIDTH, HEIGHT))
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.lights = pg.sprite.Group()
        self.player = Player(self)
        ground_x_pos = 0
        for i in range(5):
            Ground(self, ground_x_pos, HEIGHT - 96)
            ground_x_pos += 288
        for urn in URN_POSITIONS:
            Urns(self, *urn)
        for lamp in LAMP_POSITIONS:
            Lamps(self, *lamp)
        for fire in FIRE_POSITIONS:
            Fire(self, *fire)
        self.run()

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # Pay attention to it
                if lowest.rect.right + 100 > self.player.pos.x > lowest.rect.left - 100:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.jump()
            if event.type == pg.KEYUP:
                self.player.jump_cut()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()


game = Game()

while game.running:
    game.new()

pg.quit()
