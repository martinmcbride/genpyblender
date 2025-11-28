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

    axes = plots.Axes().of_start((-1, -1, -1)).of_extent((2, 2, 2)).with_divisions((.5, .5, .5))
    axes.draw()
    plot = plots.Plot3dZofXY(axes).of_function(lambda x, y :1.2*math.cos(6*x)*math.sin(6*y), precision=100).fill(colormap.ViridianMap(0, 1)).stroke([0, 0, 0.2, 1])
    plot.plot()

    return camera_object

make_image.make_blender_image("basic_clipped_xyz_plot", draw, 500, 500)