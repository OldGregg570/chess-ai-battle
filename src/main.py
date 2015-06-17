import itertools
from timeit import default_timer as timer
from ai.Combatants import Randy, ScholarsMate, CounterScholarsMate, Noob
from Battle import Battle
import logging
import os
import sys

logging.basicConfig()
log = logging.getLogger('Main')
log.setLevel(logging.getLevelName('INFO'))

STRING_INIT = "Running {0} games ...\nExpected Duration: {1} {2}"

MEAN_GAME_LENGTH_HIGH_ESTIMATE = 1.5 #seconds

SECONDS_PER_MINUTE = 60.0
MINUTES_PER_HOUR = 60.0

# The estimated number of trials that can be simulated in five minutes on my machine
FIVE_MINUTE_THRESHOLD = 5 * (SECONDS_PER_MINUTE / MEAN_GAME_LENGTH_HIGH_ESTIMATE)

LONG_RUN_WARNING_THRESHOLD = 3

# TODO: grab these from a config file somehow
AI = [Randy, CounterScholarsMate, ScholarsMate, Noob]
DEFAULT_TRIAL_COUNT = 100

# Returns the dict key for a pair of combatants
get_battle_key = lambda p1, p2: '{0} vs {1}'.format(p1.__name__, p2.__name__)


def time_estimate(trials):
    """
    Print a time estimate for the current simulation. If the simulation is expected to take more
    than four hours, warn the user
    :return:
    """
    total_trials = len(AI)**2 * trials
    unit = 'hours'

    if total_trials > FIVE_MINUTE_THRESHOLD:
        log.info('Calculating expected runtime ...')
        estimate_trials = 6
        start_time = timer()
        Battle(estimate_trials, Randy, Randy).run()

        expected_duration = int(((timer() - start_time) * total_trials) / estimate_trials / SECONDS_PER_MINUTE / MINUTES_PER_HOUR)

        if expected_duration > LONG_RUN_WARNING_THRESHOLD:
            raw_input('WARNING: This simulation is expected to take over {0} hours. Press any key to continue ...'.format(expected_duration))
    else:
        expected_duration = 5
        unit = 'minutes'

    log.info(STRING_INIT.format(str(total_trials), str(expected_duration), unit))


def report_results(results_dict):
    """
    Report the results into a file called table_data
    :param results_dict:
    :return:
    """
    with open('./src/table_data', 'w') as fout:
        fout.writelines('TABLE_DATA = ')
        for pair in results_dict.iteritems():
            fout.writelines('\'' + str(pair).replace("'", '') + '\' + \n')
        fout.writelines('\'\'\n')


def print_progress_bar(progress, p1=None, p2=None):
    p = int(progress)
    os.system('cls' if os.name == 'nt' else 'clear')
    if p1 and p2:
        print "Current Battle: {0} vs {1}".format(p1, p2)
    else:
        print "Done!"

    print '\n'
    print '[{0}{1}]'.format('#' * p, '-' * (100 - p))


def main():
    """
    Runs all possible battles and logs results
    """
    trials = DEFAULT_TRIAL_COUNT if len(sys.argv) > 0 else int(sys.argv[1])
    print trials
    battle_count = len(AI)**2
    time_estimate(trials)
    results_dict = {}
    trial_num = 0

    # For each possible battle b in all pair permutations of the list of AI ...
    for p1, p2 in itertools.product(AI, AI):
        progress = float(trial_num) / float(battle_count) * 100.0
        print_progress_bar(progress, p1.__name__, p2.__name__)
        results_dict[get_battle_key(p1, p2)] = Battle(trials, p1, p2).run()
        trial_num += 1

    print_progress_bar(100.0)
    report_results(results_dict)

if __name__ == "__main__":
    main()