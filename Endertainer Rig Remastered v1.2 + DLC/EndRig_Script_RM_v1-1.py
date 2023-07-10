bl_info = {
    "name": "Endertainer Rig Add-On (Remastered)",
    "author": "Endertainer007 & BlueEvil",
    "version": (1, 1, 0),
    "blender": (3, 4, 1),
    "location": "View3d > Sidebar > EndRig",
    "description": "Adds a Rig UI panel for the Endertainer Rig",
    "warning": "Only works with the Remastered version of the Rig",
    "category": "EndRig",
}

import bpy
from bpy.props import (StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        EnumProperty,
                        PointerProperty,
                        )

#━━━━━━━━━━━━━━━━━━━
#     Operators     
#━━━━━━━━━━━━━━━━━━━

def toggleButton(obj, pos, propName, text):
    
    context = "Show"
    if(getattr(obj, propName, True)):
        context = "Hide"
        
    text = text.replace("s/h", context)
    
    context = "SHOW"
    if(getattr(obj, propName, True)):
        context = "HIDE"
        
    text = text.replace("S/H", context)
    
    if(getattr(obj, propName, True)):
        pos.prop(obj, propName, toggle=True, text="", icon="CHECKBOX_HLT")
    else:
        pos.prop(obj, propName, toggle=True, text="", icon="CHECKBOX_DEHLT")
    return getattr(obj, propName, True)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Custom Properties     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Object.SettingsTab= EnumProperty(
    items = [('Default', 'Default', 'EndRig Default properties'), 
            ('Custom', 'Custom ', 'EndRig Custom properties')  ],
    override = {"LIBRARY_OVERRIDABLE"},
    name = "SettingsTab1")
    
bpy.types.Object.BodyLimbSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.CustomSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.SubsurfSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.PerformanceSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
        
#━━━━━━━━━━━━━━━━━━━━
#     Main Panel     
#━━━━━━━━━━━━━━━━━━━━

class MainPanel(bpy.types.Panel):
    bl_label = "Rig Settings"
    bl_idname = "EndRig_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EndRig RM'
    
    propBone = "PROP_Custom_Settings"
    
    @classmethod
    def poll(self, context):
        try:
            return (bpy.context.active_object.get("rig_id") == "EndRig_RM")
        except (AttributeError, KeyError, TypeError):
            return False
    
    def getProperties(self, rig) -> list:
        props = []
        for k in rig.pose.bones[self.propBone].keys():
            props.append(k)
        return props
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        pose_bones = context.active_object.pose.bones
        rig = bpy.context.active_object
        scr = bpy.context.scene.render
        sdo = bpy.context.space_data.overlay
        
#======================
#     Settings Tab     
#======================

        b = layout.box()
        r = b.row(align=True)
        r.label(text= "PROP Dashboard", icon= 'MENU_PANEL')
        r = b.row(align=True)
        r.prop(obj, "SettingsTab", text = "SettingsTab", expand=True)

#----------------------------
#     Default Settings     
#----------------------------

        if obj.get('SettingsTab') == 0:
            
            ## Body & Limb Settings
            
            b1 = b.box()
            r1 = b1.row(align=True)
            r1.label(text= "Body & Limb", icon= 'CON_KINEMATIC')
            if(toggleButton(obj, r1, "BodyLimbSettings", "")):
                r1 = b1.row(align=True)
                r1.prop(pose_bones['PROP_Main_Settings'], '["IK_Hybrid"]', text='IK Hybrid')
                r1 = b1.row(align=True)
                r1.label(text= "      Right Arm")
                r1.label(text= "      Left Arm")
                c1 = b1.column(align=True)
                g1 = c1.grid_flow(columns=2, align=True)
                g1.prop(pose_bones['PROP_Main_Settings'], '["RArm_IKFK_Switch"]', text='IK/FK')
                g1.prop(pose_bones['PROP_Main_Settings'], '["RArm_Wrist_IK"]', text='Wrist IK')
                g1.prop(pose_bones['PROP_Main_Settings'], '["LArm_IKFK_Switch"]', text='IK/FK')
                g1.prop(pose_bones['PROP_Main_Settings'], '["LArm_Wrist_IK"]', text='Wrist IK')
                g1 = c1.grid_flow(columns=1, align=True)
                g1.prop(pose_bones['PROP_Main_Settings'], '["Arm_IKFK_Switch_Mode"]', text='IK-FK Switch Mode')
                g1.prop(pose_bones['PROP_Main_Settings'], '["Finger_Rig"]', text='Finger Rig')
                g1.prop(pose_bones['PROP_Main_Settings'], '["Arm_Switch_Mode"]', text='Arm Switch Mode')
                r1 = b1.row(align=True)
                r1.label(text= "      Right Leg")
                r1.label(text= "      Left Leg")
                c1 = b1.column(align=True)
                g1 = c1.grid_flow(columns=2, align=True)
                g1.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IKFK_Switch"]', text='IK/FK')
                g1.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IKFK_Switch"]', text='IK/FK')
                g1 = c1.grid_flow(columns=1, align=True)
                g1.prop(pose_bones['PROP_Main_Settings'], '["Leg_IKFK_Switch_Mode"]', text='IK-FK Switch Mode')
                g1.prop(pose_bones['PROP_Main_Settings'], '["Ankle_Swap"]', text='Ankle Swap')
                g1.prop(pose_bones['PROP_Main_Settings'], '["Leg_Switch_Mode"]', text='Leg Switch Mode')
            
            ## Customization Settings
            
            b2 = b.box()
            r2 = b2.row(align=True)
            r2.label(text= "Customization", icon= 'ARMATURE_DATA')
            if(toggleButton(obj, r2, "CustomSettings", "")):
                c2 = b2.column(align=True)
                # Arm Type List
                if pose_bones['PROP_Customization_Settings'].get('Arm_Type') == 0:
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Arm_Type"]', text='Arm Type: Steve')
                if pose_bones['PROP_Customization_Settings'].get('Arm_Type') == 1:
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Arm_Type"]', text='Arm Type: Alex')
                #---
                c2.prop(pose_bones['PROP_Customization_Settings'], '["Eyelid_Lines"]', text='Eyelid Lines')
                c2.prop(pose_bones['PROP_Customization_Settings'], '["Lips"]', text='Lips')
                c2 = b2.column(align=True)
                g2 = c2.grid_flow(columns=1, align=True)
                g2.prop(pose_bones['PROP_Customization_Settings'], '["Tongue"]', text='Tongue')
                g2 = c2.grid_flow(columns=1, align=True)
                g2.prop(pose_bones['PROP_Customization_Settings'], '["RArm_Stretch"]', text='RArm Stretch')
                g2.prop(pose_bones['PROP_Customization_Settings'], '["LArm_Stretch"]', text='LArm Stretch')
                g2.prop(pose_bones['PROP_Customization_Settings'], '["RLeg_Stretch"]', text='RLeg Stretch')
                g2.prop(pose_bones['PROP_Customization_Settings'], '["LLeg_Stretch"]', text='LLeg Stretch')
                
            ## Performance Settings
            
            b3 = b.box()
            r3 = b3.row(align=True)
            r3.label(text= "Performance", icon= 'RECOVER_LAST')
            if(toggleButton(obj, r3, "PerformanceSettings", "")):
                bb3 = b3.box()
                cc3 = bb3.column(align=True)
                if scr.use_simplify:
                    cc3.prop(scr, "use_simplify", text='Enable Simplify')
                else:
                    cc3.prop(scr, "use_simplify", text='Enable Simplify')
                if scr.use_simplify == True:
                    cc3.prop(scr, "simplify_subdivision", text = "Max Subdivision")
                c3 = b3.column(align=True)
                c3.prop(pose_bones['PROP_Render_Settings'], '["Bool_Viewport"]', text='Bool Viewport')
                c3 = b3.column(align=True)
                c3.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Face"]', text='Anti-Lag (Face)')
                c3.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Body"]', text='Anti-Lag (Body)')
                c3.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Arm"]', text='Anti-Lag (Arm)')
                c3.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Leg"]', text='Anti-Lag (Leg)')
            
            ## Subdivision Surface Settings
            
            b4 = b.box()
            r4 = b4.row(align=True)
            r4.label(text= "Render Quality", icon= 'RENDER_STILL')
            if(toggleButton(obj, r4, "SubsurfSettings", "")):
                c4 = b4.column(align=True)
                c4.prop(pose_bones['PROP_Render_Settings'], '["Face_SubSurf_Viewport"]', text='Face Viewport')
                c4.prop(pose_bones['PROP_Render_Settings'], '["Face_SubSurf_Render"]', text='Face Render')
                c4 = b4.column(align=True)
                c4.prop(pose_bones['PROP_Render_Settings'], '["Body_SubSurf_Viewport"]', text='Body Viewport')
                c4.prop(pose_bones['PROP_Render_Settings'], '["Body_SubSurf_Render"]', text='Body Render')
                c4 = b4.column(align=True)
                c4.prop(pose_bones['PROP_Render_Settings'], '["RArm_SubSurf_Viewport"]', text='RArm Viewport')
                c4.prop(pose_bones['PROP_Render_Settings'], '["RArm_SubSurf_Render"]', text='RArm Render')
                c4.prop(pose_bones['PROP_Render_Settings'], '["LArm_SubSurf_Viewport"]', text='LArm Viewport')
                c4.prop(pose_bones['PROP_Render_Settings'], '["LArm_SubSurf_Render"]', text='LArm Render')
                c4 = b4.column(align=True)
                c4.prop(pose_bones['PROP_Render_Settings'], '["RLeg_SubSurf_Viewport"]', text='RLeg Viewport')
                c4.prop(pose_bones['PROP_Render_Settings'], '["RLeg_SubSurf_Render"]', text='RLeg Render')
                c4.prop(pose_bones['PROP_Render_Settings'], '["LLeg_SubSurf_Viewport"]', text='LLeg Viewport')
                c4.prop(pose_bones['PROP_Render_Settings'], '["LLeg_SubSurf_Render"]', text='LLeg Render')

#-------------------------
#     Custom Settings     
#-------------------------

        if obj.get('SettingsTab') == 1:
            
            c = b.column(align=True)
            for p in self.getProperties(rig):
                c.prop(bpy.context.active_object.pose.bones[f'{self.propBone}'], '["%s"]' % str(p))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Register & Unregister     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
def register():
    bpy.utils.register_class(MainPanel)
    
def unregister():
    bpy.utils.unregister_class(MainPanel)
    
if __name__== "__main__":
    register()