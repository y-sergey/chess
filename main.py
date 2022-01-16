from chess.console.display import Display
from chess.game.board import Board
from chess.game.game import Game
from chess.game.square import Square


def get_file(pos):
    return ord(pos.lower()) - ord('a')


def get_rank(pos):
    return int(pos) - 1


def run_game():
    game = Game()
    display = Display(game.board())
    display.show()

    while True:
        player = game.current_player().name
        prompt = f'{player} to play. Make a move or type "exit" to exit: '
        text = input(prompt).strip().lower()
        if text == 'exit':
            break

        pos_from = Square(file=get_file(text[0]), rane2e4k=get_rank(text[1]))
        pos_to = Square(file=get_file(text[2]), rank=get_rank(text[3]))
        move_ok = game.move(pos_from, pos_to)
        display.show()
        if not move_ok:
            print(f'Move \'{text}\' is illegal')


if __name__ == '__main__':
    run_game()
