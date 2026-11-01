import asyncio
import pygame
pygame.init()
WIDTH =500
HEIGHT = 600
slide = 1
song = 1
level_count = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow the Rythm")
background = pygame.image.load("assets/image_assets/ftr_bg.png").convert()
background_blank = pygame.image.load("assets/image_assets/bg.png").convert()
start_button = pygame.image.load("assets/image_assets/start.png").convert_alpha()
left_arrow = pygame.image.load("assets/image_assets/left_arrow.png").convert_alpha()
back_arrow = pygame.image.load("assets/image_assets/left_arrow.png").convert_alpha()
right_arrow = pygame.image.load("assets/image_assets/right_arrow.png").convert_alpha()
font = pygame.font.SysFont(None, 50)
song_text = font.render("", True, (255, 255, 255))
start_button = pygame.transform.smoothscale(start_button, ((start_button.get_width())*0.1, (start_button.get_height())*0.1))
right_arrow = pygame.transform.smoothscale(right_arrow, ((right_arrow.get_width())*0.03, (right_arrow.get_height())*0.03))
left_arrow = pygame.transform.smoothscale(left_arrow, ((left_arrow.get_width())*0.3, (left_arrow.get_height())*0.3))
back_arrow = pygame.transform.smoothscale(back_arrow, ((back_arrow.get_width())*0.1, (back_arrow.get_height())*0.1))
start_rect = start_button.get_rect(topleft=(150, 400))
left_arrow_rect = left_arrow.get_rect(topleft=(20, 500))
back_arrow_rect = back_arrow.get_rect(topleft=(425, 20))
right_arrow_rect = right_arrow.get_rect(topleft=(300, 500))
start_mask = pygame.mask.from_surface(start_button)
right_arrow_mask = pygame.mask.from_surface(right_arrow)
left_arrow_mask = pygame.mask.from_surface(left_arrow)
back_arrow_mask = pygame.mask.from_surface(back_arrow)
clock = pygame.time.Clock()
font = pygame.font.SysFont(False, 75)
song_name = font.render("", True, (255, 255, 255))
song_names = ["The Tutorial","The beggining", "hard level"]
#mv ~/Downloads/bg.png ~/Desktop/hack_club_projects/follow_the_rythm/assets/image_assets/
def draw_game():
    global font
    font = pygame.font.SysFont(False, 50)
    song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
    screen.blit(background_blank, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (100, 0, WIDTH-200, HEIGHT))
    screen.blit(song_text, ((WIDTH/2)-(17*(len(song_names[song-1])/2)), 5))
    screen.blit(back_arrow, (425, 20))
def draw_bg():
    global font
    font = pygame.font.SysFont(False, 75)
    screen.blit(background, (0, 0))
    screen.blit(start_button, (150, 400))
def level_select():
    global song_name, song_text, song_names, song, font
    font = pygame.font.SysFont(False, 75)
    song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
    screen.blit(background_blank, (0, 0))
    song_name = font.render(f"level : {song}", True, (255, 255, 255))
    if song != 1:
        screen.blit(left_arrow, (20, 500))
    if song != level_count:
        screen.blit(right_arrow, (300, 500))
    screen.blit(start_button, (150, 300))            
    screen.blit(song_text, ((WIDTH/2)-(27*(len(song_names[song-1])/2)), 50))
    screen.blit(song_name, (5, 5))
    screen.blit(back_arrow, (425, 20))

async def main():
    running = True
    global slide, song, level_count, song_name, song_text, start_rect, start_mask
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
                        song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
                        start_rect = start_button.get_rect(topleft=(150, 300))
                        start_mask = pygame.mask.from_surface(start_button)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and slide == 2:
                if left_arrow_rect.collidepoint(event.pos) and song != 1:
                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - left_arrow_rect.x,
                        event.pos[1] - left_arrow_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if left_arrow_mask.get_at(local_pos):
                        song-=1
                        song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
                elif right_arrow_rect.collidepoint(event.pos) and song != level_count:
                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - right_arrow_rect.x,
                        event.pos[1] - right_arrow_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if right_arrow_mask.get_at(local_pos):
                        song+=1
                        song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
                elif back_arrow_rect.collidepoint(event.pos):

                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - back_arrow_rect.x,
                        event.pos[1] - back_arrow_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if back_arrow_mask.get_at(local_pos):
                        slide-=1
                        start_rect = start_button.get_rect(topleft=(150, 400))
                        start_mask = pygame.mask.from_surface(start_button)
                        song_text = font.render("", True, (255, 255, 255))
                elif start_rect.collidepoint(event.pos):
                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - start_rect.x,
                        event.pos[1] - start_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if start_mask.get_at(local_pos):
                        slide+=1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and slide == 3:
                if back_arrow_rect.collidepoint(event.pos):

                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - back_arrow_rect.x,
                        event.pos[1] - back_arrow_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if back_arrow_mask.get_at(local_pos):
                        slide-=1

        clock.tick(60)
        screen.fill((0, 0, 0))
        if slide == 1:
            draw_bg()
        elif slide == 2:
            level_select()
        elif slide == 3:
            draw_game()
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
