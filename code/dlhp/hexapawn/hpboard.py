import copy

from dlhp.hexapawn.hptypes import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass


BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))
# Top left to lower right diagonal
DIAG_1 = (Point(1, 1), Point(2, 2), Point(3, 3))
# Top right to lower left diagonal
DIAG_2 = (Point(1, 3), Point(2, 2), Point(3, 1))


class Board:
    def __init__(self):
        self._grid = {}

    def place(self, player, start_point, end_point):
        assert self.get(start_point) == player
        assert self.is_on_grid(start_point)
        assert self.is_on_grid(end_point)
        #assert self._grid.get(point) is None
        self._grid[end_point] = player
        self._grid[start_point] = None

    @staticmethod
    def is_on_grid(point):
        return 1 <= int(point.row) <= BOARD_SIZE and \
            1 <= int(point.col) <= BOARD_SIZE

    def get(self, point):
        """Return the content of a point on the board.
        Returns None if the point is empty, or a Player if there is a
        stone on that point.
        """
        return self._grid.get(point)


class Move:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point


class GameState:
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        next_board = copy.deepcopy(self.board)
        next_board.place(self.next_player, move.start_point, move.end_point)
        return GameState(next_board, self.next_player.other, move)

    @classmethod
    def new_game(cls):	
        board = Board()
        board._grid[Point(1, 1)] = Player.o
        board._grid[Point(1, 2)] = Player.o
        board._grid[Point(1, 3)] = Player.o
        board._grid[Point(3, 1)] = Player.x
        board._grid[Point(3, 2)] = Player.x
        board._grid[Point(3, 3)] = Player.x
        return GameState(board, Player.x, None)

    def is_valid_move(self, move):	
        return (
            ((
            self.board.get(move.end_point) is None and            #forward to empty spot
            (move.end_point.col == move.start_point.col) and
			    (((move.end_point.row == move.start_point.row + 1)
			     and self.next_player == Player.o)
			  or ((move.end_point.row == move.start_point.row - 1)
			     and self.next_player == Player.x))
            )
            or 
			(
            self.board.get(move.end_point) == self.next_player.other and    #diagonal capture
            abs(move.end_point.col - move.start_point.col) == 1 and
			    (((move.end_point.row == move.start_point.row + 1)
			     and self.next_player == Player.o)
			  or ((move.end_point.row == move.start_point.row - 1)
			     and self.next_player == Player.x))
            ))
			and
            #not self.is_over()
            #and 
            self.board.get(move.start_point) == self.next_player
            )

    def legal_moves(self):
        moves = []
        for startRow in ROWS:
            for startCol in COLS:
                for row in ROWS:
                    for col in COLS:
                        move = Move(Point(startRow, startCol), Point(row, col))
                        if self.is_valid_move(move):
                            moves.append(move)
        return moves

    def is_over(self):	# no legal_moves for curr player , reach end , no pawns left
        if self._reached_end(Player.x):
            return True
        if self._reached_end(Player.o):
            return True
        if self._no_legal_moves(Player.x):
            return True
        if self._no_legal_moves(Player.o): 
            return True
        if all(self.board.get(Point(row, col)) is not None
               for row in ROWS
               for col in COLS):
            return True
        return False
		
    def _no_legal_moves(self, player):	
        moves = self.legal_moves()
        if len(moves) == 0 and \
            self.next_player == player:
            return True
        return False
		
    def _reached_end(self, player):	
        if (self.board.get(Point(1, 1)) == Player.x or \
                self.board.get(Point(1, 2)) == Player.x or \
                self.board.get(Point(1, 3)) == Player.x) and \
                player == Player.x:
            return True
        if (self.board.get(Point(3, 1)) == Player.o or \
                self.board.get(Point(3, 2)) == Player.o or \
                self.board.get(Point(3, 3)) == Player.o) and \
				player == Player.o:
            return True
        return False

    def winner(self):
        if self._reached_end(Player.x):
            return Player.x
        if self._reached_end(Player.o):
            return Player.o
        if self._no_legal_moves(Player.o):
            return Player.x
        if self._no_legal_moves(Player.x):
            return Player.o
        return None