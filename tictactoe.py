"""Tic-Tac-Toe vs a minimax algorithm."""
import copy

class Board:
    """A tic-tac-toe board."""
    W = 3
    H = 3

    def __init__(self, tilestate=None):
        if tilestate is None:
            self.tiles = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
            # X goes first
            self.nextplayer = 1
        else:
            self.tiles = tilestate
            # Because X goes first, if the number of blank tiles is odd then it's X's turn.
            if sum([tilestate[i].count(0) for i in range(3)]) % 2 == 1:
                self.nextplayer = 1
            else:
                self.nextplayer = 2

    def get_valid_moves(self):
        """Return the coordinates of empty spaces."""
        moves = []
        for row in range(3):
            for col in range(3):
                if not self.tiles[row][col]:
                    moves.append((row, col))
        return moves

    def is_full(self):
        """Return whether or not the current board is full."""
        return len(self.get_valid_moves()) == 0

    def winner(self):
        """Returns the winner of the game, if it's finished.
        -1: Not finished
        0: Draw
        1: X
        2: O
        """

        if self.tiles[0][0] == self.tiles[1][1] and \
           self.tiles[0][0] == self.tiles[2][2] and \
           self.tiles[0][0]:
            return self.tiles[0][0]
        for row in self.tiles:
            if row == [1, 1, 1] or row == [2, 2, 2]:
                return row[0]

        r_tiles = list(zip(*reversed(self.tiles)))
        if r_tiles[0][0] == r_tiles[1][1] and \
           r_tiles[0][0] == r_tiles[2][2] and \
           r_tiles[0][0]:
            return r_tiles[0][0]
        for col in r_tiles:
            if col == (1, 1, 1) or col == (2, 2, 2):
                return col[0]

        if self.is_full():
            return 0
        return -1

    def make_move(self, position):
        """Returns a new board where the given move has been made."""
        if position not in self.get_valid_moves():
            self.display_board()
            raise ValueError("The given tile {0} is already filled.".format(position))

        newtiles = copy.deepcopy(self.tiles)
        newtiles[position[0]][position[1]] = copy.copy(self.nextplayer)
        return Board(newtiles)

    def update_tiles(self, newboard):
        """Update the state of this board to that of the given board."""
        self.tiles = copy.deepcopy(newboard.tiles)
        self.nextplayer = copy.copy(newboard.nextplayer)

    def display_board(self):
        """Print out the entire board in an easily readable format."""
        print(" {0} | {1} | {2} ".format(*map(self.render_tile, self.tiles[0])))
        print("-----------")
        print(" {0} | {1} | {2} ".format(*map(self.render_tile, self.tiles[1])))
        print("-----------")
        print(" {0} | {1} | {2} ".format(*map(self.render_tile, self.tiles[2])))

    @staticmethod
    def render_tile(tile):
        """Convert the numerical token of a tile into its visual representation."""
        return [" ", "X", "O"][tile] # 0 -> [ ]; # 1 -> X; 2 -> O

def minimax_i(board):
    """Return the highest valued move by minimaxing."""
    moves = board.get_valid_moves()
    player = copy.copy(board.nextplayer)
    best_value = -2
    best_move = (-1, -1)
    for move in moves:
        move_value = minimax_r(board.make_move(move), player, -10, 10)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

def minimax_r(board, player, alpha, beta):
    """Return the value of the best move by minimaxing."""
    result = board.winner()
    if result != -1: # If game is finished
        if result == 0: # A draw is neutral
            return 0
        if result == player: # A win is positive
            return 1
        return -1 # A loss is negative

    moves = board.get_valid_moves()
    if board.nextplayer == player: # Maximizing
        best_value = -10
        for move in moves:
            score = minimax_r(board.make_move(move), player, alpha, beta)
            best_value = max(best_value, score)
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
        return best_value

    else: # Minimizing
        best_value = 10
        for move in moves:
            score = minimax_r(board.make_move(move), player, alpha, beta)
            best_value = min(best_value, score)
            beta = min(beta, best_value)
            if alpha >= beta:
                break
        return best_value


def play_game():
    """Play one game, Human vs Minimax"""
    game_board = Board()
    go_text = "{0}: Enter your move x,y.\n>> "
    turn = True
    while game_board.winner() == -1:
        if turn:
            game_board.display_board()
            valid_moves = game_board.get_valid_moves()
            p_move = input(go_text.format(game_board.render_tile(game_board.nextplayer))).split(",")
            player_loc = (3-int(p_move[1]), int(p_move[0])-1) # Translate 1-3 x, y to 0-2 y-x
            while player_loc not in valid_moves:
                p_move = input("Bad format or invalid move. Enter another move.\n>> ").split(",")
                player_loc = (3-int(p_move[1]), int(p_move[0])-1)

            game_board.update_tiles(game_board.make_move(player_loc))
        else:
            print("Computer is thinking...")
            move = minimax_i(copy.deepcopy(game_board))
            game_board.update_tiles(game_board.make_move(move))
        turn = not turn
    game_board.display_board()
    result = game_board.winner()
    if result:
        print("Game over. {0} wins!".format(game_board.render_tile(result)))
    else:
        print("Game over. It's a draw.")

PLAYING = True
while PLAYING:
    play_game()
    PLAYING = input("Play again?\n>> ").lower() in ["true", "yes", "y", "1"]
