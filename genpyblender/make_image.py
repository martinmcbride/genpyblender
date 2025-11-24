# Author:  Martin McBride
# Created: 2025-11-02
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3

import bpy
from genpyblender import utils

def make_blender_image(outfile, draw, width, height):
    output_file_path = bpy.path.relpath(outfile)
    resolution_percentage = 100
    num_samples = 128
    utils.clean_objects()

    utils.set_white_background()

    bpy.context.scene.render.engine = 'CYCLES'

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = [1, 1, 1, 1]
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 1

    camera_object = draw(width, height, 0, 1)

    scene = bpy.data.scenes["Scene"]
    utils.set_output_properties(scene, resolution_percentage, output_file_path, res_x=width, res_y=height)
    utils.set_cycles_renderer(scene, camera_object, num_samples)

def example_blender_draw_function(pixel_width, pixel_height, frame_no, frame_count):
    pass