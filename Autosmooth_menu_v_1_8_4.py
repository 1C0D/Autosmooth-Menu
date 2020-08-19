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
    "version": (1, 8, 4),
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

    context.space_data.overlay.show_overlays = True
    context.space_data.shading.show_xray_wireframe = False
    context.space_data.shading.show_xray = False

    context.space_data.overlay.show_face_orientation = not bool(
        context.scene.show_faces_orientation)


bpy.types.Scene.show_faces_orientation = bpy.props.BoolProperty(
    get=get_face_orientation,
    set=set_face_orientation,
    update=update_face_orientation
)


# Shadesmooth
def get_smooth(self):

    for e in bpy.context.selected_objects:
        for poly in e.data.polygons:
            if poly.use_smooth is False:
                return poly.use_smooth

    if not bpy.context.selected_objects:
        return False

    return True


def set_smooth(self, value):

    for e in bpy.context.selected_objects:
        for poly in e.data.polygons:
            poly.use_smooth = value


def update_smooth(self, context):

    for e in context.selected_objects:
        for poly in e.data.polygons:
            poly.use_smooth = bool(self.shadesmooth_toggle)


bpy.types.Scene.shadesmooth_toggle = bpy.props.BoolProperty(
    get=get_smooth,
    set=set_smooth,
    update=update_smooth,
    description="Shade Flat/Smooth toggle"
)


# Autosmooth
def get_autosmooth(self):
    # possible to enter edit mode with the context object not selected...
    if bpy.context.object and not bpy.context.selected_objects:
        return bpy.context.object.data.use_auto_smooth

    for e in bpy.context.selected_objects:
        if e.data.use_auto_smooth is False:
            return e.data.use_auto_smooth
    return True


def set_autosmooth(self, value):

    if bpy.context.object and not bpy.context.selected_objects:
        bpy.context.object.data.use_auto_smooth = value

    for e in bpy.context.selected_objects:
        e.data.use_auto_smooth = value


def update_autosmooth(self, context):

    if context.object and not context.selected_objects:
        context.object.data.use_auto_smooth = bool(self.autosmooth_toggle)

    for e in context.selected_objects:
        e.data.use_auto_smooth = bool(self.autosmooth_toggle)


bpy.types.Scene.autosmooth_toggle = bpy.props.BoolProperty(
    get=get_autosmooth,
    set=set_autosmooth,
    update=update_autosmooth
)


# Autosmooth Angle
def get_autosmoothangle(self):

    return (round(degrees(bpy.context.object.data.auto_smooth_angle), 1))


def set_autosmoothangle(self, value):

    bpy.context.scene.Temp = value


def update_autosmoothangle(self, context):

    for e in context.selected_objects:
        e.data.auto_smooth_angle = radians(context.scene.Temp)
    if context.object.data.auto_smooth_angle != radians(context.scene.Temp):
        context.object.data.auto_smooth_angle = radians(context.scene.Temp)


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

    context.space_data.overlay.show_face_orientation = False

    context.space_data.overlay.show_overlays = bool(
        self.overlays_toggle)


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

    context.space_data.overlay.show_overlays = True
    context.space_data.overlay.show_wireframes = bool(
        self.show_wireframes)


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

    # context.space_data.overlay.show_face_orientation = False

    if context.space_data.shading.type == 'WIREFRAME':
        context.space_data.shading.show_xray_wireframe = bool(self.show_xray)

    else:
        context.space_data.shading.show_xray = bool(self.show_xray)


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
            if object.mode == 'EDIT':
                bm = bmesh.from_edit_mesh(me)
                for f in bm.faces:
                    if f.select == True:
                        faces.append(f)
                if self.out_flip:
                    bmesh.ops.recalc_face_normals(bm, faces=faces)  # out
                else:
                    bmesh.ops.reverse_faces(
                        bm, faces=faces, flip_multires=True)  # flip
                bmesh.update_edit_mesh(me)
            else:
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

        return not len(bpy.context.selected_objects) == 0


def set_select(self, value):

    pass


def update_select(self, context):

    if bpy.context.mode == 'EDIT_MESH':

        if self.select_toggle:

            bpy.ops.mesh.select_all(action='DESELECT')
        else:
            bpy.ops.mesh.select_all(action='SELECT')

    else:
        if self.select_toggle:

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


# non manifold
class NON_OT_MANIFOLD(bpy.types.Operator):
    """select non manifold auto edge"""
    bl_idname = "non.manifold"
    bl_label = "select non manifold"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        bpy.ops.mesh.select_all(action='DESELECT')
        context.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.mesh.select_non_manifold()
        context.space_data.shading.type = 'WIREFRAME'
        context.space_data.shading.show_xray_wireframe = True

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


# Edge Split sculpt
def update_edgesplit(self, context):

    if self.edgesplit_toggle:

        cao = bpy.context.active_object

        if len([m for m in bpy.context.object.modifiers if m.type == "EDGE_SPLIT"]) < 1:
            bpy.ops.object.modifier_add(type='EDGE_SPLIT')
            context.object.modifiers["EdgeSplit"].use_edge_angle = False
            context.object.modifiers["EdgeSplit"].show_expanded = False

        context.scene.autosmooth_toggle = True
        context.scene.shadesmooth_toggle = True

    else:

        bpy.ops.object.modifier_remove(modifier="EdgeSplit")


bpy.types.Scene.edgesplit_toggle = bpy.props.BoolProperty(
    update=update_edgesplit,
    description='add edgesplit set by autosmooth angle'
)


# Unmark all
class UNMARK_OT_All(bpy.types.Operator):
    bl_idname = "unmark.all"
    bl_label = "Clear all marks"
    bl_options = {'REGISTER', 'UNDO'}

    ex_sharp: BoolProperty(default=True, name="sharp")
    ex_bvl: BoolProperty(default=True, name="bevel")
    ex_crs: BoolProperty(default=True, name="crease")
    ex_seam: BoolProperty(default=True, name="seam")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        for obj in context.selected_objects:
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            bv = bm.edges.layers.bevel_weight.verify()
            cr = bm.edges.layers.crease.verify()

            for e in bm.edges:
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

    update_markbevel(self, context)
    update_marksharp(self, context)
    update_markcrease(self, context)
    update_markseam(self, context)
    selectsharpedge(self, context)


def selectsharpedge(self, context):

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.edges_select_sharp(
        sharpness=radians(context.scene.sharpangle))
    update_inverseur(self, context)


def update_inverseur(self, context):

    if self.inverseur == True:
        bpy.ops.mesh.select_all(action='INVERT')
    if bpy.context.scene.sharpangle == 0.0:
        bpy.ops.mesh.select_all(action='DESELECT')
    else:
        pass


def update_marksharp(self, context):

    if self.marksharp == True:
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        update_inverseur(self, context)
        bpy.ops.mesh.mark_sharp(clear=False)

        context.scene.markbevel = False
        context.scene.markseam = False
        context.scene.markcrease = False


def update_markbevel(self, context):

    if self.markbevel == True:
        bpy.ops.transform.edge_bevelweight(value=-1)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        update_inverseur(self, context)
        update_bevelWeight(self, context)

        context.scene.marksharp = False
        context.scene.markseam = False
        context.scene.markcrease = False


def update_markcrease(self, context):

    if self.markcrease == True:
        bpy.ops.transform.edge_crease(value=-1)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        update_inverseur(self, context)
        update_edgeCrease(self, context)

        context.scene.markbevel = False
        context.scene.markseam = False
        context.scene.marksharp = False


def update_markseam(self, context):

    if self.markseam == True:
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(
            sharpness=radians(context.scene.sharpangle))
        update_inverseur(self, context)
        bpy.ops.mesh.mark_seam(clear=False)

        context.scene.markbevel = False
        context.scene.marksharp = False
        context.scene.markcrease = False


def update_bevelWeight(self, context):

    for ob in context.selected_objects:
        context.view_layer.objects.active = ob
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        bv = bm.edges.layers.bevel_weight.verify()

        for e in bm.edges:
            if e.select == True:
                e[bv] = self.bevelWeight

        bmesh.update_edit_mesh(me)  # , False, False)


def update_edgeCrease(self, context):

    for ob in context.selected_objects:
        context.view_layer.objects.active = ob
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        cr = bm.edges.layers.crease.verify()

        for e in bm.edges:
            if e.select == True:
                e[cr] = self.edgeCrease

        bmesh.update_edit_mesh(me, False, False)


bpy.types.Scene.bevelWeight = bpy.props.FloatProperty(
    description="Set Bevel Weight",
    name="bevelWeight",
    min=0.0,
    max=1.0,
    step=0.01,
    default=0.7,
    update=update_bevelWeight
)

bpy.types.Scene.edgeCrease = bpy.props.FloatProperty(
    description="Set Crease Weight",
    name="edgeCrease",
    min=0.0,
    max=1.0,
    step=0.01,
    default=0.4,
    update=update_edgeCrease
)

bpy.types.Scene.sharpangle = bpy.props.FloatProperty(
    default=180, min=0, max=180, precision=2,
    update=update_sharpangle
)
bpy.types.Scene.inverseur = bpy.props.BoolProperty(update=update_inverseur)
bpy.types.Scene.marksharp = bpy.props.BoolProperty(update=update_marksharp)
bpy.types.Scene.markbevel = bpy.props.BoolProperty(update=update_markbevel)
bpy.types.Scene.markseam = bpy.props.BoolProperty(update=update_markseam)
bpy.types.Scene.markcrease = bpy.props.BoolProperty(update=update_markcrease)


# manual
def update_marksharp1(self, context):

    if self.marksharp1 == True:

        context.scene.markbevel1 = False
        context.scene.markseam1 = False
        context.scene.markcrease1 = False


def update_markbevel1(self, context):

    if self.markbevel1 == True:

        update_bevelWeight(self, context)

        context.scene.marksharp1 = False
        context.scene.markseam1 = False
        context.scene.markcrease1 = False


def update_markcrease1(self, context):

    if self.markcrease1 == True:

        update_edgeCrease(self, context)

        context.scene.markbevel1 = False
        context.scene.markseam1 = False
        context.scene.marksharp1 = False


def update_markseam1(self, context):

    if self.markseam1 == True:

        context.scene.markbevel1 = False
        context.scene.marksharp1 = False
        context.scene.markcrease1 = False


bpy.types.Scene.marksharp1 = bpy.props.BoolProperty(update=update_marksharp1)
bpy.types.Scene.markbevel1 = bpy.props.BoolProperty(update=update_markbevel1)
bpy.types.Scene.markseam1 = bpy.props.BoolProperty(update=update_markseam1)
bpy.types.Scene.markcrease1 = bpy.props.BoolProperty(update=update_markcrease1)


# sel marked edges
def sel_bevel(self, context):

    if context.scene.selbevel == True:

        context.scene.selsharp = False
        context.scene.selseam = False
        context.scene.selcrease = False
        context.scene.inverseur1 = True

        obj = bpy.context.object
        for obj in context.selected_objects:
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            bv = bm.edges.layers.bevel_weight.verify()

            for v in bm.verts:
                v.select = False
            bm.select_flush_mode()

            for e in bm.edges:

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

    if context.scene.selcrease == True:

        context.scene.selbevel = False
        context.scene.selsharp = False
        context.scene.selseam = False

        for obj in context.selected_objects:
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            cr = bm.edges.layers.crease.verify()

            for e in bm.edges:
                if context.scene.inverseur1 == False:

                    if e[cr] >= self.threshold_crease_select and e[cr] > 0:

                        e.select = True
                    else:
                        e.select = False
                else:
                    if e[cr] <= self.threshold_crease_select and e[cr] > 0:

                        e.select = True
                    else:
                        e.select = False

            bmesh.update_edit_mesh(me, False, False)


bpy.types.Scene.selcrease = bpy.props.BoolProperty(
    update=sel_crease)  # bizarre

bpy.types.Scene.threshold_crease_select = bpy.props.FloatProperty(
    description="Set threshold of crease selection",
    name="CreaseWeight threshold",
    min=0,
    max=1,
    precision=2,
    default=1,
    update=sel_crease
)


def sel_sharp(self, context):

    if self.selsharp == True:
        context.scene.selbevel = False
        context.scene.selseam = False
        context.scene.selcrease = False

        for obj in context.selected_objects:
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            # bm.select_mode = {'VERT'}
            for v in bm.verts:
                v.select = False
            bm.select_flush_mode()

            for e in bm.edges:
                if not e.smooth:
                    e.select = True

            # bm.select_mode = {'EDGE'}

            bmesh.update_edit_mesh(me, False)


bpy.types.Scene.selsharp = bpy.props.BoolProperty(update=sel_sharp)


def sel_seam(self, context):

    if context.scene.selseam == True:

        context.scene.selbevel = False
        context.scene.selsharp = False
        context.scene.selcrease = False

        for obj in context.selected_objects:
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            # bm.select_mode = {'VERT'}
            for v in bm.verts:
                v.select = False
            bm.select_flush_mode()

            for e in bm.edges:
                if e.seam:
                    e.select = True

            bmesh.update_edit_mesh(me, False)


bpy.types.Scene.selseam = bpy.props.BoolProperty(update=sel_seam)


def update_inverseur1(self, context):

    if bpy.context.scene.threshold_bevel_select == 0:
        bpy.ops.mesh.select_all(action='DESELECT')
    if context.scene.inverseur1 == True:
        bpy.ops.mesh.select_all(action='INVERT')


bpy.types.Scene.inverseur1 = bpy.props.BoolProperty(update=update_inverseur1)

edge_select_mode = [
    ("0", "Disabled", "OFF"),
    ("1", "Mark by angle", "Select & Mark edges by angle"),
    ("2", "Mark Selected", "Mark selection"),
    ("3", "Select Marked Edg", "Get selection of Marked edges")
]


def update_enum(self, context):

    if context.scene.enum_select == "3":

        if context.scene.selcrease:
            sel_crease(self, context)
        if context.scene.selbevel:
            sel_bevel(self, context)
        if context.scene.selseam:
            sel_seam(self, context)
        if context.scene.selsharp:
            sel_sharp(self, context)


bpy.types.Scene.enum_select = bpy.props.EnumProperty(
    name="edges mark",
    description="Select & Mark, Select Marked",
    items=edge_select_mode,
    update=update_enum
)


# show more love

def show_more_love(self, context):
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

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # if obj and obj.type == 'MESH':
        if obj.mode in {'OBJECT'}:
            obj_data = context.active_object.data
            row = layout.row()
            row.label(text="Object Mode")
            row.scale_y = 0.8
            # row.prop(context.scene, "love", text="", icon='HEART')
            row.operator("object.editmode_toggle",
                         text="", icon='ARROW_LEFTRIGHT')
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
                                   icon='FILE_REFRESH', text="Flip")
                op1.out_flip = False

        elif obj.mode in {'SCULPT'}:
            obj_data = context.active_object.data
            layout.label(text="Sculpt Mode")
            label = "Shade Smooth ON" if context.scene.shadesmooth_toggle else "Shade Smooth OFF"
            layout.prop(context.scene, "shadesmooth_toggle",
                        text=label, toggle=True)
            layout.separator()
            row = layout.row(align=True)
            if context.scene.edgesplit_toggle == False:
                row.prop(context.scene, "edgesplit_toggle",
                         text="Sculpt ESplit")
            if context.scene.edgesplit_toggle:
                sub = row.row()
                sub.scale_x = 0.75
                sub.prop(context.scene, "edgesplit_toggle", text="S ESplit")
                row.prop(context.scene, "autosmoothangle",
                         text="ES angle", slider=True)
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
            row.operator("non.manifold", text="", icon='FILE_TICK')
            row = layout.row(align=True)
            row.label(text="Edg Sel & Mark")
            row.prop(context.scene, "enum_select", text="")
            row.operator("unmark.all", text="", icon='ALIGN_FLUSH')

            if context.scene.enum_select == "1":
                row = layout.row()
                row.prop(context.scene, "sharpangle",
                         text="EdgSelect angle", slider=True)
                icon1 = 'FORWARD'if bpy.context.scene.inverseur else 'BACK'
                row.prop(context.scene, "inverseur", text="", icon=icon1)
                row = layout.row(align=True)
                row.scale_y = 0.8
                sub = row.row()
                sub.scale_x = 0.8
                sub.prop(context.scene, "markbevel", text="Bvl")
                row.prop(context.scene, "marksharp", text="Sharp")
                row.prop(context.scene, "markcrease", text="Crease")
                row.prop(context.scene, "markseam", text="Seam")
                row = layout.row(align=True)
                if context.scene.markbevel:
                    row.scale_y = 0.7
                    row.prop(context.scene, "bevelWeight",
                             text="bevel weight", slider=True)
                if context.scene.markcrease:
                    row.scale_y = 0.7
                    row.prop(context.scene, "edgeCrease",
                             text="crease weight", slider=True)

            if context.scene.enum_select == "2":
                row = layout.row(align=True)
                row.scale_y = 0.8
                sub = row.row()
                sub.scale_x = 0.8
                sub.prop(context.scene, "markbevel1", text="Bvl")
                row.prop(context.scene, "marksharp1", text="Sharp")
                row.prop(context.scene, "markcrease1", text="Crease")
                row.prop(context.scene, "markseam1", text="Seam")
                row = layout.row(align=True)
                if context.scene.markbevel1:
                    row.scale_y = 0.7
                    row.prop(context.scene, "bevelWeight",
                             text="bevel weight", slider=True)
                if context.scene.markcrease1:
                    row.scale_y = 0.7
                    row.prop(context.scene, "edgeCrease",
                             text="crease weight", slider=True)
                if context.scene.marksharp1:
                    row.scale_y = 0.7
                    row.operator("mesh.mark_sharp",
                                 text="Sharp ON").clear = False
                    row.operator("mesh.mark_sharp",
                                 text="Sharp OFF").clear = True
                if context.scene.markseam1:
                    row.scale_x = 0.7
                    row.operator("mesh.mark_seam",
                                 text="Seam ON").clear = False
                    row.operator("mesh.mark_seam",
                                 text="Seam OFF").clear = True

            if context.scene.enum_select == "3":
                row = layout.row(align=True)
                row.scale_y = 0.8
                sub = row.row()
                sub.scale_x = 0.8
                sub.prop(context.scene, "selbevel", text="Bvl")
                row.prop(context.scene, "selsharp", text="Sharp")
                row.prop(context.scene, "selcrease", text="Crease")
                row.prop(context.scene, "selseam", text="Seam")
                row = layout.row(align=True)
                icon1 = 'FORWARD'if bpy.context.scene.inverseur1 else 'BACK'
                if context.scene.selbevel:
                    row.scale_y = 0.8
                    row.prop(context.scene,
                             "threshold_bevel_select", slider=True)
                    row.prop(context.scene, "inverseur1", text="", icon=icon1)
                if context.scene.selcrease:
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
                op = row.operator("toggle.normals_operator",
                                  text="Normals OUT")
                op.out_flip = True
                op1 = row.operator("toggle.normals_operator",
                                   icon='FILE_REFRESH', text='Flip')
                op1.out_flip = False

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
            # One day...
            # sub.prop_search(kmi, "idname", bpy.context.window_manager, "operators_all", text="")
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
    NON_OT_MANIFOLD,
    ASM_addonPrefs,
    TEMPLATE_OT_Add_Hotkey,
    TOGGLE_OT_Normals
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
