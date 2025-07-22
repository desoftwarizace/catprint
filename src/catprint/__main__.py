import asyncio
import catprint.print
import PIL.Image
import sys

async def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m catprint <image_path>")
        sys.exit(1)

    try:
        img = PIL.Image.open(sys.argv[1])
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    if img.width != 384:
        print("Image width must be 384 pixels.")
        sys.exit(1)

    await catprint.print.print_image(img)


asyncio.run(main())
