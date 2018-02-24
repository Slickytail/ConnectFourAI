"""Connect Four vs a minimax algorithm."""
import copy
class Board:
    """A connect four board."""
    W = 7
    H = 6
    NUMTILES = W*H
    ODDSQUARES = NUMTILES % 2

    def __init__(self, tilestate=None, lastmove=None):
        if tilestate is None:
            self.tiles = [[0 for i in range(self.W)] for j in range(self.H)]
            # X goes first
            self.nextplayer = 1
            self.lastmove = (self.W+1/2, 0)
        else:
            self.tiles = tilestate
            self.lastmove = lastmove
            # Because X goes first, if the number of blank tiles is odd then it's X's turn.
            if sum([row.count(0) for row in tilestate]) % 2 == self.ODDSQUARES:
                self.nextplayer = 1
            else:
                self.nextplayer = 2

    def get_valid_moves(self):
        """Return which columns aren't empty."""
        return [i for i in range(self.W) if not self.tiles[self.H-1][i]]

    def is_full(self):
        """Return whether or not the current board is full."""
        return all([i for i in self.tiles[self.H-1]])

    def get_length(self):
        """Return the number of moves that have been made."""
        return self.NUMTILES - sum([row.count(0) for row in self.tiles])

    def winner(self):
        """Returns the winner of the game, if it's finished.
        -1: Not finished
        0: Draw
        1: X
        2: O
        """
        # Minor optimization
        if self.NUMTILES - sum([self.tiles[i].count(0) for i in range(self.H)]) < 7:
            return -1
        w = self.lastmove[0]
        h = self.lastmove[1]
        # Horizontal wins
        for col in range(self.W - 3): # Check each column in the row of lastmove
            if self.list_is_uniform(self.tiles[h][col:col+4]) and self.tiles[h][col] > 0:
                return self.tiles[h][w]

        if not any(self.tiles[3]):
            return -1
        # Vertical wins
        # Only need to check the four with lastmove at the top
        if h >= 3:
            if self.list_is_uniform([self.tiles[h-i][w] for i in range(4)]):
                return self.tiles[h][w]

        # Diagonal, bottom-left to top-right
        l_dist = min(h, w)
        r_dist = min(self.H - h - 1, self.W - w - 1)
        s_y, s_x = (h-l_dist, w-l_dist)
        for i in range(l_dist+r_dist-2):
            if self.list_is_uniform([self.tiles[s_y+i+j][s_x+i+j] for j in range(4)]) and \
            self.tiles[s_y+i][s_x+i] == self.tiles[h][w]:
                return self.tiles[h][w]

        # Diagonal, top-left to bottom-right
        l_dist = min(self.H - h - 1, w)
        r_dist = min(h, self.W - w - 1)
        s_y, s_x = (h+l_dist, w-l_dist)
        for i in range(l_dist+r_dist-2):
            if self.list_is_uniform([self.tiles[s_y-i-j][s_x+i+j] for j in range(4)]) and \
            self.tiles[s_y-i][s_x+i] == self.tiles[h][w]:
                return self.tiles[h][w]

        if self.is_full():
            return 0
        return -1

    def make_move(self, position):
        """Returns a new board where the given move has been made."""
        h = 0
        while h < self.H:
            if self.tiles[h][position] == 0:
                break
            h += 1
        # Find the highest empty tile, like dropping a physical tile
        newtiles = copy.copy(self.tiles)
        newtiles[h] = copy.copy(self.tiles[h]) # copy the row that gets changed
        newtiles[h][position] = self.nextplayer
        return Board(newtiles, (position, h))

    def update_tiles(self, newboard):
        """Update the state of this board to that of the given board."""
        self.tiles = newboard.tiles
        self.nextplayer = newboard.nextplayer
        self.lastmove = newboard.lastmove

    def display_board(self):
        """Print out the entire board in an easily readable format."""
        for row in self.tiles[::-1]:
            print("|"+("|".join(map(self.render_tile, row)))+"|")
        print(" "+(" ".join(map(str, range(1, self.W+1))))+" ")

    @staticmethod
    def render_tile(tile):
        """Convert the numerical token of a tile into its visual representation."""
        return [" ", "X", "O"][tile] # 0 -> [ ]; # 1 -> X; 2 -> O

    @staticmethod
    def list_is_uniform(lst):
        """Return whether or not the list is uniform"""
        return not lst or lst.count(lst[0]) == len(lst)

def heuristic(board, player):
    """Find sequences in a board and score them"""
    total_value = []
    opponent = [0, 2, 1][player]
    height = board.H
    width = board.W
    tile = board.tiles
    r = range
    for y in r(board.H):
        for x in r(board.W):
            if tile[y][x] == player:
                # Horiz Sequence
                if x < width - 3:
                    seq = [tile[y][x+j] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y][x+j], tile[y-1][x+j] if y else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))
                if x > 2:
                    seq = [tile[y][x-j] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y][x-j], tile[y-1][x-j] if y else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))

                # Vert Sequence
                if y < height - 3:
                    seq = [tile[y+j][x] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y+j][x], tile[y+j-1][x] if y else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))

                # Diag1 Sequence
                if x < width - 3 and y < height - 3:
                    seq = [tile[y+j][x+j] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y+j][x+j], tile[y+j-1][x+j] if y else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))
                if x > 2 and y > 2:
                    seq = [tile[y-j][x-j] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y-j][x-j], tile[y-j-1][x-j] if y-j else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))

                # Diag2 Sequence
                if x < width - 3 and y > 2:
                    seq = [tile[y-j][x+j] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y-j][x+j], tile[y-j-1][x+j] if y-j else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))
                if x > 2  and y < height - 3:
                    seq = [tile[y+j][x-j] for j in r(4)]
                    if opponent not in seq:
                        seq = [form(tile[y+j][x-j], tile[y+j-1][x-j] if y else 1) for j in r(4)]
                        if seq:
                            total_value.append(score_sequence(seq))
    if total_value.count(10) > 1:
        total_value.append(25)
    return sum(total_value)

def score_sequence(tiles):
    """Calculate the value of a sequence of 4 tiles."""
    scores = [[1000, 10, 3, 0],
              [5, 2, 0],
              [1, 0],
              [0]]
    support = tiles.count(1)
    empty = tiles.count(0)
    return scores[empty][support]


def form(tile, support):
    """Format a tile based on its supportedness. 2: Filled; 1: Supported; 0: Unsupported."""
    if tile:
        return 2
    if support:
        return 1
    return 0


def minimax_i(board, start_depth):
    """Return the highest valued move by minimaxing."""
    best_value = -100000
    best_move = None
    alpha = -100000
    beta = 100000
    moves = board.get_valid_moves()
    for move in moves:
        value = minimax_r(board.make_move(move), board.nextplayer, alpha, beta, start_depth)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)
        if alpha >= beta:
            break
    return best_move

def minimax_r(board, player, alpha, beta, depth):
    """Return the value of the best move by minimaxing."""
    result = board.winner()
    if result != -1: # If game is finished
        if result == 0: # A draw is neutral
            return 0
        if result == player: # A win is positive, and a fast win (higher depth) is better
            return 1000 + depth
        return -(1000 + depth) # A loss is negative, and a slow win (lower depth) is better
    if depth <= 0:
        return heuristic(board, player) - heuristic(board, [0, 2, 1][player])
        # Synergy of minmaxer minus synergy of other player

    moves = sorted(board.get_valid_moves(), key=lambda x: abs(x-board.lastmove[0]))
    if board.nextplayer == player: # Maximizing
        best_value = -100000
        for move in moves:
            if alpha >= beta:
                break
            score = minimax_r(board.make_move(move), player, alpha, beta, depth-1)
            best_value = max(best_value, score)
            alpha = max(alpha, best_value)
        return best_value

    else: # Minimizing
        best_value = 100000
        for move in moves:
            if alpha >= beta:
                break
            score = minimax_r(board.make_move(move), player, alpha, beta, depth-1)
            best_value = min(best_value, score)
            beta = min(beta, best_value)
        return best_value

def play_game():
    """Play one game, Human vs Minimax"""
    game_board = Board()
    go_text = "{0}: Enter your column.\n>> "
    heuristic_text = "{0} Position Rating: {1}"
    turn = input("Do you want to go first?\n>> ").lower() in ["true", "yes", "y", "1"]
    while game_board.winner() == -1:
        game_board.display_board()
        print(heuristic_text.format(game_board.render_tile(1), heuristic(game_board, 1)))
        print(heuristic_text.format(game_board.render_tile(2), heuristic(game_board, 2)))
        if turn:
            """
            valid_moves = game_board.get_valid_moves()
            p_move = input(go_text.format(game_board.render_tile(game_board.nextplayer)))
            good_move = False
            if p_move.isdigit():
                good_move = True
                player_loc = int(p_move)-1
                if player_loc not in valid_moves:
                    good_move = False
            while not good_move:
                p_move = input("Bad format or invalid move. Enter another move.\n>> ")
                if p_move == "exit":
                    break
                if p_move.isdigit():
                    good_move = True
                    player_loc = int(p_move)-1
                    if player_loc not in valid_moves:
                        good_move = False
            if p_move == "exit":
                break

            game_board.update_tiles(game_board.make_move(player_loc))
            """
            print("Computer is thinking...")
            move = minimax_i(game_board, 4)
            game_board.update_tiles(game_board.make_move(move))
            print(" " + ("  "*move)+"v")
            
        else:
            print("Computer is thinking...")
            move = minimax_i(game_board, 4)
            game_board.update_tiles(game_board.make_move(move))
            print(" " + ("  "*move)+"v")
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
