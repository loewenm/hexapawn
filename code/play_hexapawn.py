from dlhp import minimax
from dlhp import hexapawn as hp

from six.moves import input

COL_NAMES = 'ABC'

def print_board(board):
    print('   A   B   C')
    for row in (1, 2, 3):
        pieces = []
        for col in (1, 2, 3):
            piece = board.get(hp.Point(row, col))
            if piece == hp.Player.x:
                pieces.append('X')
            elif piece == hp.Player.o:
                pieces.append('O')
            else:
                pieces.append(' ')
        print('%d  %s' % (row, ' | '.join(pieces)))


def move_from_coords(text):
    col_name = text[0]
    row = int(text[1])
    end_col = text[3]
    end_row = int(text[4])
    return hp.Move(hp.Point(row, COL_NAMES.index(col_name) + 1), hp.Point(end_row, COL_NAMES.index(end_col) + 1))


def main():
    game = hp.GameState.new_game()

    human_player = hp.Player.x
    # bot_player = hp.Player.o

    bot = minimax.MinimaxAgent()

    while not game.is_over():
        print_board(game.board)
        if game.next_player == human_player:
            human_move = input('Human >> ')
            move = move_from_coords(human_move.strip())
        else:
            move = bot.select_move(game)
            print('Bot moved...')
        game = game.apply_move(move)

    print_board(game.board)
    winner = game.winner()
    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()