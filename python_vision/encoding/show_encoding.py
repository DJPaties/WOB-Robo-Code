from load_encoded_file import load_encoded_file
import os
from dotenv import load_dotenv,dotenv_values
#load the variable
load_dotenv()

def show_encod(encoding_file):

    try:
        #loading the encoding file
        list_item=load_encoded_file(encoding_file)
        print("the item of tuple")
        for item in list_item:
            print(item[0])
                
    except :
        print(f"error occur") 

show_encod(os.getenv("ENCODE_FILE"))

