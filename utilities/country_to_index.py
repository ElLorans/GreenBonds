country_to_index = {'Australia': '.AXJO', #S&P/ASX 200
                    'Austria': '.ATX',
                    'Belgium': '.BFX', # BEL20
                    'Bermuda': '.SPX', # ?????????
                    'Brazil': '.BVSP',
                    'British Virgin Islands': '.SPX', # ???????? 
                    'Canada': '.SPTSE', # S&P/TSX60
                    'Cayman Islands': '.SPX', # ???????
                    'Chile': '.SPIPSA', # S&P IPSA CLP
                    'China (Mainland)': '.SSEC', # SHANGHAI SE COMPOSITE INDEX
                    'China': '.SSEC', # SHANGHAI SE COMPOSITE INDEX
                    'Colombia': '.COLCAP', # Colombia Capitalization Index
                    'Denmark': '.OMXC20', # OMX Copenaghen 20 Index
                    'Finland': '.OMXH25', # OMX Helsinki 25 Index
                    'France': '.FCHI', # CAC40
                    'Germany': '.GDAXI', # Deutsche Borse DAX Index
                    'Greece': '.ATFMI', # FTSE/Athex Market Index
                    'Hong Kong': '.HSI', # Hang Seng Index
                    'India': '.BSESN', # S&P BSE Sensex Index
                    'Italy': '.FTMIB', # FTSE MIB Index
                    'Japan': '.N225E', # Nikkei 225 Index (.N225 has no data)
                    'Lithuania': '.OMXVGI', # OMX VILNIUS GI
                    'Luxembourg': '.LUXX', # Luxembourg Se LuxX Index
                    'Malaysia': '.KLSE', # FTSE Bursa Malaysia KLCI Index
                    'Mexico': '.MXX', # S&P/BMV Ipc
                    'Morocco': '.MASI', # Casablanca SE All Share Index
                    'Namibia': '.FTN098', # FTSE NSX Overall. Alternatives are FTSE NSX Local ...
                    'Netherlands': '.AEX', #Amsterdam Exchanges Index
                    'New Zealand': '.NZ50', #S&P NZX50
                    'Nigeria': '.NGSEINDEX', # Nigerian Stock Exchange All Share Index
                    'Norway': '.OBX', # Oslo Stock Exchange Equity Index
                    'Peru': '.SPBLPGPT', #S&P/BVL Peru General Index
                    'Philippines': '.PSI', # The Philippines Stock Exchange PSEi Index       
                    'Poland': '.WIG', # Warsaw SE WIG POLAND Index 
                    'Portugal': '.PSI20', # Euronext Lisbon PSI Index       
                    'Singapore': '.STI',      # Straits Times Index             
                    'South Africa': '.JTOPI', # FTSE/JSE SE TOP40 Index
                    'South Korea': '.KS11', # Korea SE KOSPI Index. Alternatives are (.KS200, .KS100, .KS50) for top 200, 100, 50
                    'Spain': '.IBEX', # IBEX 35 Index 
                    'Sweden': '.OMXS30', # OMX Stockholm 30 Index
                    'Switzerland': '.SSMI', # Swiss Market Index  
                    'Taiwan': '.TWII',            # TAIWAN SE WEIGHTED INDEX      
                    'Thailand': '.SETI', # SET Index
                    'Turkey': '.XU100', # BIST 100 INDEX
                    'United Arab Emirates': '.ADI', # Abu Dhabi Securities Exchange General (Main) Index 
                    'United Kingdom': '.FTSE', # .FTSE 100 Index
                    'United States': '.SPX', 
                    'Eurobond Market': '.STOXX' # STOXX Euro 600 Price Index
            }


#pivot_column = 'Country of Incorporation'

#country_count = pd.pivot_table(public_df[[pivot_column, 'Ticker']],
#               index=[pivot_column],
#               aggfunc='count')
#country_count
# for c in country_count['Ticker'].index:
#    if c not in country_to_index:
#        print(c)
#        in_same_country = public_df[public_df['Country of Incorporation'] == c]['Ultimate Parent Id'].unique()
#        print(indexes[indexes.Instrument.isin([int(x) for x in in_same_country])]['Index RIC'].unique())
