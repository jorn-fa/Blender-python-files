from math import radians
from mathutils import Vector
from mathutils import Matrix
import re
import bpy



bl_info = {
	'name': 'Object creator for Farming Simulator 19',
	'author': 'Hiel Jorn',
	'blender': (2, 80, 0),
	'version': (2, 0, 0),
	'category': 'All',
	'description': 'Object creation panel',
	'wiki_url': '',
	'tracker_url': '',
	'category': 'Game Engine',
}





def initSceneProperties(scn):
	print("Object creator - Loaded")
	return
	initSceneProperties(bpy.context.scene)


class SCV_PT_addCreateMenu(bpy.types.Panel):

	
	label_0 = "-- Transforms at 0,0 --"
	label_1 = "-- Cameras  --"
	label_2 = "-- Attachers--"
	label_3 = "-- Wheels --"
	label_4 = "-- Lights --"
	label_5 = "-- Transform in edit mode --"
	
	

	bl_label = "Create Points :"
	bl_space_type = 'VIEW_3D'
	bl_region_type = "TOOLS"
	

	def draw(self, context):
		
		layout = self.layout
		layout.use_property_split = True # Active single-column layout

		layout.label(text= self.label_5)
		row = layout.row()
		layout.operator("mesh.createatpoints", icon='ACTION', text="At Selected")
		
		splitA = row.split(factor=1)
		colA = splitA.column()
		

		layout.label(text = self.label_0)

		row = layout.row()
		split = row.split(factor=1)
		col = split.column()
		col.operator("mesh.createpoints", icon='ACTION', text="workarea").type="workareas"
		col.operator("mesh.createpoints", icon='ACTION', text="visuals").type="visuals"
		col.operator("mesh.createpoints", icon='ACTION', text="exhaust").type="exhaust"
		col.operator("mesh.createpoints", icon='ACTION', text="mirrors").type="mirrors"
		col.operator("mesh.createpoints", icon='ACTION', text="exit point").type="exit"
				
		col.operator("mesh.createpoints", icon='ACTION', text="player").type="player"
		
		
		col.operator("mesh.createpoints", icon='ACTION', text="extra collisions").type="collisions"
		col.operator("mesh.createpoints", icon='ACTION', text="effects").type="effects"
		row = layout.row()
		
		
		
		layout.label( text = self.label_1)
		split = layout.split(factor=1)		  
		col2 = split.column()
		col2.operator("mesh.createcamera", icon='ACTION', text="indoor camera").type="indoor"
		col2.operator("mesh.createcamera", icon='ACTION', text="outdoor camera").type="outdoor"
		col2.operator("mesh.createcamera", icon='ACTION', text="edit camera").type="editCam"
		row = layout.row()
		
		layout.label( text = self.label_2)
		split = layout.split(factor=1)		  
		col3 = split.column()
		col3.operator("mesh.createpoints", icon='ACTION', text="front attacher").type="attacher_front"
		col3.operator("mesh.createpoints", icon='ACTION', text="rear attacher").type="attacher_rear"
		row = layout.row()
		
		layout.label( text = self.label_3)
		split = layout.split(factor=1)		  
		col4 = split.column()
		col4.operator("mesh.createpoints", icon='ACTION', text="4 wheels").type="0_wheels"
		col4.operator("mesh.createpoints", icon='ACTION', text="wheel left").type="wheel_left"
		col4.operator("mesh.createpoints", icon='ACTION', text="wheel right").type="wheel_right"
		row = layout.row()
		
		
		layout.label( text = self.label_4)
		split = layout.split(factor=1)		  
		col5 = split.column()
		col5.operator("mesh.createlights", icon='ACTION', text="turn lights").type="turnlights"
		col5.operator("mesh.createlights", icon='ACTION', text="brake lights").type="brakelights"
		col5.operator("mesh.createlights", icon='ACTION', text="revers lights").type="reverselights"
		col5.operator("mesh.createlights", icon='ACTION', text="default lights").type="defaultlights"
		col5.operator("mesh.createlights", icon='ACTION', text="work lights").type="worklights"
		col5.operator("mesh.createlights", icon='ACTION', text="beacon lights").type="beaconlights"
		row = layout.row()
		
		#layout.label(text = "clearing")
		#split = layout.split(factor=1)		  
		#col6 = split.column()
		#col6.operator("mesh.createblank", icon='ACTION', text="restart")
		row = layout.row()
		
		
		
class SCV_OT_CreateAtPoint(bpy.types.Operator):
	
	bl_idname = 'mesh.createatpoints'
	bl_label = 'Farming tranformCreatorAtPoint'
	type : bpy.props.StringProperty()
	def invoke(self, context, event):		
		
		ob = bpy.context.object
		ob.update_from_editmode()

		me = ob.data
		verts_sel = [v.co for v in me.vertices if v.select]
		pivot = sum(verts_sel, Vector()) / len(verts_sel)
		previous = bpy.context.object		
		changeMe = bpy.data.objects.new("ChangeMe", None, )
		changeMe.location=ob.matrix_world @ pivot
		bpy.context.scene.collection.objects.link( changeMe)					
		
		return {"FINISHED"}

	
class SCV_OT_TranformCreator(bpy.types.Operator):
	bl_idname = 'mesh.createpoints'
	bl_label = 'Farming tranformCreator'
	bl_space_type = 'VIEW_3D'
	bl_region_type = "TOOLS"



	type : bpy.props.StringProperty()

	def invoke(self, context, event):
		
		gamePointsString="gamePoints"
		if not bpy.data.objects.get(gamePointsString) and (not self.type[:6]=="0_whee") and (not self.type[:6]=="wheel_"):
			bpy.ops.object.mode_set(mode = 'OBJECT')
			bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
			bpy.context.active_object.name = gamePointsString


		gamePoints=bpy.data.objects.get(gamePointsString)
		
		for obj in bpy.data.objects:
			if obj.type=="EMPTY" and obj.name.lower()==self.type and (not self.type[:6]=="wheel_") and (not self.type[:6]=="0_whee"): 
				
					def draw(self, context):
						self.layout.label(text="Already exists.")
				
					bpy.context.window_manager.popup_menu(draw, title="Error", icon='INFO')
					
			if not obj.type=="EMPTY" and obj.name.lower()==self.type: 
				
					def draw(self, context):
						self.layout.label(text="Already exists as non empty")
				
					bpy.context.window_manager.popup_menu(draw, title="Error", icon='INFO')
			
		if not bpy.data.objects.get(self.type) or (self.type[:6]=="0_whee"):	
			
			
				if (not self.type[:6]=="0_whee"):
					bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))				
					bpy.context.active_object.name = self.type

				toCheck=["mirrors","exit","effects"]

				if self.type in toCheck :				
					bpy.data.objects.get(self.type).parent=gamePoints


				if self.type=="exhaust":
					exhausts = bpy.data.objects.get("exhaust")							
					bpy.ops.object.mode_set(mode = 'OBJECT')
					bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
					bpy.context.active_object.name = self.type
					bpy.context.active_object.parent = exhausts					
					exhausts.parent=gamePoints
					
				if self.type=="workareas":
					names=["workAreaStart","workAreaWidth","workAreaHeight"]
					for name in names:
						bpy.ops.object.mode_set(mode = 'OBJECT')
						bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
						bpy.context.active_object.name = name
						bpy.context.active_object.parent = bpy.data.objects.get(self.type)
						bpy.data.objects.get(self.type).parent=gamePoints
						
				if self.type=="0_wheels":			
    
					names=["wheel_L1","wheel_R1","wheel_L2","wheel_R2"]
					for name in names:
						if not bpy.data.objects.get(name):							
							bpy.ops.object.mode_set(mode = 'OBJECT')
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							me = bpy.context.active_object.name = name						
							bpy.context.active_object.parent = bpy.data.objects.get(self.type)						
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							bpy.context.active_object.name = name+"_drive"
							bpy.context.active_object.parent = bpy.data.objects.get(name)
				
				if self.type=="player":
					names=["playerskin","leftFoot","rightFoot","leftArm","rightArm"]
					for name in names:
						rotationAxis=(radians(0),radians(0),radians(0))
						bpy.ops.object.mode_set(mode = 'OBJECT')
						if name=="rightArm": rotationAxis=(radians(270),radians(-30),radians(90))
						if name=="leftArm": rotationAxis=(radians(-90),radians(0),radians(270))
						bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0),rotation=rotationAxis)
						bpy.context.active_object.name = name
						bpy.context.active_object.parent = bpy.data.objects.get(self.type)
					bpy.data.objects.get("player").parent=gamePoints
						
				if self.type[:8]=="attacher":
					names=["attacherjoints"]
					if not bpy.data.objects.get("attacherJoints"):
							bpy.ops.object.mode_set(mode = 'OBJECT')
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0) ,rotation=(0,0,radians(90)))
							bpy.context.active_object.name = "attacherJoints"
							bpy.data.objects.get("attacherJoints").parent=gamePoints
		
		
		
		
		if self.type[:8]=="attacher":
				for item in bpy.data.objects:
					if item.name[:9]=="attacher_":
						parent = bpy.data.objects.get("attacherJoints")
						if item.name[:10]=="attacher_f":
							item.rotation_euler =(0,0,radians(180))
							
						item.parent=parent
					
		
		if self.type[:5]=="wheel":
				counter=[0,0]
				
				if not bpy.data.objects.get("0_wheels"):
					bpy.ops.object.mode_set(mode = 'OBJECT')
					bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))					
					child=bpy.context.active_object.name = "0_wheels"

				#bpy.data.objects.get("0_wheels").parent=gamePoints
					
				
				for wheels in bpy.data.objects:
					if wheels.name[:7]=="wheel_L" and len(wheels.name)<10: counter[0] +=1
					if wheels.name[:7]=="wheel_R" and len(wheels.name)<10: counter[1] +=1

		
				for item in bpy.data.objects:
					if item.name[:6]=="wheel_" and len(item.name)<12:
						
						if item.name=="wheel_left": 
							item.name="wheel_L"+str(counter[0]+1)
							parent=item
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							bpy.context.active_object.name = item.name+"_drive"
							bpy.context.active_object.parent=parent
						
						if item.name=="wheel_right" and len(item.name)<12:
							item.name="wheel_R"+str(counter[1]+1)
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							bpy.context.active_object.name = item.name+"_drive"
							bpy.context.active_object.parent=item
						
						parent = bpy.data.objects.get("0_wheels")
						item.parent=parent
						
					
					
					


		return {"FINISHED"}


class SCV_OT_Clearer(bpy.types.Operator):
	bl_idname = 'mesh.createblank'
	bl_label = 'Farming clearerbtton'
	type : bpy.props.StringProperty()
	verify="cameras"

	def invoke(self, context, event):
	
		bpy.ops.object.mode_set(mode = 'OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects.get("Cube").select = True
		all = bpy.ops.object.select_all(action='INVERT')
		for obj in all : bpy.ops.object.delete()
		bpy.ops.object.mode_set(mode = 'OBJECT')
	
		return {"FINISHED"}



class SCV_OT_CameraCreator(bpy.types.Operator):
	bl_idname = 'mesh.createcamera'
	bl_label = 'Farming tranformCreator'
	type : bpy.props.StringProperty()
	verify="cameras"

	def invoke(self, context, event):
		
		if not bpy.data.objects.get(self.verify) and not self.type=="editCam":
					#bpy.ops.object.mode_set(mode = 'OBJECT')
					#bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))					
					#bpy.context.active_object.name = "cameras"
					cameras = bpy.data.objects.new("cameras", None, )
					cameras.location=(0.0, 0.0, 0.0)					
					bpy.context.scene.collection.objects.link( cameras)		


			
		if not bpy.data.objects.get(self.type):
				bpy.ops.object.mode_set(mode = 'OBJECT')
				bpy.ops.object.camera_add(location=(0.0, 0.0, 0.0),rotation=(0.0, 0.0, 0.0))

				

								
				bpy.context.active_object.name = self.type
				bpy.context.active_object.data.name = self.type
				#no parent on editcam
				if not self.type=="editCam":
					bpy.context.active_object.parent = bpy.data.objects.get(self.verify)
				
				if self.type=="outdoor":
					names=["cameraRaycastNode1","cameraRaycastNode2","cameraRaycastNode3"]
					for name in names:
						bpy.ops.object.mode_set(mode = 'OBJECT')
						bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
						bpy.context.active_object.name = name
						bpy.context.active_object.parent = bpy.data.objects.get(self.verify)				
					
					
					bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0) ,rotation=(radians(20),0,0))
					bpy.context.active_object.name = "outdoorCameraTarget"
					bpy.context.active_object.parent = bpy.data.objects.get(self.verify)
					bpy.data.objects.get("outdoor").parent=bpy.data.objects.get("outdoorCameraTarget")
					fix=bpy.data.objects.get("outdoor")
					fix.location=(0,15,0)
					fix.rotation_euler =(radians(-90),radians(180),0)
					bpy.data.cameras[fix.data.name].lens=54.432
					
				if self.type=="editCam":
					wheels="0_wheels"
					if not bpy.data.objects.get(wheels):
						bpy.ops.object.mode_set(mode = 'OBJECT')
						bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
						bpy.context.active_object.name = wheels


					editCam=bpy.data.objects.get("editCam")
					editCam.location=(10,-7,4)
					bpy.data.cameras[editCam.data.name].lens=50

					parent = bpy.data.objects.new("a_cameraTarget", None, )
					parent.location=(0.0, 0.0, 0.0)					
					bpy.context.scene.collection.objects.link( parent)		
					parent.parent=bpy.data.objects.get(wheels)
					
					constraint = editCam.constraints.new('TRACK_TO')
					constraint.name="Track nulpunt"
					constraint.up_axis="UP_Y"
					constraint.track_axis="TRACK_NEGATIVE_Z"
					constraint.target=parent

					editCam.parent=bpy.data.objects.get("a_cameraTarget")
					
					

					


					
				if self.type=="indoor":
					fix=bpy.data.objects.get("indoor")
					
					#TODO: Hoek nakijken
					fix.rotation_euler =(radians(-90),radians(180),0)
					
					bpy.data.cameras[fix.data.name].lens=60
					
					
					
				
					

		return {"FINISHED"}


class SCV_OT_Lightcreator(bpy.types.Operator):
	bl_idname = 'mesh.createlights'
	bl_label = 'Farming lightCreator'
	type : bpy.props.StringProperty()
	verify="lights"

	
	def invoke(self, context, event):
		
		
		#read scene and collect light names
		lights=[]
		for obj in bpy.data.objects:
			if "light" in obj.name.lower():				
				lights.append(obj.name)
		
		
		for obj in bpy.data.objects:
			if obj.type=="EMPTY" and obj.name.lower()==self.type and not self.type=="beaconlights": 
				
					def draw(self, context):
						self.layout.label("Already exists")
				
					bpy.context.window_manager.popup_menu(draw, title="Error", icon='INFO')
					
			if not obj.type=="EMPTY" and obj.name.lower()==self.type: 
				
					def draw(self, context):
						self.layout.label("Already exists as non empty")
				
					bpy.context.window_manager.popup_menu(draw, title="Error", icon='INFO')
			
		if not bpy.data.objects.get(self.type) or self.type=="beaconlights":
		
			if self.type=="turnlights":
						
						names=["turnLightLeftBack","turnLightRightBack","turnLightLeftFront","turnLightRightFront"]
						lightnames=["lights","turnlights","staticLights"]
						for mainlights in lightnames:
							if not bpy.data.objects.get(mainlights):
								bpy.ops.object.mode_set(mode = 'OBJECT')
								bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
								bpy.context.active_object.name = mainlights
								if not mainlights=="lights": bpy.context.active_object.parent = bpy.data.objects.get("lights")
							
							
						parent = bpy.data.objects.get("turnlights")
						
						for name in names:
							bpy.ops.object.mode_set(mode = 'OBJECT')
							if "Back" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(90),0,0))
							if "Front" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(-90),0,0))

							obj = bpy.data.objects.get(bpy.context.active_object.name)

							for lamp in bpy.data.lights:
								if lamp.name == obj.data.name:
									lamp.distance=4
									lamp.spot_size=radians(140)
									lamp.spot_blend=0.6
									lamp.color=(0.31,0.14,0)
									#lamp.shadow_method=('NOSHADOW')
							bpy.context.active_object.name = name							
							bpy.context.active_object.parent = parent
							
			if self.type=="brakelights" :
					
					names=["brakeLightLeft","brakeLightRight"]
					lightnames=["lights","brakelights","staticLights"]
					for mainlights in lightnames:
						if not bpy.data.objects.get(mainlights):
							bpy.ops.object.mode_set(mode = 'OBJECT')
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							bpy.context.active_object.name = mainlights
							parent = bpy.data.objects.get("brakelights")
							if not mainlights=="lights": bpy.context.active_object.parent = bpy.data.objects.get("lights")
							

					for name in names:
							bpy.ops.object.mode_set(mode = 'OBJECT')
							if "Left" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(75),0,radians(-20)))
							if "Right" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(75),0,radians(20)))

							obj = bpy.data.objects.get(bpy.context.active_object.name)

							for lamp in bpy.data.lights:
								if lamp.name == obj.data.name:
									lamp.distance=2.5
									lamp.spot_size=radians(170)
									lamp.spot_blend=0.4
									lamp.color=(0.2,0,0)
									#lamp.shadow_method=('NOSHADOW')
							bpy.context.active_object.name = name							
							bpy.context.active_object.parent = parent
				
			if self.type=="defaultlights" :
					
					names=["frontLightLow","frontLightHighLeft","frontLightHighRight","highBeamLow","highBeamHighLeft","highBeamHighRight","cabLight"]
					lightnames=["lights","defaultlights","staticLights"]
					for defaultlights in lightnames:
						if not bpy.data.objects.get(defaultlights):
							bpy.ops.object.mode_set(mode = 'OBJECT')
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							bpy.context.active_object.name = defaultlights
							parent = bpy.data.objects.get("defaultlights")
							if not defaultlights=="lights": bpy.context.active_object.parent = bpy.data.objects.get("lights")

					for name in names:
							bpy.ops.object.mode_set(mode = 'OBJECT')
							# if "low" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(-90),radians(10),0))
							bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(-70),0,0))

							obj = bpy.data.objects.get(bpy.context.active_object.name)
							
							if "Left" in name: obj.rotation_euler=(radians(-70),0,radians(10))
							if "Right" in name: obj.rotation_euler=(radians(-70),0,radians(-10))
							if "cabLight" in name: obj.rotation_euler=(0,0,0)
							

							for lamp in bpy.data.lights:
								if lamp.name == obj.data.name:
									
									distance = 20 if "Low" in name else 25
									if name=="cablight" : distance = 5
									lamp.distance=distance
									lamp.spot_size=radians(80)
									lamp.spot_blend=0.4
									lamp.color=(.85,0.85,1)
									#lamp.shadow_method=('NOSHADOW')
							bpy.context.active_object.name = name							
							bpy.context.active_object.parent = parent
							
			if self.type=="reverselights" :
					
					names=["reverseLightLeft","reverseLightRight"]
					lightnames=["lights","reverselights","staticLights"]
					for reversefights in lightnames:
						if not bpy.data.objects.get(reversefights):
							bpy.ops.object.mode_set(mode = 'OBJECT')
							bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
							bpy.context.active_object.name = reversefights
							parent = bpy.data.objects.get("reverselights")
							if not reversefights=="lights": bpy.context.active_object.parent = bpy.data.objects.get("lights")

					for name in names:
							bpy.ops.object.mode_set(mode = 'OBJECT')
							# if "low" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(-90),radians(10),0))
							bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(-70),0,0))

							obj = bpy.data.objects.get(bpy.context.active_object.name)
							
							if "Left" in name: obj.rotation_euler=(radians(70),0,0)
							if "Right" in name: obj.rotation_euler=(radians(70),0,0)
							

							for lamp in bpy.data.lights:
								if lamp.name == obj.data.name:
									
									distance = 20 if "Low" in name else 25
									lamp.distance=distance
									lamp.spot_size=radians(80)
									lamp.spot_blend=0.4
									lamp.color=(.85,0.85,1)
									#lamp.shadow_method=('NOSHADOW')
							bpy.context.active_object.name = name							
							bpy.context.active_object.parent = parent
							
			if self.type=="beaconlights" :
				
				lightnames=["lights","beaconlights","staticLights"]
				
				counter=0
				
				for beaconlights in bpy.data.objects:
					if "beaconlight_" in beaconlights.name.lower() :
						counter +=1
				
				for defaultlights in lightnames:
					if not bpy.data.objects.get(defaultlights):
						bpy.ops.object.mode_set(mode = 'OBJECT')
						bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
						bpy.context.active_object.name = defaultlights
						parent = bpy.data.objects.get("beaconlights")
						if not defaultlights=="lights": bpy.context.active_object.parent = bpy.data.objects.get("lights")
					
				bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
				name = "beaconLight_"+str(counter+1)
				bpy.context.active_object.name = name
								
				
				bpy.context.active_object.parent = bpy.data.objects.get("beaconlights")
				
				
				
			if self.type=="worklights":
						
						names=["worklightFrontHigh","worklightFrontLow","worklightBackHigh","worklightBackLow"]
						lightnames=["lights","worklights","staticLights"]
						for mainlights in lightnames:
							if not bpy.data.objects.get(mainlights):
								bpy.ops.object.mode_set(mode = 'OBJECT')
								bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0.0, 0.0, 0.0))
								bpy.context.active_object.name = mainlights
								if not mainlights=="lights": bpy.context.active_object.parent = bpy.data.objects.get("lights")
							
							
						parent = bpy.data.objects.get("worklights")
						
						for name in names:
							bpy.ops.object.mode_set(mode = 'OBJECT')
							if "Back" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(90),0,0))
							if "Front" in name : bpy.ops.object.light_add(type='SPOT',location=(0.0, 0.0, 0.0),rotation=(radians(-90),0,0))

							obj = bpy.data.objects.get(bpy.context.active_object.name)

							for lamp in bpy.data.lights:
								if lamp.name == obj.data.name:
									
									distance = 20 if "Low" in name else 25
									lamp.distance=distance									
									angle = radians(130) if "Low" in name else radians(90)
									lamp.spot_size=angle
									lamp.spot_blend=0.6
									lamp.color=(0.85,0.85, 1)
									#lamp.shadow_method=('NOSHADOW')
							bpy.context.active_object.name = name							
							bpy.context.active_object.parent = parent
		
		return {"FINISHED"}




classes = (SCV_PT_addCreateMenu, SCV_OT_TranformCreator, SCV_OT_CameraCreator, SCV_OT_Lightcreator, SCV_OT_Clearer, SCV_OT_CreateAtPoint, )



register, unregister = bpy.utils.register_classes_factory(classes)



