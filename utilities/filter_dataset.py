import pandas as pd


def filter_dataset(df):
    """
    Return public_df [2013, 2019].
    """
    total_len = len(df.index)
    df = df[df['Issue Date'].dt.year >= 2013]
    df = df[df['Issue Date'].dt.year < 2020]
    
    print(f"Excluded {total_len - len(df.index)} rows over {total_len}. "
          "Green bonds before 2012 must be due to errors and 2020 might "
          "pollute data due to COVID and year not finished yet.")
    return df
