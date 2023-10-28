import cv2
import mediapipe as mp
import serial
import time
cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)
serialport=serial.Serial("COM10",115200,timeout=0.1)
old_code=""
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
write_instruction(serialport,"#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1500#17P1500#18P1500#19P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n")
# time.sleep(2)
time.sleep(0.5)
while True:
    success, image = cap.read()
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
        code = ""
        counter = 21
        for i in msg:
            if i == 1:
                value = 500
            else:
                value = 2500
            
            code+=f"#{counter}P{value}"
            counter+=1
        code+= "T1000D1000\r\n"
        # print(code)
        
        print("OLD CODE:", old_code)
        print("NEW CODE:", code)
        
        if old_code != code:
            # print("Not same make same")
            old_code = code
            write_instruction(serialport,code)

        else:
            pass
        if msg == [0,0,1,1,0]:
            cv2.putText(image, "scissors", (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
        if msg == [0,0,0,0,0]:
            cv2.putText(image, "rock", (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
        if msg == [1,1,1,1,1]:
            cv2.putText(image, "paper", (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
        time.sleep(0.2)
        #  #21P500#22P500#23P500#24P500#25P500T1000D1000
    cv2.imshow("Finger detection :", image)
    cv2.waitKey(1)