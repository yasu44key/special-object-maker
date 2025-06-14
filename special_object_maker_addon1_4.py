bl_info = {
    "name": "Special Object Maker",
    "author": "Yoshiki Yasunaga & ChatGPT",
    "version": (1, 4, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Special Objects",
    "description": "Add special primitives (spindle, capsule, torus, pyramid, gear, star) at the 3D cursor",
    "category": "Object",
    "support": "COMMUNITY"
}

import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, IntProperty, BoolProperty, PointerProperty
from math import pi, cos, sin

# プロパティ定義
class SpecialObjectProperties(PropertyGroup):
    show_spindle: BoolProperty(name="Spindle Parameters", default=True)
    show_capsule: BoolProperty(name="Capsule Parameters", default=True)
    show_torus:   BoolProperty(name="Torus Parameters",   default=False)
    show_pyramid: BoolProperty(name="Pyramid Parameters", default=False)
    show_gear:    BoolProperty(name="Gear Parameters",    default=False)
    show_star:    BoolProperty(name="Star Parameters",    default=False)

    # Spindle
    spindle_radius:   FloatProperty(name="Radius", default=1.0, min=0.01, max=10.0)
    spindle_height:   FloatProperty(name="Height", default=2.0, min=0.01, max=10.0)
    spindle_segments: IntProperty(name="Segments", default=32, min=3, max=64)

    # Capsule
    capsule_radius:              FloatProperty(name="Radius", default=0.5, min=0.01, max=10.0)
    capsule_height:              FloatProperty(name="Height", default=2.0, min=0.01, max=10.0)
    capsule_segments:            IntProperty(name="Segments", default=32, min=3, max=64)
    capsule_hemisphere_segments: IntProperty(name="Hemisphere Segments", default=16, min=1, max=36)

    # Torus
    torus_major_radius:   FloatProperty(name="Major Radius", default=1.0, min=0.01, max=10.0)
    torus_minor_radius:   FloatProperty(name="Minor Radius", default=0.25, min=0.01, max=5.0)
    torus_major_segments: IntProperty(name="Major Segments", default=48, min=3, max=128)
    torus_minor_segments: IntProperty(name="Minor Segments", default=12, min=3, max=64)

    # Pyramid
    pyramid_base_size: FloatProperty(name="Base Size", default=1.0, min=0.01, max=10.0)
    pyramid_height:    FloatProperty(name="Height", default=1.5, min=0.01, max=10.0)

    # Gear
    gear_teeth:       IntProperty(name="Teeth", default=16, min=3, max=64)
    gear_inner_radius: FloatProperty(name="Inner Radius", default=0.5, min=0.01, max=10.0)
    gear_outer_radius: FloatProperty(name="Outer Radius", default=1.0, min=0.01, max=10.0)
    gear_depth:        FloatProperty(name="Depth", default=0.3, min=0.01, max=10.0)

    # Star
    star_points:      IntProperty(name="Points", default=5, min=3, max=12)
    star_inner_radius: FloatProperty(name="Inner Radius", default=0.5, min=0.01, max=10.0)
    star_outer_radius: FloatProperty(name="Outer Radius", default=1.0, min=0.01, max=10.0)
    star_depth:        FloatProperty(name="Depth", default=0.3, min=0.01, max=10.0)

# オペレーター: スピンドル
class OBJECT_OT_add_spindle(Operator):
    bl_idname = "object.add_spindle"
    bl_label = "Add Spindle"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        props = context.scene.special_object_props
        cursor = context.scene.cursor.location
        # 上部コーン
        bpy.ops.mesh.primitive_cone_add(radius1=props.spindle_radius, radius2=0, depth=props.spindle_height/2,
                                        vertices=props.spindle_segments, location=cursor)
        top = context.object
        top.location.z += props.spindle_height/4
        # 下部コーン
        bpy.ops.mesh.primitive_cone_add(radius1=0, radius2=props.spindle_radius, depth=props.spindle_height/2,
                                        vertices=props.spindle_segments, location=cursor)
        bottom = context.object
        bottom.location.z -= props.spindle_height/4
        # 結合
        bpy.ops.object.select_all(action='DESELECT')
        top.select_set(True); bottom.select_set(True)
        context.view_layer.objects.active = top
        bpy.ops.object.join()
        return {'FINISHED'}

# オペレーター: カプセル
class OBJECT_OT_add_capsule(Operator):
    bl_idname = "object.add_capsule"
    bl_label = "Add Capsule"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        props = context.scene.special_object_props
        cursor = context.scene.cursor.location.copy()
        r = props.capsule_radius; h = props.capsule_height
        # 上半球
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=props.capsule_segments,
            ring_count=props.capsule_hemisphere_segments,
            location=(cursor.x,cursor.y,cursor.z+h/2))
        top = context.object
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=(cursor.x,cursor.y,cursor.z+h/2), plane_no=(0,0,-1), use_fill=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        # 下半球
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=props.capsule_segments,
            ring_count=props.capsule_hemisphere_segments,
            location=(cursor.x,cursor.y,cursor.z-h/2))
        bottom = context.object
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=(cursor.x,cursor.y,cursor.z-h/2), plane_no=(0,0,1), use_fill=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        # 中央シリンダー
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=props.capsule_segments, location=cursor)
        middle = context.object
        # 結合
        bpy.ops.object.select_all(action='DESELECT')
        for o in (top,bottom,middle): o.select_set(True)
        context.view_layer.objects.active = middle
        bpy.ops.object.join()
        return {'FINISHED'}

# オペレーター: トーラス
class OBJECT_OT_add_torus(Operator):
    bl_idname = "object.add_torus"
    bl_label = "Add Torus"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        p = context.scene.special_object_props; c = context.scene.cursor.location
        bpy.ops.mesh.primitive_torus_add(major_radius=p.torus_major_radius,
            minor_radius=p.torus_minor_radius, major_segments=p.torus_major_segments,
            minor_segments=p.torus_minor_segments, location=c)
        return {'FINISHED'}

# オペレーター: ピラミッド
class OBJECT_OT_add_pyramid(Operator):
    bl_idname = "object.add_pyramid"
    bl_label = "Add Pyramid"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        p = context.scene.special_object_props; c = context.scene.cursor.location.copy()
        size = p.pyramid_base_size; h = p.pyramid_height
        verts=[( size/2, size/2,0),(-size/2, size/2,0),(-size/2,-size/2,0),( size/2,-size/2,0),(0,0,h)]
        faces=[(0,1,2,3),(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
        mesh = bpy.data.meshes.new("Pyramid"); mesh.from_pydata(verts,[],faces); mesh.update()
        obj = bpy.data.objects.new("Pyramid",mesh); obj.location=c
        context.collection.objects.link(obj)
        return {'FINISHED'}

# オペレーター: ギア
class OBJECT_OT_add_gear(Operator):
    bl_idname = "object.add_gear"
    bl_label = "Add Gear"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        p = context.scene.special_object_props; c = context.scene.cursor.location.copy()
        teeth = p.gear_teeth; r1 = p.gear_inner_radius; r2 = p.gear_outer_radius; d = p.gear_depth
        verts=[]; faces=[]
        # 頂点生成
        for i in range(teeth*2):
            angle = i * pi / teeth
            r = r2 if i%2==0 else r1
            verts.append((r*cos(angle), r*sin(angle), d/2))
            verts.append((r*cos(angle), r*sin(angle), -d/2))
        # フェイス生成
        for i in range(teeth*2):
            v0 = i*2; v1 = (i*2+2)%(teeth*2*2); v2 = v1+1; v3 = v0+1
            faces.append((v0,v1,v2,v3))
        # 上下面
        top_face = tuple(range(0, teeth*4, 2))
        bottom_face = tuple(range(1, teeth*4, 2))
        faces.append(top_face)
        faces.append(bottom_face)
        mesh = bpy.data.meshes.new("Gear"); mesh.from_pydata(verts,[],faces); mesh.update()
        obj = bpy.data.objects.new("Gear",mesh); obj.location=c
        context.collection.objects.link(obj)
        return {'FINISHED'}

# オペレーター: スター
class OBJECT_OT_add_star(Operator):
    bl_idname = "object.add_star"
    bl_label = "Add Star"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        p = context.scene.special_object_props; c = context.scene.cursor.location.copy()
        pts = p.star_points; r1 = p.star_inner_radius; r2 = p.star_outer_radius; d = p.star_depth
        verts=[]; faces=[]
        # 頂点生成
        for i in range(pts*2):
            angle = i*pi/pts
            r = r2 if i%2==0 else r1
            z = d/2
            verts.append((r*cos(angle), r*sin(angle), z))
            verts.append((r*cos(angle), r*sin(angle), -z))
        # フェイス
        for i in range(pts*2):
            v0 = i*2; v1 = ((i*2+2)%(pts*4)); v2 = v1+1; v3 = v0+1
            faces.append((v0,v1,v2,v3))
        top_face = tuple(range(0, pts*4, 2))
        bottom_face = tuple(range(1, pts*4, 2))
        faces.append(top_face); faces.append(bottom_face)
        mesh = bpy.data.meshes.new("Star"); mesh.from_pydata(verts,[],faces); mesh.update()
        obj = bpy.data.objects.new("Star",mesh); obj.location=c
        context.collection.objects.link(obj)
        return {'FINISHED'}

# UIパネル
class VIEW3D_PT_special_object_panel(Panel):
    bl_label = "Special Object Maker"
    bl_idname = "VIEW3D_PT_special_object_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Special Objects'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout; p = context.scene.special_object_props
        for label, flag, props in (
            ("Spindle", p.show_spindle, ("spindle_radius","spindle_height","spindle_segments")),
            ("Capsule", p.show_capsule, ("capsule_radius","capsule_height","capsule_segments","capsule_hemisphere_segments")),
            ("Torus", p.show_torus, ("torus_major_radius","torus_minor_radius","torus_major_segments","torus_minor_segments")),
            ("Pyramid", p.show_pyramid, ("pyramid_base_size","pyramid_height")),
            ("Gear", p.show_gear, ("gear_teeth","gear_inner_radius","gear_outer_radius","gear_depth")),
            ("Star", p.show_star, ("star_points","star_inner_radius","star_outer_radius","star_depth")),
        ):
            box = layout.box()
            box.prop(p, flag and "show_"+label.lower() or flag, icon='TRIA_DOWN' if flag else 'TRIA_RIGHT', emboss=False)
            if flag:
                for prop_name in props:
                    box.prop(p, prop_name)
            box.operator(f"object.add_{label.lower()}", text=f"Add {label}")

classes = [SpecialObjectProperties,
           OBJECT_OT_add_spindle, OBJECT_OT_add_capsule, OBJECT_OT_add_torus,
           OBJECT_OT_add_pyramid, OBJECT_OT_add_gear, OBJECT_OT_add_star,
           VIEW3D_PT_special_object_panel]

def register():
    for cls in classes: bpy.utils.register_class(cls)
    bpy.types.Scene.special_object_props = PointerProperty(type=SpecialObjectProperties)

def unregister():
    for cls in reversed(classes): bpy.utils.unregister_class(cls)
    del bpy.types.Scene.special_object_props

if __name__ == "__main__":
    register()
