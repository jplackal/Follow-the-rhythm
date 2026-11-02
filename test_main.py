
import main
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