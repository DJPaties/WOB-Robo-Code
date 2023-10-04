from create_delete_new.save import capture_faces
from encoding.add_last_encoder import add_to_encod
from encoding.load_encoded_file import load_encoded_file


def add_new_face(name,folder_path,encoding_file,number_image):
    global cap
    #reopen the camera and save the 100 images
    print('capture face')
    capture_faces(folder_path,number_image)
    #the folder to add encoding 
    print("start adding to encoding file....")
    add_to_encod(name)
    print('add to encoding done!')
    #load again the encoding file
    encoding_list=load_encoded_file(encoding_file)
    myListId,encodListKnown=zip(*encoding_list)
    return  myListId,encodListKnown
