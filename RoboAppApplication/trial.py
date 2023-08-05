import serial
import time

arduino = serial.Serial(port='COM10', baudrate=9600, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().decode().strip()  # Convert bytes to string and remove whitespace characters
    return data


while True:
    num = input("Enter a number: ")
    try:
        num = int(num)  # Convert the input string to an integer
        value = write_read(str(num))  # Convert the integer back to a string before sending
        print(value)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
