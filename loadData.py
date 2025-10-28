import requests
import json
from tqdm import tqdm  # optional but nice for progress display
import matplotlib.patches as patches
import matplotlib.pyplot as plt


def build_tracking_list(url):
    all_frames = []

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        print("Streaming data from:", url)

        for line in tqdm(r.iter_lines(), unit="frame"):
            if not line:
                continue
            frame_data = json.loads(line.decode("utf-8"))

            # Skip invalid periods
            if frame_data.get("period") is None:
                continue

            # Extract ball data
            ball_data = frame_data.get("ball_data", {})
            ball = {
                "x": ball_data.get("x"),
                "y": ball_data.get("y"),
                "z": ball_data.get("z"),
                "is_detected": ball_data.get("is_detected"),
            }

            # Extract player data
            players = []
            for p in frame_data.get("player_data", []):
                players.append({
                    "id": p.get("id"),
                    "team": p.get("team_id"),
                    "x": p.get("x"),
                    "y": p.get("y"),
                    "z": p.get("z"),
                    "speed": p.get("speed"),
                    "orientation": p.get("orientation")
                })

            # Combine everything for this frame
            frame_entry = {
                "frame": frame_data.get("frame"),
                "timestamp": frame_data.get("timestamp"),
                "period": frame_data.get("period"),
                "ball": ball,
                "players": players
            }

            all_frames.append(frame_entry)

    return all_frames
