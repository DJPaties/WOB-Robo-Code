import cv2
from concurrent.futures import ThreadPoolExecutor
import w2n
import os
from helperstictactoe import check_turn, check_for_win, draw_board
import random
import time
from ExtraTTS import tts
executor = ThreadPoolExecutor()
image = cv2.imread("blackscreen.png")
msg = ""
options_O = []
options_X = []
global endgame
endgame = False
import speech_recognition as sr 

tts("Let's play. You are X and I am O.","en-US")
tts(" Start","en-US")

def stt(languageCode):
    lang_code = languageCode
    # Create a recognizer object
    r = sr.Recognizer()
    
    # Open the microphone for capturing the speech
    with sr.Microphone() as source:
        print("Listening...")   
        
        # Adjust the energy threshold for silence detection
        r.energy_threshold = 4000

        audio = r.listen(source)

        try:

            text = r.recognize_google(audio, language=lang_code)
            print("You said:", text)
            

        
        except sr.UnknownValueError:
            #TODO here in future time is where will we implement the sleep function that turns microphoneoff
            # when there is no one talking to him
             x = stt(lang_code)
             return x
        except sr.RequestError as e:
            text="Could not request results from Google Speech Recognition service; {0}".format(e)
            print(text)
            # self.open_mic()
        
        return text
def input_msg():
    # booleanX = True
    # booleanO = False
    # while True:
    #     count = 0

    #     global msg
    #     msg = stt("en")
    #     # msg = "I choose 8"
        
    #     msg_list = msg.split(" ")
        
    #     print(msg_list)
    #     for word in msg_list:
    #         x = w2n.word_to_num(word)
    #         print(x)
    #         if x != None:
    #             count +=int(x)
                    
    #     msg = int(count)
    #     print(type(msg))
    #     # print(count)
    #     # if msg.isdigit():    
    #     print("!")
    #     if int(msg)>9 or int(msg)<1:
    #         print("invalid input")
    #     elif int(msg) in options_O or int(msg) in options_X:
    #         print("Already taken")
    #     elif booleanX:
    #         options_X.append(int(msg))
    #         booleanX= False
    #         booleanO = True
    #     elif booleanO:
    #         options_O.append(int(msg))
    #         booleanX = True
    #         booleanO = False
    #     # else:
    #     #     print("invalid Input")
    spots = {1 : '1', 2 : '2', 3: '3', 4 : '4', 5 : '5', 
         6 : '6', 7 : '7',  8 : '8', 9 : '9'}
    playing, complete = True, False
    turn = 0
    prev_turn = -1
    global endgame
    while playing:
        time.sleep(0.5)
        count = 0
    # Reset  the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Draw the current Game Board
        draw_board(spots)
        # If an invalid turn occurred, let the player know
        if prev_turn == turn:
            print("Invalid spot selected, please pick another.")
        prev_turn = turn
        print("Player " + str((turn % 2) +1 ) + "'s turn: Pick your spot or press q to quit")
        
        # Get input and make sure it's valid
        if check_turn(turn) == 'X': 
            non_O_X_keys = [key for key, value in spots.items() if value not in ('O', 'X')]
            msg = random.choice(non_O_X_keys)
            turn += 1
            if check_turn(turn) == 'X': options_X.append(int(msg))
            else: options_O.append(int(msg))
            spots[int(msg)] = check_turn(turn)
            answers = ["I will choose ","My choice will be", "I'll go with ","Hmmm. give me "]
            tts(f"{random.choice(answers)}{msg}","en-US")
            # time.sleep(1)
        else:
            msg = stt("en")
            msg_list = msg.split(" ")
            print(msg_list)
            for word in msg_list:
                x = w2n.word_to_num(word)
                print(x)
                if x != None:
                    count +=int(x)
                        
            msg = int(count)
            # The game has ended, 
            print(msg,"HELLo")
            # if msg == 'stop':
            #     playing = False
            if int(msg) in spots:
                print(2)
            # Check if the spot is already taken.
                if not spots[int(msg)] in {"X", "O"}:
                # If not, update board and increment the turn
                    turn += 1
                    if check_turn(turn) == 'X': options_X.append(int(msg))
                    else: options_O.append(int(msg))
                    spots[int(msg)] = check_turn(turn)
            
        # Check if the game has ended (and if someone won)
        if check_for_win(spots): playing, complete,endgame = False, True,True
        if turn > 8:
            playing = False
            endgame = True
        print(2)
    # Update the board one last time. 
    os.system('cls' if os.name == 'nt' else 'clear')
    draw_board(spots)
    # If there was a winner, say who won
    if complete:
        if check_turn(turn) == 'X': tts("Nice one, you win.","en-US")#print("Player 1 Wins!")
        else: tts("I won easily.","en-US")#print("Player 2 Wins!")
    else: 
    # Tie Game
        tts("Its a draw. We'll catch on later then.","en-US")
        print("No Winner")
    
     

executor.submit(input_msg)

for i in range(1, 3):
    cv2.line(image, (0, i * image.shape[0] // 3), (image.shape[1], i * image.shape[0] // 3), (255, 255, 255), 2)
    cv2.line(image, (i * image.shape[1] // 3, 0), (i * image.shape[1] // 3, image.shape[0]), (255, 255, 255), 2)

cv2.imshow("Tic Tac Toe Layout", image)

while True:
    modified_image = image.copy()

    
    for i in options_O:
        if i == 1:
            cv2.circle(modified_image, (image.shape[0] // 6, image.shape[0] // 6), 100, (255, 0, 255), 5)
        if i == 2:
            cv2.circle(modified_image, (image.shape[0] // 2, image.shape[0] // 6), 100, (255, 0, 255), 5)
        if i == 3:
            cv2.circle(modified_image, (image.shape[0] // 2 + image.shape[0]//3, image.shape[0] // 6), 100, (255, 0, 255), 5)
        if i == 4:
            cv2.circle(modified_image, (image.shape[0] // 6, image.shape[0] // 2), 100, (255, 0, 255), 5)
        if i == 5:
            cv2.circle(modified_image, (image.shape[0] // 2, image.shape[0] // 2), 100, (255, 0, 255), 5)
        if i == 6:
            cv2.circle(modified_image, (image.shape[0] // 2 + image.shape[0]//3, image.shape[0] // 2), 100, (255, 0, 255), 5)
        if i == 7:
            cv2.circle(modified_image, (image.shape[0] // 6, image.shape[0] // 2 + image.shape[0]//3), 100, (255, 0, 255), 5)
        if i == 8:
            cv2.circle(modified_image, (image.shape[0] // 2, image.shape[0] // 2 + image.shape[0]//3), 100, (255, 0, 255), 5)
        if i == 9:
            cv2.circle(modified_image, (image.shape[0] // 2 + image.shape[0]//3, image.shape[0] // 2 + image.shape[0]//3), 100, (255, 0, 255), 5)
    
    for j in options_X:
        if j==1:
            center_x, center_y = image.shape[1] // 6, image.shape[0] // 6
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==2:
            center_x, center_y = image.shape[1] // 2, image.shape[0] // 6
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==3:
            center_x, center_y = image.shape[1] // 2+image.shape[1] // 3, image.shape[0] // 6
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==4:
            center_x, center_y = image.shape[1] // 6, image.shape[0] // 2
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==5:
            center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==6:
            center_x, center_y = image.shape[1] // 2+image.shape[1] // 3, image.shape[0] // 2
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==7:
            center_x, center_y = image.shape[1] // 6,image.shape[1] // 2+ image.shape[0] // 3
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==8:
            center_x, center_y = image.shape[1] // 2, image.shape[0] // 2+image.shape[0] // 3
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)
        if j==9:
            center_x, center_y = image.shape[1] // 2+image.shape[1] // 3, image.shape[0] // 2+ image.shape[0]//3
            arm_length = 100
            cv2.line(image, (center_x - arm_length, center_y - arm_length), 
                    (center_x + arm_length, center_y + arm_length), (255, 0, 255), 5)
            cv2.line(image, (center_x - arm_length, center_y + arm_length), 
                    (center_x + arm_length, center_y - arm_length), (255, 0, 255), 5)


    # print(random.choice(options))

    cv2.imshow("Tic Tac Toe Layout", modified_image)
    
    # Check if the 'q' key is pressed to break the loop
    key = cv2.waitKey(100)
    if key != -1:
        if key == ord('q'):
            break
    
    if endgame :
        time.sleep(1)
        break

cv2.destroyAllWindows()
