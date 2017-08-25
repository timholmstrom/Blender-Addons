# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# END GPL LICENSE BLOCK #####

bl_info = {
	"name" : "MSwap",
	"author" : "Tim Holmström",
	"version" : (0, 1, 1),
	"blender" : (2, 78, 0),
	"location" : "View3D > Tools Panel",
	"description" : "Swaps current material for matching material(using Viewport Color).",
	"warning" : "",
	"wiki_url" : "",
	"tracker_url" : "",
	"category" : "User",
}

if "bpy" in locals():
	import imp
	if "mspanel" in locals():
		imp.reload(mspanel)
	if "mswap" in locals():
		imp.reload(mswap)
else:
	from . import mspanel
	from . import mswap

import bpy
from bpy.types import Scene, Operator, AddonPreferences
from bpy.props import FloatProperty, StringProperty

class MswapAddonPreferences(AddonPreferences):
	bl_idname = __name__

	filepath = StringProperty(
				name="Path",
				subtype="FILE_PATH",
				)

	def draw(self, context):
		layout = self.layout
		layout.label(text="Specifies a .blend file for swapping materials.")
		layout.prop(self, "filepath")

class OBJECT_OT_addon_prefs_mswap(Operator):
	bl_idname = "object.addon_prefs_mswap"
	bl_label = "MSwap preferences"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		# if addon_prefs.filepath is not None:
		# 	with bpy.data.libraries.load(addon_prefs.filepath) as (data_from, data_to):
		# 		data_to.materials = data_from.materials
		# 		# swap_materials = data_from.materials
		# else:
		# 	pass

		return {'FINISHED'}

def register():
	bpy.utils.register_module(__name__)
	Scene.mswap_threshold = FloatProperty(name = "Color Threshold", description = "How much a material's color can differ from fake-user materials", default = 0.08)

def unregister():
	bpy.utils.unregister_module(__name__)
	del Scene.mswap_threshold

if __name__ == "__main__":
	register()
