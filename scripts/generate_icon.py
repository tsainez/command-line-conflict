import os

from PIL import Image, ImageDraw, ImageFont


def create_icon(filepath="icon.ico"):
    size = (256, 256)
    # Background color: Dark Grey/Black
    bg_color = (30, 30, 30)
    # Foreground color: Matrix Green
    fg_color = (0, 255, 0)

    image = Image.new("RGBA", size, bg_color)
    draw = ImageDraw.Draw(image)

    # Draw a border
    border_width = 10
    draw.rectangle(
        [0, 0, size[0] - 1, size[1] - 1], outline=fg_color, width=border_width
    )

    # Draw ">"
    # Points for the triangle/arrow
    arrow_points = [(60, 60), (140, 128), (60, 196)]
    draw.line(arrow_points, fill=fg_color, width=20, joint="curve")

    # Draw "_"
    cursor_points = [(160, 196), (220, 196)]
    draw.line(cursor_points, fill=fg_color, width=20)

    image.save(
        filepath,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)],
    )
    print(f"Icon saved to {filepath}")


if __name__ == "__main__":
    create_icon()
