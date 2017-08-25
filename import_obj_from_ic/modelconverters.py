import bpy
from bpy.types import Operator
from bpy import ops

class MultiOperator(Operator):
	bl_label = "Convert Model"
	bl_idname = "object.multi_operator"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		# Make the last added object in the scene active (in this case the imported object)
		context.scene.objects.active = bpy.data.objects[len(bpy.data.objects) - 1:][0]
		imported_object = context.object
		imported_object.select = True
		
		ops.object.scale_transform()
		ops.object.add_parent_cube()

		parentCube = context.object
		ops.object.select_all(action='DESELECT')

		imported_object.select = True
		context.scene.objects.active = imported_object

		ops.object.separate_by_material()
		ops.object.select_all(action='DESELECT')

		parentCube.select = True
		context.scene.objects.active = parentCube

		# Transforms the location of the parent cube to sit at ground level
		parentCube.location[2] = parentCube.dimensions[2] / 2
		ops.object.origin_set(type='ORIGIN_CURSOR')

		return {'FINISHED'}

class ScaleTransform(Operator):
	"""Set origin ('GEOMETRY_ORIGIN', 'BOUNDS'), clears location and scales an object(default=0.001)"""
	bl_label = "Set Origin and Scale"
	bl_idname = "object.scale_transform"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		objScale = context.scene.chose_obj_scale

		ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')
		ops.object.location_clear(clear_delta=False)
		ops.transform.resize(value=(objScale, objScale, objScale))
		ops.object.transform_apply(location=False, rotation=True, scale=True)

		return {'FINISHED'}

class AddParentCube(Operator):
	"""Adds a cube and makes it the parent of active object"""
	bl_label = "Add Parent Cube"
	bl_idname = "object.add_parent_cube"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		childObject = context.object
		childObjectDim = context.object.dimensions

		ops.mesh.primitive_cube_add(radius=1, location=(0, 0, 0))
		parentCube = context.object
		parentCube.name = "ParentCube_" + childObject.name

		context.object.cycles_visibility.camera = False
		context.object.cycles_visibility.diffuse = False
		context.object.cycles_visibility.glossy = False
		context.object.cycles_visibility.transmission = False
		context.object.cycles_visibility.scatter = False
		context.object.cycles_visibility.shadow = False
		context.object.draw_type = 'WIRE'

		parentCube.dimensions = childObjectDim
		ops.object.transform_apply(location=False, rotation=False, scale=True)

		ops.object.select_all(action='DESELECT')

		childObject.select = True
		parentCube.select = True

		ops.object.parent_set(type='OBJECT', keep_transform=False)

		return {'FINISHED'}


class SeparateByMaterial(Operator):
	bl_label = "Separate By Material"
	bl_idname = "object.separate_by_material"
	bl_options = {"REGISTER", "UNDO"}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		ops.object.mode_set(mode='EDIT')
		ops.mesh.select_all(action='DESELECT') # TEST
		ops.mesh.select_all(action='SELECT')
		ops.mesh.separate(type="MATERIAL")
		ops.object.editmode_toggle()

		return {'FINISHED'}
