import cv2
import os
import time
from dotenv import load_dotenv,dotenv_values

load_dotenv()


def capture_faces(folder_path, num_images):
    global cap
    print('capture faces starting...')
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Load the pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # Open the camera
    cap = cv2.VideoCapture(1)
    # x, y, width, height = 300, 000, 700, 700

    count = 0
    while count < num_images:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # frame_height = frame.shape[0]
        # frame = frame[y:y+height, x:x+width]
        print('reading done')

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:


            # Save the face image to a file
            image=frame
            image_path = os.path.join(folder_path, f"face_{count}.jpg")
            time.sleep(0.4)
            cv2.imwrite(image_path, image)
            
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            count += 1

        # Display the frame with detected faces
        cv2.imshow(folder_path, frame)

        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

