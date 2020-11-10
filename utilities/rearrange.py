import pandas as pd


def rearrange(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return df with many columns after pivoting and transposing a df with one column.
    :param df: pd.DataFrame with columns ['Instrument', 'Date', 'Close Price']
    :return: pd.DataFrame with datetime index and one column for every Instrument with values from Close Price.
    """
    df = df.pivot(index='Instrument', columns='Date', values='Close Price').transpose()
    df.index = pd.to_datetime(df.index)
    return df
