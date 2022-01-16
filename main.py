from chess.game.board import Board
from chess.console.display import Display
from chess.game.square import Square


def get_file(pos):
    return ord(pos.lower()) - ord('a')


def get_rank(pos):
    return int(pos) - 1


def run_game():
    board = Board()
    display = Display(board)
    display.show()

    while True:
        text = input('Make a move or type "exit" to exit: ').strip().lower()
        if text == 'exit':
            break
        pos_from = Square(file=get_file(text[0]), rank=get_rank(text[1]))
        pos_to = Square(file=get_file(text[2]), rank=get_rank(text[3]))
        board.move(pos_from, pos_to)
        display.show()


if __name__ == '__main__':
    run_game()
