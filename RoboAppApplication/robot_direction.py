#!/usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
import serial
import time

##1P1768#2P1120#3P1655#4P2021#5P697#6P1796#7P1852#8P1204#9P1430#10P1486T1000D500 podtion right above left

execute = ThreadPoolExecutor()
serialport=serial.Serial("COM7",115200,timeout=0.1)

def write_instruction(serialport,instruction):
    print("try")
    try:
        serialport.write(instruction.encode("utf-8"))
        print("2")
        while True:
            print("loop")
            str=serialport.readall().decode("utf-8")
            
            break
        print("instruction execution successful for:")
        print(instruction)
    except Exception as e:
        print(e)


def raise_right_Hand():
        print('start raise right hand')
        write_instruction(serialport,"#21P2500#22P2500#23P2500#24P2500#25P2500#26P2500#29P2069T2000D2000\r\n")
        time.sleep(5)

def raise_left_hand():
    print('start raise left hand')
    write_instruction(serialport,"#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1250#9P2050T2000D2000\r\n")
    time.sleep(5)

def box_right_hand():
    print('start box right hansd')
    write_instruction(serialport,"#12P1130#14P1568#21P2500#22P2500#23P2500#24P2500#25P2500#26P2170#27P1514#29P1711T1000D1000\r\n")
    time.sleep(5)

def box_left_hand():
    print('start box left hand')
    write_instruction(serialport,"#1P2500#2P2500#3P2500#4P2500#5P2500#6P600#7P1432#8P1500#9P1812T1000D1000\r\n")
    time.sleep(5)

def relax_mode():
    print('relax mode')
    write_instruction(serialport,"#1P500#2P500#3P500#4P500#5P500#6P1430#12P1119#13P1937#14P1529#19P2021#21P500#22P500#23P500#24P500#25P500#26P1458T1000D1000\r\n")
    time.sleep(5)

def talking_position():
    print('talking position')
    counter=1
    while True:
        print('talking position1')
        write_instruction(serialport,"#1P2500#2P2500#3P2500#4P2500#5P2500#6P920#7P1458#8P1349#9P1680#12P1250#13P1550#14P1630#21P500#22P500#23P500#24P500#25P500#27P1970#28P1352#29P1731T1000D1000\r\n")
        time.sleep(0.5)
        write_instruction(serialport,"#1P500#2P500#3P500#4P500#5P500#7P1480#12P1410#13P1290#14P1400#21P2500#22P2500#23P2500#24P2500#27P1860T1000D1000\r\n")
        time.sleep(0.5)
        counter+=1
        if counter==3:
            break

def reset_moves():
    print('reset moves')
    write_instruction(serialport,"#1P1500#2P1500#3P1500#4P1500#5P1500#6P900#7P942#8P1500#9P1500#10P1500#11P1881#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P1458#27P900#28P1500#29P1500#30P1500#31P1500#32P1500T500D500\r\n")
    time.sleep(2)

def hello_function():
    print('start hello')
    write_instruction(serialport,"#12P1050#14P1530#19P2300#21P500#22P500#23P500#24P500#25P500#26P1920#27P1400#29P1730T500D500\r\n")
    time.sleep(5)
    
def close_hand():
    print('close hand')
    write_instruction(serialport,"#21P1965#22P1993#23P1880#24P1627#25P2500T1000D1000\r\n")
    time.sleep(5)

def like_function():
    print("like")
    write_instruction(serialport,"#1P2500#2P2500#3P2500#4P2500#5P500#6P641#7P942#8P1204#9P2218#11P1881#12P1266#13P1430#14P1407#15P1120#19P923#25P1500#26P1458#28P1500#29P1500T500D500\r\n")
    time.sleep(5)
   


def start_task():
    
    message = input("Enter command:")
    if message == "raise right hand":
        raise_right_Hand()
        reset_moves()

    elif message == "raise left hand":
        raise_left_hand()
        reset_moves()

    elif message == "hello":
        hello_function()
        reset_moves()

    elif message == "talking":
        talking_position()
        reset_moves()

    elif message == "relax mode":
        relax_mode()
        reset_moves()
    
    elif message == "close hand":
        close_hand()
        reset_moves()

    elif message == "box right hand":
        box_right_hand()
        reset_moves()
    
    elif message == "box left hand":
        box_left_hand()
        reset_moves()
    
    elif message == "like":
        like_function()
        reset_moves()


    
    # try:

        
        # print('start')
        # #Execution of preset instructions
        # write_instruction(serialport,"#1P1570#2P1500#3P1500#4P1500#21P1500#22P1500#23P1500#24P1500#25P1500T1000D800\r\n")
        
        # time.sleep(2)
        # print("Moh")
        # write_instruction(serialport,"#1P1768#2P1345#3P2049#4P1768#21P1570#22P1711#23P1627#24P1824#25P2021T1000D800\r\n")
        # time.sleep(4)
        # write_instruction(serialport,"#1P1570#2P1500#3P1500#4P1500#21P1500#22P1500#23P1500#24P1500#25P1500T1000D800\r\n")
        # time.sleep(4)
        # # #Test for action groups,Group 1 run 3 times
        # # write_instruction(serialport,"G1F3\r\n")

        # # serialport.close()

    # except Exception as e:
    #     print("error",e)

# def run():
#     future3 = execute.submit(start_task)
#     future = execute.submit(mouthLoop(serialport))
    
#     return future,future3

# run()