from enum import Enum
from color import *
from mvpolicy import *

class PieceT(Enum):
    NONE = 0,
    KING = 1,
    QUEEN = 2,
    ROOK = 3,
    BISHOP = 4,
    KNIGHT = 5,
    PAWN = 6

class Piece:
    def __init__(self, policy=None, ptype=PieceT.NONE, coord=(0, 0), color=ColorT.NONE):
        self.policy = policy
        self.ptype = ptype
        self.coord = coord
        self.color = color

    def move(self, dest):
        self.coord = dest