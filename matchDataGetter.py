import requests

# Define the URL
matchID = 2015213
url = f"https://raw.githubusercontent.com/SkillCorner/opendata/refs/heads/master/data/matches/{matchID}/{matchID}_tracking_extrapolated.jsonl"

# Make a GET request to fetch data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
# Parse and print JSON data
    data = response.json()
    print(data)
else:
    print(f"Error: Request failed with status code {response.status_code}")