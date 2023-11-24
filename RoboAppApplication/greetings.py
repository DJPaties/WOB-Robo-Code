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
                    talking_scenario(5,"any", "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P500#8P1500#9P1430#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1510#17P1500#18P1500#19P2500#20P1510#21P600#22P600#23P1000#24P1060#25P1000#26P2500#27P1500#28P1400#29P1820#30P2192#31P1500#32P1500T500D500\r\n")
                    close_hand = False
                print("Grab COunter", grab_counter)
                if grab_counter == 50:
                    if langauge_code == "en-US":
                        tts("Leave my hand. ","en-US")
                    else:
                        tts("تْرُوكْ إِيِدِيْ, شو بِيِكْ يَا خَيّْيِ ",'ar-LB')
            elif counter>=3:
                servo_command_2 = "#1P2200#2P2200#3P2500#4P2500#5P2500#6P500#7P2000#8P1400#9P1500#10P1852#11P1500#12P1500#13P1400#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1400#28P1500#29P1650#30P2472#31P1500#32P1500T500D500\r\n"
                talking_scenario(5,"any", servo_command_2)
                time.sleep(1)
                break
            print("IR Sensor Values:", data)
                
        except KeyboardInterrupt:
            break

    ser.close()

# hand_shaking("ar-LB")