import requests
import json
from tqdm import tqdm  # optional but nice for progress display
import matplotlib.patches as patches
import matplotlib.pyplot as plt


url = "https://media.githubusercontent.com/media/SkillCorner/opendata/master/data/matches/2015213/2015213_tracking_extrapolated.jsonl"

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


# Example usage:
tracking_list = build_tracking_list(url)

# Print example of the first frame
import pprint
pprint.pp(tracking_list[0])
print(f"\n✅ Total frames loaded: {len(tracking_list)}")

def perFrame(frame, data):
    return tracking_list[frame]

def make_graph(frame_index, tracking_list):

    fig, ax = plt.subplots(figsize=(10, 6.5))
    
    x_min, x_max = -52.5, 52.5
    y_min, y_max = -34, 34

    # Draw outer border (field boundary)
    field_outline = patches.Rectangle(
        (x_min, y_min), x_max - x_min, y_max - y_min,
        linewidth=2, edgecolor='black', facecolor='green', alpha=0.15
    )
    ax.add_patch(field_outline)

    # Center line
    ax.plot([0, 0], [y_min, y_max], color='white', linewidth=2)

    # Center circle
    center_circle = patches.Circle((0, 0), 9.15, fill=False, color='white', linewidth=2)
    ax.add_patch(center_circle)

    # Center spot
    ax.plot(0, 0, 'wo', markersize=4)

    # Penalty boxes
    # Left penalty box
    ax.add_patch(patches.Rectangle((-52.5, -20.15), 16.5, 40.3, fill=False, color='white', linewidth=2))
    # Right penalty box
    ax.add_patch(patches.Rectangle((52.5 - 16.5, -20.15), 16.5, 40.3, fill=False, color='white', linewidth=2))

    # Goal boxes
    ax.add_patch(patches.Rectangle((-52.5, -7.32), 5.5, 14.64, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((52.5 - 5.5, -7.32), 5.5, 14.64, fill=False, color='white', linewidth=2))

    # Goals (optional)
    ax.add_patch(patches.Rectangle((-52.5 - 2, -3.66), 2, 7.32, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((52.5, -3.66), 2, 7.32, fill=False, color='white', linewidth=2))

    # Penalty spots
    ax.plot(-52.5 + 11, 0, 'wo', markersize=4)
    ax.plot(52.5 - 11, 0, 'wo', markersize=4)

    # Arcs at top of penalty boxes
    left_arc = patches.Arc((-52.5 + 11, 0), 18.3, 18.3, angle=0, theta1=308, theta2=52, color='white', linewidth=2)
    right_arc = patches.Arc((52.5 - 11, 0), 18.3, 18.3, angle=0, theta1=128, theta2=232, color='white', linewidth=2)
    ax.add_patch(left_arc)
    ax.add_patch(right_arc)

    frame = tracking_list[frame_index]

    x = []
    x.append(frame['ball']['x'])
    for i in range(len(frame['players'])):
        x.append(frame['players'][i]['x'])
    y = []
    y.append(frame['ball']['y'])
    for i in range(len(frame['players'])):
        y.append(frame['players'][i]['y'])

    # Plot all points except the first
    plt.scatter(x[1:], y[1:], color='blue', label='Players')

    # Plot the first point in a different color
    plt.scatter(x[0], y[0], color='red', label='Ball', s=100)

    # Set custom x (domain) and y (range) limits
    plt.xlim(-52.5, 52.5)  # domain
    plt.ylim(-34, 34)      # range

    # Center the axes at (0, 0)
    ax = plt.gca()  # Get current axes
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # Hide the top and right spines
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(1.5)

    # Move ticks to bottom and left
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # Add labels, title, legend
    # Add labels and manually position them at the edges
    ax.set_xlabel('X values', labelpad=10)
    ax.set_ylabel('Y values', labelpad=10)
    ax.xaxis.set_label_coords(1, -0.05)   # right edge, vertically centered
    ax.yaxis.set_label_coords(-0.05, 1)   # top edge, horizontally centered
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('Field with Ball and Player Locations')
    plt.legend()
    plt.grid(True)

    # Show the plot
    return fig, ax


make_graph(0, tracking_list)
