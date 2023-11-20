import cv2
import json
import pykinect_azure as pykinect
import time
from serialSender2 import head_movement
import serial
global signal
signal = True
# if __name__ == "__main__":
def set_signal(boolean):
    global signal
    signal = boolean





def start_eye():
	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(track_body=True)

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	# Start body tracker
	bodyTracker = pykinect.start_body_tracker()

	cv2.namedWindow('Depth image with skeleton',cv2.WINDOW_NORMAL)
	global code
	code = "#1P1500\r\n"
	global new_code
	new_code = ""
	global face_code
	face_code = "#2P1500T500D500\r\n"
	while True:	

		# Get capture
		capture = device.update()

		# Get body tracker frame
		body_frame = bodyTracker.update()

		# Get the color depth image from the capture
		ret_depth, depth_color_image = capture.get_colored_depth_image()

		# Get the colored body segmentation
		ret_color, body_image_color = body_frame.get_segmentation_image()
		if signal == False:
			break

		if not ret_depth or not ret_color:
			continue
		
		bodies = body_frame.get_bodies()
		# print(bodies)
		if len(bodies)>0:
			for body in bodies:
				x = body_frame.get_body(0)
				x_pos = (x.get_joint_info()['head']['positionx'])
				y_pos = (x.get_joint_info()['head']['position y'])
				# print(x_pos,y_pos)
				if x_pos>800:
					#1300 eye
					#200 head
					new_code = "#1P1300\r\n"
					face_code = "#2P1700T500D500\r\n"
					
				elif x_pos>700:
					#1360 eye
					#1570 head
					new_code = "#1P1360\r\n"
					face_code = "#2P1650T500D500\r\n"
					
				elif x_pos>600:
					#1390
					#1560
					new_code = "#1P1390\r\n"
					face_code = "#2P1590T500D500\r\n"
					
				elif x_pos>500:
					#1390
					#1550
					new_code = "#1P1390\r\n"
					face_code = "#2P1570T500D500\r\n"
					
				elif x_pos>300:
					#1440 eye
					#1520 head
					new_code = "#1P1440\r\n"
					face_code = "#2P1540T500D500\r\n"
					
				elif x_pos>200:
					#1480 eye
					#1520 head
					new_code = "#1P1480\r\n"
					face_code = "#2P1520T500D500\r\n"
					

				elif x_pos>0:
					#1520 eye
					#1500 head
					new_code = "#1P1520\r\n"
					face_code = "#2P1500T500D500\r\n"
					
				elif x_pos>-200:
					#1520 eye
					#1470 head
					new_code = "#1P1540\r\n"
					face_code = "#2P1470T500D500\r\n"
					
				elif x_pos>-300:
					#1560 eye
					#1450 head
					new_code = "#1P1560\r\n"
					face_code = "#2P1450T500D500\r\n"
					
				elif x_pos>-500:
					#210
					#1420
					new_code = "#1P1610\r\n"
					face_code = "#2P1420T500D500\r\n"
					
				elif x_pos>-600:
					#210
					#1420
					new_code = "#1P1610\r\n"
					face_code = "#2P1370T500D500\r\n"
					
				elif x_pos>-700:
					#240 eye
					#1410 head
					new_code = "#1P1640\r\n"
					face_code = "#2P1350T500D500\r\n"
					
				elif x_pos>-800:
					#1700 eye
					#1400 head
					new_code = "#1P1700\r\n"
					face_code = "#2P1300T500D500\r\n"
				
				if new_code != code:
					# print("Code:", code)
					# print("Face code,", face_code)
					code = new_code
					try:
						head_movement(code)
						time.sleep(0.2)
						head_movement(face_code)
						# time.sleep(0.1)
					except ValueError as e:
						print(e)
					
					
					


		# Combine both images
		combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)

		# Draw the skeletons
		combined_image = body_frame.draw_bodies(combined_image)

		# Overlay body segmentation on depth image
		cv2.imshow('Depth image with skeleton',combined_image)

		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):  
			break

start_eye()