import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

def make_graph(frame_index, tracking_list):
    fig, ax = plt.subplots(figsize=(10, 6.5))
    
    x_min, x_max = -52.5, 52.5
    y_min, y_max = -34, 34

    # Draw field outline
    field_outline = patches.Rectangle(
        (x_min, y_min), x_max - x_min, y_max - y_min,
        linewidth=2, edgecolor='black', facecolor='green', alpha=0.15
    )
    ax.add_patch(field_outline)

    # Center line and circle
    ax.plot([0, 0], [y_min, y_max], color='white', linewidth=2)
    ax.add_patch(patches.Circle((0, 0), 9.15, fill=False, color='white', linewidth=2))
    ax.plot(0, 0, 'wo', markersize=4)  # center spot

    # Penalty and goal boxes
    ax.add_patch(patches.Rectangle((-52.5, -20.15), 16.5, 40.3, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((52.5 - 16.5, -20.15), 16.5, 40.3, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((-52.5, -7.32), 5.5, 14.64, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((52.5 - 5.5, -7.32), 5.5, 14.64, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((-52.5 - 2, -3.66), 2, 7.32, fill=False, color='white', linewidth=2))
    ax.add_patch(patches.Rectangle((52.5, -3.66), 2, 7.32, fill=False, color='white', linewidth=2))

    # Penalty arcs
    ax.add_patch(patches.Arc((-52.5 + 11, 0), 18.3, 18.3, angle=0, theta1=308, theta2=52, color='white', linewidth=2))
    ax.add_patch(patches.Arc((52.5 - 11, 0), 18.3, 18.3, angle=0, theta1=128, theta2=232, color='white', linewidth=2))

    # Get frame data
    frame = tracking_list[frame_index]

    # Ball + player coordinates
    x = [frame['ball']['x']] + [p['x'] for p in frame['players']]
    y = [frame['ball']['y']] + [p['y'] for p in frame['players']]

    # Plot players (blue) and ball (red)
    ax.scatter(x[1:], y[1:], color='blue', label='Players')
    ax.scatter(x[0], y[0], color='red', s=100, label='Ball')

    # Axis limits
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')

    # Center axes
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # Border
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(1.5)

    # Ticks
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Labels at edges
    ax.set_xlabel('X values', labelpad=10)
    ax.set_ylabel('Y values', labelpad=10)
    ax.xaxis.set_label_coords(1, -0.05)
    ax.yaxis.set_label_coords(-0.05, 1)

    ax.set_title('Field with Ball and Player Locations')
    ax.legend()
    ax.grid(True)

    # Save figure to a BytesIO object instead of showing
    img_bytes = BytesIO()
    fig.savefig(img_bytes, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)  # Close the figure to avoid memory leaks
    img_bytes.seek(0)

    return img_bytes
