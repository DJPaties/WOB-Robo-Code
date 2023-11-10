from module_vision.method_old import start  
from encoding.load_encoded_file import load_encoded_file
import os
from dotenv import load_dotenv,dotenv_values
# from opencv_test import show_cv2
import threading
from concurrent.futures import ThreadPoolExecutor


load_dotenv()


#load the pre-encoded file
# encoding_list=load_encoded_file(os.getenv("ENCODE_FILE"))
encoding_list=load_encoded_file("C:/Users/WOB/Desktop/WOB-Robo-Code-main/python_vision/encoding/EncodeFile.p")
# encoding_list =['adnan']
print("encoding...")

#open the camera  and start recognize the face 
#and take new user if he's not exist
start(encoding_list ,ip_address= 'localhost' , port= 12345)

# t1=threading.Thread(target=start,args=encoding_list)
# t2=threading.Thread(target=show_cv2)

# t1.start()
# t2.start()

# pool=ThreadPoolExecutor(2)
# work1=pool.submit(start)
# work2=pool.submit(show_cv2)

