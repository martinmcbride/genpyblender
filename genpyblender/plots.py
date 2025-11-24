# Author:  Martin McBride
# Created: 2025-11-03
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
import math
import bpy
import bmesh
from mathutils import Vector


def align_perpendicular_to_camera(object, camera):
    view_vector = camera.matrix_world.to_quaternion() @ Vector((0, 0, 1))
    object.rotation_euler = view_vector.to_track_quat('Z', 'Y').to_euler()
    bpy.context.view_layer.update()

def create_diffuse_material(mesh, colour, name):
    material = bpy.data.materials.new(name = name)
    material.diffuse_color = colour
    mesh.data.materials.append(material)

class Axes():

    def __init__(self):
        self.xaxis_color = (1, 0, 0, 1)
        self.yaxis_color = (0, 1, 0, 1)
        self.zaxis_color = (0, 0, 1, 1)
        self.div_color = (0, 0, 0, 1)
        self.plane_color = (0.8, 0.8, 0.8, 1)
        self.div_radius = 0.01
        self.axis_radius = 0.02

        # Positions of axes in blender coordinates
        self.axis_start = (-1, -1, -1)
        self.axis_end = (1, 1, 1)
        self.div_positions = None

        # Axis dimensions in graph space
        self.start = (0, 0, 0)
        self.extent = (1, 1, 1)
        self.divisions = (0.2, 0.2, 0.2)

        self.font_size = 0.15
        self.text_offset_x = (0, -0.25, -0.05)
        self.text_offset_y = (0.05, -0.05, -0.05)
        self.text_offset_z = (0.05, 0, -0.05)
        self.steps = None

    def convert_points_graph_to_blender(self, x, y, z):
        end = tuple([e + s for s, e in zip(self.start, self.extent)])
        xo = ((x - self.start[0]) * (self.axis_end[0] - self.axis_start[0]) / (
                    end[0] - self.start[0])) + self.axis_start[0]
        yo = ((y - self.start[1]) * (self.axis_end[1] - self.axis_start[1]) / (
                    end[1] - self.start[1])) + self.axis_start[1]
        zo = ((z - self.start[2]) * (self.axis_end[2] - self.axis_start[2]) / (
                    end[2] - self.start[2])) + self.axis_start[2]
        return xo, yo, zo

    def convert_points_blender_to_graph(self, xo, yo, zo):
        end = tuple([e + s for s, e in zip(self.start, self.extent)])
        x = ((xo - self.axis_start[0]) * (end[0] - self.start[0]) / (
                    self.axis_end[0] - self.axis_start[0])) + self.start[0]
        y = ((yo - self.axis_start[1]) * (end[1] - self.start[1]) / (
                    self.axis_end[1] - self.axis_start[1])) + self.start[1]
        z = ((zo - self.axis_start[2]) * (end[2] - self.start[2]) / (
                    self.axis_end[2] - self.axis_start[2])) + self.start[2]
        return x, y, z

    def _get_divs(self, start, end, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= end:
            divs.append(n)
            n += div
        return divs

    def _set_divisions(self):
        end = tuple([e + s for s, e in zip(self.start, self.extent)])
        div_values = [self._get_divs(self.start[i], end[i], self.divisions[i]) for i in range(3)]
        x_positions = tuple([self.convert_points_graph_to_blender(v, 0, 0)[0] for v in div_values[0]])
        y_positions = tuple([self.convert_points_graph_to_blender(0, v, 0)[1] for v in div_values[1]])
        z_positions = tuple([self.convert_points_graph_to_blender(0, 0, v)[2] for v in div_values[2]])
        self.div_positions = (x_positions, y_positions, z_positions)
        self.steps = tuple(div_values)
        print("STEPS", self.steps)

    def add_axis_text(self, value, location):
#        print("ADD", value, location)
        bpy.ops.object.text_add(enter_editmode=False, align='WORLD')
        obj = bpy.context.active_object
        obj.location = location
        text_data = obj.data
        text_data.body = value
        text_data.size = self.font_size
        text = bpy.context.active_object
        align_perpendicular_to_camera(text, bpy.data.objects.get("Camera"))
        create_diffuse_material(text, (0, 0, 0, 1), "text_material")

    def cylinder_between(self, x1, y1, z1, x2, y2, z2, r, color):

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        dist = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius=r,
            depth=dist,
            location=(dx / 2 + x1, dy / 2 + y1, dz / 2 + z1)
        )

        phi = math.atan2(dy, dx)
        theta = math.acos(dz / dist)

        bpy.context.object.rotation_euler[1] = theta
        bpy.context.object.rotation_euler[2] = phi

        mat = bpy.data.materials.new("col")
        mat.diffuse_color = color
        bpy.context.object.active_material = mat

    def plane(self, orientation):
        end = tuple([e + s for s, e in zip(self.start, self.extent)])
        bpy.ops.mesh.primitive_plane_add()
        plane = bpy.context.active_object
        if orientation == "x":
            plane.location = Vector((0, 1, 0))
            angle = math.radians(90)
            plane.rotation_euler[0] = angle
            for p, pa in zip(self.steps[0], self.div_positions[0]):
                self.cylinder_between(pa, self.axis_end[1], self.axis_start[2], pa, self.axis_end[1], self.axis_end[2], self.div_radius, self.div_color)
                if pa < 0.9:
                    self.add_axis_text(f"{p: .1f}", (pa + self.text_offset_x[0], self.axis_start[1] + self.text_offset_x[1], self.axis_start[2] + self.text_offset_x[2]))
            for p, pa in zip(self.steps[2], self.div_positions[2]):
                self.cylinder_between(self.axis_start[0], self.axis_end[1], pa, self.axis_end[0], self.axis_end[1], pa, self.div_radius, self.div_color)

        if orientation == "y":
            plane.location = Vector((-1, 0, 0))
            angle = math.radians(90)
            plane.rotation_euler[1] = angle
            for p, pa in zip(self.steps[1], self.div_positions[1]):
                self.cylinder_between(self.axis_start[0], pa, self.axis_start[2], self.axis_start[0], pa, self.axis_end[2], self.div_radius, self.div_color)
                if pa > -0.9 and pa < 0.9:
                    self.add_axis_text(f"{p: .1f}", (self.axis_end[0] + self.text_offset_y[0], pa + self.text_offset_y[1], self.axis_start[2] + self.text_offset_y[2]))
            for p, pa in zip(self.steps[2], self.div_positions[2]):
                self.cylinder_between(self.axis_start[0], self.axis_start[1], pa, self.axis_start[0], self.axis_end[1], pa, self.div_radius, self.div_color)

        if orientation == "z":
            plane.location = Vector((0, 0, -1))
            for p, pa in zip(self.steps[0], self.div_positions[0]):
                self.cylinder_between(pa, self.axis_start[1], self.axis_start[2], pa, self.axis_end[1], self.axis_start[2], self.div_radius, self.div_color)
            for p, pa in zip(self.steps[2], self.div_positions[2]):
                if pa > -0.9:
                    self.add_axis_text(f"{p: .1f}", (self.axis_end[0] + self.text_offset_z[0], self.axis_end[1] + self.text_offset_z[1], pa + self.text_offset_z[2]))
            for p, pa in zip(self.steps[1], self.div_positions[1]):
                self.cylinder_between(self.axis_start[0], pa, self.axis_start[2], self.axis_end[0], pa, self.axis_start[2], self.div_radius, self.div_color)

        plane.scale = Vector((1, 1, 1))

        mat = bpy.data.materials.new("col")
        mat.diffuse_color = self.plane_color
        plane.active_material = mat

    def draw_axes(self):
        r = self.axis_radius
        self.cylinder_between(-1, 1, -1, 1, 1, -1, r, color=self.xaxis_color)
        self.cylinder_between(-1, -1, -1, -1, 1, -1, r, color=self.yaxis_color)
        self.cylinder_between(-1, 1, -1, -1, 1, 1, r, color=self.zaxis_color)

    def draw(self):
        self._set_divisions()
        self.plane("x")
        self.plane("y")
        self.plane("z")
        self.draw_axes()


class BasePlot:

    def __init__(self, axes, function, colormap, precision=20):
        self.axes = axes
        self.function = function
        self.colormap = colormap
        self.precision = precision

    def crop_plot(self, plot_obj):
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        cube = bpy.context.selected_objects[0]

        bpy.ops.object.select_all(action='DESELECT')
        cube.hide_render = True
        plot_obj.select_set(True)
        bpy.context.view_layer.objects.active = plot_obj

        bpy.ops.object.modifier_add(type='BOOLEAN')
        plot_obj.modifiers[0].object = cube
        plot_obj.modifiers[0].operation = 'INTERSECT'
        bpy.ops.object.modifier_apply(modifier=plot_obj.modifiers[0].name)

    def apply_colormap(self):
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the active object (which is the cube)
        graph_object = bpy.context.active_object
        # Get the mesh data
        mesh = graph_object.data

        # Switch to Vertex Paint mode
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')

        # Set the active vertex color layer
        active_vc_layer = graph_object.data.vertex_colors.active
        if active_vc_layer is None:
            active_vc_layer = graph_object.data.vertex_colors.new()

        # Loop through the vertices and set them to color from map
        for poly in graph_object.data.polygons:
            for loop_index in poly.loop_indices:
                loop = graph_object.data.loops[loop_index]
                vertex_index = loop.vertex_index
                vert = mesh.vertices[vertex_index]
                # vert.co.z is the z-value of the graph element in blender coords, ie in the range -1 to +1.
                # The colormap has input range 0 to 1. This code maps between the two.
                color = self.colormap((vert.co.z + 1) / 2)
                active_vc_layer.data[loop_index].color = color

        # Create a new material
        mat = bpy.data.materials.new(name="Vertex Color Material")
        graph_object.data.materials.append(mat)

        # Get a reference to the material
        mat = graph_object.data.materials[0]

        # Create a new node tree for the material
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Add a Vertex Color node
        vc_node = nodes.new(type='ShaderNodeVertexColor')
        vc_node.layer_name = 'Attribute'
        vc_node.location = (0, 0)  # Optional: Set the location of the node

        # Add a Principled BSDF shader node
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (400, 0)  # Optional: Set the location of the node

        # Add an Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (600, 0)  # Optional: Set the location of the node

        # Connect the nodes
        mat.node_tree.links.new(vc_node.outputs["Color"], bsdf_node.inputs["Base Color"])
        mat.node_tree.links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

        bpy.ops.object.mode_set(mode='OBJECT')

    def plot(self):
        pass

class Plot3dZofXY(BasePlot):

    def __init__(self, axes, function, colormap, precision=20):
        super().__init__(axes, function, colormap, precision)
        self.show_lines = True
        self.line_color = (0, 0, 0.5, 0)
        self.line_radius = 0.01

    def draw_lines(self):
        for x in self.axes.div_positions[0]:
            for i in range(self.precision):
                y0 = 2 * i / self.precision - 1
                y1 = 2 * (i + 1) / self.precision - 1

                xg, y0g, _ = self.axes.convert_points_blender_to_graph(x, y0, 0)
                z0g = self.function(xg, y0g)
                x, y0, z0 = self.axes.convert_points_graph_to_blender(xg, y0g, z0g)

                xg, y1g, _ = self.axes.convert_points_blender_to_graph(x, y1, 0)
                z1g = self.function(xg, y1g)
                x, y1, z1 = self.axes.convert_points_graph_to_blender(xg, y1g, z1g)

                self.axes.cylinder_between(x, y0, z0, x, y1, z1, self.line_radius, self.line_color)

        for y in self.axes.div_positions[1]:
            for i in range(self.precision):
                x0 = 2 * i / self.precision - 1
                x1 = 2 * (i + 1) / self.precision - 1

                x0g, yg, _ = self.axes.convert_points_blender_to_graph(x0, y, 0)
                z0g = self.function(x0g, yg)
                x0, y, z0 = self.axes.convert_points_graph_to_blender(x0g, yg, z0g)

                x1g, yg, _ = self.axes.convert_points_blender_to_graph(x1, y, 0)
                z1g = self.function(x1g, yg)
                x1, y, z1 = self.axes.convert_points_graph_to_blender(x1g, yg, z1g)

                self.axes.cylinder_between(x0, y, z0, x1, y, z1, self.line_radius, self.line_color)

    def plot(self):
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=self.precision, y_subdivisions=self.precision,
                                        location=(0, 0, 0))

        bpy.ops.object.mode_set(mode='EDIT')

        obj = bpy.context.active_object
        mesh = obj.data

        bm = bmesh.from_edit_mesh(mesh)

        for v in bm.verts:
            x, y, _ = self.axes.convert_points_blender_to_graph(v.co.x, v.co.y, 0)
            z = self.function(x, y)
            v.co.z += self.axes.convert_points_graph_to_blender(x, y, z)[2]

        bmesh.update_edit_mesh(mesh)

        self.apply_colormap()

        if self.show_lines:
            self.draw_lines()

        self.crop_plot(obj)
