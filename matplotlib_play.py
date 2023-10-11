#!/usr/bin/env python3
"""
matplotlib playground to try to make slides
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import imageio.v2 as imageio

text_kwargs = dict(
    family='sans-serif',
    ha='center',
    va='center',
    fontsize=45,
    color='black',
    wrap=True,
    fontweight='semibold',
    )

user = 'bsbanotto'
year = str(2023)

# Creating a 8 x 8 blank red screen
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
# Scaling the axis to fill 100% of the figure
plt.gca().set_position([0, 0, 1, 1])
# Hiding the axes
ax.axis('off')

# Putting a bunch of circles on that screen
radius = .72
colors = ['black',
          'red',
          'orange',
          'yellow',
          'green',
          'blue',
          'violet',
          ]
for circles in range(0, 7):
    circle = patches.Circle(xy=(.5, .5), radius=radius, color=colors[circles])
    ax.add_patch(circle)
    radius -= 0.05

# Create an offwhite starburst
center = (.5, .5)
height = 1
width = .50

pt1 = ((center[0] - (width / 2)), center[1])
pt2 = ((center[0] + (width / 2)), center[1])
pt3 = (center[0], height)


# Define the vertices of the isosceles triangle
vertices = np.array([pt1, pt2, pt3])

# Calculate the midpoint of the base
midpoint = (vertices[0] + vertices[1]) / 2.0

# Number of triangles to rotate
num_triangles = 18

# Calculate the rotation angle for each triangle
rotation_angle = 360.0 / num_triangles

# Plot the original isosceles triangle
triangle = patches.Polygon(vertices, closed=True, edgecolor=(224/255, 224/255, 224/255), facecolor=(224/255, 224/255, 224/255))
ax.add_patch(triangle)

# Rotate and plot the remaining triangles
for i in range(1, num_triangles):
    # Rotate the vertices using a rotation matrix
    rotation_matrix = np.array([[np.cos(np.radians(i * rotation_angle)), -np.sin(np.radians(i * rotation_angle))],
                                [np.sin(np.radians(i * rotation_angle)), np.cos(np.radians(i * rotation_angle))]])
    rotated_vertices = np.dot(vertices - midpoint, rotation_matrix) + midpoint

    # Plot the rotated triangle
    rotated_triangle = patches.Polygon(rotated_vertices, closed=True, edgecolor=(224/255, 224/255, 224/255), facecolor=(224/255, 224/255, 224/255))
    ax.add_patch(rotated_triangle)

# Displaying lines of font with a pause between each one
text1 = 'Welcome to ' + user + '\'s'
plt.text(.5, .73, text1, **text_kwargs)
plt.savefig(fname='1.png', format='png')
text2 = year
plt.text(.5, .565, text2, **text_kwargs)
plt.savefig(fname='2.png', format='png')
plt.text(.5, .435, 'GitHub', **text_kwargs)
plt.savefig(fname='3.png', format='png')
plt.text(.5, .295, 'Year in Review!', **text_kwargs)
plt.savefig(fname='4.png', format='png')

png_files = [f for f in os.listdir('./') if f.endswith('.png')]
png_files.sort()
images = []

for png_file in png_files:
    images.append(imageio.imread(os.path.join('./', png_file)))
imageio.mimsave('./' + '/output_gif.gif',
                images,
                duration=750,
                loop=0
                )

plt.show()