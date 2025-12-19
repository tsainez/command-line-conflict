from command_line_conflict.components.floating_text import FloatingText


def test_floating_text_initialization():
    """Test that FloatingText initializes with correct values."""
    text = "10"
    color = (255, 0, 0)
    lifetime = 1.5
    speed = 1.0

    ft = FloatingText(text=text, color=color, lifetime=lifetime, speed=speed)

    assert ft.text == text
    assert ft.color == color
    assert ft.lifetime == lifetime
    assert ft.speed == speed


def test_floating_text_default_speed():
    """Test that FloatingText uses the default speed if not provided."""
    text = "Miss"
    color = (200, 200, 200)
    lifetime = 1.0

    ft = FloatingText(text=text, color=color, lifetime=lifetime)

    assert ft.speed == 2.0  # Default value
