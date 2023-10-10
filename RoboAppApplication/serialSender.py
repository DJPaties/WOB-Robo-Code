import serial
import json
import time
ser = serial.Serial('COM4', baudrate=115200, timeout=0.1)
serialport2 = serial.Serial("COM6",9600,timeout=0.1)

def mouth(delay):
        # Create a JSON object with the 'delayyy' parameter
        data = {'delayyy': delay}  # Change the delay value as needed

        try:
                serialized_data = json.dumps(data)
                serialport2.write(serialized_data.encode())

                time.sleep(1)  # Wait for 1 second before sending the next data
        except KeyboardInterrupt:
            serialport2.close()
            print("Serial connection closed.")

def talking_scenario(delay):
    counter=0
    while counter<delay:
        ser.write("#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1367#12P1600#13P1567#15P2133#16P1400#17P1500#18P1500#19P1500#20P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n".encode())
        time.sleep(1)
        counter+=1.1
        # print(counter)
        if counter > delay:
            break
        ser.write("#13P1400#15P1867T1000D1000\r\n".encode())
        time.sleep(1)
        counter+=1.1
        # print(counter)
        if counter > delay:
            break
        ser.write("#13P1333T1000D1000\r\n".encode())
        time.sleep(1)
        counter+=1.1
        # print(counter)
        if counter > delay:
            break
        ser.write("#8P1467#9P1667#10P1856#11P1567#12P2500#13P1733#15P1867#16P1333T1000D1000\r\n".encode())
        time.sleep(1)
        counter+=1.1
        # print(counter)
        if counter > delay:
            break
        ser.write("#12P1200#13P1567#15P1967#16P1467#27P1700#28P1467#29P1633T1000D1000\r\n".encode())
        time.sleep(1)
        counter+=1.1
        # print(counter)
        if counter > delay:
            break
    print("end Move")

def Ser(server_command):
    ser.write(server_command.encode())


