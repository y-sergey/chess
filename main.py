from chess.game.board import Board
from chess.console.display import Display


def run_game():
    board = Board()
    display = Display(board)
    display.show()

    while True:
        text = input('Make a move or type "exit" to exit: ').strip()
        if text.lower() == 'exit':
            break
        move = text.split(' ')
        board.move(move[0], move[1])
        display.show()


if __name__ == '__main__':
    run_game()
