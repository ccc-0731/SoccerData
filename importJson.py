import requests

url = "https://raw.githubusercontent.com/username/soccer-tracking/main/data/match_001_tracking_extrapolated.jsonl"
filename = "tracking_extrapolated.jsonl"

with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("✅ File downloaded locally as", filename)
