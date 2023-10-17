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
    name = remove_accents(name)
    name = ''.join([word.capitalize() for word in name.split()])
    name = re.sub('[^A-Za-z0-9]+', '', name)
    return name



def get_primitive_name(obj):
    blender_to_r3f = {
        "Cube": "boxGeometry",
        "UV Sphere": "sphereGeometry",
        "Icosphere": "icosahedronGeometry",
        "Cylinder": "cylinderGeometry",
        "Cone": "coneGeometry",
        "Torus": "torusGeometry",
        "Plane": "plane",
        "Circle": "circleGeometry",
        # ... (additional mappings if necessary)
    }
    object_type = obj.type
    if object_type == "MESH" and obj.data.name in blender_to_r3f:
        return blender_to_r3f[obj.data.name]
    else:
        return None  # Return None if no matching primitive is found




class EXPORT_OT_jsx(Operator):
    """Copy to React Three Fiber JSX"""
    bl_idname = "export.jsx_rtf"
    bl_label = "Copy JSX for RTF"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        formatted_objects = []

        for obj in bpy.context.scene.objects:
            primitive_name = get_primitive_name(obj)
            if primitive_name is not None:  # Only add JSX for recognized primitives
                formatted_objects.append(
                    f'''
    <mesh position={{[{format(obj.location.x, ".4f")}, {format(obj.location.y, ".4f")}, {format(obj.location.z, ".4f")}]}}>
      <{primitive_name}  />
      <meshStandardMaterial color="gray" />
    </mesh>
                    '''
                )
            elif obj.type == 'LAMP':
                light_type = obj.data.type
                if light_type == 'POINT':
                    formatted_objects.append(
                        f'<pointLight position={{[{format(obj.location.x, ".4f")}, {format(obj.location.y, ".4f")}, {format(obj.location.z, ".4f")}]}} />\n'
                    )
                elif light_type == 'SUN':
                    formatted_objects.append(
                        f'<ambientLight />\n'
                    )
                # ... (additional conditions for other light types if necessary)
            elif obj.type == 'CAMERA':
                formatted_objects.append(
                    f'<Camera position={{[{format(obj.location.x, ".4f")}, {format(obj.location.y, ".4f")}, {format(obj.location.z, ".4f")}]}} />\n'
                )
            # ... (additional conditions for other object types if necessary)

        jsx_content = "".join(formatted_objects)
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
