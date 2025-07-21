#!/usr/bin/env python3

# based on: https://github.com/amber-sixel/gb01print/blob/main/gb01print.py

import enum
import itertools
import sys
import typing

from bleak import BleakClient, BleakScanner
import crc8

import PIL.Image

PRINTER_WIDTH = 384


class Command(enum.Enum):
    RETRACT_PAPER = b"\xa0"  # Data: Number of steps to go back
    FEED_PAPER = b"\xa1"  # Data: Number of steps to go forward
    DRAW_BITMAP = (
        b"\xa2"  # Data: Line to draw. 0 bit -> don't draw pixel, 1 bit -> draw pixel
    )
    GET_DEV_STATE = b"\xa3"  # Data: 0
    CONTROL_LATTICE = b"\xa6"  # Data: Eleven bytes, all constants. One set used before printing, one after.
    GET_DEV_INFO = b"\xa8"  # Data: 0
    OTHER_FEED_PAPER = b"\xbd"  # Data: one byte, set to a device-specific "Speed" value before printing, and to 0x19 before feeding blank paper
    DRAWING_MODE = b"\xbe"  # Data: 1 for Text, 0 for Images
    SET_ENERGY = b"\xaf"  # Data: 1 - 0xFFFF
    SET_QUALITY = b"\xa4"  # Data: 0x31 - 0x35. APK always sets 0x33 for GB01

    class Lattice(enum.Enum):
        PRINT = b"\xaa\x55\x17\x38\x44\x5f\x5f\x5f\x44\x38\x2c"
        FINISH = b"\xaa\x55\x17\x00\x00\x00\x00\x00\x00\x00\x17"

    class PrintSpeed(enum.Enum):
        IMAGE = b"\0x23"
        BLANK = b"\0x19"

    def format(self: typing.Self, data: bytes | int) -> bytes:
        if isinstance(data, int):
            data = (data).to_bytes(2, byteorder="little")
        return (
            b"Qx"
            + self.value
            + b"\x00"
            + bytes([len(data)])
            + b"\x00"
            + data
            + crc8.crc8(bytes(data)).digest()
            + b"\x00"
        )


async def print_image(img: PIL.Image.Image) -> None:
    assert img.width == PRINTER_WIDTH, f"Image width must be {PRINTER_WIDTH} pixels"

    data = b"".join(
        (
            Command.SET_QUALITY.format(b"\x33"),
            Command.CONTROL_LATTICE.format(Command.Lattice.PRINT.value),
            Command.SET_ENERGY.format(17500),
            Command.DRAWING_MODE.format(b"\x00"),
            Command.OTHER_FEED_PAPER.format(Command.PrintSpeed.IMAGE.value),
            *(
                Command.DRAW_BITMAP.format(bytes(reversed(chunk)))
                for chunk in itertools.batched(
                    img.convert("RGB")
                    .convert("1")
                    .point(lambda p: 255 - p)
                    .transpose(PIL.Image.Transpose.FLIP_TOP_BOTTOM)
                    .tobytes(),
                    PRINTER_WIDTH // 8,
                )
            ),
            Command.CONTROL_LATTICE.format(Command.Lattice.FINISH.value),
            Command.FEED_PAPER.format(50),
        )
    )

    try:
        device = next((d for d in (await BleakScanner.discover()) if d.name == "MX06"))
    except StopIteration:
        print("Printer not found. Make sure it is powered on and in range.")
        sys.exit(1)

    async with BleakClient(device) as client:
        for chunk in itertools.batched(data, n=128):
            await client.write_gatt_char(
                "0000AE01-0000-1000-8000-00805F9B34FB", bytearray(chunk)
            )


__all__ = ["print_image"]


if __name__ == "__main__":
    import asyncio
    asyncio.run(print_image(PIL.Image.open(sys.argv[1])))
