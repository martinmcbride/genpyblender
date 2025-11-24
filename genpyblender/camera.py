# Author:  Martin McBride
# Created: 2025-11-02
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
# Based on part on https://github.com/yuki-koyama/blender-cli-rendering
import math
from typing import Tuple

import bpy
from mathutils import Vector


def create_camera(location: Tuple[float, float, float]) -> bpy.types.Object:
    bpy.ops.object.camera_add(location=location)

    return bpy.context.object

def set_camera_params(camera: bpy.types.Camera,
                      focus_target_object: bpy.types.Object,
                      lens: float = 85.0,
                      fstop: float = 1.4) -> None:
    # Simulate Sony's FE 85mm F1.4 GM
    camera.sensor_fit = 'HORIZONTAL'
    camera.sensor_width = 36.0
    camera.sensor_height = 24.0
    camera.lens = lens
    camera.dof.use_dof = False
    camera.dof.focus_object = focus_target_object
    camera.dof.aperture_fstop = fstop
    camera.dof.aperture_blades = 11
    camera.type = "ORTHO"

def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()


def create_plot_camera(distance=4, xy_rot=-math.pi/4, z_rot=math.pi/6, scale=3.8):
    location = (distance*math.cos(xy_rot), distance*math.sin(xy_rot), distance*math.cos(z_rot))
    camera_object = create_camera(location)
    look_at(camera_object, Vector((0, 0, 0)))
    set_camera_params(camera_object.data, None, lens=50.0)
    camera_object.data.ortho_scale = scale
    return camera_object

