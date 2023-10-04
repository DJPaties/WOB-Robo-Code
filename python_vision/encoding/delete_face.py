import shutil
import os
from load_encoded_file import load_encoded_file
import pickle
from dotenv import load_dotenv,dotenv_values

load_dotenv()



# face name =  folder name  yes
#remove all the folder     yes

#remove the encoding of this face     
    #split the encodind into encod and id
    #  loop through the list and compare the id with the folder and remove the encoding of the same index
    # re save the file encoding
    

def delete_face(name , encoding_file):
    folder_path =os.path.join('','image',name)   # Specify the path to the folder you want to remove
    print(folder_path)

    try:
        if (name in os.listdir(os.path.join('','image'))):
            
            ## Use the shutil.rmtree() function to remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"the folder {folder_path} removed successfully")
            
        else :
            print(f" the folder {name} doesn't exist ")
            # return

        #loading the encoding file
        encoding_list=load_encoded_file(encoding_file)
        
        print(f"the list_id before .....")
        for item in encoding_list:
            print(item[0])
            
        #filter the encoding_list
        encoding_list= [tup for tup in encoding_list if tup[0].split('/')[0]!=name]
        

                
        print(f"the list_id after .....")
        for item in encoding_list:
            print(item[0])
        print("updating the list done! ")


        #here save all the result in a filera
        file_data=open(encoding_file,"wb")
        pickle.dump(encoding_list,file_data)
        file_data.close()
        print("file saved !")
        
        print("----------------------------------------------------------------")
            
    except NameError as e :
        print(f"error is {e} in deleting the item") 


name=input("enter the name to delete ")
delete_face(name,os.getenv("ENCODE_FILE"))

