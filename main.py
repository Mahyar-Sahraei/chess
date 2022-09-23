from board import Board
from visualizer import Visualizer

if __name__ == '__main__':
    #paths to required json configurations
    board_config = 'sets/standard/board.json'
    setting_config = 'sets/standard/setting.json'

    main_board = Board(board_config)
    visualizer = Visualizer(main_board, setting_config)
    visualizer.start()