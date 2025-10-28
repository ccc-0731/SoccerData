import requests
import json
import pandas as pd
from tqdm import tqdm  # shows progress bar, optional but nice

matchID = 2015213
url = "https://media.githubusercontent.com/media/SkillCorner/opendata/master/data/matches/2015213/2015213_tracking_extrapolated.jsonl"

def load_tracking_data(url):

    # Stream and flatten soccer tracking data from JSONL format.
    # Handles keys: frame, timestamp, period, ball_data, player_data

    frames = []

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        print("Streaming data from:", url)
        for i, line in enumerate(tqdm(r.iter_lines(), unit="frame")):
            if not line:
                continue
            frame_data = json.loads(line.decode("utf-8"))

            frame_id = frame_data.get("frame")
            timestamp = frame_data.get("timestamp")
            period = frame_data.get("period")

            if period is not None: # only process valid periods
                # Ball data
                ball = frame_data.get("ball_data", {})
                frames.append({
                    "frame": frame_id,
                    "timestamp": timestamp,
                    "period": period,
                    "object": "ball",
                    "player_id": None,
                    "x": ball.get("x"),
                    "y": ball.get("y"),
                    "z": ball.get("z"),
                    "is_detected": ball.get("is_detected")
                })

                # Player data
                for p in frame_data.get("player_data", []):
                    frames.append({
                        "frame": frame_id,
                        "timestamp": timestamp,
                        "period": period,
                        "object": "player",
                        "player_id": p.get("id"),
                        "x": p.get("x"),
                        "y": p.get("y"),
                        "z": p.get("z"),
                        "team": p.get("team_id"),
                        "speed": p.get("speed"),
                        "orientation": p.get("orientation")
                    })

    df = pd.DataFrame(frames)
    return df

def get_frames(url):
    frames = []

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        print("Streaming data from:", url)

        for i, line in enumerate(tqdm(r.iter_lines(), unit="frame")):
            if not line:
                continue
            frame_data = json.loads(line.decode("utf-8"))

            frame_id = frame_data.get("frame")
            frames.append({"frame": frame_id})
    df = pd.DataFrame(frames)
    return df

def get_object_data(object, url):

    frames = []
    p = object

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        print("Streaming data from:", url)

        for i, line in enumerate(tqdm(r.iter_lines(), unit="frame")):
            if not line:
                continue

            frame_data = json.loads(line.decode("utf-8"))

            frame_id = frame_data.get("frame")
            timestamp = frame_data.get("timestamp")
            period = frame_data.get("period")

            if period is not None: # only process valid periods
                frames.append({
                    "frame": frame_id,
                    "timestamp": timestamp,
                    "period": period,
                    "object": "player",
                    "player_id": p.get("id"),
                    "x": p.get("x"),
                    "y": p.get("y"),
                    "z": p.get("z"),
                    "team": p.get("team_id"),
                    "speed": p.get("speed"),
                    "orientation": p.get("orientation")
                })


# Example usage
df = load_tracking_data(url)
print("✅ Loaded DataFrame shape:", df.shape)

print(df["frame"].head(50))
ballData = get_frames(url)
for i in range(50):
    print(ballData.at[i, "frame"])
