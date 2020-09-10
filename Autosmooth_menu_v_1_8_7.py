# ##### BEGIN GPL LICENSE BLOCK #####
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
# ##### END GPL LICENSE BLOCK #####

from bpy.props import FloatProperty, BoolProperty
from math import radians, degrees
import bmesh
import rna_keymap_ui
import bpy

bl_info = {
    "name": " Autosmooth Menu",
    "author": "1COD",
    "version": (1, 8, 8),
    "blender": (2, 83, 0),
    "location": "View3D",
    "description": "Autosmooth menu, Alt X",
    "warning": "",
    "wiki_url": "",
    "category": "Menu"
}


# Faces Orientation
def get_face_orientation(self):

    return bpy.context.space_data.overlay.show_face_orientation


def set_face_orientation(self, value):

    pass

def update_face_orientation(self, context):
    
    if context.scene.show_faces_orientation is False:
        context.space_data.overlay.show_overlays = True
        bpy.context.scene.show_xray = False
        context.space_data.overlay.show_face_orientation = True    

    else:
        context.space_data.overlay.show_face_orientation = False

bpy.types.Scene.show_faces_orientation = bpy.props.BoolProperty(
    get=get_face_orientation,
    set=set_face_orientation,
    update=update_face_orientation
)

# Shadesmooth (sculpt)
def get_smooth(self):

    if bpy.context.selected_objects:
        return (bpy.context.object.data.polygons[0].use_smooth)
    else:
        return False

    return True

def set_smooth(self, value):

    bpy.context.object.data.polygons[0].use_smooth = value

def update_smooth(self, context):

    if context.scene.shadesmooth_toggle:
        for poly in context.object.data.polygons:
            poly.use_smooth = True
        context.scene.tool_settings.sculpt.use_smooth_shading = True
    else:
        for poly in context.object.data.polygons:
            poly.use_smooth = False        
        context.scene.tool_settings.sculpt.use_smooth_shading = False

bpy.types.Scene.shadesmooth_toggle = bpy.props.BoolProperty(
    get=get_smooth,
    set=set_smooth,
    update=update_smooth,
    description="Shade Flat/Smooth toggle"
)


# Autosmooth
def get_autosmooth(self):

    for e in bpy.context.selected_objects:
        if e.type == "MESH":
            if e.data.use_auto_smooth == False:
                return False
    if len([obj for obj in bpy.context.selected_objects if obj.type == 'MESH']) == 0:
        return False
    return True     


def set_autosmooth(self, value):

    for e in bpy.context.selected_objects:
        if e.type == "MESH":
            if e.data.use_auto_smooth == False:
                e.data.use_auto_smooth = value
            else:
                list(bpy.context.selected_objects)[0].data.use_auto_smooth = value


def update_autosmooth(self, context):

    for e in context.selected_objects:
        if e.type == "MESH":
        # dont need to set if context.object because by default autosmooth do it
            e.data.use_auto_smooth = bool(context.scene.autosmooth_toggle)
        
    if context.object.mode == 'SCULPT':
        
        context.scene.autosmooth_toggle       

bpy.types.Scene.autosmooth_toggle = bpy.props.BoolProperty(
    get=get_autosmooth,
    set=set_autosmooth,
    update=update_autosmooth
)


# Autosmooth Angle
def get_autosmoothangle(self):
    
    for e in bpy.context.selected_objects:
        if e.type == "MESH":
            return (round(degrees(e.data.auto_smooth_angle), 1))
        else:
            return 0
    return True


def set_autosmoothangle(self, value):

    if bpy.context.object and bpy.context.object.type == "MESH":
        bpy.context.scene.Temp = value


def update_autosmoothangle(self, context):

    for e in context.selected_objects:
        if e.type == 'MESH':
            e.data.auto_smooth_angle = radians(context.scene.Temp)
            if e.data.auto_smooth_angle != radians(context.scene.Temp):
                e.data.auto_smooth_angle = radians(context.scene.Temp)


bpy.types.Scene.Temp = bpy.props.FloatProperty(
    default=30, min=0, max=180, precision=1)
bpy.types.Scene.autosmoothangle = bpy.props.FloatProperty(default=30, min=0, max=180,
                                                          precision=1,
                                                          get=get_autosmoothangle,
                                                          set=set_autosmoothangle,
                                                          update=update_autosmoothangle)


# Overlay toggle
def get_overlay_toggle(self):

    return bpy.context.space_data.overlay.show_overlays


def set_overlay_toggle(self, value):

    bpy.context.space_data.overlay.show_overlays = value


def update_overlay_toggle(self, context):

    context.space_data.overlay.show_overlays = bool(
        context.scene.overlays_toggle)


bpy.types.Scene.overlays_toggle = bpy.props.BoolProperty(
    get=get_overlay_toggle,
    set=set_overlay_toggle,
    update=update_overlay_toggle
)


# Wireframe toggle
def get_wireframe_toggle(self):

    return bpy.context.space_data.overlay.show_wireframes


def set_wireframe_toggle(self, value):

    bpy.context.space_data.overlay.show_wireframes = value


def update_wireframe_toggle(self, context):

    context.space_data.overlay.show_wireframes = bool(
        context.scene.show_wireframes)


bpy.types.Scene.show_wireframes = bpy.props.BoolProperty(
    get=get_wireframe_toggle,
    set=set_wireframe_toggle,
    update=update_wireframe_toggle
)


# Xray toggle
def get_xray_toggle(self):

    if bpy.context.space_data.shading.type == 'WIREFRAME':
        return bpy.context.space_data.shading.show_xray_wireframe
    else:
        return bpy.context.space_data.shading.show_xray


def set_xray_toggle(self, value):

    if bpy.context.space_data.shading.type == 'WIREFRAME':
        bpy.context.space_data.shading.show_xray_wireframe = value
    else:
        bpy.context.space_data.shading.show_xray = value


def update_xray_toggle(self, context):

    if context.space_data.shading.type == 'WIREFRAME':
        context.space_data.shading.show_xray_wireframe = bool(context.scene.show_xray)

    else:
        context.space_data.shading.show_xray = bool(context.scene.show_xray)


bpy.types.Scene.show_xray = bpy.props.BoolProperty(
    get=get_xray_toggle,
    set=set_xray_toggle,
    update=update_xray_toggle
)


# alpha Xray
def get_xray_alpha(self):

    if bpy.context.space_data.shading.type == 'WIREFRAME':
        return bpy.context.space_data.shading.xray_alpha_wireframe
    else:
        return bpy.context.space_data.shading.xray_alpha


def set_xray_alpha(self, value):

    if bpy.context.space_data.shading.type == 'WIREFRAME':
        bpy.context.scene.Temp1 = value
    else:
        bpy.context.scene.Temp2 = value


def update_xray_alpha(self, context):

    if context.space_data.shading.type == 'WIREFRAME':
        context.space_data.shading.xray_alpha_wireframe = context.scene.Temp1

    else:
        context.space_data.shading.xray_alpha = bpy.context.scene.Temp2


bpy.types.Scene.Temp1 = bpy.props.FloatProperty()
bpy.types.Scene.Temp2 = bpy.props.FloatProperty()
bpy.types.Scene.xray_alpha = FloatProperty(
    name="Alpha",
    description="set transparency",
    min=0.01, max=1,
    default=1,
    get=get_xray_alpha,
    set=set_xray_alpha,
    update=update_xray_alpha,
    precision=1
)


class TOGGLE_OT_Normals(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "toggle.normals_operator"
    bl_label = "Toggle Normals"
    bl_options = {'REGISTER', 'UNDO'}

    out_flip: bpy.props.BoolProperty(default=True)

    def execute(self, context):

        faces = []

        if context.selected_objects:
            objects = [
                object for object in context.selected_objects if object.type == 'MESH']
        else:
            objects = [
                object for object in context.scene.objects if object.type == 'MESH']

        for object in objects:
            me = object.data

            bm = bmesh.new()
            bm.from_mesh(me)
            if self.out_flip:
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            else:
                bmesh.ops.reverse_faces(
                    bm, faces=bm.faces[:], flip_multires=True)
            bm.to_mesh(me)
            # trick: something light to update object mode
            context.scene.tool_settings.use_transform_pivot_point_align ^= True
            context.scene.tool_settings.use_transform_pivot_point_align ^= True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if context.mode == 'EDIT_MESH':
            text = '> normals out' if self.out_flip else '> flip normals'
        if context.object.mode == 'OBJECT':
            text = '> all normals out' if self.out_flip else '> flip all normals'
        layout.prop(self, "out_flip", text=text)


bpy.types.Scene.checkboxnormals = bpy.props.BoolProperty()  # for the panel


# select/unselect
def get_select(self):

    if bpy.context.mode == 'EDIT_MESH':

        mesh = bmesh.from_edit_mesh(bpy.context.object.data)

        return not len([v for v in mesh.verts if v.select]) == 0

    else:
        return not len([obj for obj in bpy.context.selected_objects if obj.type == 'MESH']) == 0


def set_select(self, value):

    pass

def update_select(self, context):

    if bpy.context.mode == 'EDIT_MESH':

        if context.scene.select_toggle:

            bpy.ops.mesh.select_all(action='DESELECT')
        else:
            bpy.ops.mesh.select_all(action='SELECT')

    else:
        if context.scene.select_toggle:

            bpy.ops.object.select_all(action='DESELECT')
        else:
            bpy.ops.object.select_all(action='SELECT')


bpy.types.Scene.select_toggle = bpy.props.BoolProperty(
    set=set_select,
    get=get_select,
    update=update_select
)


# Vertex/E/F toggle
class VEF_OT_toggle(bpy.types.Operator):
    bl_idname = "vef.toggle"
    bl_label = "verts/edg/faces toggle"

    def execute(self, context):

        selectionMode = (bpy.context.scene.tool_settings.mesh_select_mode)

        if selectionMode[0]:
            bpy.ops.mesh.select_mode(type='EDGE')
        elif selectionMode[1]:
            bpy.ops.mesh.select_mode(type='FACE')
        else:
            bpy.ops.mesh.select_mode(type='VERT')

        return {'FINISHED'}
        
#select NGONS
class NGON_OT_select(bpy.types.Operator):
    bl_idname = "ngons.select"
    bl_label = "select Ngons"
    
    def execute(self, context):

        cao = context.active_object
        bm = bmesh.from_edit_mesh(cao.data)
        bm.normal_update()

        for f in bm.faces:
            f.select = False
        bm.select_flush(False)

        faces = [f for f in bm.faces if len(f.verts) > 4]

        for f in faces:
            f.select = True

        bmesh.update_edit_mesh(cao.data)
        
        return {'FINISHED'}


class TRIS_OT_select(bpy.types.Operator):
    bl_idname = "tris.select"
    bl_label = "select Triangles"
    
    def execute(self, context):

        cao = context.active_object
        bm = bmesh.from_edit_mesh(cao.data)
        bm.normal_update()

        for f in bm.faces:
            f.select = False
        bm.select_flush(False)

        faces = [f for f in bm.faces if len(f.verts) == 3]

        for f in faces:
            f.select = True

        bmesh.update_edit_mesh(cao.data)
        
        return {'FINISHED'}


# toggle shading
def get_toggle_shading(self):

    return bpy.context.space_data.shading.type == 'WIREFRAME'

def set_toggle_shading(self, value):

    pass

def update_toggle_shading(self, context):

    bpy.ops.view3d.toggle_shading(type='WIREFRAME')

bpy.types.Scene.toggle_shading = bpy.props.BoolProperty(
    default=False,
    get=get_toggle_shading,
    set=set_toggle_shading,
    update=update_toggle_shading)


# Unmark all
class UNMARK_OT_All(bpy.types.Operator): ###
    bl_idname = "unmark.all"
    bl_label = "Clear all marks"
    bl_options = {'REGISTER', 'UNDO'}

    ex_sharp: BoolProperty(default=False, name="sharp")
    ex_bvl: BoolProperty(default=False, name="bevel")
    ex_crs: BoolProperty(default=False, name="crease")
    ex_seam: BoolProperty(default=False, name="seam")

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):

        for obj in context.selected_objects:
            if obj.type == "MESH":
                me = obj.data
                bm = bmesh.from_edit_mesh(me)            
                bv = bm.edges.layers.bevel_weight.verify()
                cr = bm.edges.layers.crease.verify()

                bm.select_mode = {'FACE'}
                for e in bm.edges:
                    bm.select_mode = {'EDGE'}
                    if e.select == True:
                        
                        if self.ex_sharp:
                            if not e.smooth:
                                e.smooth = True

                        if self.ex_bvl:                        
                            if e[bv] > 0:
                                e[bv] = 0

                        if self.ex_crs:                        
                            if e[cr] > 0:
                                e[cr] = 0

                        if self.ex_seam:
                            if e.seam:
                                e.seam = False

                bmesh.update_edit_mesh(me, False)

        return {'FINISHED'}


# Sharpangle select
def update_sharpangle(self, context):

    if context.scene.mark_type=="bevel":
        update_markbevel(self, context)
        if bpy.context.scene.sharpangle == 0 and context.scene.inverseur:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.edge_bevelweight(value=-1)
            bpy.ops.mesh.select_all(action='DESELECT')
            
    if context.scene.mark_type=="sharp":
        update_marksharp(self, context)
        if bpy.context.scene.sharpangle == 0 and context.scene.inverseur:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
        
    if context.scene.mark_type=="crease":
        update_markcrease(self, context)
        if bpy.context.scene.sharpangle == 0 and context.scene.inverseur:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.edge_crease(value=-1)
            bpy.ops.mesh.select_all(action='DESELECT')
            
    if context.scene.mark_type=="seam":
        update_markseam(self, context)
        if bpy.context.scene.sharpangle == 0 and context.scene.inverseur:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_seam(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            
    if context.scene.mark_type=="none":
        selectsharpedge(self, context)
        if bpy.context.scene.sharpangle == 0 and context.scene.inverseur:
            bpy.ops.mesh.select_all(action='DESELECT')


def selectsharpedge(self, context):

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.edges_select_sharp(
        sharpness=radians(context.scene.sharpangle))
    if context.scene.inverseur:
        bpy.ops.mesh.select_all(action='INVERT')


def update_inverseur(self, context):

    bpy.ops.mesh.select_all(action='INVERT')
    if context.scene.mark_type=="bevel":
        update_markbevel(self, context)
    if context.scene.mark_type=="crease":
        update_markcrease(self, context)
    if context.scene.mark_type=="sharp":
        update_marksharp(self, context)
    if context.scene.mark_type=="seam":
        update_markseam(self, context)
    if context.scene.mark_type=="none":
        selectsharpedge(self, context)


def update_marksharp(self, context):

    if context.scene.mark_type=="sharp":
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        if context.scene.inverseur:
            bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.mark_sharp(clear=False)

def update_markbevel(self, context):

    if context.scene.mark_type=="bevel":
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.edge_bevelweight(value=-1)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        if context.scene.inverseur:
            bpy.ops.mesh.select_all(action='INVERT')
        update_bevelWeight(self, context)


def update_markcrease(self, context):

    if context.scene.mark_type=="crease":
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.edge_crease(value=-1)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        if context.scene.inverseur:
            bpy.ops.mesh.select_all(action='INVERT')
        update_edgeCrease(self, context)

def update_markseam(self, context):

    if context.scene.mark_type=="seam":
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        if context.scene.inverseur:
            bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.mark_seam(clear=False)


def update_bevelWeight(self, context):

    for obj in context.selected_objects:
        if obj.type == "MESH":
            context.view_layer.objects.active = obj
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            bv = bm.edges.layers.bevel_weight.verify()
            
            bm.select_mode = {'EDGE'}
            for e in bm.edges:
                if e.select == True:
                    e[bv] = context.scene.bevelWeight

            bmesh.update_edit_mesh(me)


def update_edgeCrease(self, context):

    for obj in context.selected_objects:
        if obj.type == "MESH":
            context.view_layer.objects.active = obj
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            cr = bm.edges.layers.crease.verify()
            sel=[]
            
            bm.select_mode = {'EDGE'}
            for e in bm.edges:
                if e.select == True:                
                    e[cr] = context.scene.edgeCrease
                    e.select = True

            bmesh.update_edit_mesh(me, False, False)

bpy.types.Scene.bevelWeight = bpy.props.FloatProperty(
    description="Set Bevel Weight",
    name="bevelWeight",
    min=0.0,
    max=1.0,
    step=0.01,
    default=1,
    update=update_bevelWeight
)

bpy.types.Scene.edgeCrease = bpy.props.FloatProperty(
    description="Set Crease Weight",
    name="edgeCrease",
    min=0.0,
    max=1.0,
    step=0.01,
    default=1,
    update=update_edgeCrease
)

bpy.types.Scene.sharpangle = bpy.props.FloatProperty(
    default=180, min=0, max=180, precision=2,
    update=update_sharpangle
)
bpy.types.Scene.inverseur = bpy.props.BoolProperty(update=update_inverseur)


# sel marked edges
def sel_bevel(self, context):

    if context.scene.mark_type=="bevel":

        for obj in context.selected_objects:
            if obj.type == "MESH":
                me = obj.data
                bm = bmesh.from_edit_mesh(me)
                bv = bm.edges.layers.bevel_weight.verify()

                bm.select_mode = {'FACE'}
                for e in bm.edges:
                    bm.select_mode = {'EDGE'}
                    if context.scene.inverseur1 == False:
                        if e[bv] >= context.scene.threshold_bevel_select and e[bv] > 0:
                            e.select = True
                        else:
                            e.select = False
                    else:
                        if e[bv] <= context.scene.threshold_bevel_select and e[bv] > 0:
                            e.select = True
                        else:
                            e.select = False


                bmesh.update_edit_mesh(me, False, False)

bpy.types.Scene.selbevel = bpy.props.BoolProperty(update=sel_bevel)

bpy.types.Scene.threshold_bevel_select = bpy.props.FloatProperty(
    description="Set threshold of bevel selection",
    name="BevelWeight threshold",
    min=0,
    max=1,
    precision=2,
    default=1,
    update=sel_bevel
)


def sel_crease(self, context):

    if context.scene.mark_type=="crease":

        for obj in context.selected_objects:
            if obj.type == "MESH":
                me = obj.data
                bm = bmesh.from_edit_mesh(me)
                
                cr = bm.edges.layers.crease.verify()

                bm.select_mode = {'FACE'}
                for e in bm.edges:
                    bm.select_mode = {'EDGE'}
                    if context.scene.inverseur1 == False:
                        if e[cr] >= context.scene.threshold_crease_select and e[cr] > 0:
                            e.select = True
                        else:
                            e.select = False
                    else:
                        if e[cr] <=  context.scene.threshold_crease_select and e[cr] > 0:
                            e.select = True
                        else:
                            e.select = False

                bmesh.update_edit_mesh(me, False, False)

bpy.types.Scene.selcrease = bpy.props.BoolProperty(
    update=sel_crease)

bpy.types.Scene.threshold_crease_select = bpy.props.FloatProperty(
    description="Set threshold of crease selection",
    name="CreaseWeight threshold",
    min=0,
    max=1.00001,
    precision=2,
    default=1,
    update=sel_crease
)

def sel_sharp(self, context):

    if context.scene.mark_type=="sharp":

        for obj in context.selected_objects:
            if obj.type == "MESH":
                me = obj.data
                bm = bmesh.from_edit_mesh(me)

                for e in bm.edges:
                    if not e.smooth:
                        e.select = True

                bmesh.update_edit_mesh(me, False)

bpy.types.Scene.selsharp = bpy.props.BoolProperty(update=sel_sharp)


def sel_seam(self, context):

    if context.scene.mark_type=="seam":

        for obj in context.selected_objects:
            if obj.type == "MESH":
                me = obj.data
                bm = bmesh.from_edit_mesh(me)

                for e in bm.edges:
                    if e.seam:
                        e.select = True

                bmesh.update_edit_mesh(me, False)

bpy.types.Scene.selseam = bpy.props.BoolProperty(update=sel_seam)


def update_inverseur1(self, context):

    bpy.ops.mesh.select_all(action='DESELECT')
    if context.scene.mark_type=="bevel":
        sel_bevel(self, context)
    if context.scene.mark_type=="crease":
        sel_crease(self, context)

bpy.types.Scene.inverseur1 = bpy.props.BoolProperty(update=update_inverseur1)

edge_mode = [
    ("0", "Select Edg & Mark:", "OFF"),
    (None),
    ("1", "Mark by angle", "Select & Mark edges by angle"),
    ("3", "Select Marked Edg", "Get selection of Marked edges"),
    ("2", "Mark Selected", "Mark selection"),
]


def update_enum(self, context):
    
    context.scene.mark_type = "none"

bpy.types.Scene.edge_mode = bpy.props.EnumProperty(
    name="",
    description="Select & Mark, Select Marked",
    items=edge_mode,
    update=update_enum
)

mark_type = [
    ("none", "None", "No type"),
    (None),
    ("bevel", "Bevel", "Bevel"),
    ("sharp", "Sharp", "Sharp"),
    ("crease", "Crease", "Crease"),
    ("seam", "Seam", "Seam")    
]


def update_enum1(self, context):

    if context.scene.edge_mode=="1":
        context.tool_settings.mesh_select_mode = (False, True, False)
        if context.scene.mark_type=="none":
            selectsharpedge(context.scene, context)
        if context.scene.mark_type=="bevel":
            update_markbevel(context.scene, context)
        if context.scene.mark_type=="crease":
            update_markcrease(context.scene, context)
        if context.scene.mark_type=="sharp":
            update_marksharp(context.scene, context)
        if context.scene.mark_type=="seam":
            update_markseam(context.scene, context)

    if context.scene.edge_mode=="2":
        context.tool_settings.mesh_select_mode = (False, True, False)
        if context.scene.mark_type=="bevel":
            update_bevelWeight(context.scene, context)
        if context.scene.mark_type=="crease":
            update_edgeCrease(context.scene, context)
        if context.scene.mark_type=="sharp":
            bpy.ops.mesh.mark_sharp(clear=False)
        if context.scene.mark_type=="seam":
            bpy.ops.mesh.mark_seam(clear=False)         
        
    if context.scene.edge_mode=="3":
        context.tool_settings.mesh_select_mode = (False, True, False)
        if context.scene.mark_type=="bevel":
            sel_bevel(self, context)
        if context.scene.mark_type=="crease":
            sel_crease(self, context)
        if context.scene.mark_type=="sharp":
            sel_sharp(self, context)
        if context.scene.mark_type=="seam":
            sel_seam(self, context)

bpy.types.Scene.mark_type = bpy.props.EnumProperty(
    name="",
    description="Select & Mark, Select Marked",
    items=mark_type,
    update=update_enum1
)


class REPEAT_OT_same_mark(bpy.types.Operator):
    bl_idname = "repeat.mark"
    bl_label = "repeat mark"

    def execute(self,context):
        update_enum1(self, context)
        return {'FINISHED'}


# show more love  
def show_more_love(self, context):  ##TO UPDATE  
    cao = bpy.context.active_object

    if context.scene.love:

        if len([m for m in bpy.context.object.modifiers if m.type == "BEVEL"]) < 1:
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
            bpy.context.object.modifiers["Bevel"].segments = 1
            bpy.context.object.modifiers["Bevel"].miter_outer = 'MITER_PATCH'

        if len([m for m in bpy.context.object.modifiers if m.type == "SUBSURF"]) < 1:
            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subdivision"].show_on_cage = True

        bpy.ops.mesh.select_all(action='DESELECT')
        mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
        for v in mesh.faces:
            v.select = True
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='VERT')
        bpy.context.scene.sharpangle = 9.57447
        bpy.context.scene.markbevel = True

        if bpy.context.scene.autosmooth_toggle == False:
            bpy.context.scene.autosmooth_toggle = True
        bpy.context.object.data.auto_smooth_angle = 0.767546

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)
        bpy.ops.object.editmode_toggle()
        if bpy.context.space_data.overlay.show_overlays == True:
            bpy.context.space_data.overlay.show_overlays = False
        bpy.context.scene.objects.active = bpy.context.scene.objects.active

    else:

        bpy.ops.object.modifier_remove(modifier="Subdivision")
        bpy.ops.object.modifier_remove(modifier="Bevel")
        bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.faces_shade_flat()
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.transform.edge_bevelweight(value=-1)
        bpy.ops.transform.edge_crease(value=-1)
        if context.scene.inverseur == True:
            context.scene.inverseur = False
        if bpy.context.space_data.overlay.show_overlays == False:
            bpy.context.space_data.overlay.show_overlays = True
        bpy.context.object.data.auto_smooth_angle = 3.14159
        bpy.ops.mesh.select_all(action='DESELECT')


bpy.types.Scene.love = bpy.props.BoolProperty(
    update=show_more_love,
    description="add subsurf and bevel modifiers\n+few settings"
)


# Panel
class AUTOSMOOTH_PT_Menu(bpy.types.Panel):
    bl_label = "Autosmooth menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "0data"  # not valid name to hide it
    bl_options = {'DEFAULT_CLOSED'}
    
    # @classmethod
    # def poll(cls, context):
        # return context.object and bpy.context.selected_objects

    def draw(self, context):
        layout = self.layout

        if context.mode in {'OBJECT'}:
            obj_data = context.active_object.data
            row = layout.row()
            row.label(text="Object Mode")
            row.scale_y = 0.8
            row.operator("object.editmode_toggle",
                         text="", icon='ARROW_LEFTRIGHT')
            row = layout.row(align=True)
            row.operator("object.shade_smooth")
            row.operator("object.shade_flat")
            row = layout.row(align=True)
            if context.scene.autosmooth_toggle == False:
                row.prop(context.scene, "autosmooth_toggle",
                         text="Auto Smooth")
            if context.scene.autosmooth_toggle:
                sub = row.row()
                sub.scale_x = 0.7
                sub.prop(context.scene, "autosmooth_toggle",
                         text="Auto Smooth")
                row.prop(context.scene, "autosmoothangle",
                         text="AS angle", slider=True)

            row = layout.row()
            row.prop(context.scene, "select_toggle",
                     text="", icon='SELECT_SET')
            row.operator("object.select_all", text="",
                         icon='EVENT_TAB').action = 'INVERT'
            row = layout.row()
            row.prop(context.scene, "show_faces_orientation",
                     text="", icon='EVENT_O', toggle=True)
            row.prop(context.scene, "toggle_shading",
                     text="", icon='SHADING_WIRE', toggle=True)
            row.prop(context.scene, "show_xray", text="", icon='XRAY')
            if context.scene.show_xray:
                sub = row.row()
                sub.scale_x = 0.2
                # ,α,slider=True)
                sub.prop(context.scene, "xray_alpha", text="")

            row.prop(context.scene, "overlays_toggle", text="", icon='OVERLAY')
            row.prop(context.scene, "show_wireframes", text="", icon='EVENT_W')
            row = layout.row(align=True)
            row.prop(context.scene, "checkboxnormals",
                     text="Recalculate Normals")  # , description="no selection=whole scene")
            if context.scene.checkboxnormals == True:
                op = row.operator("toggle.normals_operator",
                                  text="Normals OUT")
                op.out_flip = True
                op1 = row.operator("toggle.normals_operator",
                                   icon='FILE_REFRESH', text="")
                op1.out_flip = False

        elif context.mode in {'SCULPT'}:
            obj_data = context.active_object.data
            layout.label(text="Sculpt Mode")
            label = "Shade Smooth ON" if context.scene.shadesmooth_toggle else "Shade Smooth OFF"
            layout.prop(context.scene, "shadesmooth_toggle",
                        text=label, toggle=True)
            row = layout.row(align=True)
            if context.scene.autosmooth_toggle == False:
                row.prop(context.scene, "autosmooth_toggle",
                         text="Auto Smooth")
            if context.scene.autosmooth_toggle:
                sub = row.row()
                sub.scale_x = 0.7
                sub.prop(context.scene, "autosmooth_toggle",
                         text="Auto Smooth")
                row.prop(context.scene, "autosmoothangle",
                         text="AS angle", slider=True)
            layout.separator()
            row = layout.row()
            row.prop(context.scene, "show_faces_orientation",
                     text="", icon='EVENT_O', toggle=True)
            row.prop(context.scene, "toggle_shading",
                     text="", icon='SHADING_WIRE', toggle=True)
            row.prop(context.scene, "show_xray", text="", icon='XRAY')
            if context.scene.show_xray:
                sub = row.row()
                sub.scale_x = 0.2
                sub.prop(context.scene, "xray_alpha", text="")
            row.prop(context.scene, "overlays_toggle", text="", icon='OVERLAY')
            row.prop(context.scene, "show_wireframes", text="", icon='EVENT_W')

        else:  # edit mode
            obj_data = context.active_object.data
            row = layout.row()
            row.label(text="Edit Mode")
            row.scale_y = 0.8
            row.prop(context.scene, "love", text="", icon='HEART')
            row.operator("object.editmode_toggle",
                         text="", icon='ARROW_LEFTRIGHT')
            row = layout.row(align=True)
            row.operator("mesh.faces_shade_smooth")
            row.operator("mesh.faces_shade_flat")
            row = layout.row(align=True)
            if context.scene.autosmooth_toggle == False:
                row.prop(context.scene, "autosmooth_toggle",
                         text="Auto Smooth")
            if context.scene.autosmooth_toggle:
                sub = row.row()
                sub.scale_x = 0.7
                sub.prop(context.scene, "autosmooth_toggle",
                         text="Auto Smooth")
                row.prop(context.scene, "autosmoothangle",
                         text="AS angle", slider=True)
            row = layout.row()
            row.prop(context.scene, "select_toggle",
                     text="", icon='SELECT_SET')
            row.operator("mesh.select_all", text="",
                         icon='EVENT_TAB').action = 'INVERT'
            icon = 'VERTEXSEL'if bpy.context.scene.tool_settings.mesh_select_mode[
                0] else 'EDGESEL' if bpy.context.scene.tool_settings.mesh_select_mode[1] else 'FACESEL'
            row.operator("vef.toggle", text="", icon=icon)
            row.operator_context="INVOKE_DEFAULT"
            row.operator("mesh.select_non_manifold", text='',icon='FILE_TICK')
            row.operator("ngons.select", text='',icon='SEQ_CHROMA_SCOPE')
            row.operator("tris.select", text='',icon='OUTLINER_OB_MESH')
            

            row = layout.row(align=True)
            row.prop(context.scene, "edge_mode", text="")
            if context.scene.edge_mode != "0":
                row.prop(context.scene, "mark_type", text="")
                row.operator("repeat.mark", text="", icon='FILE_REFRESH')
                if context.scene.mark_type=="bevel":
                    op=row.operator("unmark.all", text="", icon='REMOVE')
                    op.ex_bvl = True
                    op.ex_sharp = False
                    op.ex_crs = False
                    op.ex_seam = False                
                elif context.scene.mark_type=="crease":
                    op=row.operator("unmark.all", text="", icon='REMOVE')
                    op.ex_bvl = False
                    op.ex_sharp = False
                    op.ex_crs = True
                    op.ex_seam = False  
                elif context.scene.mark_type=="sharp":
                    op=row.operator("unmark.all", text="", icon='REMOVE')
                    op.ex_bvl = False
                    op.ex_sharp = True
                    op.ex_crs = False
                    op.ex_seam = False
                elif context.scene.mark_type=="seam":
                    op=row.operator("unmark.all", text="", icon='REMOVE')
                    op.ex_bvl = False
                    op.ex_sharp = False
                    op.ex_crs = False
                    op.ex_seam = True                    
                else:
                    op=row.operator("unmark.all", text="", icon='REMOVE')
                    op.ex_bvl = True
                    op.ex_sharp = True
                    op.ex_crs = True
                    op.ex_seam = True

            row = layout.row(align=True)
            if context.scene.edge_mode == "1":
                row.prop(context.scene, "sharpangle",
                         text="EdgSelect angle", slider=True)
                icon1 = 'FORWARD'if bpy.context.scene.inverseur else 'BACK'
                row.prop(context.scene, "inverseur", text="", icon=icon1)
                
            if context.scene.edge_mode == "1" or context.scene.edge_mode == "2":
                row = layout.row()
                if context.scene.mark_type == "bevel":
                    row.scale_y = 0.7
                    row.prop(context.scene, "bevelWeight",
                             text="bevel weight", slider=True)
                if context.scene.mark_type == "crease":
                    row.scale_y = 0.7
                    row.prop(context.scene, "edgeCrease",
                             text="crease weight", slider=True)

            if context.scene.edge_mode == "3":

                row = layout.row()
                icon1 = 'FORWARD'if bpy.context.scene.inverseur1 else 'BACK'
                if context.scene.mark_type == "bevel":
                    row.scale_y = 0.8
                    row.prop(context.scene,
                             "threshold_bevel_select", slider=True)
                    row.prop(context.scene, "inverseur1", text="", icon=icon1)
                if context.scene.mark_type == "crease":
                    row.scale_y = 0.8
                    row.prop(context.scene,
                             "threshold_crease_select", slider=True)
                    row.prop(context.scene, "inverseur1", text="", icon=icon1)

            row = layout.row()
            row.prop(context.scene, "show_faces_orientation",
                     text="", icon='EVENT_O', toggle=True)
            row.prop(context.scene, "toggle_shading",
                     text="", icon='SHADING_WIRE', toggle=True)
            row.prop(context.scene, "show_xray", text="", icon='XRAY')
            if context.scene.show_xray:
                sub = row.row()
                sub.scale_x = 0.2
                sub.prop(context.scene, "xray_alpha", text="")
            row.prop(context.scene, "overlays_toggle", text="", icon='OVERLAY')
            row.prop(context.scene, "show_wireframes", text="", icon='EVENT_W')
            row = layout.row(align=True)
            row.prop(context.scene, "checkboxnormals",
                     text="Recalculate Normals")
            if context.scene.checkboxnormals == True:
                op=row.operator("mesh.normals_make_consistent", text="Normals OUT")
                op.inside=False
                row.operator("mesh.flip_normals", text="", icon='FILE_REFRESH')


#-----------------------------------------addon prefs-hotkey-reg-------------------------------------------#


keymaps_items_dict = {

    "Autosmooth Menu": ['wm.call_panel', 'AUTOSMOOTH_PT_Menu', '3D View '
                                         'Generic', 'VIEW_3D', 'WINDOW', 'X',
                                         'PRESS', False, False, True
                        ]
}


class ASM_addonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text="Autosmooth menu: default key Alt X")
        col.label(text="Object/Edit/Sculpt Modes")

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        draw_keymap_items(kc, layout)


addon_keymaps = []


def draw_keymap_items(kc, layout):

    for name, items in keymaps_items_dict.items():
        kmi_name, kmi_value, km_name = items[:3]
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text=name)
        col.separator()
        km = kc.keymaps[km_name]
        get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col)


def draw_kmi(display_keymaps, kc, km, kmi, layout, level):
    map_type = kmi.map_type
    col = layout.column()

    if kmi.show_expanded:
        col = col.column(align=True)
        box = col.box()
    else:
        box = col.column()

    split = box.split()

    # header bar
    row = split.row(align=True)
    row.prop(kmi, "show_expanded", text="", emboss=False)
    row.prop(kmi, "active", text="", emboss=False)

    if km.is_modal:
        row.separator()
        row.prop(kmi, "propvalue", text="")
    else:
        row.label(text=kmi.name)

    row = split.row()
    row.prop(kmi, "map_type", text="")
    if map_type == 'KEYBOARD':
        row.prop(kmi, "type", text="", full_event=True)
    elif map_type == 'MOUSE':
        row.prop(kmi, "type", text="", full_event=True)
    elif map_type == 'NDOF':
        row.prop(kmi, "type", text="", full_event=True)
    elif map_type == 'TWEAK':
        subrow = row.row()
        subrow.prop(kmi, "type", text="")
        subrow.prop(kmi, "value", text="")
    elif map_type == 'TIMER':
        row.prop(kmi, "type", text="")
    else:
        row.label()
    # Expanded, additional event settings
    if kmi.show_expanded:
        box = col.box()

        split = box.split(factor=0.4)
        sub = split.row()

        if km.is_modal:
            sub.prop(kmi, "propvalue", text="")
        else:
            sub.prop(kmi, "idname", text="")

        if map_type not in {'TEXTINPUT', 'TIMER'}:
            sub = split.column()
            subrow = sub.row(align=True)

            if map_type == 'KEYBOARD':
                subrow.prop(kmi, "type", text="", event=True)
                subrow.prop(kmi, "value", text="")
            elif map_type in {'MOUSE', 'NDOF'}:
                subrow.prop(kmi, "type", text="")
                subrow.prop(kmi, "value", text="")

            subrow = sub.row()
            subrow.scale_x = 0.75
            subrow.prop(kmi, "any", toggle=True)
            subrow.prop(kmi, "shift", toggle=True)
            subrow.prop(kmi, "ctrl", toggle=True)
            subrow.prop(kmi, "alt", toggle=True)
            subrow.prop(kmi, "oskey", text="Cmd", toggle=True)
            subrow.prop(kmi, "key_modifier", text="", event=True)

        # Operator properties
        box.template_keymap_item_properties(kmi)

        # Modal key maps attached to this operator
        if not km.is_modal:
            kmm = kc.keymaps.find_modal(kmi.idname)
            if kmm:
                rna_keymap_ui.draw_km(display_keymaps, kc, kmm, None,
                                      layout, level + 1)
                layout.context_pointer_set("keymap", km)


def get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col):

    # for menus and pie_menu
    if kmi_value:
        for km_item in km.keymap_items:
            if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
                col.context_pointer_set('keymap', km)
                draw_kmi([], kc, km, km_item, col, 0)
                return

        col.label(text=f"No hotkey entry found for {kmi_value}")
        col.operator(TEMPLATE_OT_Add_Hotkey.bl_idname, icon='ADD')

    # for operators
    else:
        if km.keymap_items.get(kmi_name):
            col.context_pointer_set('keymap', km)
            draw_kmi([], kc, km, km.keymap_items[kmi_name], col, 0)
        else:
            col.label(text=f"No hotkey entry found for {kmi_name}")
            col.operator(TEMPLATE_OT_Add_Hotkey.bl_idname, icon='ADD')


def add_hotkey(kc, x_keymaps):

    if not kc:
        return

    for items in keymaps_items_dict.values():
        kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
        eventType, eventValue, ctrl, shift, alt = items[5:]
        km = kc.keymaps.new(name=km_name, space_type=space_type,
                            region_type=region_type)

        kmi = km.keymap_items.new(kmi_name, eventType,
                                  eventValue, ctrl=ctrl, shift=shift,
                                  alt=alt

                                  )
        if kmi_value:
            kmi.properties.name = kmi_value

        kmi.active = True

    x_keymaps.append((km, kmi))


def remove_hotkey(x_keymaps):
    ''' clears all addon level keymap hotkeys stored in x_keymaps '''

    kmi_values = [item[1] for item in keymaps_items_dict.values() if item]
    kmi_names = [item[0] for item in keymaps_items_dict.values() if item not in [
        'wm.call_menu', 'wm.call_menu_pie']]

    for km, kmi in x_keymaps:
        # remove addon keymap for menu and pie menu
        if hasattr(kmi.properties, 'name'):
            if kmi_values:
                if kmi.properties.name in kmi_values:
                    km.keymap_items.remove(kmi)

        # remove addon_keymap for operators
        else:
            if kmi_names:
                if kmi.name in kmi_names:
                    km.keymap_items.remove(kmi)

    x_keymaps.clear()


class TEMPLATE_OT_Add_Hotkey(bpy.types.Operator):
    ''' Add hotkey entry '''
    bl_idname = "template.add_hotkey"
    bl_label = "Add Hotkeys"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user  # user
        add_hotkey(kc, addon_keymaps)

        self.report({'INFO'},
                    "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}


classes = (
    AUTOSMOOTH_PT_Menu,
    VEF_OT_toggle,
    UNMARK_OT_All,
    REPEAT_OT_same_mark,
    ASM_addonPrefs,
    TEMPLATE_OT_Add_Hotkey,
    TOGGLE_OT_Normals,
    NGON_OT_select,
    TRIS_OT_select
)


def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # hotkey setup
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    add_hotkey(kc, addon_keymaps)


def unregister():

    # hotkey cleanup
    remove_hotkey(addon_keymaps)

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
