from chess.bot.minimax_bot import MiniMaxBot
from chess.console.display import Display
from chess.game.bishop import Bishop
from chess.game.board import File
from chess.game.board import Rank
from chess.game.color import Color
from chess.game.game import Game
from chess.game.knight import Knight
from chess.game.move import Move
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


def get_move(game: Game, move_text: str) -> Move:
    if not 4 <= len(move_text) <= 5:
        return None
    src_file = get_file(move_text[0])
    src_rank = get_rank(move_text[1])
    dst_file = get_file(move_text[2])
    dst_rank = get_rank(move_text[3])

    for rank in [src_rank, dst_rank]:
        if not Rank.is_valid(rank):
            return None
    for file in [src_file, dst_file]:
        if not File.is_valid(file):
            return None

    src = Square(file=src_file, rank=src_rank)
    dst = Square(file=dst_file, rank=dst_rank)
    promo_piece = None
    if len(move_text) == 5:
        piece_name = move_text[4].upper()
        constructor = PIECE_CONSTRUCTORS.get(piece_name, None)
        if not constructor:
            return None
        promo_piece = constructor(game.current_player())
    return src, dst, promo_piece


def run_game():
    game = Game()
    display = Display(game.board())
    display.show()

    # Some test moves
    test_moves = [
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

    test_castle_moves = [
        'e2e4', 'd7d5',
        'f1c4', 'c8e6',
        'g1f3', 'b8c6'
    ]

    initial_moves = []
    for move in initial_moves:
        print(f'\n\nMoving {move}')
        src, dst, promo_piece = get_move(game, move) or (None, None, None)
        result = False
        if src:
            result = game.validate_and_move(src, dst, promo_piece)
        if not result:
            raise Exception(f'Illegal move {move}')
        if game.is_check():
            raise Exception('Unexpected check')
        display.show()
        print(f'Last move - {move}')

    bot = MiniMaxBot(Color.BLACK, game)
    while True:
        player = game.current_player()
        if game.result():
            print(f'{game.result().name}! Game over.')
            break
        if game.is_check():
            print('CHECK ->')
        advantage = game.board().get_material_advantage(Color.WHITE)
        print(f'{player.name} to play. Material advantage: {advantage}')

        # Bot move
        if player == bot.color():
            bot_move = bot.move()
            result = game.validate_and_move(bot_move.source, bot_move.dest, bot_move.pawn_promotion_piece)
        # Human move
        else:
            prompt = 'Make a move or type "exit" to exit: '
            text = input(prompt).strip().lower()
            if text == 'exit':
                break
            src, dst, promo_piece = get_move(game, text) or (None, None, None)
            result = False
            if src:
                result = game.validate_and_move(src, dst, promo_piece)
        display.show()
        if not result:
            print(f'Move \'{text}\' is illegal')


if __name__ == '__main__':
    run_game()
