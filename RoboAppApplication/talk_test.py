
import serial
import time
ser = serial.Serial('COM10', baudrate=115200, timeout=0.1)

def talking_scenario(delay, mode,server_command):

    try: 
        if mode == "talking":
            counter=0
            while counter<delay:
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P2467#8P1500#9P1700#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P600#24P600#25P1000#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
                time.sleep(1.1)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P2467#8P1100#9P1700#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P600#24P600#25P1000#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())

                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P2467#8P1100#9P1700#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P600#24P600#25P1000#26P2500#27P1733#28P1567#29P1700#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1067#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1200#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2200#25P1000#26P2500#27P1733#28P1567#29P1700#30P2472#31P1500#32P1500T1000D1000\r\n".encode())

                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1067#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P650#22P650#23P650#24P600#25P1000#26P2500#27P1733#28P1167#29P1700#30P2472#31P1500#32P1500T1000D1000\r\n".encode())

                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1067#8P1200#9P1800#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P650#22P650#23P650#24P600#25P1000#26P2500#27P1733#28P1167#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())

                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P500#2P500#3P500#4P500#5P600#6P500#7P1500#8P1200#9P1800#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2200#25P2200#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())

                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break
                ser.write("#1P600#2P500#3P500#4P500#5P700#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P600#24P600#25P1000#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())

                time.sleep(1.2)
                counter+=1.1
                print(counter)
                if counter > delay:
                    break

            print("end Move")
            ser.write("#1P500#2P500#3P500#4P700#5P500#6P500#7P1500#8P1500#9P1410#10P1852#11P1367#12P1600#13P1500#14P1415#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P600#24P500#25P800#26P2500#27P1500#28P1500#29P1600#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
    except ValueError as err:
        pass

talking_scenario(1.3, "talking","server_command")