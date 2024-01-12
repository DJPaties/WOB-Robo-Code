import pykinect_azure as pykinect
import cv2 as cv
import json
import ast
from concurrent.futures import ThreadPoolExecutor
import time
import requests
import speech_recognition as sr

class BodyTracking:
    def __init__(self) -> None:
        self.righthand = False
        self.lefthand = True
        self.head = False
        self.trackingObject = "Right Hand"
        self.x_pos= 0
        self.code = ""
        self.new_code = ""
        self.detection = False
        self.exit_flag = True
        self.execute = ThreadPoolExecutor()

  
    def get_voice_command(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio,language="ar")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def process_command(self, command):
        if "شمال" in command or 'left' in command:
            self.trackingObject = 'left'
            print("Focus on the left hand.")
        elif "right hand" in command or 'يمين' in command:
            self.trackingObject = 'right'
            print("Focus on the right hand.")
        elif "راس" in command or "عيون" in command or "منخار" in command or "تم" in command:
            self.trackingObject='head'
            print("Focus on the head.")
        elif "وقف" in command or "بيكفي" in command or "خلاص"in command:
            self.exit_flag = False
            print("exiting")
        else:
            print(command)
            print("Command not recognized.")

    def runVoice(self):
        while self.exit_flag:
            voice_command = self.get_voice_command()
            if voice_command:
                self.process_command(voice_command)

    def send_message(self,msg):
    # print(msg)
    
        url = 'http://127.0.0.1:50001/command'
        data = {'message': msg}
        requests.post(url, json=data)
        
    def get_joint_position(self,data_list,joint_name):
        
        for i, line in enumerate(data_list):
            if line == f"{joint_name}:":
                position_line = data_list[i + 1]
                position = position_line.split(":")[1].strip()
                position_list = ast.literal_eval(str(position))
                position_dict = {'x': position_list[0], 'y': position_list[1], 'z': position_list[2]}
                return position_dict

    def get_input(self):
        while True:
            msg = input(">")
            self.trackingObject = msg

    def parse_data_string(self,data_string):
        lines = data_string.strip().split('\n')
        result = {}
        current_joint = ""

        for line in lines:
            if line.startswith("Body:"):
                continue
            elif line.endswith("Joint info:"):
                current_joint = line[:-12].strip()
                result[current_joint] = {}
            else:
                key, value = map(str.strip, line.split(':', 1))
                result[current_joint][key] = value

        return result

    def start_tracking(self):
        pykinect.initialize_libraries(track_body=True)
        
        device_config = pykinect.default_configuration
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
        device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        
        device = pykinect.start_device(config=device_config)
        bodyTracker = pykinect.start_body_tracker()
        
        cv.namedWindow("Depth Image with skeleton",cv.WINDOW_NORMAL)
        
        print_once = True
        
        while True:
            capture = device.update()
            body_frame = bodyTracker.update()
            
            ret_depth, depth_color_image = capture.get_colored_depth_image()
            
            ret_color, body_image_color = body_frame.get_segmentation_image()
            
            if not ret_depth or not ret_color:
                continue
        
            bodies = body_frame.get_bodies()
            if len(bodies)>0:
                for body in bodies:
                    if print_once:
                        x = body_frame.get_body(0)
                        
                        if self.trackingObject == 'right':            
                            self.x_pos = x.get_joint_info()['left hand']['positionx']
                        elif self.trackingObject == "left":
                            self.x_pos = x.get_joint_info()['right hand']['positionx']
                        elif self.trackingObject == "head":
                            self.x_pos = x.get_joint_info()['head']['positionx']
                        if self.x_pos>800:
                            self.new_code = "#1P1300T500\r\n"
                            face_code = "#2P1700T500"
                        elif self.x_pos>600:
                            self.new_code = "#1P1390T500\r\n"
                            face_code = "#2P1590T500"                   
                        elif self.x_pos>500:
                            self.new_code = "#1P1390T500\r\n"
                            face_code = "#2P1570T500"                
                        elif self.x_pos>300:
                            self.new_code = "#1P1440T500\r\n"
                            face_code = "#2P1540T500"
                            
                        elif self.x_pos>200:
                            #1480 eye
                            #1520 head
                            self.new_code = "#1P1480T500\r\n"
                            face_code = "#2P1520T500"
                        elif self.x_pos>0:
                            #1520 eye
                            #1500 head
                            self.new_code = "#1P1520T500\r\n"
                            face_code = "#2P1500T500"
                            
                        elif self.x_pos>-200:
                            #1520 eye
                            #1470 head
                            self.new_code = "#1P1540T500\r\n"
                            face_code = "#2P1470T500"
                            
                        elif self.x_pos>-300:
                            #1560 eye
                            #1450 head
                            self.new_code = "#1P1560T500\r\n"
                            face_code = "#2P1450T500"
                            
                        elif self.x_pos>-500:
                            #210
                            #1420
                            self.new_code = "#1P1610T500\r\n"
                            face_code = "#2P1420T500"
                            
                        elif self.x_pos>-600:
                            #210
                            #1420
                            self.new_code = "#1P1610T500\r\n"
                            face_code = "#2P1370T500"
                            
                        elif self.x_pos>-700:
                            #240 eye
                            #1410 head
                            self.new_code = "#1P1680T500\r\n"
                            face_code = "#2P1350T500"
                            
                        elif self.x_pos>-800:
                            #1700 eye
                            #1400 head
                            self.new_code = "#1P1750T500\r\n"
                            face_code = "#2P1300T500"
                        
                        if self.new_code != self.code:
                            # print("Code:", code)
                            # print("Face code,", face_code)
                            self.code = self.new_code
                            try:
                                print("Executed code")
                                self.send_message(self.code)
                                time.sleep(0.4)
                                # head_movement(face_code)
                                # time.sleep(0.1)
                            except ValueError as e:
                                print(e)
            
            combined_image = cv.addWeighted(depth_color_image, 0.6,body_image_color,0.4,0)
            combined_image = body_frame.draw_bodies(combined_image)
            cv.imshow("Depth image with skeleton",combined_image)
            if cv.waitKey(1) == ord('q'):
                break
            if not self.exit_flag:
                break
        
        
    def run(self):


        future2 = self.execute.submit(self.runVoice)
        future1 = self.execute.submit(self.start_tracking)
        return future1, future2

if __name__ == "__main__":
    app = BodyTracking()
    app.run()

            