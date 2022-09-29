import numpy as np

from color import ColorT
from piece import PieceT

class Checker:
    def __init__(self, board):
        self.board = board

    def is_checked(self, k_coord, op_color):
        return self.check_king(k_coord, op_color) or\
               self.check_pawn(k_coord, op_color) or\
               self.check_knight(k_coord, op_color) or\
               self.check_rook(k_coord, op_color) or\
               self.check_bishop(k_coord, op_color)

    def check_king(self, coord, color):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (dx == 0 and dy == 0):
                    continue
                new_coord = (coord[0] + dy, coord[1] + dx)
                tile = self.board.get_tile(new_coord)
                if tile is None:
                    continue
                if tile.has_piece:
                    if tile.piece.ptype == PieceT.KING and\
                        tile.piece.color == color:
                        return True
        return False

    def check_rook(self, coord, color):
        directions = [
            (range(1, coord[0] + 1), (-1, 0)),                #up
            (range(1, coord[1] + 1), (0, -1)),                #left
            (range(1, self.board.height - coord[0]), (1, 0)), #down
            (range(1, self.board.width - coord[1]), (0, 1)),  #right
        ]
        for rng, idx in directions:
            for delta in rng:
                tile = self.board.get_tile((coord[0] + delta*idx[0], coord[1] + delta*idx[1]))
                if tile is None:
                    break
                if tile.has_piece:
                    ptype = tile.piece.ptype
                    if (ptype == PieceT.ROOK or ptype == PieceT.QUEEN) and\
                        tile.piece.color == color:
                        return True
                    break
        return False

    def check_bishop(self, coord, color):
        dist_up = coord[0] + 1
        dist_left = coord[1] + 1
        dist_down = self.board.height - coord[0]
        dist_right = self.board.width - coord[1]

        directions = [
            (range(1, min(dist_up, dist_left)), (-1, -1)),  #up_left
            (range(1, min(dist_down, dist_left)), (1, -1)), #down_left
            (range(1, min(dist_down, dist_right)), (1, 1)), #down_right
            (range(1, min(dist_up, dist_right)), (-1, 1)),  #up_right
        ]
        for rng, idx in directions:
            for delta in rng:
                tile = self.board.get_tile((coord[0] + delta*idx[0], coord[1] + delta*idx[1]))
                if tile is None:
                    break
                if tile.has_piece:
                    ptype = tile.piece.ptype
                    if (ptype == PieceT.BISHOP or ptype == PieceT.QUEEN) and\
                        tile.piece.color == color:
                        return True
                    break
        return False

    def check_knight(self, coord, color):
        for delta in (-2, -1, 1, 2):
            for sign in (-1, 1):
                new_coord = (coord[0] + delta, coord[1] + sign * (3 - abs(delta)))
                tile = self.board.get_tile(new_coord)
                if tile is None:
                    continue
                if tile.has_piece:
                    if tile.piece.ptype == PieceT.KNIGHT and\
                        tile.piece.color == color:
                        return True
        return False

    def check_pawn(self, coord, color):
        p_dir = self.board.white_pawn_dir
        if color == ColorT.BLACK:
            p_dir = self.board.black_pawn_dir

        fn = lambda x: 1 - abs(x) - x
        coord1 = (coord[0] + fn(p_dir[1]), coord[1] + fn(p_dir[0]))
        fn = lambda x: abs(x) - 1 - x
        coord2 = (coord[0] + fn(p_dir[1]), coord[1] + fn(p_dir[0]))
        tiles = [
            self.board.get_tile(coord1),
            self.board.get_tile(coord2)
        ]
        for tile in tiles:
            if tile is None:
                continue
            if tile.has_piece:
                if tile.piece.ptype == PieceT.PAWN and\
                    tile.piece.color == color:
                    return True
        return False