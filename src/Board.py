#import pygame
#from pygame import Rect
import chess
import logging

logging.basicConfig()
log = logging.getLogger('Board')
log.setLevel(logging.getLevelName('INFO'))

# Constants
SQUARE_COUNT = 8
SQUARE_SIZE = 40
DISPLAY_SIZE = (SQUARE_SIZE * SQUARE_COUNT, SQUARE_SIZE * SQUARE_COUNT)
SPRITE_SIZE = int(SQUARE_SIZE / 1.5)
PADDING = int(SQUARE_SIZE / 5.5)
BLACK = 90, 90, 100
WHITE = 200, 200, 200
PLAYER_NAMES = ['p1', 'p2']

IMG_LOAD = lambda asset: pygame.transform.scale(pygame.image.load('./assets/' + asset), (SPRITE_SIZE, SPRITE_SIZE))

SPRITE_DICT = {
    'p': IMG_LOAD('black_pawn.png'),    'P': IMG_LOAD('white_pawn.png'),
    'r': IMG_LOAD('black_castle.png'),  'R': IMG_LOAD('white_castle.png'),
    'n': IMG_LOAD('black_knight.png'),  'N': IMG_LOAD('white_knight.png'),
    'b': IMG_LOAD('black_bishop.png'),  'B': IMG_LOAD('white_bishop.png'),
    'k': IMG_LOAD('black_king.png'),    'K': IMG_LOAD('white_king.png'),
    'q': IMG_LOAD('black_queen.png'),   'Q': IMG_LOAD('white_queen.png')}


class Board(chess.Board):
    def __init__(self, with_gui=False):
        """
        Chess Board class. Wraps GUI and python-chess board API and adds some extra functionality.
        :param with_gui: Render a GUI for this board on the paint method
        :return:
        """
        super(Board, self).__init__()
        self.__half_move_clock = 0
        self.screen = pygame.display.set_mode(DISPLAY_SIZE) if with_gui else None
        pass

    @property
    def clock(self):
        """
        Return the current clock value. Each player's turn increments the clock
        :return:
        """
        return self.__half_move_clock

    def paint(self):
        """
        Paints the board
        :return:
        """
        self.screen.fill(BLACK)
        for x, y in [(x, y) for x in range(SQUARE_COUNT) for y in range(SQUARE_COUNT)]:
            self._paint_square(x, y)
            self._paint_piece(x, y)
        pygame.display.flip()
        pass

    def get_winner(self):
        """
        Return the winner if there is one
        :return: 'stalemate', 'p1' or 'p2'
        """
        ret_val = None
        if self.is_game_over():
            if self.is_stalemate() or self.is_insufficient_material():
                ret_val = 'stalemate'
            else:
                ret_val = self.current_player()
        return ret_val

    def tick(self):
        """
        Increment the half-move clock and sleep if specified
        :return: None
        """
        self.__half_move_clock += 1

    def current_player(self):
        """
        Returns pN depending on which players turn it is
        :return: Boolean
        """
        return PLAYER_NAMES[self.__half_move_clock % 2]

    def _paint_square(self, x, y):
        """
        Paints the chess pattern
        :return:
        """
        r = Rect(SQUARE_SIZE * (x + (y % 2)), SQUARE_SIZE * y, SQUARE_SIZE, SQUARE_SIZE)
        if x % 2 == 0:
            pygame.draw.rect(self.screen, WHITE, r)
        pass

    def _paint_piece(self, x, y):
        """
        Paint the chess sprites onto the
        :return: None
        """
        f = lambda n: (n * SQUARE_SIZE) + PADDING

        piece = self.piece_at((SQUARE_COUNT - 1 - y) * SQUARE_COUNT + x)

        r = Rect(f(x), f(y), SPRITE_SIZE, SPRITE_SIZE)
        if piece:
            self.screen.blit(SPRITE_DICT[str(piece)], r)
        pass

    def get_pieces(self, color):
        """
        Returns a list of pieces of a provided color.
        :param team:
        :return:
        """
        ret_val = []

        def is_correct_case(p):
            char = str(p)
            if color == chess.WHITE:
                return char.isupper()
            else:
                return char.islower()

        for n in range(SQUARE_COUNT ** 2):
            piece = self.piece_at(n)
            if is_correct_case(piece):
                ret_val.append(n)

        return ret_val
