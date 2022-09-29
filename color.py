from enum import Enum

class ColorT(Enum):
    NONE = 0,
    WHITE = 1,
    BLACK = 2

    def switch_color(color):
        if color == ColorT.BLACK:
            return ColorT.WHITE
        return ColorT.BLACK