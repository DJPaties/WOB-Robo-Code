
import json
import time
import serial

def mouth(delay):
        serialport2 = serial.Serial("COM6",9600)
        # Create a JSON object with the 'delayyy' parameter
        
        data = {'delay': delay}  # Change the delay value as needed
        print(data)
        try:
                serialized_data = json.dumps(data)
                serialport2.write(serialized_data.encode()+b'\n')

                time.sleep(1)  # Wait for 1 second before sending the next data
        except KeyboardInterrupt:
            serialport2.close()
            print("Serial connection closed.")




def talking_scenario(delay, mode,server_command):
    ser = serial.Serial('COM10', baudrate=115200, timeout=0.1)
    try:
        
        if mode == "talking":
            counter=0
            while counter<delay:
                ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1500#8P1500#9P1500#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P2200#21P2200#22P2200#23P2200#24P2200#25P2000#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T500D500\r\n".encode())
                # ser.write("#13P1200T500D500\r\n").enc
                time.sleep(0.7)
                counter+=1
                print(counter)
                if counter > delay:
                    break
                ser.write("#13P1400#15P1430T500D500\r\n".encode())
                # ser.write(f"#20P{random.choice(eye_positions)}\r\n".encode())
                time.sleep(0.7)
                counter+=1
                print(counter)
                if counter> delay:
                    break
                ser.write("#13P1000T500D500\r\n".encode())
                time.sleep(0.7)
                counter+=1
                print(counter)
                if counter > delay:
                    break
                ser.write("#7P2000#8P1467#9P1667#10P1856#11P1567#12P2500#13P1000#15P1430#27P1500T500D500\r\n".encode())
                # ser.write(f"#20P{random.choice(eye_positions)}\r\n".encode())
                time.sleep(0.7)
                counter+=1
                print(counter)
                if counter > delay:
                    break
                ser.write("#7P500#12P1200#13P800#15P1430#27P1700#28P1467#29P1633T500D500\r\n".encode())
                # ser.write(f"#20P{random.choice(eye_positions)}\r\n".encode())
                time.sleep(0.7)
                counter+=1
                print(counter)
                if counter > delay:
                    break

            print("end Move")
            ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P500#8P1500#9P1410#10P1852#11P1367#12P1600#13P1100#14P1415#15P1500#16P1500#17P1500#18P1500#19P1500#20P1500#21P2200#22P2200#23P2200#24P2200#25P2200#26P2500#27P1200#28P1500#29P1600#30P2472#31P1500#32P1500T500D500\r\n".encode())
            time.sleep(1.2)
        else:
            ser.write(server_command.encode())
            print("executed cOMMAND")
    except ValueError as e:
        print(e)
# def Ser(server_command):
#     ser = serial.Serial('COM3', baudrate=115200, timeout=0.1)
#     ser.write(server_command.encode())
# mouth(5)

# talking_scenario(7.5, "talking","server_command")