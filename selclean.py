import pandas as pd

df_cupsdata = pd.read_csv('fifacupsdata.csv')

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]
#df_cupsdata[df_cupsdata['away'].isnull()]
df_cupsdata.rename(columns={'home':'HomeTeam', 'away':'AwayTeam', 'year':'Year'}, inplace=True)
#print(df_cupsdata.dtypes)
#df_cupsdata = df_cupsdata.astype({'Home'})
df_cupsdata['HomeTeam'] = df_cupsdata['HomeTeam'].str.strip()
df_cupsdata['AwayTeam'] = df_cupsdata['AwayTeam'].str.strip()

delete_index = df_cupsdata[df_cupsdata['HomeTeam'].str.contains('Sweden') &
            df_cupsdata['AwayTeam'].str.contains('Austria')].index
df_cupsdata.drop(index = delete_index, inplace=True)


df_cupsdata['score'] = df_cupsdata['score'].str.replace('[^\d–]', '', regex=True)
#print(df_cupsdata[df_cupsdata['score'].str.contains('[^\d–]')])
#print(df_cupsdata['score'].str.split('–'))
df_cupsdata[['HomeGoals', 'AwayGoals']] = df_cupsdata['score'].str.split('–', expand=True)
df_cupsdata.drop('score', axis=1, inplace=True)
df_cupsdata = df_cupsdata.astype({'HomeGoals': int, 'AwayGoals': int, 'Year': int})

# print(df_cupsdata.dtypes)

#verify matches colected each year
for year in years:
    print(year, len(df_cupsdata[df_cupsdata['Year']==year]))



away_nan_indexes = df_cupsdata[df_cupsdata['AwayTeam'].isnull()].index
print(away_nan_indexes)
# df_cupsdata.loc[away_nan_indexes[0], 'AwayTeam'] = 'Yugoslavia'
# df_cupsdata.loc[away_nan_indexes[1], 'AwayTeam'] = 'Dutch East Indies'
print(df_cupsdata[df_cupsdata['AwayTeam'].str.contains('Turkey')])