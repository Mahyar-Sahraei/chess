from board import Board
from visualizer import Visualizer

if __name__ == '__main__':
    # main_board = Board('sets/standard/std_board.json')
    # visualizer = Visualizer(main_board, 'sets/standard/std_setting.json')
    main_board = Board('sets/custom1/cst1_board.json')
    visualizer = Visualizer(main_board, 'sets/custom1/cst1_setting.json')
    visualizer.start()