import json
import numpy as np

from color import ColorT
from piece import Piece, PieceT

class Tile:
    def __init__(self, coord=(0, 0), available=False, has_piece=False, piece=Piece()):
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
        self.piece.move(coord)

    def put_piece(self, piece):
        self.has_piece = True
        self.piece = piece
        piece.move(self.coord)

    def pick_piece(self):
        self.has_piece = False
        piece = self.piece
        self.piece = Piece()
        return piece



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
            pieces.append(Piece(PieceT.KING, tuple(king), color))
        for queen in conf['q']:
            pieces.append(Piece(PieceT.QUEEN, tuple(queen), color))
        for rook in conf['r']:
            pieces.append(Piece(PieceT.ROOK, tuple(rook), color))
        for bishop in conf['b']:
            pieces.append(Piece(PieceT.BISHOP, tuple(bishop), color))
        for knight in conf['n']:
            pieces.append(Piece(PieceT.KNIGHT, tuple(knight), color))
        for pawn in conf['p']:
            pieces.append(Piece(PieceT.PAWN, tuple(pawn), color))
        return pieces


    def put_piece(self, piece, where):
        tile = self.get_tile(where)
        if tile.available:
            if not tile.has_piece:
                tile.put_piece(piece)
            else:
                raise Exception('Requested tile is not empty!')
        else:
            raise Exception('Requested tile is not available!')

    def move_piece(self, src, dest):
        src_tile = self.get_tile(src)
        dest_tile = self.get_tile(dest)
        if not (src_tile.available and src_tile.has_piece):
            raise Exception('Invalid source tile')
        if not dest_tile.available:
            raise Exception('Invalid source tile')
        if dest_tile.has_piece:
            if src_tile.piece.color == dest_tile.piece.color:
                raise Exception('Invalid source tile')
        piece = src_tile.pick_piece()
        dest_tile.put_piece(piece)

    def get_tile(self, coord):
        return self.tile_array[coord[0]][coord[1]]