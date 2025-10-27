import pandas as pd

url = "https://raw.githubusercontent.com/SkillCorner/opendata/refs/heads/master/data/matches/2015213/2015213_phases_of_play.csv"
df = pd.read_csv(url)

print(df.head())
