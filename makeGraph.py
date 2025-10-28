import matplotlib
matplotlib.use('Agg') 
import requests
import json
import matplotlib.pyplot as plt
from tqdm import tqdm  # optional but nice for progress display

def make_graph(frame_index, tracking_list):
    # Example data
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

    # Add labels, title, legend
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('Field with Ball and Player Locations')
    plt.legend()
    plt.grid(True)

    # Instead of showing the plot here, return the figure
    return fig

