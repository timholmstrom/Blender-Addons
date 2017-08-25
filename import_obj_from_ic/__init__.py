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
	"name" : "IronCAD Model Setup",
	"author" : "Tim Holmström",
	"version" : (0, 1, 0),
	"blender" : (2, 78, 0),
	"location" : "View3D > Tools Panel",
	"description" : "Centers, scales and separates object by materials.",
	"warning" : "",
	"wiki_url" : "",
	"tracker_url" : "",
	"category" : "User",
}

if "bpy" in locals():
	import imp
	if "modelcpanel" in locals():
		imp.reload(modelcpanel)
	if "modelconverters" in locals():
		imp.reload(modelconverters)
else:
	from . import modelcpanel
	from . import modelconverters

import bpy
from bpy.types import Scene
from bpy.props import FloatProperty

def register():
	bpy.utils.register_module(__name__)
	Scene.chose_obj_scale = FloatProperty(name = "Object Scale", description = "Chose what scale your objects gets", default = 0.001)

def unregister():
	bpy.utils.unregister_module(__name__)
	del Scene.chose_obj_scale

if __name__ == "__main__":
	register()
