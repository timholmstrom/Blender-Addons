import bpy
from math import sqrt
from bpy import ops
from bpy.types import Operator

class MtlToCycles(Operator):
	"""Reads a mtl file and converts it's values to Cycles"""
	bl_label = "Convert from Mtl file"
	bl_idname = "object.mtl_to_cycles"
	bl_options = {"REGISTER", "UNDO"}

	filename_ext = ".mtl"
	filter_glob = bpy.props.StringProperty(default="*.mtl", options={'HIDDEN'})

	filepath = bpy.props.StringProperty(name="File Path", description="Filepath for .mtl file", default="")

	@classmethod
	def poll(cls, context):
		return (context.active_object is not None and context.object.active_material is not None)

	def execute(self, context):
		context.scene.MtlPath = self.properties.filepath
		mtl = readMtl(self.properties.filepath)

		for obj in context.selected_objects:
			for material_slot in obj.material_slots:
				if material_slot.material.name in mtl:
					convertMaterial(material_slot.material, mtl[material_slot.material.name][0], mtl[material_slot.material.name][1])

		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)

		return {'RUNNING_MODAL'}


def readMtl(filepath):
	materials = {}
	with open(filepath) as f:
		mtl = f.read()
		lines = mtl.split("\n")
		matname = ""
		for line in lines:
			if line.startswith("newmtl"):
				matName = line.split("newmtl ")[1]
				materials[matName] = [None, None]
			if line.startswith("Ns"):
				ns = line.split("Ns ")[1]
				materials[matName][0] = float(ns)
			if line.startswith("illum"):
				illum = line.split("illum ")[1]
				materials[matName][1] = int(illum)

	return materials

def convertMaterial(material, ns, illum):
	diffuse_colorR = s2lin(material.diffuse_color[0])
	diffuse_colorG = s2lin(material.diffuse_color[1])
	diffuse_colorB = s2lin(material.diffuse_color[2])
	# diffuse_colorR = material.diffuse_color[0]
	# diffuse_colorG = material.diffuse_color[1]
	# diffuse_colorB = material.diffuse_color[2]

	specular_color = material.specular_color

	roughness = ironNsToRoughness(ns)
	if roughness is None:
		roughness = 2.0

	material.use_nodes = True
	nodes = material.node_tree.nodes
	nodes.clear()

	node_output = nodes.new('ShaderNodeOutputMaterial')
	node_output.location = (100, 0)

	node_group = nodes.new('ShaderNodeGroup')
	node_group.location = (-300, 0)

	if illum == 3:
		node_group.node_tree = bpy.data.node_groups['Metal']
		node_group.inputs[0].default_value = (diffuse_colorR, diffuse_colorG, diffuse_colorB, 1)
		node_group.inputs[1].default_value = (specular_color[0], specular_color[1], specular_color[2], 1)
		node_group.inputs[2].default_value = roughness
	else:
		node_group.node_tree = bpy.data.node_groups['Glossy']
		node_group.inputs[0].default_value = (diffuse_colorR, diffuse_colorG, diffuse_colorB, 1)
		node_group.inputs[1].default_value = roughness

	links = material.node_tree.links
	link = links.new(node_group.outputs[0], node_output.inputs[0])

def s2lin(x):
	a = 0.055
	if x <=0.04045 :
		y = x * (1.0 / 12.92)
	else:
		y = pow( (x + a) * (1.0 / (1 + a)), 2.4)
	return y

def ironNsToRoughness(value):
    if value < 5.0:
        ns = 1.0
    elif value > 1605.0:
        ns = 0.0
    else:
        ns = 1.0 - (sqrt(value - 5) * 0.025)
    return ns
