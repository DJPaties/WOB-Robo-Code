import serial
from TTS import tts
from serialSender import talking_scenario
import time
def hand_shaking(langauge_code):
    print("Entered welcome scenario")
    ser = serial.Serial("COM15", 9600)
    msg = None
    counter = 0
    hang_greet_counter = 0
    grab_counter = 0
    close_hand = True
    while True:
        try:
            data = ser.readline().decode()
            if data != msg:
                msg = data
                counter+=1
                print("Counter")
            if counter == 1:
                hang_greet_counter +=1
                print("Hang counter:", hang_greet_counter)
                if hang_greet_counter == 70:
                    if langauge_code == "en-US":
                        tts("I'm still waiting.","en-US")
                    else:
                        tts("مَعَاشْ تْخَلِّينِي نَاطِرْ ","ar-LB")

            elif counter == 2:
                grab_counter +=1
                if close_hand:
                    talking_scenario(5,"any", "#1P2500#2P2500#3P2500#4P1900#5P1500#6P830#7P1476#8P1440#9P1842#10P1380#11P1500#12P1900#13P2500#14P1540#15P2140#16P1200#17P1500#18P1500#19P1500#20P1500#21P740#22P1180#23P1300#24P1260#25P1300#26P1350#27P1700#28P1660#29P2500#30P1500#31P1500#32P1500T500D500\r\n")
                    close_hand = False
                print("Grab COunter", grab_counter)
                if grab_counter == 50:
                    if langauge_code == "en-US":
                        tts("Leave my hand. ","en-US")
                    else:
                        tts("تْرُوكْ إِيِدِيْ, شو بِيِكْ يَا خَيّْيِ ",'ar-LB')
            elif counter>=3:
                servo_command_2 = "#1P2500#2P2500#3P2500#4P1900#5P1500#6P1570#7P1486#8P1500#9P1842#10P1380#11P1500#12P1900#13P1540#14P1540#15P2140#16P1200#17P1500#18P1500#19P1500#20P1500#21P2340#22P2420#23P2340#24P2380#25P2500#26P1360#27P1500#28P1660#29P2500#30P1500#31P1500#32P1500T500D500\r\n"
                talking_scenario(5,"any", servo_command_2)
                time.sleep(1)
                break
            print("IR Sensor Values:", data)
                    
        except KeyboardInterrupt:
            break

    ser.close()

# hand_shaking("ar-LB")