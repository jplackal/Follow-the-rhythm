import asyncio
import pygame
pygame.init()
screen_mult = 1.2
WIDTH =500
HEIGHT = 600
slide = 1
song = 1
level_count = 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow the Rythm")
background = pygame.image.load("assets/image_assets/ftr_bg.png").convert()
start_button = pygame.image.load("assets/image_assets/start.png").convert_alpha()
left_arrow = pygame.image.load("assets/image_assets/left_arrow.png").convert_alpha()
right_arrow = pygame.image.load("assets/image_assets/right_arrow.png").convert_alpha()
start_button = pygame.transform.smoothscale(start_button, ((start_button.get_width())*0.1, (start_button.get_height())*0.1))
right_arrow = pygame.transform.smoothscale(right_arrow, ((right_arrow.get_width())*0.03, (right_arrow.get_height())*0.03))
left_arrow = pygame.transform.smoothscale(left_arrow, ((left_arrow.get_width())*0.3, (left_arrow.get_height())*0.3))
start_rect = start_button.get_rect(topleft=(150, 400))
left_arrow_rect = left_arrow.get_rect(topleft=(20, 500))
right_arrow_rect = right_arrow.get_rect(topleft=(300, 500))
start_mask = pygame.mask.from_surface(start_button)
right_arrow_mask = pygame.mask.from_surface(right_arrow)
left_arrow_mask = pygame.mask.from_surface(left_arrow)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
#mv ~/Downloads/left_arrow.png ~/Desktop/hack_club_projects/follow_the_rythm/assets/image_assets/
def draw_bg():
        screen.blit(background, (0, 0))
        screen.blit(start_button, (150, 400))
def level_select():
        if song != 1:
            screen.blit(left_arrow, (20, 500))
        if song != level_count:
            screen.blit(right_arrow, (300, 500))

async def main():
    running = True
    global slide, song, level_count
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and slide == 1:
                if start_rect.collidepoint(event.pos):
                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - start_rect.x,
                        event.pos[1] - start_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if start_mask.get_at(local_pos):
                        song = 1
                        slide+=1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and slide == 2:
                if left_arrow_rect.collidepoint(event.pos) and song != 1:
                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - left_arrow_rect.x,
                        event.pos[1] - left_arrow_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if left_arrow_mask.get_at(local_pos):
                        song-=1
                elif right_arrow_rect.collidepoint(event.pos) and song != level_count:
                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - right_arrow_rect.x,
                        event.pos[1] - right_arrow_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if right_arrow_mask.get_at(local_pos):
                        song+=1
        clock.tick(60)
        screen.fill((0, 0, 0))
        if slide == 1:
            draw_bg()
        elif slide == 2:
            level_select()
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
