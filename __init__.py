# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.



bl_info = {
    "name": "ShortPie",
    "description": "Quick pie menu for creating mesh.",
    "author": "skdsam",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Object Properties",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/skdsam/Shortpie",
    "category": "3D View"
}


###############   IMPORTS
import bpy
from bpy.utils import previews
import os
import math


###############   INITALIZE VARIABLES
###############   FUNCTIONS
def exec_line(line):
    exec(line)

def sn_print(tree_name, *args):
    if tree_name in bpy.data.node_groups:
        item = bpy.data.node_groups[tree_name].sn_graphs[0].prints.add()
        for arg in args:
            item.value += str(arg) + ";;;"
        if bpy.context and bpy.context.screen:
            for area in bpy.context.screen.areas:
                area.tag_redraw()
    print(*args)

def sn_cast_string(value):
    return str(value)

def sn_cast_boolean(value):
    if type(value) == tuple:
        for data in value:
            if bool(data):
                return True
        return False
    return bool(value)

def sn_cast_float(value):
    if type(value) == str:
        try:
            value = float(value)
            return value
        except:
            return float(bool(value))
    elif type(value) == tuple:
        return float(value[0])
    elif type(value) == list:
        return float(len(value))
    elif not type(value) in [float, int, bool]:
        try:
            value = len(value)
            return float(value)
        except:
            return float(bool(value))
    return float(value)

def sn_cast_int(value):
    return int(sn_cast_float(value))

def sn_cast_boolean_vector(value, size):
    if type(value) in [str, bool, int, float]:
        return_value = []
        for i in range(size):
            return_value.append(bool(value))
        return tuple(return_value)
    elif type(value) == tuple:
        return_value = []
        for i in range(size):
            return_value.append(bool(value[i]) if len(value) > i else bool(value[0]))
        return tuple(return_value)
    elif type(value) == list:
        return sn_cast_boolean_vector(tuple(value), size)
    else:
        try:
            value = tuple(value)
            return sn_cast_boolean_vector(value, size)
        except:
            return sn_cast_boolean_vector(bool(value), size)

def sn_cast_float_vector(value, size):
    if type(value) in [str, bool, int, float]:
        return_value = []
        for i in range(size):
            return_value.append(sn_cast_float(value))
        return tuple(return_value)
    elif type(value) == tuple:
        return_value = []
        for i in range(size):
            return_value.append(sn_cast_float(value[i]) if len(value) > i else sn_cast_float(value[0]))
        return tuple(return_value)
    elif type(value) == list:
        return sn_cast_float_vector(tuple(value), size)
    else:
        try:
            value = tuple(value)
            return sn_cast_float_vector(value, size)
        except:
            return sn_cast_float_vector(sn_cast_float(value), size)

def sn_cast_int_vector(value, size):
    return tuple(map(int, sn_cast_float_vector(value, size)))

def sn_cast_color(value, use_alpha):
    length = 4 if use_alpha else 3
    value = sn_cast_float_vector(value, length)
    tuple_list = []
    for data in range(length):
        data = value[data] if len(value) > data else value[0]
        tuple_list.append(sn_cast_float(min(1, max(0, data))))
    return tuple(tuple_list)

def sn_cast_list(value):
    if type(value) in [str, tuple, list]:
        return list(value)
    elif type(value) in [int, float, bool]:
        return [value]
    else:
        try:
            value = list(value)
            return value
        except:
            return [value]

def sn_cast_blend_data(value):
    if hasattr(value, "bl_rna"):
        return value
    elif type(value) in [tuple, bool, int, float, list]:
        return None
    elif type(value) == str:
        try:
            value = eval(value)
            return value
        except:
            return None
    else:
        return None

def sn_cast_enum(string, enum_values):
    for item in enum_values:
        if item[1] == string:
            return item[0]
        elif item[0] == string.upper():
            return item[0]
    return string


###############   IMPERATIVE CODE
#######   ShortPie
addon_keymaps = {}


###############   EVALUATED CODE
#######   ShortPie
class SNA_AddonPreferences_EC8E6(bpy.types.AddonPreferences):
    bl_idname = 'shortpie'
    menu_tabs: bpy.props.EnumProperty(name='menu tabs',description='menu tabs',options=set(),items=[('Links', 'Links', 'Links'), ('Settings', 'Settings', 'Settings')])

    def draw(self, context):
        try:
            layout = self.layout
            if bpy.context.preferences.addons['shortpie'].preferences.menu_tabs == r"Links":
                row = layout.row(align=False)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(bpy.context.preferences.addons['shortpie'].preferences,'menu_tabs',icon_value=0,text=r"menu tabs",emboss=True,expand=True,)
                layout.separator(factor=1.0)
                row = layout.row(align=False)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                col = row.column(align=False)
                col.enabled = True
                col.alert = False
                col.scale_x = 1.0
                col.scale_y = 2.0
                op = col.operator("wm.url_open",text=r"Discord Channel",emboss=True,depress=False,icon_value=bpy.context.scene.shortpie_icons['DISCORD'].icon_id)
                op.url = r"https://discord.gg/pPCXyqst"
                op = col.operator("wm.url_open",text=r"GitHub",emboss=True,depress=False,icon_value=227)
                op.url = r"https://github.com/skdsam/Shortpie"
                col = row.column(align=False)
                col.enabled = True
                col.alert = False
                col.scale_x = 1.0
                col.scale_y = 2.0
                op = col.operator("wm.url_open",text=r"Donate PayPal",emboss=True,depress=False,icon_value=bpy.context.scene.shortpie_icons['PAYPAL'].icon_id)
                op.url = r"https://www.paypal.com/paypalme/smiller1977/2"
                op = col.operator("wm.url_open",text=r"Blender Youtube",emboss=True,depress=False,icon_value=bpy.context.scene.shortpie_icons['YOUTUBE'].icon_id)
                op.url = r"https://www.youtube.com/c/BlenderFoundation"
            else:
                pass
            if bpy.context.preferences.addons['shortpie'].preferences.menu_tabs == r"Settings":
                row = layout.row(align=False)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(bpy.context.preferences.addons['shortpie'].preferences,'menu_tabs',icon_value=0,text=r"menu tabs",emboss=True,expand=True,)
                layout.separator(factor=1.0)
                col = layout.column(align=False)
                col.enabled = True
                col.alert = False
                col.scale_x = 1.0
                col.scale_y = 1.0
                col.label(text=r"Shortcut is =>   ctrl + shift + /",icon_value=0)
            else:
                pass
        except Exception as exc:
            print(str(exc) + " | Error in addon preferences")


class SNA_MT_tm_Pie_Menu_232A1(bpy.types.Menu):
    bl_idname = "SNA_MT_tm_Pie_Menu_232A1"
    bl_label = "tm Pie Menu"


    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        try:
            layout = self.layout
            layout = layout.menu_pie()
            op = layout.operator("mesh.primitive_cube_add",text=r"Create Cube",emboss=True,depress=False,icon_value=287)
            op.size = 2.0
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
            op = layout.operator("mesh.primitive_cylinder_add",text=r"Create Cylinder",emboss=True,depress=False,icon_value=293)
            op.vertices = 32
            op.radius = 1.0
            op.depth = 2.0
            op.end_fill_type = sn_cast_enum(r"NGON", [("NOTHING","Nothing","Don't fill at all"),("NGON","N-Gon","Use n-gons"),("TRIFAN","Triangle Fan","Use triangle fans"),])
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
            op = layout.operator("mesh.primitive_cone_add",text=r"Create Cone",emboss=True,depress=False,icon_value=295)
            op.vertices = 32
            op.radius1 = 1.0
            op.radius2 = 0.0
            op.depth = 2.0
            op.end_fill_type = sn_cast_enum(r"NGON", [("NOTHING","Nothing","Don't fill at all"),("NGON","N-Gon","Use n-gons"),("TRIFAN","Triangle Fan","Use triangle fans"),])
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
            op = layout.operator("mesh.primitive_torus_add",text=r"Create Torus",emboss=True,depress=False,icon_value=294)
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.major_segments = 48
            op.minor_segments = 12
            op.mode = sn_cast_enum(r"MAJOR_MINOR", [("MAJOR_MINOR","Major/Minor","Use the major/minor radii for torus dimensions"),("EXT_INT","Exterior/Interior","Use the exterior/interior radii for torus dimensions"),])
            op.major_radius = 1.0
            op.minor_radius = 0.25
            op.abso_major_rad = 1.25
            op.abso_minor_rad = 1.0
            op = layout.operator("mesh.primitive_ico_sphere_add",text=r"Create Ico Sphere",emboss=True,depress=False,icon_value=290)
            op.subdivisions = 2
            op.radius = 1.0
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
            op = layout.operator("mesh.primitive_uv_sphere_add",text=r"Create UV Sphere",emboss=True,depress=False,icon_value=289)
            op.segments = 32
            op.ring_count = 16
            op.radius = 1.0
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
            op = layout.operator("mesh.primitive_circle_add",text=r"Create Circle",emboss=True,depress=False,icon_value=288)
            op.vertices = 32
            op.radius = 1.0
            op.fill_type = sn_cast_enum(r"NOTHING", [("NOTHING","Nothing","Don't fill at all"),("NGON","N-Gon","Use n-gons"),("TRIFAN","Triangle Fan","Use triangle fans"),])
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
            op = layout.operator("mesh.primitive_plane_add",text=r"Create Plane",emboss=True,depress=False,icon_value=286)
            op.size = 2.0
            op.calc_uvs = True
            op.enter_editmode = False
            op.align = sn_cast_enum(r"WORLD", [("WORLD","World","Align the new object to the world"),("VIEW","View","Align the new object to the view"),("CURSOR","3D Cursor","Use the 3D cursor orientation for the new object"),])
            op.location = bpy.context.scene.cursor.location
            op.rotation = (0.0, 0.0, 0.0)
            op.scale = (1.0, 1.0, 1.0)
        except Exception as exc:
            print(str(exc) + " | Error in tm Pie Menu pie menu")

def register_key_3798F():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
        kmi = km.keymap_items.new("wm.call_menu_pie",
                                    type= "BACK_SLASH",
                                    value= "PRESS",
                                    repeat= False,
                                    ctrl=True,
                                    alt=False,
                                    shift=True)
        kmi.properties.name = "SNA_MT_tm_Pie_Menu_232A1"
        addon_keymaps['3798F'] = (km, kmi)


###############   REGISTER ICONS
def sn_register_icons():
    icons = ["DISCORD","PAYPAL","YOUTUBE",]
    bpy.types.Scene.shortpie_icons = bpy.utils.previews.new()
    icons_dir = os.path.join( os.path.dirname( __file__ ), "icons" )
    for icon in icons:
        bpy.types.Scene.shortpie_icons.load( icon, os.path.join( icons_dir, icon + ".png" ), 'IMAGE' )

def sn_unregister_icons():
    bpy.utils.previews.remove( bpy.types.Scene.shortpie_icons )


###############   REGISTER PROPERTIES
def sn_register_properties():
    pass

def sn_unregister_properties():
    pass


###############   REGISTER ADDON
def register():
    sn_register_icons()
    sn_register_properties()
    bpy.utils.register_class(SNA_AddonPreferences_EC8E6)
    bpy.utils.register_class(SNA_MT_tm_Pie_Menu_232A1)
    register_key_3798F()


###############   UNREGISTER ADDON
def unregister():
    sn_unregister_icons()
    sn_unregister_properties()
    for key in addon_keymaps:
        km, kmi = addon_keymaps[key]
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_MT_tm_Pie_Menu_232A1)
    bpy.utils.unregister_class(SNA_AddonPreferences_EC8E6)