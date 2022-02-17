from chess.console.display import Display
from chess.game.bishop import Bishop
from chess.game.board import File
from chess.game.board import Rank
from chess.game.game import Game
from chess.game.knight import Knight
from chess.game.piece import Piece
from chess.game.queen import Queen
from chess.game.rook import Rook
from chess.game.square import Square

PIECE_CONSTRUCTORS = {
    Piece.KNIGHT: Knight,
    Piece.BISHOP: Bishop,
    Piece.ROOK: Rook,
    Piece.QUEEN: Queen
}


def get_file(pos):
    return ord(pos.lower()) - ord('a')


def get_rank(pos):
    return ord(pos.lower()) - ord('1')


def run_move(game: Game, move_text: str):
    if not 4 <= len(move_text) <= 5:
        return False
    src_file = get_file(move_text[0])
    src_rank = get_rank(move_text[1])
    dst_file = get_file(move_text[2])
    dst_rank = get_rank(move_text[3])

    for rank in [src_rank, dst_rank]:
        if not Rank.is_valid(rank):
            return False
    for file in [src_file, dst_file]:
        if not File.is_valid(file):
            return False

    src = Square(file=src_file, rank=src_rank)
    dst = Square(file=dst_file, rank=dst_rank)
    promo_piece = None
    if len(move_text) == 5:
        piece_name = move_text[4].upper()
        constructor = PIECE_CONSTRUCTORS.get(piece_name, None)
        if not constructor:
            return False
        promo_piece = constructor(game.current_player())
    return game.move(src, dst, pawn_promotion=promo_piece)


def run_game():
    game = Game()
    display = Display(game.board())
    display.show()

    # Some test moves
    initial_moves = [
        'e2e4', 'd7d5',
        'f1c4', 'a7a6',
        'a2a4', 'd5e4',
        'a1a3', 'a8a7',
        'a3e3', 'g7g5',
        'e3e4', 'd8d7',
        'd1h5', 'e8d8',
        'e1e2', 'd7d6',
        'g1f3', 'b8d7',
        'e2f1'
    ]

    fools_mate_moves = [
        'e2e4', 'e7e5',
        'd1h5', 'a7a6',
        'f1c4', 'a6a5'
    ]

    scholar_mate_moves = [
        'e2e4', 'f7f6',
        'd2d4', 'g7g5'
    ]

    initial_moves = scholar_mate_moves
    for move in []:
        print(f'\n\nMoving {move}')
        if not run_move(game, move):
            raise Exception(f'Illegal move {move}')
        if game.is_check():
            raise Exception('Unexpected check')
        display.show()
        print(f'Last move - {move}')

    while True:
        player = game.current_player().name
        if game.result():
            print(f'{game.result().name}! Game over.')
            break
        if game.is_check():
            print('CHECK ->')
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
