import bpy
import sys
import math
import os


working_dir_path = os.path.abspath("/nas/martin/7-software-projects/genpyblender/")
sys.path.append(working_dir_path)

from mathutils import Vector
from genpyblender import make_image, utils, camera, lighting, colormap, plots


def draw(pixel_width, pixel_height, frame_no, frame_count):

    camera_object = camera.create_plot_camera()

    axes = plots.Axes().of_start((-1, -1, 0)).of_extent((2, 2, 2)).with_divisions((0.5, 0.5, 0.5))
    axes.draw()
    plot = plots.Plot3dZofXY(axes).of_function(lambda x, y :2 - (x*x +y*y)).fill(colormap.ViridianMap(0, 1)).stroke([1, 0, 0, 1])
    plot.plot()

    ## Lights
    lighting.create_sun_light(rotation=(0.0, math.pi * 0.5, -math.pi * 0.1))

    return camera_object

make_image.make_blender_image("basic_3d_plot", draw, 500, 500)