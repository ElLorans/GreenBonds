import numpy as np
import pandas as pd
from scipy import stats


def get_table1(df):
    """
    Df must have columns ['Year', '$ Amount (billion)'].
    """
    table1 = pd.pivot_table(df,
                            index=['Year'],
                            values=['$ Amount (billion)'],
                            aggfunc={'Year': 'count',
                                     '$ Amount (billion)': np.sum})  # defaults to 'All'

    # format_dict = {'$ Amount (billion':'${0:,.0f}'}
    # table.style.format(format_dict)

    table1['# Bonds'] = table1['Year']
    table1 = table1[['# Bonds', '$ Amount (billion)']]  # sort columns, remove duplicate 'Year' column
    return table1


def pvalue_to_star(array_like) -> str:
    statistic, pvalue = stats.ttest_1samp(array_like, 0)
    if pvalue < 0.01:
        return '***'
    if pvalue < 0.05:
        return '**'
    elif pvalue < 0.1:
        return '*'
    return ''


def get_table6(event_cars, intervals, winsorize=False):
    if winsorize is True:
        event_cars = {k: stats.mstats.winsorize(v, limits=0.01) for k, v in event_cars.items()}
    avg = {k: np.mean(v) for k, v in event_cars.items()}
    # get standard error
    se = {k: stats.sem(v) for k, v in event_cars.items()}
    # add pvalue
    car_strings = [str(round(v, 3)) + pvalue_to_star(event_cars[k]) for k, v in avg.items()]
    std_err_values = [round(v, 3) for v in se.values()]
    table6 = pd.DataFrame({'CAR': car_strings,
                           'Std. Err.': std_err_values,
                           'Event time': [str(list(interval)) for interval in intervals]}
                          ).set_index('Event time')
    return table6


if __name__ == "__main__":
    print(stats.mstats.winsorize(range(100), limits=0.01))
