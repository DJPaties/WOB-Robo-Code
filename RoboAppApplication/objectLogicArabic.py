import os
import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types
import json
from TTS import tts
# beard_detect = False
#the JSON file you downloaded in step 5 above
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'object.json'

# Instantiates a client
client = vision.ImageAnnotatorClient()

#set this thumbnail as the url
# image = types.Image()
# image.source.image_uri = 'https://i.ytimg.com/vi/UQQHSbeIaB0/maxresdefault.jpg'

with open('names.json', 'r') as json_file:
    data = json.load(json_file)
    object_names = data['object_names']

def analyze_image():
    file_name = 'sample.png'
    image_path = os.path.join('', file_name)

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image =types.Image(content=content)
    #### LABEL DETECTION ######
    detected_objects = ""
    response_label = client.label_detection(image=image)


    mobile_names = ["mobile phone","telephone","smartphone", "telephony","communication device","portable communications device"]
    display_electronic=["display device","electronic device"]
    cup_names = ["cup","mug"]
    bottles = ["plastic bottle","bottle","Plastic bottle"]
    try:

        print("Entered Loop")
        telephone_count = 0
        cup_count = 0
        bottles_count = 0
        display_electronic_counter=0
        for label in response_label.label_annotations:
            matching_objects = [obj for obj in object_names if label.description.lower() == obj.lower()]
            if label.description.lower()  in mobile_names:
                
                if telephone_count>0:
                    pass
                else:
                    detected_objects += "تَلِيفونْ , "
                telephone_count+=1
            elif label.description.lower()  in cup_names:
                
                if cup_count>0:
                    pass
                else:
                    detected_objects += "كِبَّايَى , "
                cup_count+=1
            elif label.description.lower()  in bottles:
                print(label.description.lower())
                if bottles_count>0:
                    pass
                else:
                    detected_objects += "ءَنِّينِى , "
                bottles_count+=1
            elif label.description.lower()  in display_electronic:
                print(label.description.lower())
                if display_electronic_counter>0:
                    pass
                else:
                    detected_objects += " شي من إلكترونيات ,  "
                display_electronic_counter+=1
            elif matching_objects:
                print(f"User input '{label.description}' matches the object: '{matching_objects[0]}'")
                detected_objects += label.description + ", "
            print({'label': label.description, 'score': label.score})
        x = "أنا شايف"+ str(detected_objects)
        print("I can see:",detected_objects)
        tts(x,"ar-LB")
    except ValueError:
        print(ValueError)

# analyze_image()