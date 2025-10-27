import pandas as pd
import json

url1 = "https://raw.githubusercontent.com/SkillCorner/opendata/refs/heads/master/data/matches/2015213/2015213_phases_of_play.csv"
phasesOfPlay = pd.read_csv(url1)

url2 = "https://raw.githubusercontent.com/SkillCorner/opendata/refs/heads/master/data/matches/2015213/2015213_dynamic_events.csv"
dynamicEvents = pd.read_csv(url2)

print(phasesOfPlay.describe())
print(dynamicEvents.describe())
# test fesafses



