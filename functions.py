from settings import *


def draw_window():
    global ANIM_COUNT
    global PAL_X_POS
    global PAL_Y_POS
    global JUMP_COUNT
    global FLIP

    bg_surface = pygame.transform.scale(pygame.image.load('assets/img/background.png').convert(), (WIDTH, HEIGHT))

    pal_anim_stay = []
    for i in range(4):
        filename = f'pal_{i}.png'
        img = pygame.transform.scale(pygame.image.load(f'assets/img/pal/stay/{filename}').convert_alpha(), (144, 144))
        pal_anim_stay.append(img)
    surf_stay = pal_anim_stay[ANIM_COUNT // 30]

    pal_anim_run = []
    for i in range(8):
        filename = f'pal_run_{i}.png'
        img = pygame.transform.scale(pygame.image.load(f'assets/img/pal/run/{filename}').convert_alpha(), (144, 144))
        pal_anim_run.append(img)
    surf_run = pal_anim_run[ANIM_COUNT // 15]

    pal_anim_jump = []
    for i in range(2):
        filename = f'pal_jump_{i}.png'
        img = pygame.transform.scale(pygame.image.load(f'assets/img/pal/jump/{filename}').convert_alpha(), (144, 144))
        pal_anim_jump.append(img)
    surf_jump = pal_anim_jump[ANIM_COUNT // 60]

    WINDOW.blit(bg_surface, (0, 0))

    if ANIM_COUNT + 1 >= FPS:
        ANIM_COUNT = 0

    if FLIP:
        surf_run = pygame.transform.flip(surf_run, True, False)
        surf_stay = pygame.transform.flip(surf_stay, True, False)
        surf_jump = pygame.transform.flip(surf_jump, True, False)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        FLIP = False
        WINDOW.blit(surf_run, (PAL_X_POS, PAL_Y_POS))
        PAL_X_POS -= SPEED
        ANIM_COUNT += 1
    elif keys[pygame.K_RIGHT]:
        FLIP = True
        WINDOW.blit(surf_run, (PAL_X_POS, PAL_Y_POS))
        PAL_X_POS += SPEED
        ANIM_COUNT += 1

    elif keys[pygame.K_SPACE]:
        if JUMP_COUNT >= -10:
            WINDOW.blit(surf_jump, (PAL_X_POS, PAL_Y_POS))
            PAL_Y_POS -= 3
            JUMP_COUNT -= 1
        else:
            WINDOW.blit(surf_jump, (PAL_X_POS, PAL_Y_POS))
            PAL_Y_POS += 1
            JUMP_COUNT += 1

    else:
        WINDOW.blit(surf_stay, (PAL_X_POS, PAL_Y_POS))
        ANIM_COUNT += 1

    pygame.display.flip()
