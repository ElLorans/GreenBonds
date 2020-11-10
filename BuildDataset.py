#%%
import datetime as dt
import os

import eikon as ek
import numpy as np
import pandas as pd
from utilities import get_eikon_key, filter_dataset, country_to_index, rearrange


KEY = get_eikon_key.get_eikon_key()

try:
    ek.set_app_key(KEY)
    bonds, err = ek.get_data(['CN151819SH='], 'TR.FirstAnnounceDate')
    # sanity check to prevent silent error
    sanity_check = bonds['First Announcement Date'][0]
    if sanity_check != '2019-07-11':
        raise ValueError(f'Sanity check not passed: {sanity_check}')
except ek.EikonError:
    raise ValueError('Please check key.secret, then run Eikon Desktop or Eikon API Proxy')

# green_bonds = pd.read_json(r'utilities\eikon_data.json', convert_dates=['Issue Date']
green_bonds = pd.read_excel(r'utilities\db.xlsx').replace(
    '--', np.nan).replace('China (Mainland)', 'China')
green_bonds = filter_dataset.filter_dataset(green_bonds)

ADDITIONAL_COLUMNS = [
    'TR.FirstAnnounceDate',
    'TR.IssuerRating',
    'TR.IsPublic',
    'TR.FiParentLongName',
    'TR.UltimateParentID',
    'TR.FiCouponClassDescription'
]

# Moodys Rating has WR for non-active bonds, so only Issuer Rating is relevant
print("\nDOWNLOADING DATASET\n")
bonds, bonds_err = ek.get_data(green_bonds.ISIN.dropna().to_list(),
                               ADDITIONAL_COLUMNS)

isin_merged = green_bonds.merge(right=bonds, how='outer', left_on='ISIN',
                                right_on='Instrument')

# get RICs from where we don't have ISIN
# isin_merged.index == green_bonds.reset_index().index, so directly use isin_merged.index
rics = isin_merged[isin_merged.ISIN.isna()]['Preferred RIC'].dropna()
rics_index = rics.index
rics = rics.to_list()

missing_bonds, errors = ek.get_data(rics,
                                    ADDITIONAL_COLUMNS)
# set index for fillna
missing_bonds.index = rics_index
# updating entire isin_merged gives error
for col in missing_bonds:
    isin_merged[col].fillna(missing_bonds[col], inplace=True)

isin_merged.rename(columns={'Organization Is Public Flag': 'IsPublic'}, inplace=True)

#%%
# GET IsParentPublic
print("\nDOWNLOADING IsParentPublic\n")
parents, err = ek.get_data(list(isin_merged['Ultimate Parent Id'].dropna().unique().astype(str)),
                           ['TR.IsPublic'])

parents.rename(columns={'Organization Is Public Flag': 'IsParentPublic'}, inplace=True)
isin_merged['IsParentPublic'] = isin_merged['Ultimate Parent Id'].map(
    dict(zip(parents.Instrument, parents.IsParentPublic)))

for col in ('IsParentPublic', 'IsPublic'):
    isin_merged[col] = isin_merged[col].map({'True': True, 'False': False})

# fill empty First Announcement Date with Issue Date
isin_merged['First Announcement Date'] = pd.to_datetime(isin_merged['First Announcement Date'].fillna(
    # fillna needs strings not dates
    isin_merged['Issue Date'].dt.strftime('%Y-%m-%d')))

# add Stock Index for Parent
isin_merged['Parent Index'] = isin_merged['Country of Incorporation'].map(
    country_to_index.country_to_index)

# Save Dataset
try:
    isin_merged.to_csv(r'Dataset\cleaned_green_bonds.csv', index=False)
except FileNotFoundError:
    os.mkdir('Dataset')
    isin_merged.to_csv(r'Dataset\cleaned_green_bonds.csv', index=False)

print("\nDATASET saved.\n")

# Get Stock Data
public_df = isin_merged[(isin_merged['IsPublic'] == True) | (isin_merged['IsParentPublic'] == True)]

min_date = public_df['First Announcement Date'].min()
max_date = public_df['First Announcement Date'].max()

starting_date = str((min_date - dt.timedelta(280)).date())
ending_date = str((max_date + dt.timedelta(80)).date())

#%%
# ClosePrice gives different results from PriceClose...
# see https://community.developers.refinitiv.com/questions/57842/get-data-inconsistent-between-an-index-and-a-singl.html
# ClosePrice appears to be superior as it incorporates specific calendar holidays
print("\nDOWNLOADING STOCK DATA\n")
list_of_identities = list(public_df['Ultimate Parent Id'].unique().astype(str))

# due to timing limits, split in 2 batches
stock_prices, err = ek.get_data(
    list_of_identities[:150],
    ['TR.ClosePrice.date', 'TR.ClosePrice'],
    {'SDate': starting_date,
     'EDate': ending_date})

print('50% Stock Data Downloaded')
#%%
stock_prices2, err2 = ek.get_data(
    list_of_identities[150:],
    ['TR.ClosePrice.date', 'TR.ClosePrice'],
    {'SDate': starting_date,
     'EDate': ending_date})

print('100% Stock Data Downloaded\n')

complete_stock_prices = pd.concat((stock_prices, stock_prices2))
#%%
# transform to get a different column for each Instrument
complete_stock_prices = rearrange.rearrange(complete_stock_prices)
complete_stock_prices.to_csv(r'Dataset\StockPrices.csv')

# Get Indexes Data
country_indexes = list(set(country_to_index.country_to_index.values()))

print("\nDOWNLOADING INDEXES DATA\n")

indexes, indexes_err = ek.get_data(
    country_indexes,
    ['TR.ClosePrice.date', 'TR.ClosePrice'],
    {'SDate': starting_date,
     'EDate': ending_date})

# transform to get a different column for each Instrument
indexes_prices = rearrange.rearrange(indexes)
indexes_prices.to_csv(r'Dataset\IndexesPrices.csv')

print("\nDATASET BUILT\n")
