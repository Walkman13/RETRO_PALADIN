from functions import *


clock = pygame.time.Clock()

GAME_IS_DONE = False

while not GAME_IS_DONE:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_IS_DONE = True

    draw_window()
