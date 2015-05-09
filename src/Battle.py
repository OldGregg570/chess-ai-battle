import time
from timeit import default_timer as timer
import chess
from lib.Lumberjack import Logger
from Board import Board



STATS_STRING = "\n\tStalemates:\t{0}\n\tPlayer 1 wins:\t{1}\n\tPlayer 2 wins:\t{2}\n"
RESULT_STRING = "\n\tResult: {0}"

log = Logger('Battle')


class Battle ():
    def __init__(self, trial_count, p1, p2, gui=False, sleep_time=0, logg=True):
        """
        Start a series of chess games.
        """
        log.set(logg)
        log.info("\n\tBattle: {0} vs {1}\n", p1.__name__, p2.__name__)
        self.trial_count = trial_count
        self.stalemates = 0
        self.player_one_wins = 0
        self.player_two_wins = 0
        self.players = {'p1': p1(chess.WHITE), 'p2': p2(chess.BLACK)}
        self.gui = gui
        self.results = None
        self.sleep_time = sleep_time
        pass

    def run(self):
        """
        Run the series of battles. Plays trial_count games
        and keeps track of wins and stalemates.
        :return: tuple: (stalemates, p1 wins, p2 wins)
        """

        for n in range(self.trial_count):
            start_time = timer()
            result = self.play_game()

            self.stalemates += result.startswith('stalemate')
            self.player_one_wins += result.startswith('p1')
            self.player_two_wins += result.startswith('p2')

            self.print_stats(n, str(timer() - start_time))

        self.results = (self.stalemates, self.player_one_wins, self.player_two_wins)
        log.info(RESULT_STRING.format(str(self.results)))
        return self.results

    def play_game(self):
        """
        Play a new game of chess. Paints the board and takes move input
        from the players.
        :return: String Winner of the round ('stalemate', 'p1', or 'p2')
        """
        ret_val = None
        board = Board(self.gui)

        if self.gui:
            board.paint()

        while not board.is_game_over():
            current_player = self.players[board.current_player()]
            try:
                move = current_player.get_move(board)
                board.push(move)
                ret_val = board.get_winner()
                board.tick()
            except ValueError:
                log.warn("\n\tInvalid Move!")

            if self.gui:
                board.paint()
                time.sleep(self.sleep_time)

        return ret_val

    def print_stats(self, round_num=None, time_elapsed=None):
        """
        Prints statistics for the round.
        :param round_num: The last completed round
        :param time_elapsed: The time the round took to complete
        :return: None
        """
        if round_num:
            log.info("\n\tRound: " + str(round_num))

        log.info(STATS_STRING.format(str(self.stalemates), str(self.player_one_wins), str(self.player_two_wins)))

        if time_elapsed:
            log.info("\n\tTime Elapsed: " + time_elapsed + "\n\n")
        pass