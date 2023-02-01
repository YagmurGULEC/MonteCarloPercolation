from percolation import Percolation
import functools
import numpy as np
import pandas as pd


# count if the system percolated out of number of trials
def estimate(nrows, ncols, prob, trials=10000):

    count = 0
    for i in range(trials):
        p = Percolation(nrows, ncols, prob)
        p.open_sites()
        if p.percolates():
            count += 1
    return count/trials


# statistical data after trials
def collectstats(nrows, ncols, trials=10000, dp=0.1):
    data_frame = pd.DataFrame()
    prob = np.arange(0, 1, dp)
    # data_frame['site_vacancy_probability'] = prob
    # data_frame['nrows'] = nrows
    # data_frame['ncols'] = ncols
    # data_frame['dp'] = dp
    # data_frame['trials'] = trials
    stats_collect = []
    for i in prob:
        stats = estimate(nrows, ncols, i,  trials)
        stats_collect.append(stats)
    # data_frame['percolation_probability'] = stats_collect
    return stats_collect
