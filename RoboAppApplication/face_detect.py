import cv2
from serialSender import talking_scenario
# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize the webcam or load a video file
cap = cv2.VideoCapture(1)  # Change the argument to a file path if you want to process a video

while True:
    # Read a frame from the video source
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale (face detection works on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw a square box around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle around the face
        center = (x + w // 2, y + h // 2)
        radius = 4
        cv2.circle(frame, center, radius, (0, 0, 255), 2)  # Red circle in the center of the face
        print(center[0])
        # if center[0]>=800:
        #     talking_scenario(5,"any", "#20P1350\r\n")
        if center[0]>=600:
            talking_scenario(5,"any", "#20P1400\r\n")
        elif center[0]>=500:
            talking_scenario(5,"any", "#20P1450\r\n")
        elif center[0]>=400:
            talking_scenario(5,"any", "#20P1500\r\n")
        elif center[0]>=300:
            talking_scenario(5,"any", "#20P1550\r\n") 
        elif center[0]>=200 :  
            talking_scenario(5,"any", "#20P1600\r\n")
        elif center[0]>=100 :  
            talking_scenario(5,"any", "#20P1650\r\n")  
    # Display the frame with the detected faces
    cv2.imshow('Face Detection', frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video source and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
