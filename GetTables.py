# %%
import os
from collections import OrderedDict
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from tqdm.auto import tqdm

from utilities import flammer_tables, create_tables

# auto resize plots for pdf files
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

FILENAME = 'cleaned_green_bonds.csv'
FLAMMER_TABLE1, FLAMMER_TABLE3, FLAMMER_TABLE4, FLAMMER_TABLE6 = flammer_tables.flammer_tables
INTERVALS = flammer_tables.INTERVALS

try:
    df = pd.read_csv(r'Dataset\cleaned_green_bonds.csv', parse_dates=['Issue Date', 'First Announcement Date'])
except FileNotFoundError:
    print('Dataset Not Found...')
    import BuildDataset

    df = pd.read_csv(r'Dataset\cleaned_green_bonds.csv', parse_dates=['Issue Date', 'First Announcement Date'])

# dtype DOES NOT WORK... WHY?? -> convert Ultimate Parent Id to str and remove .0 if present
df['Ultimate Parent Id'] = df['Ultimate Parent Id'].astype(
    str).str.replace('.0', '', regex=False)  # regex=False is faster than escaping the '.' with '\.0'

# EXCLUDE municipalities?? I think so, because they are government
df = df[df['Issuer Type'] != 'Non-US Munis']
# Exclude State-Owned companies
# df = df[df['Sector'] != 'Agency']
#####

# Year column is needed for pivot and unique()
df['Year'] = df['Issue Date'].dt.year

# parse_dates() and pd.to_datetime() fail due to a single date > 3000
try:
    df['Maturity'] = df['Maturity'].apply(
        # exclude time part with .split()
        lambda x: datetime.strptime(x.split(' ', 1)[0], '%Y-%m-%d').date() if not pd.isna(x) else pd.NaT)

except AttributeError:
    print('Maturity has already been converted to date.')

# float required to avoid stack overflow
df['$ Amount (billion)'] = df['Amount Issued (USD)'].astype(float) / 1000000000

# My Table 1. Corporate green bonds over time
table1 = create_tables.get_table1(df)
# Figure 1. Evolution of corporate green bonds

# Panel A. Issuance of corporate green bonds (in $B)
figure1_panelA = table1['# Bonds'].plot.bar(title='# Green Bonds')
try:
    figure1_panelA.get_figure().savefig(r'Results\Figure1PanelA.pdf')
except FileNotFoundError:
    os.mkdir('Results')
    figure1_panelA.get_figure().savefig(r'Results\Figure1PanelA.pdf')

# Panel B. Number of corporate green bonds issued
figure1_panelB = table1['$ Amount (billion)'].plot.bar(title='$ Amount (billion)')
figure1_panelB.get_figure().savefig(r'Results\Figure1PanelB.pdf')

# My Table 2. Corporate green bonds by industry
column = 'Sector'
table2 = pd.pivot_table(df,
                        index=[column],
                        values=['$ Amount (billion)'],
                        aggfunc={column: 'count',
                                 '$ Amount (billion)': np.sum})

table2.rename(columns={column: '# Bonds'}, inplace=True)  # cannot sort if column.name == index.name
sorter = '# Bonds'
table2 = table2[[sorter, '$ Amount (billion)']].sort_values(by=[sorter], ascending=False)

# My Table 3. Corporate green bonds by country
pivot_column = 'Country of Incorporation'  # Country of Issue uses 'Eurobond Mkt' for most EU

table3 = pd.pivot_table(df,
                        index=[pivot_column],
                        values=['$ Amount (billion)'],
                        aggfunc={pivot_column: 'count',
                                 '$ Amount (billion)': np.sum})

table3['# Bonds'] = table3[pivot_column]
table3 = table3[['# Bonds', '$ Amount (billion)']].sort_values('$ Amount (billion)', ascending=False)

#public = df[df['IsPublic'] == True]
#private = df[df['IsPublic'] == False]

public = df[df['IsParentPublic'] == True]
private = df[df['IsParentPublic'] == False]

public_table4 = dict()
private_table4 = dict()
all_firms_table4 = dict()

# combinations (dict, df, name: str)
df_to_info = ((all_firms_table4, df, 'All'), (private_table4, private, 'Private'),
              (public_table4, public, 'Public'))

table4_columns = list()  # list of dfs

# create a df (the column of the final df) for each combination
for dictionary, dataframe, col_name in df_to_info:
    dictionary['# Green bonds'] = len(dataframe.index)

    # number of unique days on which a given firm issues green bonds (summed across all firms)
    # group by Issuer, get Issue Date and len of np.array of unique values (.str. is required)
    dictionary['# Green bond issuer-days'] = dataframe.groupby('Issuer')['Issue Date'].unique(
    ).str.len().sum()

    dictionary['# Green bond issuer-years'] = dataframe.groupby('Issuer')['Year'].unique(
    ).str.len().sum()

    dictionary['# Green bond issuers'] = len(dataframe.Issuer.unique())
    dictionary['Amount (in $M)'] = round(dataframe['$ Amount (billion)'].mean(
    ) * 1000, 2)
    dictionary['Amount (in $M) Standard Deviation'] = round(
        dataframe['$ Amount (billion)'].std(), 2)
    dictionary['Certified (1/0)'] = np.NaN
    dictionary['Certified (1/0) Standard Deviation'] = np.NaN

    # get Maturity (years)
    dated = dataframe[['Issue Date', 'Maturity']].dropna()
    # cannot use vectorized subtraction due to date > 3000
    maturities_years = np.array(
        [(start - end.date()).days /
         365 for start, end in zip(
            dated.Maturity, dated['Issue Date'])
         ]
    )

    dictionary['Maturity (years)'] = np.round(np.mean(maturities_years), 2)
    dictionary['Maturity (years) Standard Deviation'] = np.round(
        np.std(maturities_years), 2)

    # Coupon Class Description and Coupon Class differ 18 times. Former could be more correct, but contains 1 NaN.
    is_fixed = dataframe['Coupon Class Description'].fillna(
        dataframe['Current Coupon Class']).str.lower().str.contains('fixed')
    dictionary['Fixed-rate bond'] = round(
        sum(is_fixed) /
        len(dataframe.index), 2
    )
    dictionary['Fixed-rate bond Standard Deviation'] = round(dataframe[is_fixed].Coupon.astype(float).std(), 2)
    dictionary['Coupon (for fixed-rate bonds)'] = round(
        dataframe[is_fixed].Coupon.astype(float).mean(), 2)
    dictionary['Coupon (for fixed-rate bonds) Standard Deviation'] = round(
        dataframe[is_fixed].Coupon.astype(float).std(), 2)

    col = pd.DataFrame.from_dict(
        dictionary, orient='index', columns=[col_name])
    table4_columns.append(col)

# combine columns
table4 = pd.concat(table4_columns, axis=1)

# without at least 1 format(), formatting sucks
# table4.loc['Amount (in $M)'] = table4.loc['Amount (in $M)'].apply(
# '${0:,.2f}'.format)
# table4.loc['Amount (in $M) Standard Deviation'] = table4.loc['Amount (in $M) Standard Deviation'].apply(
#    '{0:,.2f}'.format)


# Compare Tables
with pd.ExcelWriter(r'Results\Table1.xlsx') as writer:
    table1.to_excel(writer, sheet_name='MyTable1')
    FLAMMER_TABLE1.to_excel(writer, sheet_name='FlammerTable1')
    (table1 - FLAMMER_TABLE1).to_excel(writer, sheet_name='Differences')

table2.to_excel(r'Results\Table2.xlsx')
# get sum of rows not in flammer_table_3
others_bonds, others_amount = table3[~table3.index.isin(FLAMMER_TABLE3.index)].sum()

# table3 with same rows of FLAMMER_TABLE3
comparable_table3 = table3[table3.index.isin(FLAMMER_TABLE3.index)].append(pd.DataFrame({
    '# Bonds': others_bonds, '$ Amount (billion)': others_amount},
    index=['Others']))

with pd.ExcelWriter(r'Results\Table3.xlsx') as writer:
    table3.to_excel(writer, sheet_name='MyTable3')
    comparable_table3.to_excel(writer, sheet_name='MyTable3SameIndex')
    FLAMMER_TABLE3.to_excel(writer, sheet_name='FlammerTable3')
    (comparable_table3 - FLAMMER_TABLE3).reindex(FLAMMER_TABLE3.index).to_excel(writer, sheet_name='Differences')

with pd.ExcelWriter(r'Results\Table4.xlsx') as writer:
    table4['Index'] = table4.index
    table4.to_excel(writer, sheet_name='MyTable4', index=False)
    worksheet = writer.sheets['MyTable4']  # pull worksheet object

    # format columns' width
    for idx, col in enumerate(table4):  # loop through all columns
        series = table4[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 1  # adding a little extra space
        try:
            worksheet.set_column(idx, idx, max_len)  # set column width
        except AttributeError:
            print('Please Install xlsxwriter to set columns width')
    FLAMMER_TABLE4.to_excel(writer, sheet_name='FlammerTable4')
    (table4 - FLAMMER_TABLE4).loc[FLAMMER_TABLE4.index].to_excel(writer, sheet_name='Differences')

print("TABLES SAVED\nSTARTING CAR ANALYSIS\n")

df['First Announcement Date'] = pd.to_datetime(df['First Announcement Date'].fillna(
    # fillna needs strings not dates
    df['Issue Date']))

stocks_prices = pd.read_csv(r'Dataset\StockPrices.csv', index_col='Date', parse_dates=['Date'])
indexes_prices = pd.read_csv(r'Dataset\IndexesPrices.csv', index_col='Date', parse_dates=['Date'])

# remove Timezone to avoid errors
for table in (indexes_prices, stocks_prices):
    table.index = table.index.tz_localize(None)

parent_to_index = dict(zip(df['Ultimate Parent Id'], df['Parent Index']))


def get_returns(price_series: pd.DataFrame, logarithm=True) -> pd.DataFrame:
    if not logarithm:
        returns_df = price_series / price_series.shift(1) - 1
    else:
        returns_df = 100 * np.log(price_series / price_series.shift(1))
    return returns_df.dropna()


def get_df_interval(df: pd.DataFrame, index_i_value, starting, ending) -> pd.DataFrame:
    """
    Return [starting, ending] rows of df around announcement_date value in index. len(df) = starting-ending+1
    :param df:
    :param index_i_value: must be in index.
    :param starting:
    :param ending:
    :return:
    """
    df = df.dropna()
    if len(df.index) > 0:
        position = df.index.get_loc(index_i_value, method='bfill')
        # if negative starting index or too high index:
        if position + starting < 0 or position + ending + 1 > len(df.index):
            raise IndexError("Out of Bounds")
        else:
            df = df.iloc[position + starting: position + ending + 1]
    return df


# copy() otherwise sort df too and get a warning
parent_public = df[df['IsParentPublic'] == True].copy()
parent_public.sort_values('First Announcement Date', ascending=False, inplace=True)

issuer_days = tuple(zip(parent_public['Ultimate Parent Id'], parent_public['First Announcement Date']))
issuer_days = list(OrderedDict.fromkeys(issuer_days))  # remove duplicates & preserve order

print(len(issuer_days), "UNIQUE ISSUER-DAYS FOUND\n")

event_results = {interval: list() for interval in INTERVALS}
first_time_issuers = list()
event_results_first_time_issuers = {interval: list() for interval in INTERVALS}
event_results_second_time_issuers = {interval: list() for interval in INTERVALS}

print("\nCAR Analysis over", len(issuer_days),  "Issuer-Days")
for identity, announcement_date in tqdm(issuer_days):
    if identity in stocks_prices.columns:
        index_name: str = parent_to_index[identity]  # corresponging index
        df_index_timeseries: pd.DataFrame = indexes_prices[[index_name]].dropna()  # index timeseries
        df_stock_timeseries: pd.DataFrame = stocks_prices[[identity]].dropna()  # stock timeseries
        try:
            df_index_timeseries = get_df_interval(df_index_timeseries, announcement_date, -220, -21)
            df_stock_timeseries = get_df_interval(df_stock_timeseries, announcement_date, -220, -21)
            if len(df_stock_timeseries) < 200:
                raise IndexError
        except IndexError:
            continue  # g to next identity, announcement_date
        if len(df_index_timeseries) != 200:
            raise ValueError('NOT ENOUGH INDEX DATA:', index_name)

        # merge df
        daily_data = pd.DataFrame()
        daily_data[identity] = df_stock_timeseries[identity].values
        daily_data[index_name] = df_index_timeseries[index_name].values

        daily_returns = get_returns(daily_data)

        model = LinearRegression()
        model.fit(X=daily_returns[[index_name]], y=daily_returns[[identity]])
        # print(model.coef_, model.intercept_)

        for starting_interval, ending_interval in INTERVALS:
            try:
                estimated_returns = model.predict(
                    get_returns(
                        get_df_interval(indexes_prices[[index_name]], announcement_date, starting_interval,
                                        ending_interval)
                    )
                )
                real_returns = get_returns(
                    get_df_interval(stocks_prices[[identity]], announcement_date, starting_interval,
                                    ending_interval))
                # car = sum(real_returns.values - estimated_returns)[0]
                car = np.sum(real_returns.values - estimated_returns)
                event_results[(starting_interval, ending_interval)].append(car)
                if identity not in first_time_issuers:
                    # event_results_first_time_issuers[(starting_interval, ending_interval)].append(car[0])
                    event_results_first_time_issuers[(starting_interval, ending_interval)].append(car)
                else:
                    # event_results_second_time_issuers[(starting_interval, ending_interval)].append(car[0])
                    event_results_second_time_issuers[(starting_interval, ending_interval)].append(car)
            except IndexError:
                pass

        if identity not in first_time_issuers:
            first_time_issuers.append(identity)
    else:
        print("NO STOCK DATA FOR:", identity)

mytable6 = create_tables.get_table6(event_results, INTERVALS)

with pd.ExcelWriter(r'Results\Table6.xlsx') as writer:
    mytable6.to_excel(writer, sheet_name='MyTable6')
    writer.sheets['MyTable6'].write_string('A8', 'N = ' + str(len(event_results[INTERVALS[0]])))

    FLAMMER_TABLE6.to_excel(writer, sheet_name='FlammerTable6')
    writer.sheets['FlammerTable6'].write_string('A8', 'N = 384')

    for table in (mytable6, FLAMMER_TABLE6):
        table['CAR'] = [el.replace('**', '') for el in table['CAR']]
        table['CAR'] = table.CAR.astype(float)
    (mytable6 - FLAMMER_TABLE6).to_excel(writer, sheet_name='Differences')

    for sheet_name, dictionary in {'First Time Issuers': event_results_first_time_issuers,
                                   'Second Time Issuers': event_results_second_time_issuers}.items():
        create_tables.get_table6(dictionary, INTERVALS).to_excel(writer, sheet_name=sheet_name)
        writer.sheets[sheet_name].write_string('A8', 'N = ' + str(len(dictionary[INTERVALS[0]])))

        winsorized_sheet_name = sheet_name+' Winsorized'
        create_tables.get_table6(dictionary, INTERVALS, winsorize=True).to_excel(
            writer, sheet_name=winsorized_sheet_name)
        writer.sheets[winsorized_sheet_name].write_string('A8', 'N = ' + str(len(dictionary[INTERVALS[0]])))

input('\nRESULTS saved in Results folder')
