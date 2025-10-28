from flask import Flask, render_template, jsonify, send_file
import pandas as pd
from loadData import build_tracking_list
from makeGraph import make_graph
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load your dataframe once (so it’s ready)
matchID = 2015213
url = "https://media.githubusercontent.com/media/SkillCorner/opendata/master/data/matches/2015213/2015213_tracking_extrapolated.jsonl"

tracking_list = build_tracking_list(url)

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
    # Generate the Matplotlib figure for this frame
    fig = make_graph(frame_id, tracking_list)

    # Save the figure into an in-memory buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # close to avoid memory leaks

    # Send it directly as an image
    return send_file(buf, mimetype='image/png')

# ---------------------------------------------------------
# 4️⃣ Run the app
# ---------------------------------------------------------
if __name__ == "__main__":
    # debug=True means Flask will auto-reload when you save code changes
    app.run(debug=True)