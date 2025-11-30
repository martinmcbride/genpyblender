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

    axes = plots.Axes().of_start((-1, -1, 0)).of_extent((2, 2, 7)).with_divisions((.5, .5, 2))
    axes.draw()
    plot = plots.Plot3dXYZofUV(axes).of_function(lambda u, v :u*math.cos(v), lambda u, v :u*math.sin(v), lambda u, v :v, u_extent=(0, 1), v_extent=(-math.pi, 3*math.pi), precision=100).fill(colormap.ViridianMap(0, 1)).clip()#.stroke([0.2, 0, 0, 1], u_divs=4, v_divs=30).clip()
    plot.plot()

    return camera_object

make_image.make_blender_image("clipped_uv_plot", draw, 500, 500)