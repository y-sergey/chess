from chess.console.display import Display
from chess.game.game import Game
from chess.game.square import Square
from chess.game.board import Rank
from chess.game.board import File


def get_file(pos):
    return ord(pos.lower()) - ord('a')


def get_rank(pos):
    return ord(pos.lower()) - ord('1')


def run_move(game, move_text):
    if len(move_text) != 4:
        return False
    src_file = get_file(move_text[0])
    src_rank = get_rank(move_text[1])
    dst_file = get_file(move_text[2])
    dst_rank = get_rank(move_text[3])

    for rank in [src_rank, dst_rank]:
        if not Rank.RANK_1.value <= rank <= Rank.RANK_8.value:
            return False
    for file in [src_file, dst_file]:
        if not File.FILE_A.value <= file <= File.FILE_H.value:
            return False

    src = Square(file=src_file, rank=src_rank)
    dst = Square(file=dst_file, rank=dst_rank)
    return game.move(src, dst)


def run_game():
    game = Game()
    display = Display(game.board())
    display.show()

    # Some test moves
    initial_moves = ['e2e4', 'd7d5',
                     'f1c4', 'a7a6',
                     'a2a4', 'd5e4',
                     'a1a3', 'a8a7',
                     'a3e3', 'g7g5',
                     'e3e4', 'd8d7',
                     'd1h5', 'e8d8',
                     'e1e2', 'd7d6',
                     'g1f3', 'b8d7']

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
        result = run_move(game, text)
        display.show()
        if not result:
            print(f'Move \'{text}\' is illegal')


if __name__ == '__main__':
    run_game()
