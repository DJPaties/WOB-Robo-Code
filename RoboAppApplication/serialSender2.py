import serial

def head_movement(command):
    ser2 = serial.Serial('COM8', baudrate=115200, timeout=0.1)
    ser2.write(command.encode())
    # print("executed cOMMAND")