import bpy
import sys
import math
import os


working_dir_path = os.path.abspath("/genpyblender/")
sys.path.append(working_dir_path)

from mathutils import Vector
from genpyblender import make_image, utils, camera, lighting, colormap, plots


def draw(pixel_width, pixel_height, frame_no, frame_count):

    camera_object = camera.create_plot_camera()
    lighting.create_sun_light()

    axes = plots.Axes().of_start((-1, -1, 0)).of_extent((2, 2, 1)).with_divisions((.5, .5, 0.2))
    axes.draw()
    plot = plots.Plot2dXYZofT(axes).of_function(lambda t :t*math.cos(t*20), lambda t :t*math.sin(t*20), lambda t :t, precision=100)
    plot.plot()

    return camera_object

make_image.make_blender_image("basic_t_plot", draw, 500, 500)