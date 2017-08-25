import bpy
from bpy.types import Operator
from bpy import ops

class MaterialSwap(Operator):
	"""Swaps material based on color"""
	bl_label = "Swap Materials"
	bl_idname = "object.material_swap"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return (context.active_object is not None and context.object.active_material is not None)

	def execute(self, context):
		fake_user_materials = self.getFakeMaterial()

		for obj in context.selected_objects:
			for material_slot in obj.material_slots:
				if material_slot.material is None:
					pass
				else:
					materialMatch = self.getClosestMaterial(material_slot.material, fake_user_materials)
					material_slot.material = materialMatch

		return {'FINISHED'}

	#Searches for fake-user materials in scene, returns list with materials
	def getFakeMaterial(self):
		fake_user_materials = []
		for material in bpy.data.materials:
			if material.use_fake_user == True:
				fake_user_materials.append(material)
			else:
				pass
		return fake_user_materials

	# Returns the fake-material which has the closest diffuse color values to the current material
	def getClosestMaterial(self, currentMaterial, fake_user_materials):
		materialDiff = []

		for fmaterial in fake_user_materials:
			rDiff = abs(currentMaterial.diffuse_color[0] - fmaterial.diffuse_color[0])
			gDiff = abs(currentMaterial.diffuse_color[1] - fmaterial.diffuse_color[1])
			bDiff = abs(currentMaterial.diffuse_color[2] - fmaterial.diffuse_color[2])

			colorDiff = rDiff + gDiff + bDiff
			materialDiff.append((fmaterial, colorDiff / 3))

		difference = ("None", 1.1)

		for material in materialDiff:
			print("Material '%s's color has a difference of: '%s' to MATERIAL: '%s's color." % (material[0].name, material[1], currentMaterial.name))
			if material[1] >= difference[1]:
				pass
			elif material[1] < difference[1]:
				difference = material
			else:
				print("Error!")

		if difference[1] >= bpy.context.scene.mswap_threshold:
			print("\nA material did not pass the threshold.")
			print("Returning 'PlaceholderMaterial'\n")
			return bpy.data.materials['PlaceholderMaterial']
		elif difference[1] < 0.0:
			print("\nERROR!!! Material: '%s' has difference: '%s' to MATERIAL: '%s'" % (difference[0].name, difference[1], currentMaterial.name))
			print("Can't have less than 0.0. Returning 'PlaceholderMaterial'\n")
			return bpy.data.materials['PlaceholderMaterial']
		else:
			print("\nMaterial: '%s's color was closest to the MATERIAL: '%s's color with difference: '%s'" % (difference[0].name, currentMaterial.name, difference[1]))
			print("Returning material: '%s'\n" % difference[0].name)
			# Returns the material
			return difference[0]
