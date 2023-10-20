import face_recognition
import cv2
import os 
from create_delete_new.save import capture_faces
from encoding.add_last_encoder import add_to_encod
from encoding.load_encoded_file import load_encoded_file

from dotenv import load_dotenv,dotenv_values
from module_vision.find_most_frequent_word import find_most_frequent_word
from module_vision.add_new_face import add_new_face
import threading
import socket
import json
import time
# from  module_vision.send_receive_socket  import send_name_socket ,receive_socket

load_dotenv()


# x, y, width, height = 300, 000, 700, 700

#this code will open the camera and encod the face and then print the name
def start (encoding_list , ip_address , port):
    
    new_face = ""
    previous_text = ""
    receive_name = ""
    #read data from encoding file
    myListId,encodListKnown=zip(*encoding_list)
    
    #add face after many unkown face
    count_to_add_face=0


    #socket setting
    ip_server = ip_address 
    port_server = port
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        server_address = (ip_server,port_server )  # Replace with the server address and port
        client_socket.connect(server_address)
    except:
        print(f"connection to server is timed out ! ")



    #initialization of design parameter
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1.5
    fontcolor = (0, 255, 0)  # Green color in BGR format
    lineThickness = 2
    cap = cv2.VideoCapture(1)
    cap.set(3,720)
    cap.set(4,1280)
    
    #Function to get name from app 
    # def thread_function():
    #     while True:
    #         name = client_socket.recieve(1024).decode()

    #         print(f'SERVER RESPONSE: ${name}')




    myListId_name=[]
    for item in myListId:
        myListId_name.append(item.split('/')[0])

    while True:
        
        
        #state: noface -existface -newface-faceKnown -4
        state='noface'
        text=""

        #read image from the camera
        success , img =cap.read()

        #resize the image
        imgS =cv2.resize(img,(0,0),None,0.25,0.25)

        #change the color
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

        #the location of the recognized face
        list_face_loc=face_recognition.face_locations(imgS)
        # print(f"the number of detected face from camera are {len(list_face_loc)}")
        
        if len(list_face_loc)>0:
            # print(f"the location is {list_face_loc}")
            state='existface'
            # print('exist face')
        
        #if the face exist encod it and make the text firstly  as unkown ( it may take name)
        if state=='existface':
            #encod the specific location in the face
            encodeCurFrame=face_recognition.face_encodings(imgS,list_face_loc)
            text="unknown"
        

        #first we will suppose that the image is not stored in the database
        # known_face=False
       
           #the list id is (folder/namefile) we will take only 
            #..the name of folder and append it to a list
            #.. so every image return true will added to list
        
        # list contain face that give us true after comparaison with the frame 
        list_of_True_face=[] 
        
        if(state=='existface'):
            for encodeFace ,_ in zip(encodeCurFrame,list_face_loc):
                
                #check for the smallest distance and print the table of matches
                matches=face_recognition.compare_faces(encodListKnown,encodeFace)
                
                distance=face_recognition.face_distance(encodListKnown,encodeFace)
                
                #update the threshold of matches from 0.6 to 0.5
                for index ,item in enumerate(distance):
                    if item <0.5:
                        matches[index]=True
                    else:
                        matches[index]=False
                
                # print(f'list {myListId_name}')
                # print(f"matches {matches}")
                # print(f"distance {distance}")
        
                # matchIndex=np.argmin(distance)
                
                
                #this count for the true face in the list
                
                for index,match in enumerate(matches):
                    if match==True:
                        # known_face=True
                        #create a list of image that have true value
                        list_of_True_face.append(myListId[index].split('/')[0])

                # #number of face that have true value in the list        
                # number_true_face=len(list_of_true)       
                # print(f"list of face {list_of_true} {number_true_face}")
                
                # get the most frequent face
                most_frequent_face = find_most_frequent_word(list_of_True_face) #take the most frequent image as text 

                most_frequent_number=0
                for item in list_of_True_face:
                    if item == most_frequent_face:
                        most_frequent_number += 1

                

                #name the photo
                if most_frequent_number>3 :
                    state= 'faceknown'
                else :
                    if state=='existface':
                        state='newface'
                





                if  state== 'faceknown':
                                       
                    #this must has a value 
                    # first_detcetion = True
                    # if (first_detcetion):
                    #     new_face = most_frequent_face
                    #     first_detcetion = False                       
                    # # text=most_frequent_face
                    print("THIS IS THE new Face:", new_face)
                    print("FACE RECOGNIZED IS :", most_frequent_face)
                    time.sleep(1)
                    if new_face != most_frequent_face:
                        # text = most_frequent_face
                        new_face = most_frequent_face
                        
                        try:
                                # send_name_socket(ip_address,port,text,True ,client_socket=client_socket)
                                jn = {'known': True, "name": new_face}
                                client_socket.send(json.dumps(jn).encode('utf-8'))
                                print("THIS IS THE SENT RESPONSE:",jn)
                                while True:
                                    name = client_socket.recv(1024).decode()
                                    print("Name received is", name)
                                    
                                    # Check if the received name is not empty
                                    if name:
                                        break  # Exit the loop when a non-empty name is receiv
                        except:
                                print("can't send to server")




                    # print(f'the most frequent case is {text}')
                    







                #if the face not know start count to 3 
                else:
                    #if the face is new start count to three else clear the count
                    if state=='newface':
                        print("new face")
                        count_to_add_face+=1
                        print(count_to_add_face)
                    else :
                        count_to_add_face=0
                        
                    #this new face to add it to the encoding file
                    if count_to_add_face ==3:
                        
                        count_to_add_face=0






                        # #send socket to the sever
                        try:
                                # send_name_socket(ip_address,port,text,True ,client_socket=client_socket)
                                jn = {'known': False, "name": ""}
                                # client_socket.send(json.dumps(jn).encode('utf-8'))
                                print("THIS IS THE SENT RESPONSE:",jn)
                                client_socket.send(json.dumps(jn).encode('utf-8'))

                                print("Waiting now for response:")
                                while True:
                                    name = client_socket.recv(1024).decode()
                                    print("Name received is", name)
                                    
                                    # Check if the received name is not empty
                                    if name:
                                        break  # Exit the loop when a non-empty name is received

                        except: 
                                print("can't send to server")
                        # threading.Thread(target=thread_function, args=(1,)).start()


                        # get user name by asking him
                        
                        # name=input("Enter new name:")
                        #release the camera
                        cap.release()
                        cv2.destroyAllWindows()

                        # name = text 
                        # reopen the camera and add new user
                        myListId,encodListKnown=add_new_face(name=name
                                    #  ,folder_path=os.path.join('image',name)
                                    , folder_path= "C:/Users/wot/Desktop/python_vision/image/"+name
                                    #  ,encoding_file=os.getenv("ENCODE_FILE")
                                    ,encoding_file='C:/Users/wot/Desktop/python_vision/encoding/EncodeFile.p'
                                     ,number_image=7)                        
                        exit(0)
                        #reopen the main camera in the main
                        # cap = cv2.VideoCapture(int( os.getenv("MY_CAMERA") ))
                        cap = cv2.VideoCapture(0)
                        count_to_add_face+=1

                        cap.set(3,720)
                        cap.set(4,1280)
        
        
                # print("................................................................................\n \n \n")
        
        
        previous_text = text      
        # Draw the text on the image
            # Calculate the position to place the text at the center of the image
        text_size, _ = cv2.getTextSize(text, font, fontScale, lineThickness)
        text_x = (img.shape[1] - text_size[0]) // 2
        text_y = (img.shape[0] + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font, fontScale, fontcolor, lineThickness)
        cv2.imshow("face Recognition", img)
        if cv2.waitKey(1)==ord('a'):
            break

    cap.release()
    cv2.destroyAllWindows()



