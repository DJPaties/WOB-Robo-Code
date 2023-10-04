import serial
import json
import time

# Define the serial port and baud rate
serial_port = 'COM6'  # Change to the correct port name
baud_rate = 9600

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate)

# Create a JSON object with the 'delayyy' parameter
data = {'delayyy': 5}  # Change the delay value as needed

try:
    
        # Serialize the JSON object and send it to Arduino
        serialized_data = json.dumps(data)
        ser.write(serialized_data.encode())

        # Optionally, wait for a response from Arduino
        # response = ser.readline().decode().strip()
        # print(f"Arduino response: {response}")

        time.sleep(1)  # Wait for 1 second before sending the next data
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
