import pandas as pd
import pickle
from scipy.stats import poisson
from string import ascii_uppercase as alphabet
from copy import deepcopy

all_tables = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')

#print(all_tables[9])
#print(all_tables[16])
#print(all_tables[23])
dict_table = {}
for letter, i in zip(alphabet, range(9,65,7)): # 11 18 25
    df = all_tables[i]
    df.rename(columns={df.columns[1]:'Team'}, inplace=True)
    df.pop('Qualification')
    dict_table[f'Group {letter}'] = df
    dict_table[f'Group {letter}']['Pts'] = 0


with open('dict_table', 'wb') as output:
    pickle.dump(dict_table, output)
dict_table = pickle.load(open('dict_table', 'rb'))
#print(dict_table['Group H'])
df_historical_data = pd.read_csv('clean_fifacupsdata.csv')
df_fixture = pd.read_csv('clean_2022fixture2.csv')

print(df_fixture)


# calculo team strength

df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]

df_home = df_home.rename(columns={'HomeTeam': 'Team', 'HomeGoals':'ScoredGoals', 'AwayGoals':'ReceivedGoals'})
df_away = df_away.rename(columns={'AwayTeam': 'Team', 'HomeGoals':'ReceivedGoals', 'AwayGoals':'ScoredGoals'})
team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby('Team').mean()
def predict_points(home, away):
    if home in team_strength.index and away in team_strength.index:
        lamb_home = team_strength.at[home,'ScoredGoals'] * team_strength.at[away,'ReceivedGoals']
        lamb_away = team_strength.at[away, 'ScoredGoals'] * team_strength.at[home, 'ReceivedGoals']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0,11):
            for y in range(0,11):
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y, lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p

        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw
        return(points_home, points_away)
    else:
        return(0,0)

# print(predict_points('Argentina', 'Mexico'))
df_fixture_group = df_fixture[:48].copy()
df_fixture_knockout = df_fixture[48:56].copy()
df_fixture_quarter = df_fixture[56:60].copy()
df_fixture_semi = df_fixture[60:62].copy()
df_fixture_final = df_fixture[62:].copy()

print(df_fixture_group)
print(dict_table['Group A']['Team'].values)

print(dict_table)

for group in dict_table:
    teams_in_group = dict_table[group]['Team'].values
    df_fixture_group_6 = df_fixture_group[df_fixture_group['HomeTeam'].isin(teams_in_group)]
    for index, row in df_fixture_group_6.iterrows():
        home, away = row['HomeTeam'], row['AwayTeam']
        points_home, points_away = predict_points(home, away)

        # sumamos los puntos correspondientes a cada eqiupo
        dict_table[group].loc[dict_table[group]['Team'] == home, 'Pts'] += points_home
        dict_table[group].loc[dict_table[group]['Team'] == away, 'Pts'] += points_away

    dict_table[group] = dict_table[group].sort_values('Pts', ascending=False).reset_index()
    dict_table[group] = dict_table[group][['Team', 'Pts']]
    dict_table[group] = dict_table[group].round(0)
print(df_fixture_knockout)
for group in dict_table:
    group_winner = dict_table[group].loc[0,'Team']
    runner_up = dict_table[group].loc[1, 'Team']
    df_fixture_knockout.replace({f'Winners {group}': group_winner,
                                f'Runners-up {group}': runner_up}, inplace=True)
df_fixture_knockout['Winner'] = '?'
print(df_fixture_knockout)
def get_winner(df_fixture_updated):
    for index, row in df_fixture_updated.iterrows():
        home, away = row['HomeTeam'], row['AwayTeam']
        points_home, points_away = predict_points(home, away)
        if points_home > points_away:
            winner = home
        else:
            winner = away
        df_fixture_updated.loc[index, 'winner'] = winner
    return df_fixture_updated
print(get_winner(df_fixture_knockout))

def update_table(df_fixture_round1, df_fixture_round2):
    for index, row in df_fixture_round1.iterrows():
        winner = df_fixture_round1.loc[index, 'winner']
        match = df_fixture_round1.loc[index, 'score']
        df_fixture_round2.replace({f'Winners {match}': winner}, inplace=True)
    df_fixture_round2['winner'] = '?'
    return df_fixture_round2
print(update_table(df_fixture_knockout, df_fixture_quarter))
print(get_winner(df_fixture_quarter))
update_table(df_fixture_quarter, df_fixture_semi)
print(get_winner(df_fixture_semi))
update_table(df_fixture_semi, df_fixture_final)
print(get_winner(df_fixture_final))