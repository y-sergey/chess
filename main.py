from chess.console.display import Display
from chess.game.game import Game
from chess.game.square import Square


def get_file(pos):
    return ord(pos.lower()) - ord('a')


def get_rank(pos):
    return int(pos) - 1


def run_move(game, text):
    pos_from = Square(file=get_file(text[0]), rank=get_rank(text[1]))
    pos_to = Square(file=get_file(text[2]), rank=get_rank(text[3]))
    return game.move(pos_from, pos_to)


def run_game():
    game = Game()
    display = Display(game.board())
    display.show()

    # Some test moves
    initial_moves = ['e2e4', 'd7d5', 'f1c4', 'a7a6', 'a2a4', 'd5e4', 'a1a3', 'a8a7', 'a3e3', 'g7g5', 'e3e4']
    for move in initial_moves:
        if not run_move(game, move):
            raise Exception(f'Illegal move {move}')
        display.show()

    while True:
        player = game.current_player().name
        prompt = f'{player} to play. Make a move or type "exit" to exit: '
        text = input(prompt).strip().lower()
        if text == 'exit':
            break
        display.show()
        if not run_move(game, text):
            print(f'Move \'{text}\' is illegal')


if __name__ == '__main__':
    run_game()
