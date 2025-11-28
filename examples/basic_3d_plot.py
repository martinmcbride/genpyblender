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

    axes = plots.Axes().of_start((-1, -1, 0)).of_extent((2, 2, 1)).with_divisions((.2, .2, .2))
    axes.draw()
    grid = [i for i in range(20)]
    plot = plots.Plot3dZofXY(axes).of_function(lambda x, y :math.exp(y)*math.cos(x), precision=20).fill(colormap.ViridianMap(0, 1)).stroke([0, 0.2, 0, 1])
    plot = plots.Plot3dXYZofUV(axes).of_function(lambda u, v :u, lambda u, v:v, lambda u, v :math.atan2(u, v), u_extent=(0, 2*math.pi), v_extent=(0, 1)).fill(colormap.ViridianMap(0, 1))
    #plot = plots.Plot2dXYZofT(axes).of_function(lambda t :.75, lambda t :0.5, lambda t :t, t_extent=(-1, 2)).noclip()
    plot.plot()

    ## Lights
    lighting.create_sun_light(rotation=(0.0, math.pi * 0.5, -math.pi * 0.1))

    return camera_object

make_image.make_blender_image("basic_3d_plot", draw, 500, 500)