from flask import Flask, render_template, jsonify, request
import pandas as pd
from importJson import load_tracking_data

app = Flask(__name__)

# Load your dataframe once (so it’s ready)
matchID = 2015213
url = "https://media.githubusercontent.com/media/SkillCorner/opendata/master/data/matches/2015213/2015213_tracking_extrapolated.jsonl"

df = load_tracking_data(url)

# ---------------------------------------------------------
# 2️⃣ Homepage route — serves index.html (the frontend)
# ---------------------------------------------------------
@app.route("/")
def index():
    # Flask will look inside the "templates" folder for this file
    return render_template("index.html")

# ---------------------------------------------------------
# 3️⃣ API route — returns tracking data for a specific frame
# ---------------------------------------------------------
@app.route("/frame/<int:frame_id>")
def get_frame(frame_id):
    # When the frontend slider requests a frame number,
    # this function finds that frame's data in df and sends it as JSON.
    
    # Filter rows in df where frame == frame_id
    frame_data = df[df["frame"] == frame_id]

    # Convert the DataFrame slice into a JSON-friendly format
    return jsonify(frame_data.to_dict(orient="records"))

# ---------------------------------------------------------
# 4️⃣ Run the app
# ---------------------------------------------------------
if __name__ == "__main__":
    # debug=True means Flask will auto-reload when you save code changes
    app.run(debug=True)