# Install dependencies if needed:
# pip install nba_api pandas matplotlib seaborn

from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# -------------------------
# STEP 1: Load Game Data
# -------------------------
print("Fetching game data from nba_api...")

gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable='2023-24')
games = gamefinder.get_data_frames()[0]

print(f"Total games fetched: {len(games)}")

# -------------------------
# STEP 2: Clean & Process
# -------------------------
# Convert date to datetime
games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])

# Add win/loss numeric column
games['WIN'] = games['WL'].apply(lambda x: 1 if x == 'W' else 0)

# Extract month (e.g., 2023-11, 2023-12)
games['MONTH'] = games['GAME_DATE'].dt.to_period('M')

# Group by TEAM + MONTH to get win rates
win_rates = games.groupby(['TEAM_NAME', 'MONTH'])['WIN'].mean().reset_index()
win_rates['MONTH'] = win_rates['MONTH'].astype(str)  # for plotting

# -------------------------
# STEP 3: Plotting
# -------------------------
# Select teams to compare
selected_teams = ['Golden State Warriors', 'Los Angeles Lakers', 'Boston Celtics']

# Filter the data
subset = win_rates[win_rates['TEAM_NAME'].isin(selected_teams)]

# Plotting
plt.figure(figsize=(14, 7))
sns.lineplot(data=subset, x='MONTH', y='WIN', hue='TEAM_NAME', marker='o')

plt.title("NBA Team Win Rate Over Time (2023–24 Season)", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Win Rate")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Team', loc='upper right')
plt.tight_layout()

# Show the plot
plt.show()
