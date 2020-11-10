"""
flammer tables 1, 3, 4
Usage:
from flammer_tables import flammer_tables
FLAMMER_TABLE1, FLAMMER_TABLE3, FLAMMER_TABLE4 = flammer_tables
"""
import pandas as pd


INTERVALS = (
    (-20, -11),
    (-10, -6),
    (-5, 10),
    (11, 20),
    (21, 60)
)

# table1
flammer_table1 = pd.DataFrame({
    'Year': range(2013, 2019),
    '# Bonds': [16, 76, 222, 156, 323, 396],
    '$ Amount (billion)': [5.0, 15.4, 28.7, 68.7, 87.8, 95.7]
})
flammer_table1.set_index('Year', inplace=True)

# table3
flammer_table3_countries = ['China',
                            'Netherlands',
                            'United States',
                            'France',
                            'Germany',
                            'Mexico',
                            'Sweden',
                            'United Kingdom',
                            'Luxembourg',
                            'Spain',
                            'Hong Kong',
                            'Japan',
                            'Australia',
                            'Italy',
                            'Norway',
                            'India',
                            'Brazil',
                            'Canada',
                            'Denmark',
                            'Austria',
                            'South Korea',
                            'United Arab Emirates',
                            'Taiwan',
                            'Singapore',
                            'Others']

flammer_table3 = pd.DataFrame({
    'Country': flammer_table3_countries,
    '# Bonds': [190, 46, 194, 157, 57, 9, 140, 25, 20, 17, 31, 37, 15, 10, 20, 17, 6, 10, 4, 5, 5, 3, 21, 10, 140],
    '$ Amount (billion)': [75.1, 33.2, 31.5, 30.8, 19.4, 12.2, 11.6, 10.8, 8.9, 7.6, 7.4, 6.7, 5.4, 4.6, 4.4, 4.2,
                           3.4, 3.4, 2.1, 1.7, 1.7, 1.6, 1.6, 1.2, 10.9]
})
flammer_table3.set_index('Country', inplace=True)

# table 4
flammer_table4_index = ['# Green bonds', '# Green bond issuer-days',
                        '# Green bond issuer-years',
                        '# Green bond issuers',
                        'Amount (in $M)',
                        'Amount (in $M) Standard Deviation',
                        'Certified (1/0)',
                        'Certified (1/0) Standard Deviation',
                        'Maturity (years)', 'Maturity (years) Standard Deviation',
                        'Fixed-rate bond', 'Fixed-rate bond Standard Deviation',
                        'Coupon (for fixed-rate bonds)',
                        'Coupon (for fixed-rate bonds) Standard Deviation',
                        'S&P rating (median)',
                        'Moodyʼs rating (median)',
                        'Bloombergʼs composite rating (median)']

flammer_table4 = pd.DataFrame({'All': [1189, 775, 526, 400, 253.4, 421.0, 0.656, 0.475, 7.7, 29.5, 0.753, 0.432,
                                       0.037, 0.022, 'A',
                                       'A3', 'A'],
                               'Private': [624, 391, 301, 231, 245.5, 329.5, 0.684, 0.465, 7.4, 5.5, 0.732, 0.443,
                                           0.038, 0.022, 'BBB+',
                                           'A3', 'BBB+'],
                               'Public': [565, 384, 225, 169, 262, 503.3, 0.625, 0.485, 8.1, 42.3, 0.775, 0.418, 0.036,
                                          0.022, 'A',
                                          'A2', 'A']},
                              index=flammer_table4_index
                              )

flammer_table6 = pd.DataFrame({'Event time': ['[-20, -11]',
                                              '[-10, -6]',
                                              '[-5, 10]',
                                              '[11, 20]',
                                              '[21, 60]'],
                               'CAR': ['-0.129', '0.051', '0.489**', '-0.029', '-0.122'],
                               'Std. Err.': [0.157, 0.245, 0.241, 0.218, 0.645]}).set_index('Event time')

flammer_tables = (flammer_table1, flammer_table3, flammer_table4, flammer_table6)
