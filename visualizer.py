import json
import pygame

from time import sleep
from color import ColorT
from piece import PieceT

class Visualizer:
    def __init__(self, board, setting_path):
        with open(setting_path, 'r') as f:
            setting = json.load(f)

        pygame.display.init()
        self.board = board
        self.tile_size = setting['tile_size']
        self.surf_size = (
            self.board.width * self.tile_size, 
            self.board.height * self.tile_size
        )
        self.surf = pygame.display.set_mode(self.surf_size)

        pfolder = setting['pieces_folder']
        tfolder = setting['tiles_folder']
        bgfile = setting['background_file']
        pieces = ['k', 'q', 'r', 'b', 'n', 'p']

        self.background = self.load_bg(bgfile)

        self.white_pieces = {}
        for piece in pieces:
            self.white_pieces[piece] = self.load(f'{pfolder}w{piece}.png')
        
        self.black_pieces = {}
        for piece in pieces:
            self.black_pieces[piece] = self.load(f'{pfolder}b{piece}.png')
        
        self.tiles = {}
        self.tiles['w'] = self.load(f'{tfolder}wt.png')
        self.tiles['b'] = self.load(f'{tfolder}bt.png')

    def load(self, path):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
        return img

    def load_bg(self, path):
        bg = pygame.image.load(path).convert()
        bg = pygame.transform.scale(bg, self.surf_size)
        return bg

    def draw(self, tile, dest, color):
        if color == ColorT.NONE:
            #draw sth if you need
            return
        elif color == ColorT.BLACK:
            self.surf.blit(self.tiles['w'], dest)
        else:
            self.surf.blit(self.tiles['b'], dest)
        if tile.has_piece:
            ptype = tile.piece.ptype
            if tile.piece.color == ColorT.WHITE:
                pset = self.white_pieces 
            else: 
                pset = self.black_pieces

            if ptype == PieceT.KING:
                self.surf.blit(pset['k'], dest)
            elif ptype == PieceT.QUEEN:
                self.surf.blit(pset['q'], dest)
            elif ptype == PieceT.ROOK:
                self.surf.blit(pset['r'], dest)
            elif ptype == PieceT.BISHOP:
                self.surf.blit(pset['b'], dest)
            elif ptype == PieceT.KNIGHT:
                self.surf.blit(pset['n'], dest)
            elif ptype == PieceT.PAWN:
                self.surf.blit(pset['p'], dest)

    def get_mouse_coord(self):
        x, y = pygame.mouse.get_pos()
        x = x // self.tile_size
        y = y // self.tile_size
        return x, y

    def render(self, coord=None, flip=True):
        if coord is not None:
            tile = self.board.get_tile(coord)
            dest = (coord[1]*self.tile_size, coord[0]*self.tile_size)
            self.draw(tile, dest, tile.color)
            if flip:
                pygame.display.flip()
            return

        self.surf.blit(self.background, (0, 0))
        for row in self.board.tile_array:
            for tile in row:
                i, j = tile.coord
                dest = (j*self.tile_size, i*self.tile_size)
                self.draw(tile, dest, tile.color)
        if flip:
            pygame.display.flip()

    def render_border(self, x, y, color=(255, 255, 0), flip=True):
        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        pygame.draw.rect(self.surf, color, rect, 4, 2)
        if flip:
            pygame.display.flip()

    def show_err(self, src, dst):
        self.render_border(
            src[1]*self.tile_size,
            src[0]*self.tile_size,
            (255, 0, 0), False)
        self.render_border(
            dst[1]*self.tile_size,
            dst[0]*self.tile_size,
            (255, 0, 0), True)
        sleep(0.7)

    def start(self):
        self.render()
        select_mode = True
        selected_src = (0, 0)
        selected_dst = (0, 0)
        turn = ColorT.WHITE
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    x, y = self.get_mouse_coord()
                    if select_mode:
                        self.render_border(x*self.tile_size, y*self.tile_size)
                        selected_src = (y, x)
                        select_mode = False
                    else:
                        selected_dst = (y, x)
                        moved = self.board.move_piece(selected_src, selected_dst, turn)
                        if moved:
                            turn = ColorT.switch_color(turn)
                        else:
                            self.show_err(selected_src, selected_dst)
                        self.render(selected_src, False)
                        self.render(selected_dst, True)
                        select_mode = True
