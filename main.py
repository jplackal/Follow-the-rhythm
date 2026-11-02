import asyncio
import pygame
pygame.init()
WIDTH =500
HEIGHT = 600
slide = 4
song = 1
level_count = 3
score = 0
new = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow the Rythm")
background = pygame.image.load("assets/image_assets/ftr_bg.png").convert()
background_blank = pygame.image.load("assets/image_assets/bg.png").convert()
start_button = pygame.image.load("assets/image_assets/start.png").convert_alpha()
miss = pygame.image.load("assets/image_assets/miss.png").convert_alpha()
early = pygame.image.load("assets/image_assets/early.png").convert_alpha()
late = pygame.image.load("assets/image_assets/late.png").convert_alpha()
perfect = pygame.image.load("assets/image_assets/perfect.png").convert_alpha()
left_arrow = pygame.image.load("assets/image_assets/left_arrow.png").convert_alpha()
back_arrow = pygame.image.load("assets/image_assets/left_arrow.png").convert_alpha()
right_arrow = pygame.image.load("assets/image_assets/right_arrow.png").convert_alpha()
check_box = pygame.image.load("assets/image_assets/check_box.png").convert_alpha()
font = pygame.font.SysFont(None, 50)
song_text = font.render("", True, (255, 255, 255))
start_button = pygame.transform.smoothscale(start_button, ((start_button.get_width())*0.1, (start_button.get_height())*0.1))
right_arrow = pygame.transform.smoothscale(right_arrow, ((right_arrow.get_width())*0.03, (right_arrow.get_height())*0.03))
left_arrow = pygame.transform.smoothscale(left_arrow, ((left_arrow.get_width())*0.3, (left_arrow.get_height())*0.3))
back_arrow = pygame.transform.smoothscale(back_arrow, ((back_arrow.get_width())*0.1, (back_arrow.get_height())*0.1))
check_box = pygame.transform.smoothscale(check_box, ((check_box.get_width())*0.1, (check_box.get_height())*0.1))
miss = pygame.transform.smoothscale(miss, ((miss.get_width())*0.03, (miss.get_height())*0.03))
late = pygame.transform.smoothscale(late, ((late.get_width())*0.03, (late.get_height())*0.03))
early = pygame.transform.smoothscale(early, ((early.get_width())*0.03, (early.get_height())*0.03))
perfect = pygame.transform.smoothscale(perfect, ((perfect.get_width())*0.03, (perfect.get_height())*0.03))
start_rect = start_button.get_rect(topleft=(150, 400))
left_arrow_rect = left_arrow.get_rect(topleft=(20, 500))
back_arrow_rect = back_arrow.get_rect(topleft=(425, 20))
right_arrow_rect = right_arrow.get_rect(topleft=(300, 500))
check_box_rect = check_box.get_rect(topleft=(150, 450))
start_mask = pygame.mask.from_surface(start_button)
right_arrow_mask = pygame.mask.from_surface(right_arrow)
left_arrow_mask = pygame.mask.from_surface(left_arrow)
back_arrow_mask = pygame.mask.from_surface(back_arrow)
check_box_mask = pygame.mask.from_surface(check_box)
clock = pygame.time.Clock()
font = pygame.font.SysFont(False, 75)
song_name = font.render("", True, (255, 255, 255))
high_score_text = font.render("", True, (255, 255, 255))
last_score_text = font.render("", True, (255, 255, 255))
song_names = ["Tutorial","The beggining", "hard level"]
score_text = font.render("", True, (255, 255, 255))
song_speeds = [4,2,3]
pending = [[],[]]
high_scores = [0,0,0]
last_score = [0,0,0]
songs_notes = [[[1, 2, 3, 4, 1, 2, 3, 4, 1, 3, 2, 4],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
               [[2,4,1,3],
                [1,2,3,4]],
               [[4,3,2,1],
                [1,2,5,6]]]
note_spacing = 72
time = 0
speed = 3
colors = [(240, 105, 105), (115, 205, 130), (245, 220, 105), (105, 165, 235)]
click = 0
def draw_game_end():
    global high_score_text, last_score_text, new, song_text, song_name
    font = pygame.font.SysFont(None, 50)
    screen.blit(background_blank, (0, 0))
    screen.blit(check_box, (150, 450))
    song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
    song_name = font.render(f"level : {song}", True, (255, 255, 255))
    if new == 0:
        screen.blit(high_score_text, ((WIDTH/2)-(17*(len(f"High Score : {high_scores[song-1]}")/2)), 150))
        high_score_text = font.render(f"High Score : {high_scores[song-1]}", True, (255, 255, 255))
    else:
        screen.blit(high_score_text, ((WIDTH/2)-(17*(len(f"NEW High Score : {high_scores[song-1]}")/2)), 150))
        high_score_text = font.render(f"NEW High Score : {high_scores[song-1]}", True, (255, 255, 255))
    last_score_text = font.render(f"Score : {last_score[song-1]}", True, (255, 255, 255))
    screen.blit(last_score_text, ((WIDTH/2)-(17*(len(f"Score : {last_score[song-1]}")/2)), 200))
    screen.blit(song_text, ((WIDTH/2)-(17*(len(f"{song_names[song-1]}")/2)), 100))
    screen.blit(song_name, ((WIDTH/2)-(17*(len(f"level : {song}")/2)), 50))

def check_game_end():
    global slide, score, start_rect, new
    for i in range (len(pending[0])-1,-1,-1):
        if 0-(pending[1][i]*note_spacing)+time >800:
            if pending[2][i] == 0:
                score -= 1
            del pending[0][i]
            del pending[1][i]
            del pending[2][i]
    if len(pending[0]) == 0:
        slide += 1
        if score > high_scores[song-1]:
            high_scores[song-1] = score
            new = 1
        else:
            new = 0
        last_score[song-1] = score
def check_sense():
    global score
    if click > 0:
        for i in range(len(pending[0])):
            if pending[2][i] == 0:
                note_y = -note_spacing * pending[1][i] + time

                if pending[0][i] == click and abs(note_y - 500) < 50:
                    score += 2
                    pending[2][i] = 3  # perfect
                    break

                elif pending[0][i] == click and abs(note_y - 500) < 125:
                    score += 1
                    if pending[0][i] == click and (note_y - 500) > 0:
                        pending[2][i] = 1  # late
                        break
                    else:
                        pending[2][i] = 2  # early
                        break

                elif pending[0][i] == click and abs(note_y - 500) < 300:
                    score -= 1
                    pending[2][i] = 4  # miss
                    break

def check_item_click():
    global click
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(0,4):
        dist = (((140+(i*72))-mouse_x)**2+((500)-mouse_y)**2)**0.5
        if dist <= 30:
            click = i+1

def draw_game():
    global font, colors, score_text, score
    font = pygame.font.SysFont(False, 50)
    song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
    screen.blit(background_blank, (0, 0))
    pygame.draw.rect(screen, (105, 105, 105), (100, 0, WIDTH-200, HEIGHT))

    pygame.draw.rect(screen, (0,0,0), (320-(10/2), 0, 10, HEIGHT))
    pygame.draw.rect(screen, (0,0,0), (248-(10/2), 0, 10, HEIGHT))
    pygame.draw.rect(screen, (0,0,0), (176-(10/2), 0, 10, HEIGHT))
    draw_notes()
    for i in range(0,4):
        pygame.draw.circle(screen, (0,0,0), (140+(i*72), 500), 35)
        pygame.draw.circle(screen, colors[i], (140+(i*72), 500), 30)
    screen.blit(song_text, ((WIDTH/2)-(17*(len(song_names[song-1])/2)), 5))
    screen.blit(back_arrow, (425, 20))
    score_text = font.render(f"{score}", True, (255, 255, 255))
    screen.blit(score_text, ((WIDTH/2)-(17*(len(f"{score}")/2)), 50))
def upload_level():
    global pending
    pending = [songs_notes[song-1][0].copy(),
               songs_notes[song-1][1].copy()]
    pending.append([])
    for i in range(0, len(pending[0])):
        pending[2].append(0)
    print(pending)
def draw_notes():
    for i in range (0, len(pending[0])):
        pygame.draw.circle(screen,(0,0,0), (140+(72*(pending[0][i]-1)), int(0 - (note_spacing * pending[1][i]))+time), 35)
        pygame.draw.circle(screen, colors[pending[0][i]-1], (140+(72*(pending[0][i]-1)), int(0 - (note_spacing * pending[1][i]))+time), 30)
        if pending[2][i] == 1:
            screen.blit(late, (140+(72*(pending[0][i]-1)-30), int(0 - (note_spacing * pending[1][i]))+time-70))
        elif pending[2][i] == 2:
            screen.blit(early, (140+(72*(pending[0][i]-1)-30), int(0 - (note_spacing * pending[1][i]))+time-70))
        elif pending[2][i] == 3:
            screen.blit(perfect, (140+(72*(pending[0][i]-1)-30), int(0 - (note_spacing * pending[1][i]))+time-70))
        elif pending[2][i] == 4:
            screen.blit(miss, (140+(72*(pending[0][i]-1)-30), int(0 - (note_spacing * pending[1][i]))+time-70))

def draw_bg():
    global font
    font = pygame.font.SysFont(False, 75)
    screen.blit(background, (0, 0))
    screen.blit(start_button, (150, 400))
def level_select():
    global song_name, song_text, song_names, song, font, high_score_text, last_score_text
    font = pygame.font.SysFont(False, 75)
    song_text = font.render(f"{song_names[song-1]}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score : {high_scores[song-1]}", True, (255, 255, 255))
    last_score_text = font.render(f"Last Score : {last_score[song-1]}", True, (255, 255, 255))
    screen.blit(background_blank, (0, 0))
    song_name = font.render(f"level : {song}", True, (255, 255, 255))
    if song != 1:
        screen.blit(left_arrow, (20, 500))
    if song != level_count:
        screen.blit(right_arrow, (300, 500))
    screen.blit(start_button, (150, 300))            
    screen.blit(song_text, ((WIDTH/2)-(27*(len(song_names[song-1])/2)), 75))
    screen.blit(high_score_text, ((WIDTH/2)-(27*(len(f"High Score : {high_scores[song-1]}")/2)), 175))
    screen.blit(last_score_text, ((WIDTH/2)-(27*(len(f"Last Score : {last_score[song-1]}")/2)), 225))
    screen.blit(song_name, (5, 5))
    screen.blit(back_arrow, (425, 20))

async def main():
    running = True
    global slide, song, level_count, song_name, song_text, start_rect, start_mask, time, speed, click, score
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
                        time = 0
                        score = 0
                        speed = song_speeds[song-1]
                        upload_level()
                        
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
                else:
                    check_item_click()
                    check_sense()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and slide == 4:
                if check_box_rect.collidepoint(event.pos):

                    # Convert the screen position to mask-local coordinates
                    local_pos = (
                        event.pos[0] - check_box_rect.x,
                        event.pos[1] - check_box_rect.y
                    )
                    # True means the clicked pixel is opaque in the mask
                    if check_box_mask.get_at(local_pos):
                        slide-=2
                        start_rect = start_button.get_rect(topleft=(150, 300))
                else:
                    check_item_click()
                    check_sense()
            elif event.type == pygame.KEYDOWN and slide == 3:
                if event.key == pygame.K_1:
                    click = 1
                    check_sense()
                if event.key == pygame.K_2:
                    click = 2
                    check_sense()
                if event.key == pygame.K_3:
                    click = 3
                    check_sense()
                if event.key == pygame.K_4:
                    click = 4
                    check_sense()
        clock.tick(60)
        screen.fill((0, 0, 0))
        if slide == 1:
            draw_bg()
        elif slide == 2:
            level_select()
        elif slide == 3:
            draw_game()
            check_game_end()
            time += speed
        elif slide == 4:
            draw_game_end()
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())