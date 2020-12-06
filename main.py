from sprites import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self, images=pal_stay)
        self.platf = Platform(0, HEIGHT - 92, WIDTH, 92)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.platf)
        self.platforms.add(self.platf)
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
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.vel.x != 0:
            self.player.pal_stay = pal_run

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.screen.blit(background, (0, 0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()


game = Game()
background = pg.transform.scale(pg.image.load('assets/img/background.png').convert(), (WIDTH, HEIGHT))
pal_stay = load_images(path='assets/img/pal/stay', size=(144, 144))
pal_run = load_images(path='assets/img/pal/run', size=(144, 144))

while game.running:
    game.new()

pg.quit()
