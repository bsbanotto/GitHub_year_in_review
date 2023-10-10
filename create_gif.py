#!/usr/bin/env python3
"""
Take our png images of stats and create a gif
"""
import os
import imageio.v2 as imageio


def create_gif(directory):
    png_files = [f for f in os.listdir(directory) if f.endswith('.png')]
    png_files.sort()
    images = []

    for png_file in png_files:
        images.append(imageio.imread(os.path.join(directory, png_file)))
    imageio.mimsave(directory + '/output_gif.gif',
                    images,
                    duration=1500,
                    loop=0
                    )
