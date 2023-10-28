import cv2
import mediapipe as mp
import serial
import time
import random
from TTS import tts
from serialSender import talking_scenario
x, y, width, height = 300, 000, 700, 700  

# serialport=serial.Serial("COM10",115200,timeout=0.1)
robot_score=0
player_score=0

def end_game():
    # write_instruction(serialport,"#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n")
    # Ser("#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n")
    reset = "#1P2500#2P2380#3P2500#4P2500#5P2380#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T500D500\r\n" 
    talking_scenario(5,"any",reset)
    tts(f"End of game, your score is {player_score}. My score is  {robot_score}. Nice Game!", "en-US")
    exit(0)

def movement_scenario(option):
    print('Movement Scenario Option :', option)
    # serialport=serial.Serial("COM8",115200,timeout=0.1)

    # def write_instruction(serialport,instruction):
    #     # print("try")
    #     try:
    #         serialport.write(instruction.encode("utf-8"))
    #         # print("2")
    #         while True:
    #             print("loop")
    #             str=serialport.readall().decode("utf-8")
                
    #             break
    #         # print("instruction execution successful for:")
    #         print(instruction)
    #     except Exception as e:
    #         print(e)


    # write_instruction(serialport, "#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    # Ser("#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    move1 = "#1P2380#2P2500#3P2500#4P2500#5P2460#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P550#22P550#23P550#24P550#25P800#26P1570#27P1740#28P1035#29P1908#30P2472#31P1500#32P1500T200D500\r\n"
    talking_scenario(5,"any",move1)
    time.sleep(3)
    
    # write_instruction(serialport, "#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1683#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    # Ser("#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1683#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    move2 = "#1P2500#2P2359#3P2500#4P2500#5P2500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P550#22P550#23P550#24P550#25P800#26P1570#27P1880#28P1035#29P1988#30P2472#31P1500#32P1500T200D500\r\n"
    talking_scenario(5,"any",move2)
    time.sleep(0.4)
    
    # write_instruction(serialport, "#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    # Ser("#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    move3 = "#1P2380#2P2500#3P2500#4P2500#5P2460#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P550#22P550#23P550#24P550#25P800#26P1570#27P1740#28P1035#29P1908#30P2472#31P1500#32P1500T200D500\r\n"
    talking_scenario(5,"any",move3)
    time.sleep(0.4)
    
    # write_instruction(serialport, "#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1683#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    # Ser("#1P500#2P2359#3P500#4P500#5P500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1683#28P1035#29P1908#30P2472#31P1500#32P1500T200D200\r\n")
    move4 = "#1P2500#2P2359#3P2500#4P2500#5P2500#6P1373#7P2331#8P1035#9P1739#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P550#22P550#23P550#24P550#25P800#26P1570#27P1880#28P1035#29P1988#30P2472#31P1500#32P1500T200D500\r\n"
    talking_scenario(5,"any",move4)

    time.sleep(0.4)
    if option == "scissors":
    # #Scissor
        print("Scissor")
        # write_instruction(serialport, "#1P500#2P2500#3P500#4P500#5P500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2500#22P2500#23P500#24P500#25P2500#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n")
        # Ser("#1P500#2P2500#3P500#4P500#5P500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P500#22P500#23P2200#24P500#25P600#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n")    
        scissor_move = "#1P2500#2P2500#3P2500#4P2500#5P2220#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P500#22P500#23P2200#24P2500#25P900#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n"
        talking_scenario(5,"any",scissor_move)
    
    #Rock
    elif option == "rock":
        print("rock")
        # write_instruction(serialport, "#1P500#2P2500#3P500#4P500#5P500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2500#22P2500#23P2500#24P1880#25P2500#26P1711#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n")
        # Ser( "#1P500#2P2500#3P500#4P500#5P500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P500#22P500#23P500#24P500#25P600#26P1711#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n")
        rock_move = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P500#22P500#23P500#24P500#25P900#26P1711#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n"
        talking_scenario(5,"any",rock_move)
    #Paper
    elif option == "paper":
        print("paper")
        # write_instruction(serialport, "#1P500#2P2500#3P500#4P500#5P500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P500#22P500#23P500#24P500#25P500#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n")
        # Ser("#1P500#2P2500#3P500#4P500#5P500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n")
        paper_move = "#1P2340#2P2500#3P2500#4P2500#5P2500#6P1373#7P1204#8P1035#9P1599#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2350#25P2200#26P1570#27P1408#28P1035#29P1908#30P2472#31P1500#32P1500T500D500\r\n"
        talking_scenario(5,"any",paper_move)
    time.sleep(1)
    # write_instruction(serialport,"#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n")


new_choice = True
def get_npc_choice():
    global new_choice
    if new_choice:
        choices = ["rock", "paper", "scissors"]
        npc_choice = random.choice(choices)
        new_choice = False
        print(npc_choice)
        movement_scenario(npc_choice)
        return npc_choice

def determine_winner(player_choice, npc_choice):
    global player_score
    global robot_score
    print(player_choice, npc_choice)
    global new_choice
    if player_choice == npc_choice:
        tts("It's a tie!")
        return "It's a tie!"
    elif player_choice == "rock":
        if npc_choice == "scissors":
            tts("You win! You chose rock and  I chose scissors.", "en-US")
            player_score+=1
            return "You win!"  
        else:
            tts("I WIN! I chose paper and you chose rock.", "en-US")
            robot_score+=1
            return "NPC wins!"
    elif player_choice == "paper":
        if npc_choice == "scissors":
            tts("I win! You chose paper and  I chose scissors.", "en-US")
            player_score+=1
            return "NPC win!"  
        else:
            tts("YOU WIN! I chose rock and you chose paper.", "en-US")
            robot_score+=1
            return "YOU wins!"
        # return "You win!" if npc_choice == "rock" else "NPC wins!"
    elif player_choice == "scissors":
        if npc_choice == "paper":
            tts("You win! I chose paper and  you chose scissors.", "en-US")
            player_score+=1
            return "You win!"  
        else:
            tts("I WIN! I chose rock and you chose scissors.", "en-US")
            robot_score+=1
            return "NPC wins!"
        # return "You win!" if npc_choice == "paper" else "NPC wins!"
    new_choice = True


cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)

msg_counter=0
old_msg = []

round_counter=0
# print(robot_choice)
def write_instruction(serialport,instruction):
    # print("try")
    try:
        serialport.write(instruction.encode("utf-8"))
        # print("2")
        while True:
            print("loop")
            str=serialport.readall().decode("utf-8")
            
            break
        # print("instruction execution successful for:")
        print(instruction)
    except Exception as e:
        print(e)

print('reset moves')
# write_instruction(serialport,"#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n")
# Ser("#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n")
talking_scenario(5,"any","#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T500D500\r\n")
tts("Let's play best out of 3", "en-US")
# time.sleep(2)
time.sleep(2)
robot_choice = get_npc_choice()
while True:
    
    success, image = cap.read()
    image_height = image.shape[0]
    image = image[y:y+height, x:x+width]
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)

    multiLandMarks = results.multi_hand_landmarks

    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
              h, w, c = image.shape
              cx, cy = int(lm.x * w), int(lm.y * h)
              handList.append((cx, cy))
        for point in handList:
            cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
        upCount = 0
        # for coordinate in finger_Coord:
        #     if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
        #         upCount += 1
        
        
        # pointer finger
        if handList[finger_Coord[0][0]][1]< handList[finger_Coord[0][1]][1]:
            pointer_finger=1
        else:
            pointer_finger=0
        #middle finger     
        if handList[finger_Coord[1][0]][1]< handList[finger_Coord[1][1]][1]:
            middle_finger=1
        else:
            middle_finger=0
        #ring finger
        if handList[finger_Coord[2][0]][1]< handList[finger_Coord[2][1]][1]:
            ring_finger=1
        else:
            ring_finger=0
        #pinky finger
        if handList[finger_Coord[3][0]][1]< handList[finger_Coord[3][1]][1]:
            pinky_finger=1
        else:
            pinky_finger=0
        #thumb_finger 
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            thumb_finger= 1
        else:
            thumb_finger=0
        msg = [pinky_finger, ring_finger,middle_finger,pointer_finger,thumb_finger]
        #        21             22             23         24             25   
        # cv2.putText(image, str(msg), (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
        # code = ""
        # counter = 21
        # for i in msg:
        #     if i == 1:
        #         value = 2300
        #     else:
        #         value = 550
            
        #     code+=f"#{counter}P{value}"
        #     counter+=1
        # code+= "T1000D1000\r\n"
        # print(code)
        
        # print("OLD CODE:", old_code)
        # print("NEW CODE:", code)
        
        # if old_code != code:
        #     # print("Not same make same")
        #     old_code = code
        #     write_instruction(serialport,code)

        # else:
        #     pass
        if round_counter<=2:
            print("Round number START: ",round_counter)                
            if old_msg != msg:
                old_msg = msg
                msg_counter=0
        
            else:
                msg_counter+=1
                print(msg_counter)
                if msg_counter>=3:
                    print(msg)
                    # global new_choice
                    if msg == [0,0,1,1,0]:
                        cv2.putText(image, "scissors", (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
                        print(determine_winner("scissors",robot_choice))
                        if round_counter < 2:
                            new_choice = True
                        else:
                            new_choice = False
                        robot_choice = get_npc_choice()
                        msg_counter = 0
                        round_counter+=1                        
                        print(robot_choice)
                    elif msg == [0,0,0,0,0]:
                        cv2.putText(image, "rock", (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
                        print(determine_winner("rock",robot_choice))
                        if round_counter < 2:
                            new_choice = True
                        else:
                            new_choice = False
                        robot_choice = get_npc_choice()
                        msg_counter = 0
                        round_counter+=1
                        print(robot_choice)
                    elif msg == [1,1,1,1,1]:
                        cv2.putText(image, "paper", (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
                        print(determine_winner("paper",robot_choice))
                        if round_counter < 2:
                            new_choice = True
                        else:
                            new_choice = False
                        robot_choice = get_npc_choice()
                        msg_counter = 0
                        round_counter+=1
                        print(robot_choice)
                    else:
                        print("Invalid input")

                    
                
        elif round_counter == 3:
            # tts(f"End of game your score is {player_score}. My score is  {robot_score}. Nice Game!")
            end_game()
            round_counter+=1
        else: 
            pass
        time.sleep(0.2)
        #  #21P500#22P500#23P500#24P500#25P500T1000D1000
    cv2.imshow("Finger detection :", image)
    cv2.waitKey(1)