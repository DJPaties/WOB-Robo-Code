import pickle

#this will  load the file that contain the preencoded face     
def load_encoded_file(file_name):
    #load the encoded file 
    file=open(file_name,"rb")
    my_list=pickle.load(file)
    file.close()
    print("encod File loaded..")
    # print(listId)
    return my_list