# Python
import matplotlib.pyplot as plt

# Sample data
x = [5, 7, 8, 7, 2, 17, 2, 9, 4, 11]
y = [-34, -17, 0, 17, 34, 6, 20, -10, 3, -20]

players = []

# Create scatter plot
plt.xlim(-52.5, 52.5)  # Adjusted to a range instead of single point
plt.ylim(-34, 34)
plt.scatter(x, y, color='blue', marker='o', s=100, alpha=0.7)

# Add labels and title
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Scatter Plot Example')

# Show the plot
plt.show()