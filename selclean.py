import pandas as pd

cupsdata = pd.read_csv('fifacupsdata.csv')
years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]
#df_cupsdata[df_cupsdata['away'].isnull()]

def clean(df_cupsdata):
    df = df_cupsdata.rename(columns={'home':'HomeTeam', 'away':'AwayTeam', 'year':'Year'})
    #print(df_cupsdata.dtypes)
    #df_cupsdata = df_cupsdata.astype({'Home'})
    df['HomeTeam'] = df['HomeTeam'].str.strip()
    df['AwayTeam'] = df['AwayTeam'].str.strip()

    delete_index = df[df['HomeTeam'].str.contains('Sweden') &
                df['AwayTeam'].str.contains('Austria')].index
    df.drop(index = delete_index, inplace=True)

    df['score'] = df['score'].str.replace('[^\d–]', '', regex=True)
    #print(df_cupsdata[df_cupsdata['score'].str.contains('[^\d–]')])
    #print(df_cupsdata['score'].str.split('–'))

    df[['HomeGoals', 'AwayGoals']] = df['score'].str.split('–', expand=True)
    df.drop('score', axis=1, inplace=True)
    df = df.astype({'HomeGoals': int, 'AwayGoals': int, 'Year': int})
    return df


def clean2(df_cupsdata):
    df = df_cupsdata.rename(columns={'home': 'HomeTeam', 'away': 'AwayTeam', 'year': 'Year'})
    # print(df_cupsdata.dtypes)
    # df_cupsdata = df_cupsdata.astype({'Home'})
    df['HomeTeam'] = df['HomeTeam'].str.strip()
    df['AwayTeam'] = df['AwayTeam'].str.strip()


    df = df.astype({'Year': int})
    return df

#    for year in years:
#        print(year, len(cupsdata[cupsdata['Year']==year]))
# print(df_cupsdata.dtypes)

cupsdata = clean(cupsdata)
#verify matches colected each year
for year in years:
    print(year, len(cupsdata[cupsdata['Year']==year]))


# 2022 Fixture

fixture2022 = pd.read_csv('2022fixture.csv')
fixture2022 = clean(fixture2022)
print(fixture2022)

fixture2022_2 = pd.read_csv('2022fixture2.csv')
fixture2022_2 = clean2(fixture2022_2)
print(fixture2022_2)

#away_nan_indexes = df_cupsdata[df_cupsdata['AwayTeam'].isnull()].index
#print(away_nan_indexes)
# df_cupsdata.loc[away_nan_indexes[0], 'AwayTeam'] = 'Yugoslavia'
# df_cupsdata.loc[away_nan_indexes[1], 'AwayTeam'] = 'Dutch East Indies'
print(cupsdata[cupsdata['AwayTeam'].str.contains('Turkey')])
cupsdata.to_csv('clean_fifacupsdata.csv', index=False)
fixture2022.to_csv('clean_2022fixture.csv', index=False)
fixture2022_2.to_csv('clean_2022fixture2.csv', index=False)