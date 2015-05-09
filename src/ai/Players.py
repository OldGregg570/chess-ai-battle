import random
import chess

NUM_FLIP = [0, 8, 7, 6, 5, 4, 3, 2, 1]
ALPHA_FLIP = {'a': 'h', 'b': 'g', 'c': 'f', 'd': 'e', 'e': 'd', 'f': 'c', 'g': 'b', 'h': 'a'}

flip_move_color = lambda move: "{0}{1}{2}{3}".format(move[0], NUM_FLIP[int(move[1])], move[2], NUM_FLIP[int(move[3])])


class AI (object):
    def __init__(self, color):
        """
        AI base class. Defines chess color (black or white)
        """
        self.color = color
        pass

    def get_move(self, board):
        pass


class Randy(AI):
    def get_move(self, board):
        """
        Randy AI
        Behavior: Randy picks a random valid move.
        """
        move_list = list(board.legal_moves)
        move_count = len(board.legal_moves)
        return move_list[random.randint(0, move_count - 1)]


class InitMove(Randy):
    def __init__(self, color, moves):
        """
        InitMove AI
        Starts out taking the moves specified by the 'moves' parameter.
        Note: Moves are to be defined for the white pieces only. Depending on the color of the AI,
        the moves will automatically be inverted.
        """
        Randy.__init__(self, color)

        # invert the moves if this AI is on the black team
        if color == chess.WHITE:
            self.moves = moves
        else:
            self.moves = [flip_move_color(m) for m in moves]
        pass

    def get_move(self, board):
        """
        Attempts to play the moves specified in the move array.
        If none of those moves are available, or if they all have been played, reverts to Randy.
        """
        index = board.clock / 2
        if index < len(self.moves):
            uci_move = chess.Move.from_uci(self.moves[board.clock / 2])
            if uci_move in board.legal_moves:
                return uci_move
            else:
                return super(InitMove, self).get_move(board)
        else:
            return super(InitMove, self).get_move(board)
        pass

class ScholarsMate(InitMove):
    def __init__(self, color):
        """
        ScholarsMate AI
        Attempts the Scholar's Mate, the classic four-move checkmate
        """
        moves = ['e2e4', 'd1h5', 'f1c4', 'h5f7']
        InitMove.__init__(self, color, moves)
        pass


class Noob(InitMove):
    def __init__(self, color):
        """
        Noob AI
        This AI will lose to a ScholarsMate every time.
        """
        moves = ['a2a3', 'b2b3', 'a3a4', 'b3b4']
        InitMove.__init__(self, color, moves)
        pass

class CounterScholarsMate(InitMove):
    def __init__(self, color):
        """
        CounterScholarsMate AI
        Counters the scholar's mate by moving a horse into a defensive position.
        """
        moves = ['e2e4', 'd1h5', 'g1h3']
        InitMove.__init__(self, color, moves)
        pass


'''

class Berserker(AI):
    """
    Berserker AI
    Attacks relentlessly.
    """
    def get_move(self, board):
        attackers = chess.SquareSet(0)
        my_pieces = board.get_pieces(self.color)

        for square in my_pieces:
            if not square is None:
                attackers &= board.attackers(self.color, square)

        print attackers

        move_list = list(board.legal_moves)
        move_count = len(board.legal_moves)
        return move_list[random.randint(0, move_count - 1)]
'''
