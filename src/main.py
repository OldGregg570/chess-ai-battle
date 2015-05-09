import itertools
from timeit import default_timer as timer
from lib.Lumberjack import Logger
from ai.Players import Randy, ScholarsMate, CounterScholarsMate, Noob
from Battle import Battle



STRING_INIT = "Running {0} games ...\nExpected Duration: {1} minutes"

SECONDS_PER_MINUTE = 60.0
MINUTES_PER_HOUR = 60.0
LONG_RUN_WARNING_THRESHOLD = 240 #minutes
log = Logger('Main')

AI = [Randy, CounterScholarsMate, ScholarsMate, Noob]
TRIAL_COUNT = 2000

# Returns the dict key for a pair of combatants
get_battle_key = lambda p1, p2: '{0} vs {1}'.format(p1.__name__, p2.__name__)


def time_estimate():
    """
    Print a time estimate for the current simulation. If the simulation is expected to take more
    than four hours, warn the user
    :return:
    """
    total_trials = len(AI)**2 * TRIAL_COUNT
    log.info('Calculating expected runtime ...')
    estimate_trials = 10
    start_time = timer()
    Battle(estimate_trials, Randy, Randy, False, 0, False).run()

    expected_duration = int(((timer() - start_time) * total_trials) / estimate_trials / SECONDS_PER_MINUTE)

    if expected_duration > LONG_RUN_WARNING_THRESHOLD:
        raw_input('WARNING: This simulation is expected to take over {0} hours. Press any key to continue ...'.format(expected_duration / MINUTES_PER_HOUR))
    else:
        log.info(STRING_INIT, str(total_trials), str(expected_duration))



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


def main():
    """
    Runs all possible battles and logs results
    """
    time_estimate()
    results_dict = {}
    # For each possible battle b in all pair permutations of the list of AI ...
    for p1, p2 in itertools.product(AI, AI):
        results_dict[get_battle_key(p1, p2)] = Battle(TRIAL_COUNT, p1, p2).run()

    report_results(results_dict)

if __name__ == "__main__":
    main()