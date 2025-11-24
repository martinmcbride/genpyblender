# Author:  Martin McBride
# Created: 2025-11-02
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
# Based on part on https://github.com/yuki-koyama/blender-cli-rendering

from typing import Tuple, Optional

import bpy

def create_sun_light(location: Tuple[float, float, float] = (0.0, 0.0, 5.0),
                     rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                     name: Optional[str] = None) -> bpy.types.Object:
    bpy.ops.object.light_add(type='SUN', location=location, rotation=rotation)

    if name is not None:
        bpy.context.object.name = name

    bpy.context.object.data.use_shadow = False

    return bpy.context.object
