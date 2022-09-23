from enum import Enum

def sign(n):
    if n == 0:
        return 0
    return 1 if n > 0 else -1

def get_delta(src, dst):
    dx = dst[1] - src[1]
    dy = dst[0] - src[0]
    return dx, dy

def check_src_dst(board, src, dst):
    dst_tile = board.get_tile(dst)
    src_tile = board.get_tile(src)
    if not (src_tile.available and src_tile.has_piece):
        return False
    if not dst_tile.available:
        return False
    if dst_tile.has_piece:
        if dst_tile.piece.color == src_tile.piece.color:
            return False
    return True

class KPolicy:
    def __init__(self, board):
        self.board = board

    def can_move(self, src, dst):
        #Castling not defined yet, due to different possible boards
        dx, dy = get_delta(src, dst)

        if not check_src_dst(self.board, src, dst):
            return False
            
        if abs(dx) > 1 or abs(dy) > 1:
            return False
        
        return True

class RPolicy:
    def __init__(self, board):
        self.board = board

    def can_move(self, src, dst):
        dx, dy = get_delta(src, dst)

        if not ((dx == 0) ^ (dy == 0)):
            return False
        
        if not check_src_dst(self.board, src, dst):
            return False

        if dx == 0 and dy != 0:
            #Vertical Move
            step = sign(dy)
            for y in range(1, abs(dy)):
                test_coord = (src[0] + y * step, src[1])
                tile = self.board.get_tile(test_coord)
                if tile is None:
                    return False
                if not tile.available or tile.has_piece:
                    return False
            return True

        elif dy == 0 and dx != 0:
            #Horizontal Move
            step = sign(dx)
            for x in range(1, abs(dx)):
                test_coord = (src[0], src[1] + x * step)
                tile = self.board.get_tile(test_coord)
                if tile is None:
                    return False
                if not tile.available or tile.has_piece:
                    return False
            return True

        return False

class BPolicy:
    def __init__(self, board):
        self.board = board

    def can_move(self, src, dst):
        dx, dy = get_delta(src, dst)
        
        if abs(dx) != abs(dy) or dx == 0:
            return False

        if not check_src_dst(self.board, src, dst):
            return False

        if dx * dy > 0:
            #y = -x line
            step = sign(dx)
            for d in range(1, abs(dy)):
                test_coord = (src[0] + d * step, src[1] + d * step)
                tile = self.board.get_tile(test_coord)
                if tile is None:
                    return False
                if not tile.available or tile.has_piece:
                    return False
            return True

        else:
            #y = x line
            step = sign(dx)
            for d in range(1, abs(dx)):
                test_coord = (src[0] - d * step, src[1] + d * step)
                tile = self.board.get_tile(test_coord)
                if tile is None:
                    return False
                if not tile.available or tile.has_piece:
                    return False
            return True

class QPolicy:
    def __init__(self, board):
        self.board = board

    def can_move(self, src, dst):
        return RPolicy.can_move(self, src, dst) or\
            BPolicy.can_move(self, src, dst)

class NPolicy:
    def __init__(self, board):
        self.board = board

    def can_move(self, src, dst):
        dx, dy = get_delta(src, dst)
        
        if dx * dx + dy * dy != 5:
            return False

        if not check_src_dst(self.board, src, dst):
            return False

        return True

class PPolicy:
    def __init__(self, board, direction, init_pos):
        self.board = board
        self.direction = direction
        self.init_pos = init_pos

    def can_move(self, src, dst):
        dx, dy = get_delta(src, dst)

        if not check_src_dst(self.board, src, dst):
            return False

        dst_tile = self.board.get_tile(dst)
        max_d = 1
        if src == self.init_pos:
            max_d = 2

        if not dst_tile.has_piece and\
            dx * self.direction[0] >= 0 and\
            dy * self.direction[1] >= 0 and\
            abs(dx) <= abs(self.direction[0] * max_d) and\
            abs(dy) <= abs(self.direction[1] * max_d):
            if abs(dx) == 2 or abs(dy) == 2:
                mid_tile = self.board.get_tile((src[0] + sign(dy), src[1] + sign(dx)))
                if not mid_tile.has_piece:
                    return True
            else:
                return True

        if abs(dx) == 1 and abs(dy) == 1 and dst_tile.has_piece:
            if dx == self.direction[0] or dy == self.direction[1]:
                return True

        return False