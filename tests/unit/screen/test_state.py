from textual_tty.terminal import Terminal
from textual_tty.constants import DEFAULT_TERMINAL_WIDTH, DEFAULT_TERMINAL_HEIGHT, DECAWM_AUTOWRAP, IRM_INSERT_REPLACE


def test_resize():
    screen = Terminal(width=DEFAULT_TERMINAL_WIDTH, height=DEFAULT_TERMINAL_HEIGHT)
    screen.cursor_x = 70
    screen.cursor_y = 20

    screen.resize(100, 30)
    assert screen.width == 100
    assert screen.height == 30
    assert screen.cursor_x == 70  # Cursor should remain if within bounds
    assert screen.cursor_y == 20
    assert screen.scroll_bottom == 29  # Should adjust to new height

    screen.resize(50, 10)
    assert screen.width == 50
    assert screen.height == 10
    assert screen.cursor_x == 49  # Cursor should clamp to new width
    assert screen.cursor_y == 9  # Cursor should clamp to new height
    assert screen.scroll_bottom == 9


def test_alternate_screen_switching():
    screen = Terminal(width=DEFAULT_TERMINAL_WIDTH, height=DEFAULT_TERMINAL_HEIGHT)
    assert not screen.in_alt_screen
    assert screen.current_buffer == screen.primary_buffer

    screen.alternate_screen_on()
    assert screen.in_alt_screen
    assert screen.current_buffer == screen.alt_buffer

    # Calling again should do nothing
    screen.alternate_screen_on()
    assert screen.in_alt_screen
    assert screen.current_buffer == screen.alt_buffer

    screen.alternate_screen_off()
    assert not screen.in_alt_screen
    assert screen.current_buffer == screen.primary_buffer

    # Calling again should do nothing
    screen.alternate_screen_off()
    assert not screen.in_alt_screen
    assert screen.current_buffer == screen.primary_buffer


def test_alignment_test():
    screen = Terminal(width=10, height=5)
    screen.alignment_test()

    expected_char = "E"
    for y in range(screen.height):
        line_text = screen.current_buffer.get_line_text(y)
        assert len(line_text) == screen.width
        assert all(char == expected_char for char in line_text)


def test_alternate_screen_on_off_restores_lines():
    screen = Terminal(width=10, height=5)
    screen.current_buffer.set(0, 0, "Hello")
    screen.alternate_screen_on()
    assert screen.current_buffer.get_line_text(0) == "          "
    screen.alternate_screen_off()
    assert screen.current_buffer.get_line_text(0) == "Hello     "


def test_set_and_clear_modes():
    screen = Terminal(width=80, height=24)

    # Test setting a private mode
    screen.set_mode(DECAWM_AUTOWRAP, private=True)
    assert screen.auto_wrap

    # Test clearing a private mode
    screen.clear_mode(DECAWM_AUTOWRAP, private=True)
    assert not screen.auto_wrap

    # Test setting a non-private mode
    screen.set_mode(IRM_INSERT_REPLACE, private=False)
    assert screen.insert_mode

    # Test clearing a non-private mode
    screen.clear_mode(IRM_INSERT_REPLACE, private=False)
    assert not screen.insert_mode

    # Test an unknown mode
    screen.set_mode(999, private=True)
    # No attribute should be set
    assert not hasattr(screen, "unknown_mode")
