import serial
import time
from flask import Flask, request
app = Flask(__name__)

ser2 = serial.Serial('COM19', baudrate=9600, timeout=0.1)
@app.route('/command', methods=['POST'])
def head_movement():
    command = request.json.get('message','')
    ser2.write(command.encode())
    print("executed cOMMAND")
    return "executed"
    
if __name__ == '__main__':
    app.run(port=50001)
