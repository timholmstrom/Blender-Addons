import bpy
from bpy.types import Panel

class MaterialConvertPanel(Panel):
    bl_label = "Material Converter"
    bl_idname = "OBJECT_PT_materialconvert_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Material"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.mtl_to_cycles")


        row = layout.row()
        row.prop(context.scene, "MtlPath")
