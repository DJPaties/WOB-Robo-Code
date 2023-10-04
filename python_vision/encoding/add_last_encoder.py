import cv2
import face_recognition
import os
import pickle

from dotenv import load_dotenv,dotenv_values
#load the variable
load_dotenv()

from encoding.load_encoded_file import load_encoded_file




## this function is to add encoding face to the encoding file
def add_to_encod( selected_folder):
        encoding_file=os.getenv("ENCODE_FILE")   
        main_folder='image'  
        print("encoding to last starting....")
        extra_encoding_list=[]
        #this function only add all the image from all folder to a list of image and also add the id(name= folder/name.img) to a other list
        for folder in os.listdir(main_folder):
            if folder== selected_folder:
                for image_name in os.listdir(os.path.join(main_folder,folder)):
                    name_file=os.path.splitext(image_name)
                    id=folder+"/"+name_file[0]
                    try:
                        
                        img=cv2.imread(os.path.join(main_folder,folder,image_name))
                        #change color order 
                        img =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                        encode =face_recognition.face_encodings(img)[0]
                        
                        my_tuple=(id,encode)
                        extra_encoding_list.append(my_tuple)
                        print(f'encode {id} done!')
                    except:
                        print(f'failed to encode {id}')

            else : continue


        encoding_list = load_encoded_file(encoding_file)
        encoding_list+=extra_encoding_list
        print("encoding done! ")


        #here save all the result in a file
        file_data=open(encoding_file,"wb")
        pickle.dump(encoding_list,file_data)
        file_data.close()
        print("file saved !")



# selected_folder=input("enter the selected folder")
# add_to_encod(selected_folder)


