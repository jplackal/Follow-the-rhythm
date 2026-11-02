import asyncio
import numpy as np
import pygame

# Set audio format before initializing Pygame.
pygame.mixer.pre_init(44100, size=-16, channels=1)
pygame.init()

WIDTH = 500
HEIGHT = 600

slide = 4
song = 1
level_count = 3
score = 0
new = 0
perfects = 0
misses = 0
earlys = 0
lates = 0

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


start_button = pygame.transform.smoothscale(
    start_button,
    (int(start_button.get_width() * 0.1), int(start_button.get_height() * 0.1)),
)
right_arrow = pygame.transform.smoothscale(
    right_arrow,
    (int(right_arrow.get_width() * 0.03), int(right_arrow.get_height() * 0.03)),
)
left_arrow = pygame.transform.smoothscale(
    left_arrow,
    (int(left_arrow.get_width() * 0.3), int(left_arrow.get_height() * 0.3)),
)
back_arrow = pygame.transform.smoothscale(
    back_arrow,
    (int(back_arrow.get_width() * 0.1), int(back_arrow.get_height() * 0.1)),
)
check_box = pygame.transform.smoothscale(
    check_box,
    (int(check_box.get_width() * 0.1), int(check_box.get_height() * 0.1)),
)
miss = pygame.transform.smoothscale(
    miss, (int(miss.get_width() * 0.03), int(miss.get_height() * 0.03))
)
late = pygame.transform.smoothscale(
    late, (int(late.get_width() * 0.03), int(late.get_height() * 0.03))
)
early = pygame.transform.smoothscale(
    early, (int(early.get_width() * 0.03), int(early.get_height() * 0.03))
)
perfect = pygame.transform.smoothscale(
    perfect, (int(perfect.get_width() * 0.03), int(perfect.get_height() * 0.03))
)

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
song_text = font.render("", True, (255, 255, 255))
score_text = font.render("", True, (255, 255, 255))
perfect_text = font.render("1", True, (255, 255, 255))
miss_text = font.render("1", True, (255, 255, 255))
early_text = font.render("1", True, (255, 255, 255))
late_text = font.render("1", True, (255, 255, 255))

song_names = ["Tutorial", "Twinkle Twinkle", "TS (HARD)"]
song_speeds = [4, 4, 10]
high_scores = [0, 0, 0]
last_score = [0, 0, 0]

# Each song has three matching lists:
#   1. Lane numbers (1-4)
#   2. Beat positions
#   3. Note numbers
#
# Note number 1 = middle C (C4).
# 2 = C#4, 3 = D4, 4 = D#4, etc.
songs_notes = [
    [
        [1, 2, 3, 4, 1, 2, 3, 4, 1, 3, 2, 4, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        [1, 3, 5, 6, 1, 3, 5, 6, 1, 5, 3, 6, 1],
    ],
    [
        [1,1,2,2,3,3,2,4,4,3,3,2,2,1,4,4,3,3,2,2,1,4,4,3,3,2,2,1,1,1,2,2,3,3,2,4,4,3,3,2,2,1, 1,2,3,4,],
        [1, 2, 3, 4,5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,22,23,25,26,27,28,29,30,31,33,34,35,36,37,38,39,41,42,43, 44,45, 46, 47,],
        [1,1,8,8,10,10,8,6,6,5,5,3,3,1,8,8,6,6,5,5,3,8,8,6,6,5,5,3,1,1,8,8,10,10,8,6,6,5,5,3,3,1,1,1,1,1],
    ],
    [
        [2,1,3,1,2,1,3,1,2,1,3,1,2,1,3,1,3,1,4,1,3,1,4,1,3,1,4,1,3,1,4,1,2,1,3,1,2,1,3,1,2,1,3,1,2,1,3,1,3,1,4,1,3,1,4,1,3,1,4,1,3,1,4,1,
        4,1,3,1,2,1,3,1,2,1,2,1,2,1,3,1,4,1,3,1,2,1,3,1,2,1,4,1,4,1,3,1,2,1,3,1,2,1,2,1,2,1,3,1,4,1,3,1,2,1,3,1,2,1,4,1,2,1,3,1,4,1,3,1,
        2,1,3,1,2,1,3,1,2,1,3,1,2,1,3,1,3,1,4,1,3,1,4,1,3,1,4,1,3,1,4,1,2,1,3,1,2,1,3,1,2,1,3,1,2,1,3,1,3,1,4,1,3,1,4,1,3,1,4,1,3,1,4,1,
        4,1,3,1,2,1,3,1,2,1,2,1,2,1,3,1,4,1,3,1,2,1,3,1,2,1,4,1,4,1,3,1,2,1,3,1,2,1,2,1,2,1,3,1,4,1,3,1,2,1,3,1,2,1,4,1,2,1,3,1,4,1,3,1,
        ],
        [],
        [4,0,7,0,4,0,7,0,4,0,7,0,4,0,7,0,5,0,8,0,5,0,8,0,5,0,8,0,5,0,8,0,4,0,7,0,4,0,7,0,4,0,7,0,4,0,7,0,5,0,8,0,5,0,8,0,5,0,8,0,5,0,8,0,
         12,0,10,0,9,0,10,0,9,0,7,0,9,0,5,0,7,0,4,0,5,0,4,0,5,0,7,0,5,0,4,0,12,0,10,0,9,0,10,0,9,0,7,0,9,0,5,0,7,0,4,0,5,0,4,0,5,0,7,0,5,0,4,0,
         4,0,7,0,4,0,7,0,4,0,7,0,4,0,7,0,5,0,8,0,5,0,8,0,5,0,8,0,5,0,8,0,4,0,7,0,4,0,7,0,4,0,7,0,4,0,7,0,5,0,8,0,5,0,8,0,5,0,8,0,5,0,8,0,
         12,0,10,0,9,0,10,0,9,0,7,0,9,0,5,0,7,0,4,0,5,0,4,0,5,0,7,0,5,0,4,0,12,0,10,0,9,0,10,0,9,0,7,0,9,0,5,0,7,0,4,0,5,0,4,0,5,0,7,0,5,0,4,0]
    ]
]
for i in range(0, 1000):
    songs_notes[2][1].append(i+1)
note_spacing = 72
time = 0
speed = 3

colors = [
    (240, 105, 105),
    (115, 205, 130),
    (245, 220, 105),
    (105, 165, 235),
]

click = 0

# pending contains five parallel lists:
# lanes, beat positions, hit statuses, sound objects, played flags.
pending = [[], [], [], [], []]


def note_number_to_frequency(note_number):
    """Convert note number 1=C4 to its frequency in Hz."""
    middle_c_frequency = 261.625565
    semitones_from_middle_c = note_number - 1
    return middle_c_frequency * (2 ** (semitones_from_middle_c / 12))


def make_tone(note_number, duration):
    """Generate a sine-wave sound for a numbered musical note."""
    sample_rate = 44100
    frequency = note_number_to_frequency(note_number)
    sample_count = max(1, int(sample_rate * duration))

    sample_times = np.arange(sample_count) / sample_rate
    wave = 0.5 * np.sin(2 * np.pi * frequency * sample_times)
    samples = (wave * 32767).astype(np.int16)

    return pygame.sndarray.make_sound(samples)


def draw_game_end():
    global high_score_text, last_score_text, new, song_text, song_name

    font = pygame.font.SysFont(None, 50)
    screen.blit(background_blank, (0, 0))
    screen.blit(check_box, (150, 450))

    song_text = font.render(song_names[song - 1], True, (255, 255, 255))
    song_name = font.render(f"level : {song}", True, (255, 255, 255))

    if new == 0:
        high_score_label = f"High Score : {high_scores[song - 1]}"
    else:
        high_score_label = f"NEW High Score : {high_scores[song - 1]}"

    high_score_text = font.render(high_score_label, True, (255, 255, 255))
    last_score_label = f"Score : {last_score[song - 1]}"
    last_score_text = font.render(last_score_label, True, (255, 255, 255))
    perfect_text = font.render(f"Perfect Notes : {perfects}", True, (255, 255, 255))
    miss_text = font.render(f"Missed Notes : {misses}", True, (255, 255, 255))
    early_text = font.render(f"Early Notes : {earlys}", True, (255, 255, 255))
    late_text = font.render(f"Late Notes : {lates}", True, (255, 255, 255))

    screen.blit(
        high_score_text,
        ((WIDTH / 2) - (17 * (len(high_score_label) / 2)), 150),
    )
    screen.blit(
        last_score_text,
        ((WIDTH / 2) - (17 * (len(last_score_label) / 2)), 200),
    )
    screen.blit(
        song_text,
        ((WIDTH / 2) - (17 * (len(song_names[song - 1]) / 2)), 100),
    )
    screen.blit(
        song_name,
        ((WIDTH / 2) - (17 * (len(f"level : {song}") / 2)), 50),
    )
    screen.blit(
        perfect_text,
        ((WIDTH / 2) - (17 * (len(f"Perfect Notes : {perfects}") / 2)), 250),
    )
    screen.blit(
        miss_text,
        ((WIDTH / 2) - (17 * (len(f"Missed Notes : {misses}") / 2)), 300),
    )
    screen.blit(
        late_text,
        ((WIDTH / 2) - (17 * (len(f"Early Notes : {earlys}") / 2)), 350),
    )
    screen.blit(
        early_text,
        ((WIDTH / 2) - (17 * (len(f"Late Notes : {lates}") / 2)), 400),
    )


def check_game_end():
    global slide, score, new, misses

    for i in range(len(pending[0]) - 1, -1, -1):
        note_y = -pending[1][i] * note_spacing + time

        # Play the sound once as the note reaches the click area.
        if note_y >= 500 and not pending[4][i]:
            pending[3][i].play()
            pending[4][i] = True

        if note_y > 800:
            if pending[2][i] == 0:
                score -= 1
                misses += 1

            # Delete this note from all five parallel lists.
            for note_list in pending:
                del note_list[i]

    if len(pending[0]) == 0:
        slide += 1

        if score > high_scores[song - 1]:
            high_scores[song - 1] = score
            new = 1
        else:
            new = 0

        last_score[song - 1] = score



def check_sense():
    global score, misses, earlys, lates, perfects

    if click > 0:
        closest_note = None
        closest_distance = float("inf")

        # Find the closest unjudged note in the clicked lane.
        for i in range(len(pending[0])):
            if pending[2][i] == 0 and pending[0][i] == click:
                note_y = -note_spacing * pending[1][i] + time
                distance = abs(note_y - 500)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_note = i

        # Judge only the closest note.
        if closest_note is not None:
            i = closest_note
            note_y = -note_spacing * pending[1][i] + time

            if closest_distance < 50:
                score += 2
                perfects += 1
                pending[2][i] = 3

            elif closest_distance < 125:
                score += 1

                if note_y - 500 > 0:
                    lates += 1
                    pending[2][i] = 1
                else:
                    earlys += 1
                    pending[2][i] = 2

            elif closest_distance < 300:
                score -= 1
                misses += 1
                pending[2][i] = 4



def check_item_click():
    global click

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i in range(4):
        distance = (
            (140 + (i * 72) - mouse_x) ** 2
            + (500 - mouse_y) ** 2
        ) ** 0.5

        if distance <= 30:
            click = i + 1


def draw_game():
    global font, score_text

    font = pygame.font.SysFont(False, 50)
    current_song_text = font.render(song_names[song - 1], True, (255, 255, 255))

    screen.blit(background_blank, (0, 0))
    pygame.draw.rect(screen, (105, 105, 105), (100, 0, WIDTH - 200, HEIGHT))

    for x in (320, 248, 176):
        pygame.draw.rect(screen, (0, 0, 0), (x - 5, 0, 10, HEIGHT))

    draw_notes()

    for i in range(4):
        pygame.draw.circle(screen, (0, 0, 0), (140 + (i * 72), 500), 35)
        pygame.draw.circle(screen, colors[i], (140 + (i * 72), 500), 30)

    screen.blit(
        current_song_text,
        ((WIDTH / 2) - (17 * (len(song_names[song - 1]) / 2)), 5),
    )
    screen.blit(back_arrow, (425, 20))

    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(
        score_text,
        ((WIDTH / 2) - (17 * (len(str(score)) / 2)), 50),
    )


def upload_level():
    global pending

    lanes = songs_notes[song - 1][0].copy()
    beat_positions = songs_notes[song - 1][1].copy()
    note_numbers = songs_notes[song - 1][2].copy()

    # A beat lasts note_spacing / speed frames at 60 FPS.
    beat_duration = note_spacing / speed / 60

    sounds = [
        make_tone(note_number, beat_duration)
        for note_number in note_numbers
    ]

    pending = [
        lanes,
        beat_positions,
        [0] * len(lanes),
        sounds,
        [False] * len(lanes),
    ]


def draw_notes():
    for i in range(len(pending[0])):
        x = 140 + (72 * (pending[0][i] - 1))
        y = int(-note_spacing * pending[1][i]) + time

        pygame.draw.circle(screen, (0, 0, 0), (x, y), 35)
        pygame.draw.circle(screen, colors[pending[0][i] - 1], (x, y), 30)

        if pending[2][i] == 1:
            screen.blit(late, (x - 30, y - 70))
        elif pending[2][i] == 2:
            screen.blit(early, (x - 30, y - 70))
        elif pending[2][i] == 3:
            screen.blit(perfect, (x - 30, y - 70))
        elif pending[2][i] == 4:
            screen.blit(miss, (x - 30, y - 70))


def draw_bg():
    screen.blit(background, (0, 0))
    screen.blit(start_button, (150, 400))


def level_select():
    global song_name, song_text, font, high_score_text, last_score_text

    font = pygame.font.SysFont(False, 75)
    song_text = font.render(song_names[song - 1], True, (255, 255, 255))
    high_score_text = font.render(
        f"High Score : {high_scores[song - 1]}",
        True,
        (255, 255, 255),
    )
    last_score_text = font.render(
        f"Last Score : {last_score[song - 1]}",
        True,
        (255, 255, 255),
    )

    screen.blit(background_blank, (0, 0))
    song_name = font.render(f"level : {song}", True, (255, 255, 255))

    if song != 1:
        screen.blit(left_arrow, (20, 500))

    if song != level_count:
        screen.blit(right_arrow, (300, 500))

    screen.blit(start_button, (150, 300))
    screen.blit(
        song_text,
        ((WIDTH / 2) - (27 * (len(song_names[song - 1]) / 2)), 75),
    )
    screen.blit(
        high_score_text,
        (
            (WIDTH / 2)
            - (27 * (len(f"High Score : {high_scores[song - 1]}") / 2)),
            175,
        ),
    )
    screen.blit(
        last_score_text,
        (
            (WIDTH / 2)
            - (27 * (len(f"Last Score : {last_score[song - 1]}") / 2)),
            225,
        ),
    )
    screen.blit(song_name, (5, 5))
    screen.blit(back_arrow, (425, 20))


def clicked_mask(mask, rect, position):
    if not rect.collidepoint(position):
        return False

    local_position = (
        position[0] - rect.x,
        position[1] - rect.y,
    )
    return mask.get_at(local_position)


async def main():
    global slide, song, time, speed, click, score
    global start_rect, start_mask, song_text, misses, earlys, lates, perfects

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if slide == 1:
                    if clicked_mask(start_mask, start_rect, event.pos):
                        song = 1
                        slide += 1
                        song_text = font.render(
                            song_names[song - 1],
                            True,
                            (255, 255, 255),
                        )
                        start_rect = start_button.get_rect(topleft=(150, 300))
                        start_mask = pygame.mask.from_surface(start_button)

                elif slide == 2:
                    if song != 1 and clicked_mask(
                        left_arrow_mask, left_arrow_rect, event.pos
                    ):
                        song -= 1

                    elif song != level_count and clicked_mask(
                        right_arrow_mask, right_arrow_rect, event.pos
                    ):
                        song += 1

                    elif clicked_mask(back_arrow_mask, back_arrow_rect, event.pos):
                        slide -= 1
                        start_rect = start_button.get_rect(topleft=(150, 400))
                        start_mask = pygame.mask.from_surface(start_button)
                        song_text = font.render("", True, (255, 255, 255))

                    elif clicked_mask(start_mask, start_rect, event.pos):
                        slide += 1
                        time = 0
                        score = 0
                        speed = song_speeds[song - 1]
                        upload_level()
                        perfects = 0
                        misses = 0
                        earlys = 0
                        lates = 0

                elif slide == 3:
                    if clicked_mask(back_arrow_mask, back_arrow_rect, event.pos):
                        slide -= 1
                    else:
                        click = 0
                        check_item_click()
                        check_sense()

                elif slide == 4:
                    if clicked_mask(check_box_mask, check_box_rect, event.pos):
                        slide -= 2
                        start_rect = start_button.get_rect(topleft=(150, 300))
                    else:
                        click = 0
                        check_item_click()
                        check_sense()

            elif event.type == pygame.KEYDOWN and slide == 3:
                if event.key in (
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                ):
                    click = event.key - pygame.K_0
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

    pygame.quit()


asyncio.run(main())
