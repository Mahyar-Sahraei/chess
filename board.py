import json
import numpy as np

from color import ColorT
from piece import Piece, PieceT
from mvpolicy import *

class Tile:
    def __init__(self, coord=(0, 0), available=False, has_piece=False, piece=None):
        self.coord = coord
        self.available = available
        self.has_piece = has_piece
        self.piece = piece
        self.color = ColorT.NONE
        if self.available:
            if (coord[0] + coord[1]) % 2 == 0:
                self.color = ColorT.BLACK
            else:
                self.color = ColorT.WHITE
        if self.has_piece:
            self.piece.move(coord)

    def put_piece(self, piece):
        self.has_piece = True
        self.piece = piece
        piece.move(self.coord)

    def pick_piece(self):
        if not self.has_piece:
            return None
        self.has_piece = False
        piece_ret = self.piece
        self.piece = None
        return piece_ret



class Board:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

        availability_map = np.array(config['availability'])
        self.height, self.width = availability_map.shape
        self.tile_array = [
                [Tile(coord=(i, j), available=availability_map[i][j] == 1) 
                for j in range(self.width)] 
            for i in range(self.height)
        ]

        wpieces = self.ld_pieces(conf=config['white'], color=ColorT.WHITE)
        for piece in wpieces:
            self.put_piece(piece, piece.coord)
        bpieces = self.ld_pieces(conf=config['black'], color=ColorT.BLACK)
        for piece in bpieces:
            self.put_piece(piece, piece.coord)

    
    def ld_pieces(self, conf, color):
        pieces = []
        for king in conf['k']:
            pieces.append(Piece(KPolicy(self), PieceT.KING, tuple(king), color))
        for queen in conf['q']:
            pieces.append(Piece(QPolicy(self), PieceT.QUEEN, tuple(queen), color))
        for rook in conf['r']:
            pieces.append(Piece(RPolicy(self), PieceT.ROOK, tuple(rook), color))
        for bishop in conf['b']:
            pieces.append(Piece(BPolicy(self), PieceT.BISHOP, tuple(bishop), color))
        for knight in conf['n']:
            pieces.append(Piece(NPolicy(self), PieceT.KNIGHT, tuple(knight), color))
        for pawn in conf['p']:
            pieces.append(Piece(PPolicy(self, tuple(conf['p_dir']), tuple(pawn)), PieceT.PAWN, tuple(pawn), color))
        return pieces


    def put_piece(self, piece, where):
        tile = self.get_tile(where)
        if tile is None:
            raise Exception(f'No tile at {where}')
        if tile.available:
            if not tile.has_piece:
                tile.put_piece(piece)
            else:
                raise Exception(f'Tile at {where} is not empty!')
        else:
            raise Exception(f'Tile at {where} is not available!')

    def move_piece(self, src, dst):
        src_tile = self.get_tile(src)
        dst_tile = self.get_tile(dst)
        if not src_tile.has_piece:
            return
        piece = src_tile.piece
        if piece.policy.can_move(src, dst):
            piece = src_tile.pick_piece()
            dst_tile.put_piece(piece)

    def get_tile(self, coord):
        try:
            return self.tile_array[coord[0]][coord[1]]
        except IndexError:
            return None