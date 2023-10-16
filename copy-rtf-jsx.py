import bpy
from bpy.types import Panel, Operator
import unicodedata
import re

bl_info = {
    "name": "React Three Fiber Copy",
    "author": "@sinanisler",
    "version": (0, 1),
    "blender": (2, 93, 0),
    "location": "RTF Tab > Copy JSX",
    "description": "Copy scene objects in React Three Fiber JSX format",
    "category": "Copy",
}

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()

def format_name(name):
    # Remove accents
    name = remove_accents(name)
    
    # Replace spaces with camel case
    name = ''.join([word.capitalize() for word in name.split()])
    
    # Remove any non-English characters
    name = re.sub('[^A-Za-z0-9]+', '', name)
    return name


class EXPORT_OT_jsx(Operator):
    """Copy to React Three Fiber JSX"""
    bl_idname = "export.jsx_rtf"
    bl_label = "Copy JSX for RTF"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        # Get formatted object names and positions from the current scene
        formatted_objects = [
            f'<{format_name(obj.name)} position={{[{format(obj.location.x, ".4f")}, {format(obj.location.y, ".4f")}, {format(obj.location.z, ".4f")}]}} />'
            for obj in bpy.context.scene.objects
        ]
        
        # Join the formatted objects line by line
        jsx_content = "\n".join(formatted_objects)
        
        # Copy the content to clipboard
        bpy.context.window_manager.clipboard = jsx_content
        
        self.report({'INFO'}, "Object names and positions copied to clipboard!")
        return {'FINISHED'}





class RTF_PT_main_panel(Panel):
    """Main RTF Panel"""
    bl_idname = "RTF_PT_main_panel"
    bl_label = "RTF Exporter JSX Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "RTF"

    def draw(self, context):
        layout = self.layout
        layout.operator("export.jsx_rtf", text="Copy JSX")

def register():
    bpy.utils.register_class(EXPORT_OT_jsx)
    bpy.utils.register_class(RTF_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(RTF_PT_main_panel)
    bpy.utils.unregister_class(EXPORT_OT_jsx)

if __name__ == "__main__":
    register()
