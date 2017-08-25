import bpy
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
	diffuse_color = material.diffuse_color
	specular_color = material.specular_color
	roughness = nsToRoughness(ns)
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
		node_group.inputs[0].default_value = (diffuse_color[0], diffuse_color[1], diffuse_color[2], 1)
		node_group.inputs[1].default_value = (specular_color[0], specular_color[1], specular_color[2], 1)
		node_group.inputs[2].default_value = roughness
	else:
		node_group.node_tree = bpy.data.node_groups['Glossy']
		node_group.inputs[0].default_value = (diffuse_color[0], diffuse_color[1], diffuse_color[2], 1)
		node_group.inputs[1].default_value = roughness

	links = material.node_tree.links
	link = links.new(node_group.outputs[0], node_output.inputs[0])

def nsToRoughness(ns):
	if ns < 9:
		return 1.0
	elif ns < 21:
		return 0.95
	elif ns < 41:
		return 0.9
	elif ns < 69:
		return 0.85
	elif ns < 105:
		return 0.8
	elif ns < 149:
		return 0.75
	elif ns < 201:
		return 0.7
	elif ns < 261:
		return 0.65
	elif ns < 329:
		return 0.6
	elif ns < 405:
		return 0.55
	elif ns < 489:
		return 0.5
	elif ns < 581:
		return 0.45
	elif ns < 681:
		return 0.4
	elif ns < 789:
		return 0.35
	elif ns < 905:
		return 0.3
	elif ns < 1029:
		return 0.25
	elif ns < 1161:
		return 0.2
	elif ns < 1301:
		return 0.15
	elif ns < 1449:
		return 0.1
	elif ns < 1605:
		return 0.05
	elif ns >= 1605:
		return 0.0
	else:
		print("Error. The 'Ns' value: %s can't be converted to roughness." % ns)
		return None
