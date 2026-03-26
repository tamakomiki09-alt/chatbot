import pandas as pd
import os

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "whl_2025.csv")

df = pd.read_csv(file_path)
print(df.head())

teams = df['home_team'].unique()
elo_ratings = {team: 1500 for team in teams}

K = 32 

def get_expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

game_results = df.groupby('game_id').agg({
    'home_team': 'first',
    'away_team': 'first',
    'home_goals': 'sum',
    'away_goals': 'sum'
}).reset_index()

for index, row in game_results.iterrows():
    home = row['home_team']
    away = row['away_team']
    
    
    actual_home_score = 1 if row['home_goals'] > row['away_goals'] else 0
    if row['home_goals'] == row['away_goals']: actual_home_score = 0.5 
    
    expected_home_score = get_expected_score(elo_ratings[home], elo_ratings[away])
    
    shift = K * (actual_home_score - expected_home_score)
    elo_ratings[home] += shift
    elo_ratings[away] -= shift

rankings = sorted(elo_ratings.items(), key=lambda x: x[1], reverse=True)
print("My Practice Power Rankings:")
for i, (team, score) in enumerate(rankings, 1):
    print(f"{i}. {team}: {round(score)}")

import matplotlib.pyplot as plt

# Convert rankings to lists
teams = [team for team, score in rankings]
scores = [score for team, score in rankings]

# Create bar chart
plt.figure(figsize=(10,6))
plt.bar(teams, scores)

# Labels and title
plt.xlabel("Teams")
plt.ylabel("Elo Rating")
plt.title("Hockey Team Power Rankings (Elo Model)")

# Rotate team names so they fit
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()