import asyncio
from catprint import print_image
import PIL.Image
import sys

asyncio.run(print_image(PIL.Image.open(sys.argv[1])))
