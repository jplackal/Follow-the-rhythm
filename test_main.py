
import main
import math
import numpy as np
from unittest.mock import patch, MagicMock, Mock


def test_draw_notes():

    # Set up test data
    main.pending = [
        [1, 2, 3, 4],  # Lanes
        [1, 2, 3, 4],  # Beat positions
        [0, 1, 2, 3]   # Statuses
    ]

    main.time = 100
    main.note_spacing = 72

    # Create a fake screen
    main.screen = MagicMock()

    with patch("pygame.draw.circle") as mock_circle:

        main.draw_notes()

        # Check that 8 circles were drawn
        assert mock_circle.call_count == 8

        # Check that 3 images were displayed
        assert main.screen.blit.call_count == 3


def test_clicked_mask_outside_rect():
    rect = Mock()
    rect.collidepoint.return_value = False

    mask = Mock()

    result = main.clicked_mask(mask, rect, (150, 150))

    assert result == False
    mask.get_at.assert_not_called()


def test_clicked_mask_inside_rect():
    rect = Mock()
    rect.x = 100
    rect.y = 100
    rect.collidepoint.return_value = True

    mask = Mock()
    mask.get_at.return_value = True

    result = main.clicked_mask(mask, rect, (120, 130))

    assert result == True
    mask.get_at.assert_called_once_with((20, 30))


def test_level_select():
    # Set up test values
    main.song = 2
    main.level_count = 3
    main.song_names = ["Song 1", "Song 2", "Song 3"]
    main.high_scores = [100, 200, 300]
    main.last_score = [50, 150, 250]

    # Replace the screen with a mock
    main.screen = Mock()

    # Mock font and text rendering
    fake_font = Mock()
    fake_font.render.side_effect = lambda *args: Mock()

    with patch("pygame.font.SysFont", return_value=fake_font):
        main.level_select()

    # Check that the font was created correctly
    pygame_font = patch("pygame.font.SysFont")

    # Check that text was rendered
    assert fake_font.render.call_count == 4

    # Song 2 is not the first or last level,
    # so both arrows should be displayed.
    assert main.screen.blit.call_count == 9


def test_draw_bg():
    # Replace screen with a mock
    main.screen = Mock()

    # Run the function
    main.draw_bg()

    # Check that blit was called twice
    assert main.screen.blit.call_count == 2

    # Check that the correct images and positions were used
    calls = main.screen.blit.call_args_list

    assert calls[0][0] == (main.background, (0, 0))
    assert calls[1][0] == (main.start_button, (150, 400))


def test_upload_level():
    # Set up test data
    main.song = 1
    main.note_spacing = 120
    main.speed = 6

    main.songs_notes = [
        [
            [1, 2, 3],       # Lanes
            [10, 20, 30],    # Beat positions
            [4, 5, 6]        # Note numbers
        ]
    ]

    # Mock make_tone so no actual sounds are generated
    with patch("main.make_tone") as mock_tone:
        mock_tone.side_effect = ["sound1", "sound2", "sound3"]

        main.upload_level()

    # Check that make_tone was called three times
    assert mock_tone.call_count == 3

    # Check the duration calculation
    expected_duration = 120 / 6 / 60

    assert mock_tone.call_args_list[0][0] == (4, expected_duration)
    assert mock_tone.call_args_list[1][0] == (5, expected_duration)
    assert mock_tone.call_args_list[2][0] == (6, expected_duration)

    # Check the pending list
    assert main.pending == [
        [1, 2, 3],
        [10, 20, 30],
        [0, 0, 0],
        ["sound1", "sound2", "sound3"],
        [False, False, False]
    ]

def test_draw_game():
    # Set up test values
    main.song = 1
    main.song_names = ["Test Song"]
    main.score = 100
    main.WIDTH = 500
    main.HEIGHT = 600
    main.colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0)
    ]

    # Replace screen with a mock
    main.screen = Mock()

    # Mock font rendering
    fake_font = Mock()
    fake_font.render.return_value = Mock()

    with patch("pygame.font.SysFont", return_value=fake_font) as mock_font, \
     patch("pygame.draw.rect") as mock_rect, \
     patch("pygame.draw.circle") as mock_circle, \
     patch.object(main, "draw_notes") as mock_draw_notes:

     main.draw_game()

    # Check font size
    mock_font.assert_called_once_with(False, 50)

    # Check rectangles
    # 1 play area + 3 lane dividers = 4
    assert mock_rect.call_count == 4

    # Check circles
    # 4 lanes * 2 circles each = 8
    assert mock_circle.call_count == 8

    # Check draw_notes was called
    mock_draw_notes.assert_called_once()

    # Check screen blits
    # Background + song text + back arrow + score = 4
    assert main.screen.blit.call_count == 4

    # Check score text
    assert fake_font.render.call_args_list[1][0] == (
        "100", True, (255, 255, 255)
    )


def test_check_item_click():
    # Test clicking the first lane
    with patch("pygame.mouse.get_pos", return_value=(140, 500)):
        main.click = 0
        main.check_item_click()

    assert main.click == 1


def test_check_item_click_fourth_lane():
    # Test clicking the fourth lane
    with patch("pygame.mouse.get_pos", return_value=(356, 500)):
        main.click = 0
        main.check_item_click()

    assert main.click == 4


def test_check_item_click_outside():
    # Test clicking outside all lanes
    with patch("pygame.mouse.get_pos", return_value=(50, 50)):
        main.click = 0
        main.check_item_click()

    assert main.click == 0

def setup_check_sense():
    main.click = 1
    main.note_spacing = 100
    main.time = 500

    main.pending = [
        [1],
        [0],
        [0],
        [],
        [False]
    ]

    main.score = 0
    main.misses = 0
    main.earlys = 0
    main.lates = 0
    main.perfects = 0

def test_check_sense_selects_closest_note():
    setup_check_sense()

    # Two notes in the same lane.
    # First note is 100 pixels away.
    # Second note is exactly at the target.
    main.pending = [
        [1, 1],
        [1, 0],
        [0, 0],
        [],
        [False, False]
    ]

    main.check_sense()

    assert main.pending[2] == [0, 3]
    assert main.score == 2
    assert main.perfects == 1

def setup_check_game_end():
    main.song = 1
    main.note_spacing = 100
    main.time = 500

    main.pending = [
        [1],
        [0],
        [0],
        [Mock()],
        [False]
    ]

    main.score = 0
    main.misses = 0
    main.slide = 1
    main.new = 0

    main.high_scores = [10]
    main.last_score = [0]

def test_check_game_end_plays_sound():
    setup_check_game_end()

    main.check_game_end()

    main.pending[3][0].play.assert_called_once()
    assert main.pending[4] == [True]

def test_check_game_end_sound_once():
    setup_check_game_end()

    main.check_game_end()
    main.check_game_end()

    main.pending[3][0].play.assert_called_once()

def test_check_game_end_deletes_note():
    setup_check_game_end()

    main.time = 801

    main.check_game_end()

    assert main.pending == [[], [], [], [], []]

def test_check_game_end_miss():
    setup_check_game_end()

    main.time = 801

    main.check_game_end()

    assert main.score == -1
    assert main.misses == 1

def test_check_game_end_new_high_score():
    setup_check_game_end()

    main.time = 801
    main.score = 20

    main.check_game_end()

    assert main.slide == 2
    assert main.high_scores[0] == 19
    assert main.last_score[0] == 19
    assert main.new == 1

def test_check_game_end_no_new_high_score():
    setup_check_game_end()

    main.time = 801
    main.score = 5

    main.check_game_end()

    assert main.slide == 2
    assert main.high_scores[0] == 10
    assert main.last_score[0] == 4
    assert main.new == 0

def setup_draw_game_end():
    main.song = 1
    main.WIDTH = 500

    main.song_names = ["Test Song"]
    main.high_scores = [100]
    main.last_score = [80]

    main.perfects = 10
    main.misses = 2
    main.earlys = 3
    main.lates = 4

    main.screen = Mock()

def test_draw_game_end():
    setup_draw_game_end()

    main.new = 0

    fake_font = Mock()
    fake_font.render.return_value = Mock()

    with patch("pygame.font.SysFont", return_value=fake_font) as mock_font:
        main.draw_game_end()

    # Check font size
    mock_font.assert_called_once_with(None, 50)

    # Check that all 8 text elements were rendered
    assert fake_font.render.call_count == 8

    # Check the high score label
    assert fake_font.render.call_args_list[2][0] == (
        "High Score : 100", True, (255, 255, 255)
    )

    # Check the last score label
    assert fake_font.render.call_args_list[3][0] == (
        "Score : 80", True, (255, 255, 255)
    )

    # Background + checkbox + 8 text elements
    assert main.screen.blit.call_count == 10

def test_draw_game_end_new_high_score():
    setup_draw_game_end()

    main.new = 1

    fake_font = Mock()
    fake_font.render.return_value = Mock()

    with patch("pygame.font.SysFont", return_value=fake_font):
        main.draw_game_end()

    # Check that the NEW label is displayed
    assert fake_font.render.call_args_list[2][0] == (
        "NEW High Score : 100", True, (255, 255, 255)
    )

    assert main.screen.blit.call_count == 10

def test_note_number_middle_c():
    frequency = main.note_number_to_frequency(1)

    assert math.isclose(frequency, 261.625565)


def test_note_number_one_semitone_up():
    frequency = main.note_number_to_frequency(2)

    expected = 261.625565 * (2 ** (1 / 12))

    assert math.isclose(frequency, expected)


def test_note_number_one_octave_up():
    frequency = main.note_number_to_frequency(13)

    expected = 261.625565 * 2

    assert math.isclose(frequency, expected)


def test_note_number_one_octave_down():
    frequency = main.note_number_to_frequency(-11)

    expected = 261.625565 / 2

    assert math.isclose(frequency, expected)

def test_make_tone():
    with patch("pygame.sndarray.make_sound", return_value="fake_sound") as mock_sound:
        result = main.make_tone(1, 1)

    # Check returned sound
    assert result == "fake_sound"

    # Check make_sound was called once
    mock_sound.assert_called_once()

    # Get the generated audio samples
    samples = mock_sound.call_args[0][0]

    # Check sample count (44100 samples for 1 second)
    assert len(samples) == 44100

    # Check sample data type
    assert samples.dtype == np.int16


def test_make_tone_short_duration():
    with patch("pygame.sndarray.make_sound", return_value="fake_sound") as mock_sound:
        main.make_tone(1, 0.5)

    samples = mock_sound.call_args[0][0]

    assert len(samples) == 22050


def test_make_tone_minimum_sample_count():
    with patch("pygame.sndarray.make_sound", return_value="fake_sound") as mock_sound:
        main.make_tone(1, 0)

    samples = mock_sound.call_args[0][0]

    # Even zero duration produces at least one sample
    assert len(samples) == 1

def test_make_tone_frequency():
    with patch("pygame.sndarray.make_sound", return_value="fake_sound") as mock_sound:
        main.make_tone(1, 1)

    samples = mock_sound.call_args[0][0]

    # Convert samples back to approximate waveform values
    wave = samples.astype(float) / 32767

    # Count zero crossings
    zero_crossings = np.where(np.diff(np.sign(wave)))[0]

    # Estimate frequency
    estimated_frequency = len(zero_crossings) / 2

    expected_frequency = main.note_number_to_frequency(1)

    assert abs(estimated_frequency - expected_frequency) < 2