import bpy

class IronCadPanel(bpy.types.Panel):
    """Panel for converting 3D CAD models"""
    bl_label = "IronCAD Model Setup"
    bl_idname = "OBJECT_PT_cmspanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Material"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("import_scene.obj")

        row = layout.separator()

        row = layout.row()
        row.operator("object.multi_operator")

        row = layout.row()
        row.prop(context.scene, "chose_obj_scale")

        row = layout.separator()
        row = layout.separator()
        
        row = layout.row()
        row.operator("object.scale_transform")

        row = layout.row()
        row.operator("object.add_parent_cube")

        row = layout.row()
        row.operator("object.separate_by_material")

        row = layout.separator()
