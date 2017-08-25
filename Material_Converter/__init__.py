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
	"name" : "Material Converter",
	"author" : "Tim Holmström",
	"version" : (0, 1, 1),
	"blender" : (2, 78, 0),
	"location" : "View3D > Tools Panel",
	"description" : "Convert materials to Cycles",
	"warning" : "",
	"wiki_url" : "",
	"tracker_url" : "",
	"category" : "User",
}


if "bpy" in locals():
	import imp
	if "convertpanel" in locals():
		imp.reload(convertpanel)
	if "matconvert" in locals():
		imp.reload(matconvert)
else:
	from . import convertpanel
	from . import matconvert

import bpy
from bpy.types import Scene
from bpy.props import StringProperty

def register():
	bpy.utils.register_module(__name__)
	Scene.MtlPath = StringProperty(name="Mtl File", attr="custompath", description="Path to mtl file", subtype="FILE_PATH")

def unregister():
	bpy.utils.unregister_module(__name__)
	del Scene.MtlPath

if __name__ == "__main__":
	register()
