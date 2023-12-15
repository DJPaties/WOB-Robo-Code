
import json
import time
import serial
import math
import time
import threading
def mouth(delay):
        serialport2 = serial.Serial("COM13",9600)
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




def talking_scenario(delay, mode,server_command):
    ser = serial.Serial('COM10', baudrate=115200)
    try:
        
        if mode == "talking":
            run_function_in_thread(delay,ser)
#             counter=0
#             while counter<delay:
#                 ser.write("#1P600#2P600#3P600#4P600#5P600#6P500#7P600#8P1500#9P1500#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P2200#21P2200#22P2200#23P2200#24P2200#25P2000#26P2500#27P1300#28P1350#29P1500#30P2472#31P1500#32P1500T1000D500\r\n".encode())
#                 # ser.write("#13P1200T500D500\r\n").enc
#                 time.sleep(1.2)
#                 counter+=1.1
#                 print(counter)
#                 if counter > delay:
#                     break
#                 ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P2233#8P1500#9P1633#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P600#21P600#22P700#23P700#24P500#25P800#26P2500#27P1100#28P1500#29P1500#30P2472#31P1500#32P1500T1000D500\r\n".encode())
#                 # ser.write("#15P1000T1000D500\r\n".encode())
#                 # ser.write(f"#20P{random.choice(eye_positions)}\r\n".encode())
#                 time.sleep(1.2)
#                 counter+=1
#                 print(counter)
#                 if counter> delay:
#                     break
#                 ser.write("#15P1200T500D500\r\n".encode())
#                 time.sleep(1.2)
#                 counter+=1
#                 print(counter)
#                 if counter > delay:
#                     break
# #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#             print("end Move")
#             ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P933#8P1500#9P1500#10P1852#11P1367#12P1600#13P1100#14P1415#15P1500#16P1500#17P1500#18P1500#19P1500#20P1500#21P2200#22P2200#23P2200#24P2200#25P2200#26P2500#27P1000#28P1500#29P1600#30P2472#31P1500#32P1500T1000D500\r\n".encode())
#             # time.sleep(1.2)
        else:
            ser.write(server_command.encode())
            print("executed cOMMAND")
    except ValueError as e:
        print(e)
# def Ser(server_command):
#     ser = serial.Serial('COM3', baudrate=115200, timeout=0.1)
#     ser.write(server_command.encode())

# talking_scenario(5,"any","#1P2300T1000\r\n")
# time.sleep(3)
# talking_scenario(5,"any","#1P700T1000\r\n")

#1P1500#2P2500#3P1353#4P2500#5P2500#6P2500#7P2500#8P2500#9P2500#10P2500#11P2500#12P2500#13P2500#14P2500#15P2500#16P2500#17P2500#18P2500#19P2500#20P2500#21P2500#22P2500#23P2500#24P2500#25P2500#26P2500#27P2500#28P2500#29P2500#30P2500#31P2500#32P2500T1000



def loop_under_timer(stop_event,delay_sleep,ser):
    # ser = serial.Serial('COM10', baudrate=115200)
    start_time = time.time()
    counter = 0

    while not stop_event.is_set():
        ser.write("#1P600#2P600#3P600#4P600#5P600#6P500#7P600#8P1500#9P1500#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P2200#21P2200#22P2200#23P2200#24P2200#25P2000#26P2500#27P1300#28P1350#29P1500#30P2472#31P1500#32P1500T1000D500\r\n".encode())
        print("Move")
        if stop_event.is_set():
            break
        time.sleep(1.2)
        counter += 1.2
        if stop_event.is_set():
            break
        ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P2233#8P1500#9P1633#10P1852#11P1367#12P1600#13P1200#14P1500#15P1500#16P1400#17P1500#18P1500#19P1500#20P600#21P600#22P700#23P700#24P500#25P800#26P2500#27P1100#28P1500#29P1500#30P2472#31P1500#32P1500T1000D500\r\n".encode())
        print("Move")
        if stop_event.is_set():
            break
        time.sleep(1.2)
        counter += 1.2
        if stop_event.is_set():
            break
        ser.write("#15P1200T500D500\r\n".encode())
        print("Move")
        if stop_event.is_set():
            break
        time.sleep(1.2)
        counter += 1.2
        if stop_event.is_set():
            break
    time.sleep(delay_sleep)
    print("end Move")
    ser.write("#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P933#8P1500#9P1500#10P1852#11P1367#12P1600#13P1100#14P1415#15P1500#16P1500#17P1500#18P1500#19P1500#20P1500#21P2200#22P2200#23P2200#24P2200#25P2200#26P2500#27P1000#28P1500#29P1600#30P2472#31P1500#32P1500T1000D500\r\n".encode())

    elapsed_time = time.time() - start_time
    print("Total Elapsed Time:", elapsed_time)

def run_function_in_thread(input_time,ser):
    stop_event = threading.Event()
    if input_time >12:
        delay_sleep = 1.5
    else:
        delay_sleep = 1
    thread = threading.Thread(target=loop_under_timer, args=(stop_event,delay_sleep,ser))
    thread.start()
    # Allow the thread to run for a specified time
    print(input_time-2)
    thread.join(timeout=(input_time-2))

    # Set the stop event to gracefully stop the thread
    stop_event.set()

    # Wait for the thread to finish
    thread.join()

# Example: Run the loop in a thread for 7.68 seconds
# timer_duration = 5.65
# run_function_in_thread(timer_duration)


# mouth(5)


# talking_scenario(7.5, "talking","server_command")