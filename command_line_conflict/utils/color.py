import math


def get_pulse_color(
    time: float, base_color: tuple[int, int, int], peak_color: tuple[int, int, int], speed: float = 5.0
) -> tuple[int, int, int]:
    """Calculates a pulsing color based on time interpolating between base_color and peak_color."""
    pulse = (math.sin(time * speed) + 1) / 2
    r = base_color[0] + int((peak_color[0] - base_color[0]) * pulse)
    g = base_color[1] + int((peak_color[1] - base_color[1]) * pulse)
    b = base_color[2] + int((peak_color[2] - base_color[2]) * pulse)
    return (r, g, b)
