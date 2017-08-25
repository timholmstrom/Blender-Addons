import bpy
from bpy.types import Panel

class MSwapPanel(Panel):
    """Panel for MSwap"""
    bl_label = "MSwap"
    bl_idname = "OBJECT_PT_mswap_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Material"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.material_swap")

        row = layout.row()
        row.prop(context.scene, "mswap_threshold")
