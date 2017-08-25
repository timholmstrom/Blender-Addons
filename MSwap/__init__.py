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
	"version" : (0, 0, 1),
	"blender" : (2, 78, 0),
	"location" : "View3D > Tools Panel",
	"description" : "Swaps current material for matching fake-user material.",
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
from bpy.types import Scene
from bpy.props import FloatProperty

def register():
	bpy.utils.register_module(__name__)
	Scene.mswap_threshold = FloatProperty(name = "Color Threshold", description = "How much a material's color can differ from fake-user materials", default = 0.08)


def unregister():
	bpy.utils.unregister_module(__name__)
	del Scene.mswap_threshold


if __name__ == "__main__":
	register()
