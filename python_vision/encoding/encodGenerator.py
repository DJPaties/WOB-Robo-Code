import cv2
import face_recognition
import os
import pickle
from dotenv import load_dotenv,dotenv_values
#load the variable
load_dotenv()

main_folder= '..\image'
encoding_list=[]



#this function only add all the image from all folder to a list of image and also add the id(name= folder/name.img) to a other list
for folder in os.listdir(main_folder):
    print(f"encoding {folder} start....")
    for image_name in os.listdir(os.path.join(main_folder,folder)):        
        file_path=os.path.join(main_folder,folder,image_name)
        try:
            img=cv2.imread(file_path)
            print(file_path)
            encode =face_recognition.face_encodings(img)[0]
            name_file=os.path.splitext(image_name)
            id=folder+"/"+name_file[0]
            
            #add the combine into tuple
            my_tuple=(id,encode)
            #append to the list
            encoding_list.append(my_tuple)
        except:
            print("face was not found , it will be removed ")
            os.remove(file_path)


    print(f"encoding {folder} finish.")

print('save the result in file...')
#here save all the result in a file
file_data=open(os.getenv("ENCODE_FILE"),"wb")
pickle.dump(encoding_list,file_data)
file_data.close()
print("file saved !")




    