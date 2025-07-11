from textual_tty.terminal import Terminal
from textual_tty import constants
from rich.text import Text, Span
from rich.style import Style


def _compare_text_with_spans(text1: Text, text2: Text):
    assert text1.plain == text2.plain
    assert len(text1.spans) == len(text2.spans)

    # Sort spans before comparison to ignore order differences
    sorted_spans1 = sorted(text1.spans, key=lambda s: (s.start, s.end, str(s.style)))
    sorted_spans2 = sorted(text2.spans, key=lambda s: (s.start, s.end, str(s.style)))

    for i in range(len(sorted_spans1)):
        assert sorted_spans1[i].start == sorted_spans2[i].start
        assert sorted_spans1[i].end == sorted_spans2[i].end
        assert sorted_spans1[i].style == sorted_spans2[i].style


def _compare_text_with_spans(text1: Text, text2: Text):
    assert text1.plain == text2.plain
    assert len(text1.spans) == len(text2.spans)

    # Sort spans before comparison to ignore order differences
    sorted_spans1 = sorted(text1.spans, key=lambda s: (s.start, s.end, str(s.style)))
    sorted_spans2 = sorted(text2.spans, key=lambda s: (s.start, s.end, str(s.style)))

    for i in range(len(sorted_spans1)):
        assert sorted_spans1[i].start == sorted_spans2[i].start
        assert sorted_spans1[i].end == sorted_spans2[i].end
        assert sorted_spans1[i].style == sorted_spans2[i].style


def _compare_text_with_spans(text1: Text, text2: Text):
    assert text1.plain == text2.plain
    assert len(text1.spans) == len(text2.spans)

    # Sort spans before comparison to ignore order differences
    sorted_spans1 = sorted(text1.spans, key=lambda s: (s.start, s.end, str(s.style)))
    sorted_spans2 = sorted(text2.spans, key=lambda s: (s.start, s.end, str(s.style)))

    for i in range(len(sorted_spans1)):
        assert sorted_spans1[i].start == sorted_spans2[i].start
        assert sorted_spans1[i].end == sorted_spans2[i].end
        assert sorted_spans1[i].style == sorted_spans2[i].style


def _compare_text_with_spans(text1: Text, text2: Text):
    assert text1.plain == text2.plain
    assert len(text1.spans) == len(text2.spans)

    # Sort spans before comparison to ignore order differences
    sorted_spans1 = sorted(text1.spans, key=lambda s: (s.start, s.end, str(s.style)))
    sorted_spans2 = sorted(text2.spans, key=lambda s: (s.start, s.end, str(s.style)))

    for i in range(len(sorted_spans1)):
        assert sorted_spans1[i].start == sorted_spans2[i].start
        assert sorted_spans1[i].end == sorted_spans2[i].end
        assert sorted_spans1[i].style == sorted_spans2[i].style


def test_write_cell_overwrite():
    screen = Terminal(width=10, height=1)
    screen.current_style = Style(color="red")
    screen.write_text("A")
    expected_line_1 = Text("A", spans=[Span(0, 1, Style(color="red"))])
    assert screen.current_buffer.lines[0] == expected_line_1
    assert screen.cursor_x == 1

    screen.current_style = Style(color="green")
    screen.write_text("B")
    expected_line_2 = Text("AB", spans=[Span(0, 1, Style(color="red")), Span(1, 2, Style(color="green"))])
    assert screen.current_buffer.lines[0] == expected_line_2
    assert screen.cursor_x == 2

    screen.set_cursor(0, 0)
    screen.current_style = Style(color="blue")
    screen.write_text("C")
    expected_line_3 = Text("CB", spans=[Span(0, 1, Style(color="blue")), Span(1, 2, Style(color="green"))])
    assert screen.current_buffer.lines[0] == expected_line_3
    assert screen.cursor_x == 1


def test_write_cell_insert_mode():
    screen = Terminal(width=10, height=1)
    screen.current_style = Style(color="red")
    screen.write_text("A")
    screen.current_style = Style(color="green")
    screen.write_text("B")
    screen.set_cursor(0, 0)
    screen.insert_mode = True
    screen.current_style = Style(color="blue")
    screen.write_text("C")
    expected_line = Text(
        "CAB",
        spans=[
            Span(0, 1, Style(color="blue")),
            Span(1, 2, Style(color="red")),
            Span(2, 3, Style(color="green")),
        ],
    )
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line)
    assert screen.cursor_x == 1


def test_write_cell_autowrap():
    screen = Terminal(width=3, height=2)
    screen.current_style = Style(color="red")
    screen.write_text("A")
    screen.current_style = Style(color="green")
    screen.write_text("B")
    screen.current_style = Style(color="blue")
    screen.write_text("C")
    expected_line_0 = Text(
        "ABC",
        spans=[
            Span(0, 1, Style(color="red")),
            Span(1, 2, Style(color="green")),
            Span(2, 3, Style(color="blue")),
        ],
    )
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line_0)
    assert screen.cursor_x == 3  # Cursor is at the end of the line
    assert screen.cursor_y == 0

    screen.current_style = Style(color="yellow")
    screen.write_text("D")  # Should wrap
    expected_line_1 = Text("D", spans=[Span(0, 1, Style(color="yellow"))])
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line_0)
    _compare_text_with_spans(screen.current_buffer.lines[1], expected_line_1)
    assert screen.cursor_x == 1
    assert screen.cursor_y == 1


def test_clear_rect():
    screen = Terminal(width=5, height=5)
    for y in range(5):
        screen.current_buffer.lines[y] = Text("ABCDE", spans=[Span(0, 5, Style(color="red"))])

    screen.current_buffer.clear_region(1, 1, 3, 3)  # Clear a 3x3 rectangle in the middle

    expected_lines = [
        Text("ABCDE", spans=[Span(0, 5, Style(color="red"))]),
        Text("A   E", spans=[Span(0, 1, Style(color="red")), Span(1, 4, Style()), Span(4, 5, Style(color="red"))]),
        Text("A   E", spans=[Span(0, 1, Style(color="red")), Span(1, 4, Style()), Span(4, 5, Style(color="red"))]),
        Text("A   E", spans=[Span(0, 1, Style(color="red")), Span(1, 4, Style()), Span(4, 5, Style(color="red"))]),
        Text("ABCDE", spans=[Span(0, 5, Style(color="red"))]),
    ]
    for i in range(5):
        _compare_text_with_spans(screen.current_buffer.lines[i], expected_lines[i])


def test_clear_screen():
    screen = Terminal(width=10, height=5)
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(5, 2)  # Cursor at Line 2, char 5

    # Mode 0: Clear from cursor to end of screen
    screen.clear_screen(constants.ERASE_FROM_CURSOR_TO_END)
    assert screen.current_buffer.lines[0] == Text("Line 0", spans=[Span(0, 6, Style(color="red"))])
    assert screen.current_buffer.lines[1] == Text("Line 1", spans=[Span(0, 6, Style(color="red"))])
    assert screen.current_buffer.lines[2] == Text("Line      ", spans=[Span(0, 5, Style(color="red"))])
    _compare_text_with_spans(screen.current_buffer.lines[3], Text(""))
    _compare_text_with_spans(screen.current_buffer.lines[4], Text(""))

    # Reset screen
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(5, 2)

    # Mode 1: Clear from beginning of screen to cursor
    screen.clear_screen(constants.ERASE_FROM_START_TO_CURSOR)
    _compare_text_with_spans(screen.current_buffer.lines[0], Text(""))
    _compare_text_with_spans(screen.current_buffer.lines[1], Text(""))
    _compare_text_with_spans(
        screen.current_buffer.lines[2], Text("     2", spans=[Span(5, 6, Style(color="red"))])
    )  # Line 2 cleared to cursor
    _compare_text_with_spans(screen.current_buffer.lines[3], Text("Line 3", spans=[Span(0, 6, Style(color="red"))]))
    _compare_text_with_spans(screen.current_buffer.lines[4], Text("Line 4", spans=[Span(0, 6, Style(color="red"))]))

    # Reset screen
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(5, 2)

    # Mode 2: Clear entire screen
    screen.clear_screen(constants.ERASE_ALL)
    for y in range(5):
        _compare_text_with_spans(screen.current_buffer.lines[y], Text(""))


def test_clear_line():
    screen = Terminal(width=10, height=1)
    screen.current_buffer.lines[0] = Text("ABCDEFGHIJ", spans=[Span(0, 10, Style(color="red"))])
    screen.set_cursor(5, 0)

    # Mode 0: Clear from cursor to end of line
    screen.clear_line(constants.ERASE_FROM_CURSOR_TO_END)
    expected_line_0 = Text("ABCDE", spans=[Span(0, 5, Style(color="red"))])
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line_0)

    # Reset
    screen.current_buffer.lines[0] = Text("ABCDEFGHIJ", spans=[Span(0, 10, Style(color="red"))])
    screen.set_cursor(5, 0)

    # Mode 1: Clear from beginning of line to cursor
    screen.clear_line(constants.ERASE_FROM_START_TO_CURSOR)
    expected_line_1 = Text("     FGHIJ", spans=[Span(5, 10, Style(color="red"))])
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line_1)

    # Reset
    screen.current_buffer.lines[0] = Text("ABCDEFGHIJ", spans=[Span(0, 10, Style(color="red"))])
    screen.set_cursor(5, 0)

    # Mode 2: Clear entire line
    screen.clear_line(constants.ERASE_ALL)
    expected_line_2 = Text("")
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line_2)


def test_insert_lines():
    screen = Terminal(width=10, height=5)
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(0, 2)  # Insert at line 2

    screen.insert_lines(1)
    expected_lines = [
        Text("Line 0", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 1", spans=[Span(0, 6, Style(color="red"))]),
        Text(""),  # Inserted blank line
        Text("Line 2", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 3", spans=[Span(0, 6, Style(color="red"))]),
    ]
    for i in range(5):
        _compare_text_with_spans(screen.current_buffer.lines[i], expected_lines[i])

    # Insert multiple lines
    screen = Terminal(width=10, height=5)
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(0, 1)
    screen.insert_lines(2)
    expected_lines = [
        Text("Line 0", spans=[Span(0, 6, Style(color="red"))]),
        Text(""),
        Text(""),
        Text("Line 1", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 2", spans=[Span(0, 6, Style(color="red"))]),
    ]
    for i in range(5):
        _compare_text_with_spans(screen.current_buffer.lines[i], expected_lines[i])


def test_delete_lines():
    screen = Terminal(width=10, height=5)
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(0, 1)  # Delete from line 1

    screen.delete_lines(1)
    expected_lines = [
        Text("Line 0", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 2", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 3", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 4", spans=[Span(0, 6, Style(color="red"))]),
        Text(""),  # New blank line at bottom
    ]
    for i in range(5):
        _compare_text_with_spans(screen.current_buffer.lines[i], expected_lines[i])

    # Delete multiple lines
    screen = Terminal(width=10, height=5)
    for y in range(5):
        screen.current_buffer.lines[y] = Text(f"Line {y}", spans=[Span(0, 6, Style(color="red"))])
    screen.set_cursor(0, 0)
    screen.delete_lines(2)
    expected_lines = [
        Text("Line 2", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 3", spans=[Span(0, 6, Style(color="red"))]),
        Text("Line 4", spans=[Span(0, 6, Style(color="red"))]),
        Text(""),
        Text(""),
    ]
    for i in range(5):
        _compare_text_with_spans(screen.current_buffer.lines[i], expected_lines[i])


def test_insert_characters():
    screen = Terminal(width=10, height=1)
    screen.current_buffer.lines[0] = Text("ABCDEFGHIJ", spans=[Span(0, 10, Style(color="red"))])
    screen.set_cursor(2, 0)  # Insert at C

    screen.insert_characters(3)
    expected_line = Text(
        "AB   CDEFG",
        spans=[
            Span(0, 2, Style(color="red")),
            Span(2, 5, Style()),
            Span(5, 10, Style(color="red")),
        ],
    )
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line)


def test_delete_characters():
    screen = Terminal(width=10, height=5)
    screen.current_buffer.lines[0] = Text("12345", spans=[Span(0, 5, Style(color="red"))])
    screen.cursor_x = 2
    screen.cursor_y = 0
    screen.delete_characters(2)
    expected_line = Text(
        "125",
        spans=[
            Span(0, 2, Style(color="red")),
            Span(2, 3, Style(color="red")),
        ],
    )
    _compare_text_with_spans(screen.current_buffer.lines[0], expected_line)
