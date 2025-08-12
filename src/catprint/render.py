import importlib.resources
import itertools
import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from catprint.printer import PRINTER_WIDTH
import importlib


def image(image: PIL.Image.Image) -> PIL.Image.Image:
    if image.mode != "1":
        image = image.convert("1")
    if image.width > PRINTER_WIDTH:
        image = image.resize(
            (PRINTER_WIDTH, int(image.height * PRINTER_WIDTH / image.width))
        )
    return image


def text(text: str, *, font_size: int = 18, line_length: int = 44) -> PIL.Image.Image:
    font = PIL.ImageFont.truetype(
        str(
            importlib.resources.files("catprint").joinpath(
                "fonts/NotoSansMono_ExtraCondensed-Regular.ttf"
            )
        ),
        font_size,
    )
    left, top, right, bottom = font.getbbox("Č")
    height = int((bottom - top) * 1.4)
    lines = [
        "".join(subline)
        for line in text.splitlines()
        for subline in itertools.batched(line, line_length)
    ]
    img = PIL.Image.new("1", (PRINTER_WIDTH, len(lines) * height), color="white")
    draw = PIL.ImageDraw.Draw(img)
    for y, line in enumerate(lines):
        draw.text((0, y * height), line, fill="black", font=font)
    return img


def banner(text: str) -> PIL.Image.Image:
    font = PIL.ImageFont.truetype(
        str(importlib.resources.files("catprint").joinpath("fonts/NotoSans_ExtraCondensed-Black.ttf")),
        PRINTER_WIDTH,
    )
    left, top, right, bottom = font.getbbox(text)
    text_width, text_height = int(right - left), int(bottom - top)
    canvas_width = text_width
    canvas_height = PRINTER_WIDTH
    img = PIL.Image.new("1", (canvas_width, canvas_height), color="white")
    PIL.ImageDraw.Draw(img).text(
        (
            (canvas_width - text_width) // 2 - left,
            (canvas_height - text_height) // 2 - top,
        ),
        text,
        fill="black",
        font=font,
    )
    return img.transpose(PIL.Image.Transpose.ROTATE_270)


def text_banner(
    text: str, *, font_size: int = 18
) -> PIL.Image.Image:
    font = PIL.ImageFont.truetype(
        str(
            importlib.resources.files("catprint").joinpath(
                "fonts/NotoSansMono_ExtraCondensed-Regular.ttf"
            )
        ),
        font_size,
    )
    _, _, char_width, char_height = font.getbbox("#")
    banner_img = banner(text)
    img = PIL.Image.new("1", (banner_img.width, banner_img.height), color="white")
    draw = PIL.ImageDraw.Draw(img)
    text_iter = itertools.cycle(c for c in text if c != " ")
    rows = int(banner_img.height / char_height)
    cols = int(banner_img.width / char_width)
    for y in range(rows):
        line_text = ""
        for x in range(cols):
            if banner_img.getpixel(
                (int((x + 0.5) * char_width), int((y + 0.5) * char_height))
            ):
                line_text += " "
            else:
                line_text += next(text_iter)
        draw.text((0, y * char_height), line_text, fill="black", font=font)
    return img


def stack(*images: PIL.Image.Image) -> PIL.Image.Image:
    max_width = max(img.width for img in images)
    resized_images = [
        img
        if img.width == max_width
        else img.resize((max_width, int(img.height * max_width / img.width)))
        for img in images
    ]
    total_height = sum(img.height for img in resized_images)
    mode = images[0].mode
    stacked_image = PIL.Image.new(mode, (max_width, total_height))
    y_offset = 0
    for img in resized_images:
        stacked_image.paste(img, (0, y_offset))
        y_offset += img.height
    return stacked_image


def blank(height: int) -> PIL.Image.Image:
    return PIL.Image.new("1", (PRINTER_WIDTH, height), color="white")
