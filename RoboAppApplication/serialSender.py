
import json
import time
import serial
import math
import time
def mouth(delay):
        serialport2 = serial.Serial("COM6",9600)
        # Create a JSON object with the 'delayyy' parameter
        delay = math.floor(delay)
        data = {'delay': delay}  # Change the delay value as needed
        print(data)
        try:
                serialized_data = json.dumps(data)
                serialport2.write(serialized_data.encode()+b'\n')

                time.sleep(1)  # Wait for 1 second before sending the next data
        except KeyboardInterrupt:
            serialport2.close()
            print("Serial connection closed.")
def talking_scenario(delay, mode, server_command):
    ser = serial.Serial('COM10', baudrate=115200)
    try:
        if mode == "talking":
            start_time = time.time()
            # time.sleep(2)
            print(time.time()-start_time, delay -1)
            while time.time() - start_time < delay -1:
                elapsed_time = time.time() - start_time
                print("Move",elapsed_time)
                ser.write("#1P600#2P600#3P600#4P600#5P600#6P500#7P600#8P1500#9P1500#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P2200#21P2200#22P2200#23P2000#24P2200#25P2000#26P2500#27P1300#28P1350#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
                time.sleep(1.2)
                if time.time() - start_time > delay -1:
                    break
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P2233#8P1500#9P1633#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P600#21P600#22P700#23P700#24P500#25P800#26P2500#27P1100#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
                time.sleep(1.2)
                elapsed_time = time.time() - start_time
                print("Move",elapsed_time)
                if time.time() - start_time > delay -1:
                    break
                ser.write("#15P1200T500D500\r\n".encode())
                time.sleep(1.2)
                elapsed_time = time.time() - start_time
                print("Move",elapsed_time)
                if time.time() - start_time > delay -1:
                    break
                time.sleep(1.2)
                if time.time() - start_time > delay -1:
                    break
            # time.sleep(delay_sleep)
            print("end Move")
            ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P933#8P1500#9P1500#10P1852#11P1367#12P1600#13P1100#14P1415#15P1500#16P1500#17P1500#18P1500#19P1500#20P1500#21P2200#22P2200#23P2000#24P2200#25P2200#26P2500#27P1000#28P1500#29P1600#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
            print(delay, "listining")
        else:
                ser.write(server_command.encode())
                print("executed cOMMAND")
    except ValueError as e:
        print(e)
        
# talking_scenario(10,"talking", "acomaos")
# mouth(5)