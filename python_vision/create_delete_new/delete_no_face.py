import os 
import cv2

    # Load the pre-trained face detector
def filter(folder):

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    list_image_path=[]

    for image_path in os.listdir(folder):
        list_image_path.append(os.path.join(folder,image_path))

    print(list_image_path)
 
    #clean all the iamge that dont have clear face
    for item in list_image_path:
        img = cv2.imread(item)
        # Convert frame to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces)==0:
            os.remove(item)
            print(f" {item} was removed succesfully..")
